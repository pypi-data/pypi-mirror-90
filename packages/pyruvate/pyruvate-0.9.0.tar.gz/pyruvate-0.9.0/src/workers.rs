use cpython::PyObject;
use crossbeam_channel::{Receiver, Sender, TryRecvError};
use log::{debug, error};
use mio::{Events, Interest, Poll, Token};
use std::collections::HashMap;
use std::io;
use std::time::Duration;

use crate::globals::SharedWSGIOptions;
use crate::pyutils::with_gil;
use crate::response::{handle_request, WSGIResponse};
use crate::transport::{
    would_block, BlockingWrite, Connection, HTTPPersistentConnection, Listener, NonBlockingWrite,
    SetBlocking,
};
use crate::workerpool::{WorkerPayload, MARKER};

/// Returns `true` if the connection is done.
fn handle_write_event<T: Connection>(response: &mut WSGIResponse<T>) -> io::Result<bool> {
    // We can (maybe) write to the connection.
    with_gil(|py, gs| {
        let mut retval = false;
        loop {
            match response.write_chunk(py, gs) {
                Ok(done) => {
                    if done {
                        retval = true;
                        break;
                    }
                }
                // Would block "errors" are the OS's way of saying that the
                // connection is not actually ready to perform this I/O operation.
                Err(ref err) if would_block(err) => break,
                // Other errors we'll consider fatal.
                Err(err) => return Err(err),
            }
        }
        Ok(retval)
    })
}

fn recv_or_try_recv<T>(block: bool, rcv: &Receiver<T>) -> Result<T, TryRecvError> {
    if block {
        match rcv.recv() {
            Ok(t) => Ok(t),
            Err(e) => Err(TryRecvError::from(e)),
        }
    } else {
        rcv.try_recv()
    }
}

pub fn write_non_blocking_worker<L: Listener, T: Connection + NonBlockingWrite>(
    idx: usize,
    thread_globals: SharedWSGIOptions,
    threadapp: PyObject,
    rcv: Receiver<(Token, WorkerPayload<T>)>,
    snd: Sender<(Token, HTTPPersistentConnection<T>)>,
) {
    // Create a poll instance.
    let mut poll = match Poll::new() {
        Ok(poll) => poll,
        Err(e) => panic!("Could not create poll intstance: {:?}", e),
    };
    // Create storage for events.
    let mut events = Events::with_capacity(1024);
    // Responses
    let mut responses: HashMap<Token, WSGIResponse<T>> = HashMap::new();

    loop {
        // if we do not need to process stashed responses,
        // we can block and use less CPU.
        match recv_or_try_recv(responses.is_empty(), &rcv) {
            Ok((token, (mut req, out))) => {
                if token == MARKER {
                    break;
                }
                debug!("Handling request in worker {}", idx);
                match out {
                    Some(connection) => {
                        debug!(
                            "worker {} creating response for token: {:?}, using connection {:?}",
                            idx, token, connection
                        );
                        let mut response =
                            WSGIResponse::new(connection, thread_globals.chunked_transfer);
                        with_gil(|py, gs| {
                            handle_request(
                                &threadapp,
                                thread_globals.clone(),
                                &mut req,
                                &mut response,
                                py,
                            );
                            loop {
                                match response.write_chunk(py, gs) {
                                    Ok(done) => {
                                        if done {
                                            debug!("wrote response immediately");
                                            break;
                                        }
                                    }
                                    Err(ref err) if would_block(err) => {
                                        break;
                                    }
                                    Err(e) => {
                                        error!("Write error: {:?}", e);
                                        response.last_chunk_or_file_sent = true;
                                        break;
                                    }
                                }
                            }
                        });
                        if !response.complete() {
                            debug!("registering response for later write: {:?}", token);
                            if let Err(e) = poll.registry().register(
                                &mut response.connection,
                                token,
                                Interest::WRITABLE,
                            ) {
                                error!("Could not register connection for writable events in worker {}, error: {:?}", idx, e);
                            }
                            responses.insert(token, response);
                        } else {
                            let mut conn = response.connection;
                            if conn.reuse() {
                                debug!(
                                    "Sending back connection {:?} for reuse in worker {}",
                                    conn, idx
                                );
                                if let Err(e) = snd.send((token, conn)) {
                                    error!("Could not send back connection for reuse in worker {}, error: {:?}", idx, e);
                                }
                            }
                        }
                    }
                    None => {
                        error!("No connection to write to");
                    }
                }
            }
            Err(e) => {
                if e.is_disconnected() {
                    error!("Couldn't receive from queue: {:?} (sender has hung up)", e);
                    break;
                }
            }
        }
        if let Err(e) = poll.poll(&mut events, Some(Duration::from_millis(0))) {
            error!("Could not poll in worker {}, error: {:?}", idx, e);
        }

        for event in events.iter() {
            debug!("Processing event: {:?}", event);
            match event.token() {
                token if event.is_writable() => {
                    // (maybe) received an event for a TCP connection.
                    if let Some(mut resp) = responses.remove(&token) {
                        debug!("Received writable event: {:?}", event);
                        match handle_write_event(&mut resp) {
                            Ok(done) => {
                                if done {
                                    // s. https://docs.rs/mio/0.7.0/mio/event/trait.Source.html#dropping-eventsources
                                    if let Err(e) = poll.registry().deregister(&mut resp.connection)
                                    {
                                        error!("Could not deregister connection: {:?}", e);
                                    }
                                } else {
                                    responses.insert(token, resp);
                                }
                            }
                            Err(e) => {
                                error!("Could not handle write event: {:?}", e);
                            }
                        }
                    }
                }
                _ => {
                    error!("Received unexpected event {:?} in worker {}", event, idx);
                }
            }
        }
    }
}

pub fn write_blocking_worker<L: Listener, T: Connection + BlockingWrite>(
    idx: usize,
    thread_globals: SharedWSGIOptions,
    threadapp: PyObject,
    rcv: Receiver<(Token, WorkerPayload<T>)>,
    snd: Sender<(Token, HTTPPersistentConnection<T>)>,
) {
    loop {
        match rcv.recv() {
            Ok((token, (mut req, out))) => {
                if token == MARKER {
                    break;
                }
                debug!("Handling request in worker {}", idx);
                match out {
                    Some(mut connection) => {
                        if let Err(e) = connection.set_blocking() {
                            error!(
                                "Could not set connection {:?} in blocking mode in worker {}: {:?}",
                                connection, idx, e
                            );
                        }
                        debug!("Using tcp stream {:?} for writing out.", connection);
                        let mut response =
                            WSGIResponse::new(connection, thread_globals.chunked_transfer);
                        with_gil(|py, gs| {
                            handle_request(
                                &threadapp,
                                thread_globals.clone(),
                                &mut req,
                                &mut response,
                                py,
                            );
                            loop {
                                let cont = match response.write_chunk(py, gs) {
                                    Ok(true) => false,
                                    Err(e) => {
                                        error!("Write error: {:?}", e);
                                        false
                                    }
                                    _ => {
                                        true
                                        // there's more to write, stay in loop
                                    }
                                };
                                if !cont {
                                    break;
                                }
                            }
                        });
                        let mut conn = response.connection;
                        if conn.reuse() {
                            if let Err(e) = snd.send((token, conn)) {
                                error!("Could not send back connection for reuse in worker {}, error: {:?}", idx, e);
                            }
                        }
                    }
                    None => {
                        error!("No connection to write to");
                    }
                }
            }
            Err(e) => {
                error!("Couldn't receive from queue: {:?} (sender has hung up)", e);
                break;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use cpython::{PyClone, PyDict, Python, PythonObject};
    use crossbeam_channel::unbounded;
    use env_logger;
    use log::debug;
    use mio::event::Source;
    use mio::net::{TcpListener as MioTcpListener, TcpStream};
    use mio::{Interest, Registry, Token};
    use python3_sys::{PyEval_RestoreThread, PyEval_SaveThread};
    use std::io::{self, Read, Seek, Write};
    use std::net::TcpListener;
    use std::os::unix::io::{AsRawFd, RawFd};
    use std::sync::mpsc::channel;
    use std::thread;
    use std::time::Duration;
    use tempfile::NamedTempFile;

    use crate::globals::shared_wsgi_options;
    use crate::request::WSGIRequest;
    use crate::response::WSGIResponse;
    use crate::transport::{self, shared_connection_options, Connection, HTTPPersistentConnection};
    use crate::workerpool::MARKER;
    use crate::workers::{handle_write_event, write_blocking_worker, write_non_blocking_worker};

    #[derive(Debug)]
    struct WriteMock {
        block_pos: usize,
        raise: bool,
        pub error: Option<io::ErrorKind>,
        pub file: NamedTempFile,
        registered: bool,
        deregistered: bool,
    }

    impl WriteMock {
        fn new(block_pos: usize, raise: bool) -> Self {
            WriteMock {
                block_pos,
                raise,
                error: None,
                file: NamedTempFile::new().unwrap(),
                registered: false,
                deregistered: false,
            }
        }
    }

    impl Write for WriteMock {
        fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
            match self.error {
                None => {
                    let num_bytes = self.file.write(&buf[0..self.block_pos]).unwrap();
                    self.error = Some(io::ErrorKind::WouldBlock);
                    Ok(num_bytes)
                }
                Some(errkind) if errkind == io::ErrorKind::WouldBlock => {
                    self.error = Some(io::ErrorKind::Other);
                    Err(io::Error::new(
                        io::ErrorKind::WouldBlock,
                        "WriteMock blocking",
                    ))
                }
                Some(errkind) if errkind == io::ErrorKind::Other => {
                    self.error = Some(io::ErrorKind::WriteZero);
                    self.file.write(buf)
                }
                Some(_) => {
                    if self.raise {
                        Err(io::Error::new(
                            io::ErrorKind::BrokenPipe,
                            "WriteMock raising",
                        ))
                    } else {
                        Ok(0)
                    }
                }
            }
        }

        fn flush(&mut self) -> io::Result<()> {
            self.file.flush()
        }
    }

    impl Read for WriteMock {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            self.file.flush().unwrap();
            let mut f = self.file.reopen().unwrap();
            f.seek(std::io::SeekFrom::Start(0)).unwrap();
            f.read(buf)
        }
    }

    impl transport::Read for WriteMock {
        fn peer_addr(&self) -> String {
            format!("WriteMock on {:?}", self.file)
        }
    }

    impl AsRawFd for WriteMock {
        fn as_raw_fd(&self) -> RawFd {
            self.file.as_raw_fd()
        }
    }

    impl Source for WriteMock {
        fn register(
            &mut self,
            _registry: &Registry,
            _token: Token,
            _interests: Interest,
        ) -> io::Result<()> {
            self.registered = true;
            Ok(())
        }
        fn reregister(
            &mut self,
            _registry: &Registry,
            _token: Token,
            _interests: Interest,
        ) -> io::Result<()> {
            Ok(())
        }
        fn deregister(&mut self, _registry: &Registry) -> io::Result<()> {
            self.deregistered = true;
            Ok(())
        }
    }

    fn dummy_persistent_connection<C: Connection>(connection: C) -> HTTPPersistentConnection<C> {
        HTTPPersistentConnection::from_connection(
            connection,
            shared_connection_options(10, Duration::from_secs(60)),
        )
    }

    fn init() {
        let _ = env_logger::builder().is_test(true).try_init();
    }

    #[test]
    fn test_write_blocking_worker() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let server_name = String::from("127.0.0.1");
                let port = String::from("0");
                let addr = server_name.clone() + ":" + &port;
                let sn = "/foo";
                let server = TcpListener::bind(addr).expect("Failed to bind address");
                let addr = server.local_addr().unwrap();
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                let token = Token(42);
                let expected = b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nExpires: Sat, 1 Jan 2000 00:00:00 GMT\r\nContent-Length: 13\r\n\r\nHello world!\n";
                let (input, rcv) = unbounded::<(
                    Token,
                    (WSGIRequest, Option<HTTPPersistentConnection<TcpStream>>),
                )>();
                let (send, _) = unbounded::<(Token, HTTPPersistentConnection<TcpStream>)>();
                let (tx, rx) = channel();
                let (snd, got) = channel();
                let t = thread::spawn(move || {
                    let (mut conn, _addr) = server.accept().unwrap();
                    let mut buf = [0; 6];
                    conn.read(&mut buf).unwrap();
                    snd.clone().send(buf).unwrap();
                    rx.recv().unwrap();
                    drop(conn);
                });
                let t2 = thread::spawn(move || {
                    let connection = TcpStream::connect(addr).expect("Failed to connect to server");
                    input
                        .send((token, (req, Some(dummy_persistent_connection(connection)))))
                        .unwrap();
                    input
                        .send((MARKER, (WSGIRequest::new(16, String::new()), None)))
                        .unwrap();
                });
                write_blocking_worker::<MioTcpListener, TcpStream>(
                    23,
                    shared_wsgi_options(
                        server_name.clone(),
                        port.clone(),
                        sn.to_string(),
                        false,
                        py,
                    ),
                    app,
                    rcv.clone(),
                    send.clone(),
                );
                let b = got.recv().unwrap();
                debug!("{:?}", b);
                assert!(b.iter().zip(expected.iter()).all(|(p, q)| p == q));
                tx.send(()).unwrap();
                t.join().unwrap();
                t2.join().unwrap();
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_write_non_blocking_worker() {
        init();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let server_name = String::from("127.0.0.1");
                let port = String::from("0");
                let sn = "/foo";
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                let token = Token(42);
                let expected = b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nExpires: Sat, 1 Jan 2000 00:00:00 GMT\r\nVia: pyruvate\r\nConnection: keep-alive\r\n\r\nHello world!\n";
                let (input, rcv) = unbounded::<(
                    Token,
                    (WSGIRequest, Option<HTTPPersistentConnection<WriteMock>>),
                )>();
                let (snd, _) = unbounded::<(Token, HTTPPersistentConnection<WriteMock>)>();
                let connection = WriteMock::new(20, false);
                let mut f = connection.file.reopen().unwrap();
                input
                    .send((token, (req, Some(dummy_persistent_connection(connection)))))
                    .unwrap();
                input
                    .send((MARKER, (WSGIRequest::new(16, String::new()), None)))
                    .unwrap();
                write_non_blocking_worker::<MioTcpListener, WriteMock>(
                    23,
                    shared_wsgi_options(
                        server_name.clone(),
                        port.clone(),
                        sn.to_string(),
                        false,
                        py,
                    ),
                    app.clone_ref(py),
                    rcv.clone(),
                    snd.clone(),
                );
                let mut buf: [u8; 20] = [0; 20];
                let b = f.read(&mut buf).unwrap();
                assert!(b == 20);
                assert!(buf == expected[..20]);
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                let token = Token(42);
                let mut connection = WriteMock::new(raw.len(), false);
                let mut f = connection.file.reopen().unwrap();
                f.seek(std::io::SeekFrom::Start(0)).unwrap();
                connection.error = Some(io::ErrorKind::Other);
                input
                    .send((token, (req, Some(dummy_persistent_connection(connection)))))
                    .unwrap();
                input
                    .send((MARKER, (WSGIRequest::new(16, String::new()), None)))
                    .unwrap();
                write_non_blocking_worker::<MioTcpListener, WriteMock>(
                    23,
                    shared_wsgi_options(server_name, port, sn.to_string(), false, py),
                    app,
                    rcv.clone(),
                    snd.clone(),
                );
                let mut buf: [u8; 200] = [0; 200];
                let b = f.read(&mut buf).unwrap();
                assert!(b == expected.len());
                assert!(buf.iter().zip(expected.iter()).all(|(p, q)| p == q));
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_write_event() {
        // function under test needs GIL
        let _gil = Python::acquire_gil();
        let connection = WriteMock::new(4, true);
        let mut r = WSGIResponse::new(dummy_persistent_connection(connection), false);
        r.current_chunk = b"Foo 42".to_vec();
        r.last_chunk_or_file_sent = true;
        let py_thread_state = unsafe { PyEval_SaveThread() };
        match handle_write_event(&mut r) {
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false);
            }
            Ok(false) => {
                let mut expected: [u8; 10] = [0; 10];
                let b = r.connection.read(&mut expected).unwrap();
                assert!(b == 4);
                assert!(&expected[..4] == b"Foo ");
                assert!(!r.complete());
            }
            _ => assert!(false),
        }
        match handle_write_event(&mut r) {
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false);
            }
            Ok(true) => {
                let mut expected: [u8; 10] = [0; 10];
                let b = r.connection.read(&mut expected).unwrap();
                assert!(b == 6);
                assert!(&expected[..6] == b"Foo 42");
            }
            _ => assert!(false),
        }
        match handle_write_event(&mut r) {
            Err(e) if e.kind() == io::ErrorKind::BrokenPipe => (),
            _ => assert!(false),
        }
        unsafe { PyEval_RestoreThread(py_thread_state) };
    }
}
