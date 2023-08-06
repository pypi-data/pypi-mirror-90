use mio::event::Source;
use mio::net::{TcpListener, TcpStream, UnixListener, UnixStream};
use mio::{Interest, Registry, Token};
use nix::fcntl::{fcntl, FcntlArg, OFlag};
use std::error;
use std::fmt::{self, Debug};
use std::io;
use std::marker::Sized;
use std::net;
use std::os::unix::io::{AsRawFd, FromRawFd, RawFd};
use std::sync::Arc;
use std::time::{Duration, Instant};

#[cfg(target_os = "linux")]
use libsystemd::activation::{receive_descriptors, IsType};
#[cfg(target_os = "linux")]
use std::os::unix::io::IntoRawFd;

pub type Result<T> = std::result::Result<T, Box<dyn error::Error>>;

// we need AsRawFd for sendfile
pub trait Write: io::Write + AsRawFd {}
impl<T: io::Write + AsRawFd> Write for T {}

pub trait NonBlockingWrite: Write + Send + Source {}
impl<T: Write + Send + Source> NonBlockingWrite for T {}

pub trait BlockingWrite: Socket + SetBlocking {}
impl<T: Socket + SetBlocking> BlockingWrite for T {}

pub trait Read: io::Read {
    fn peer_addr(&self) -> String;
}

pub fn would_block(err: &io::Error) -> bool {
    err.kind() == io::ErrorKind::WouldBlock
}

/// set a file descriptor into blocking mode
pub trait SetBlocking: AsRawFd {
    fn set_blocking(&mut self) -> Result<()>;
}

impl<T: AsRawFd> SetBlocking for T {
    #[inline]
    fn set_blocking(&mut self) -> Result<()> {
        let flags = fcntl(self.as_raw_fd(), FcntlArg::F_GETFL)?;
        let mut new_flags = OFlag::from_bits(flags).expect("Could not create flags from bits");
        new_flags.remove(OFlag::O_NONBLOCK);
        fcntl(self.as_raw_fd(), FcntlArg::F_SETFL(new_flags))?;
        Ok(())
    }
}

/// set a file descriptor into non-blocking mode
pub trait SetNonBlocking {
    type Fd;
    fn set_nonblocking(self) -> Result<Self::Fd>;
}

impl SetNonBlocking for RawFd {
    type Fd = RawFd;
    #[inline]
    fn set_nonblocking(self) -> Result<Self::Fd> {
        let flags = fcntl(self, FcntlArg::F_GETFL)?;
        let mut new_flags = OFlag::from_bits(flags).expect("Could not create flags from bits");
        new_flags.insert(OFlag::O_NONBLOCK);
        fcntl(self, FcntlArg::F_SETFL(new_flags))?;
        Ok(self)
    }
}

pub trait Socket: AsRawFd + io::Write + Read + Send + Source {}
impl<S: AsRawFd + io::Write + Read + Send + Source> Socket for S {}

pub trait Connection: Socket + Debug + SetBlocking + Sync {}
impl<T: Socket + Debug + SetBlocking + Sync> Connection for T {}

// A HTTP persistent connection keeps track of it's use count
pub struct HTTPPersistentConnectionOptions {
    pub max_reuse_count: u8,
    pub keepalive_timeout: Duration,
}

pub type SharedConnectionOptions = Arc<HTTPPersistentConnectionOptions>;

pub fn shared_connection_options(
    max_reuse_count: u8,
    keepalive_timeout: Duration,
) -> SharedConnectionOptions {
    Arc::new(HTTPPersistentConnectionOptions {
        max_reuse_count,
        keepalive_timeout,
    })
}

pub struct HTTPPersistentConnection<C: Connection> {
    connection: C,
    count: u8,
    created: Instant,
    options: SharedConnectionOptions,
}

impl<C: Connection> HTTPPersistentConnection<C> {
    pub fn from_connection(connection: C, options: SharedConnectionOptions) -> Self {
        HTTPPersistentConnection {
            connection,
            count: 0,
            created: Instant::now(),
            options,
        }
    }

    pub fn expire(&mut self) {
        self.count = self.options.max_reuse_count
    }

    pub fn expired(&self) -> bool {
        (self.count >= self.options.max_reuse_count)
            || (self.created.elapsed() >= self.options.keepalive_timeout)
    }

    pub fn reuse(&mut self) -> bool {
        self.count += 1;
        !self.expired()
    }
}

impl<C: Connection> Debug for HTTPPersistentConnection<C> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.connection.fmt(f)
    }
}

impl<C: Connection> io::Read for HTTPPersistentConnection<C> {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        self.connection.read(buf)
    }
}

impl<C: Connection> io::Write for HTTPPersistentConnection<C> {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        self.connection.write(buf)
    }

    fn flush(&mut self) -> io::Result<()> {
        self.connection.flush()
    }
}

impl<C: Connection> Read for HTTPPersistentConnection<C> {
    fn peer_addr(&self) -> String {
        Read::peer_addr(&self.connection)
    }
}

impl<C: Connection> AsRawFd for HTTPPersistentConnection<C> {
    fn as_raw_fd(&self) -> RawFd {
        self.connection.as_raw_fd()
    }
}

impl<C: Connection> Source for HTTPPersistentConnection<C> {
    fn register(
        &mut self,
        registry: &Registry,
        token: Token,
        interests: Interest,
    ) -> io::Result<()> {
        self.connection.register(registry, token, interests)
    }

    fn reregister(
        &mut self,
        registry: &Registry,
        token: Token,
        interests: Interest,
    ) -> io::Result<()> {
        self.connection.reregister(registry, token, interests)
    }

    fn deregister(&mut self, registry: &Registry) -> io::Result<()> {
        self.connection.deregister(registry)
    }
}

impl Read for TcpStream {
    fn peer_addr(&self) -> String {
        match TcpStream::peer_addr(&self) {
            Ok(addr) => format!("{}", addr.ip()),
            Err(_) => String::new(),
        }
    }
}

impl Read for UnixStream {
    fn peer_addr(&self) -> String {
        match UnixStream::peer_addr(&self) {
            Ok(addr) => {
                if let Some(addr) = addr.as_pathname() {
                    match addr.as_os_str().to_os_string().into_string() {
                        Ok(addr) => addr,
                        Err(_) => String::new(),
                    }
                } else {
                    String::new()
                }
            }
            Err(_) => String::new(),
        }
    }
}

/// commonalities of TCPListener + UnixListener
pub trait Listening {
    type Connected: Connection;
    fn accept(
        &self,
        options: SharedConnectionOptions,
    ) -> io::Result<HTTPPersistentConnection<Self::Connected>>;
    fn local_addr_string(&self) -> String;
}

// s. https://stackoverflow.com/questions/53713354/implementing-traits-without-repeating-methods-already-defined-on-the-struct
impl Listening for TcpListener {
    type Connected = TcpStream;
    fn accept(
        &self,
        options: SharedConnectionOptions,
    ) -> io::Result<HTTPPersistentConnection<Self::Connected>> {
        match TcpListener::accept(&self) {
            Ok((conn, _)) => Ok(HTTPPersistentConnection::from_connection(conn, options)),
            Err(e) => Err(e),
        }
    }

    fn local_addr_string(&self) -> String {
        match self.local_addr() {
            Ok(addr) => format!("{}", addr),
            Err(e) => format!("TCPListener error: {:?}", e),
        }
    }
}

impl Listening for UnixListener {
    type Connected = UnixStream;
    fn accept(
        &self,
        options: SharedConnectionOptions,
    ) -> io::Result<HTTPPersistentConnection<Self::Connected>> {
        match UnixListener::accept(&self) {
            Ok((conn, _)) => Ok(HTTPPersistentConnection::from_connection(conn, options)),
            Err(e) => Err(e),
        }
    }

    fn local_addr_string(&self) -> String {
        match self.local_addr() {
            Ok(addr) => match addr.as_pathname() {
                Some(path) => format!("{}", path.display()),
                None => " - ".to_string(),
            },
            Err(e) => format!("UnixListener error: {:?}", e),
        }
    }
}

pub trait Listener: Listening + Source + FromRawFd {}
impl<L: Listening + Source + FromRawFd> Listener for L {}

pub trait SocketActivation: Sized + FromRawFd {
    /// get a socket activated by systemd
    fn from_active_socket() -> Result<Self>;
}

#[cfg(target_os = "linux")]
macro_rules! create_from_active_socket {
    ($S: ty, $testfn: ident, $errmsg: literal) => {
        match receive_descriptors(false) {
            Ok(mut possible_fds) => {
                // check whether systemd has passed a valid file descriptor
                if !possible_fds.is_empty() {
                    let fd = possible_fds.remove(0);
                    if fd.$testfn() {
                        let rawfd = fd.into_raw_fd().set_nonblocking()?;
                        Ok(unsafe { <$S>::from_raw_fd(rawfd) })
                    } else {
                        Err(Box::new(io::Error::new(io::ErrorKind::Other, $errmsg)))
                    }
                } else {
                    Err(Box::new(io::Error::new(
                        io::ErrorKind::Other,
                        "Could not get file descriptors",
                    )))
                }
            }
            Err(e) => Err(Box::new(e)),
        }
    };
}

#[cfg(target_os = "linux")]
impl SocketActivation for TcpListener {
    fn from_active_socket() -> Result<TcpListener> {
        create_from_active_socket!(TcpListener, is_inet, "File descriptor must be a TCP socket")
    }
}

#[cfg(target_os = "linux")]
impl SocketActivation for UnixListener {
    fn from_active_socket() -> Result<UnixListener> {
        create_from_active_socket!(
            UnixListener,
            is_unix,
            "File descriptor must be a Unix Domain socket"
        )
    }
}

pub fn parse_server_info(addr: &str) -> (String, String) {
    match addr.parse::<net::SocketAddr>() {
        Ok(ipaddr) => (format!("{}", ipaddr.ip()), format!("{}", ipaddr.port())),
        Err(_) => (String::from(addr), String::new()),
    }
}

#[cfg(test)]
mod tests {

    #[cfg(target_os = "linux")]
    use log::debug;
    use mio::net::{self, TcpListener, UnixListener, UnixStream};
    use nix::fcntl::{fcntl, FcntlArg, OFlag};
    #[cfg(target_os = "linux")]
    use nix::unistd::dup2;
    use rand::seq::SliceRandom;
    #[cfg(target_os = "linux")]
    use std::env::set_var;
    use std::fs::remove_file;
    use std::io;
    use std::net::SocketAddr;
    use std::os::unix::io::AsRawFd;
    #[cfg(target_os = "linux")]
    use std::process::id;
    use std::sync::mpsc::channel;
    use std::thread;
    use std::time::Duration;
    #[cfg(target_os = "linux")]
    use tempfile::tempfile;

    #[cfg(target_os = "linux")]
    use crate::transport::SocketActivation;
    use crate::transport::{
        parse_server_info, shared_connection_options, would_block, Connection,
        HTTPPersistentConnection, Listening, Read, SetNonBlocking,
    };

    fn random_filename() -> String {
        let mut rng = &mut rand::thread_rng();
        (b'0'..=b'z')
            .map(|c| c as char)
            .filter(|c| c.is_alphanumeric())
            .collect::<Vec<_>>()
            .choose_multiple(&mut rng, 7)
            .collect()
    }

    fn dummy_persistent_connection<C: Connection>(
        connection: C,
        timeoutsecs: u8,
    ) -> HTTPPersistentConnection<C> {
        HTTPPersistentConnection::from_connection(
            connection,
            shared_connection_options(42, Duration::from_secs(timeoutsecs.into())),
        )
    }

    #[test]
    fn test_would_block() {
        let wbe = io::Error::new(io::ErrorKind::WouldBlock, "foo");
        assert!(would_block(&wbe));
        let nwbe = io::Error::new(io::ErrorKind::Other, "foo");
        assert!(!would_block(&nwbe));
    }

    #[test]
    fn test_set_nonblocking() {
        let addr: SocketAddr = "127.0.0.1:0".parse().unwrap();
        let listener = TcpListener::bind(addr).unwrap();
        let before = net::TcpStream::connect(listener.local_addr().unwrap()).unwrap();
        let o_before =
            OFlag::from_bits(fcntl(before.as_raw_fd(), FcntlArg::F_GETFL).unwrap()).unwrap();
        assert!(o_before.contains(OFlag::O_NONBLOCK));
        match before.as_raw_fd().set_nonblocking() {
            Ok(after) => {
                let o_after = OFlag::from_bits(fcntl(after, FcntlArg::F_GETFL).unwrap()).unwrap();
                assert!(o_after.contains(OFlag::O_NONBLOCK));
            }
            Err(_) => {
                assert!(false);
            }
        }
    }

    #[cfg(target_os = "linux")]
    #[test]
    fn test_from_active_socket_tcp() {
        // no systemd environment
        match TcpListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // no file descriptors
        set_var("LISTEN_FDS", "0");
        set_var("LISTEN_PID", format!("{}", id()));
        match TcpListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // file descriptor is not a socket
        let tmp = tempfile().unwrap();
        dup2(tmp.as_raw_fd(), 3).unwrap();
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match TcpListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // Success
        let si = "127.0.0.1:0".parse().unwrap();
        let listener = TcpListener::bind(si).unwrap();
        dup2(listener.as_raw_fd(), 3).unwrap(); // must be >= 3 (SD_LISTEN_FDS_START)
                                                // see libsystemd.activation for how this works
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match TcpListener::from_active_socket() {
            Ok(sock) => {
                assert!(sock.as_raw_fd() == 3);
            }
            Err(_) => assert!(false),
        }
    }

    #[cfg(target_os = "linux")]
    #[test]
    fn test_from_active_socket_unix() {
        // no file descriptors
        set_var("LISTEN_FDS", "0");
        set_var("LISTEN_PID", format!("{}", id()));
        match UnixListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // file descriptor is not a socket
        let si = "127.0.0.1:0".parse().unwrap();
        let tcp = TcpListener::bind(si).unwrap();
        dup2(tcp.as_raw_fd(), 3).unwrap();
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match UnixListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // Success
        let socketfile = "/tmp/".to_owned() + &random_filename() + ".socket";
        let listener = UnixListener::bind(&socketfile).unwrap();
        dup2(listener.as_raw_fd(), 3).unwrap(); // must be >= 3 (SD_LISTEN_FDS_START)
                                                // see libsystemd.activation for how this works
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match UnixListener::from_active_socket() {
            Ok(sock) => {
                debug!("{:?}", sock);
                assert!(sock.as_raw_fd() == 3);
            }
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false)
            }
        }
        remove_file(socketfile).unwrap();
    }

    #[test]
    fn test_parse_server_info() {
        assert!(
            parse_server_info("127.0.0.1:7878") == ("127.0.0.1".to_string(), "7878".to_string())
        );
        assert!(
            parse_server_info("/tmp/pyruvate.sock")
                == ("/tmp/pyruvate.sock".to_string(), String::new())
        );
    }

    #[test]
    fn test_local_addr_string_tcp() {
        let si = "127.0.0.1:33333".parse().unwrap();
        let listener = TcpListener::bind(si).unwrap();
        assert!(listener.local_addr_string() == "127.0.0.1:33333");
    }

    #[test]
    fn test_local_addr_string_unix() {
        let si = "/tmp/".to_owned() + &random_filename() + ".socket";
        let listener = UnixListener::bind(&si).unwrap();
        assert!(listener.local_addr_string() == si);
        remove_file(si).unwrap();
    }

    #[test]
    fn test_peer_addr_unix() {
        let si = "/tmp/".to_owned() + &random_filename() + ".socket";
        let _listener = UnixListener::bind(&si).unwrap();
        let socket = UnixStream::connect(&si).unwrap();
        let got = Read::peer_addr(&socket);
        remove_file(&si).unwrap();
        assert_eq!(got, si);
    }

    #[test]
    fn test_listening_unix_accept() {
        let si = "/tmp/".to_owned() + &random_filename() + ".socket";
        let server = UnixListener::bind(&si).unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let coptions = shared_connection_options(10, Duration::from_secs(60));
        thread::spawn(move || {
            loop {
                match Listening::accept(&server, coptions.clone()) {
                    Ok(conn) => {
                        snd.clone().send(conn).unwrap();
                        break;
                    }
                    Err(e) if would_block(&e) => (),
                    Err(_) => assert!(false),
                }
            }
            rx.recv().unwrap();
        });
        let _socket = UnixStream::connect(&si).unwrap();
        let conn = got.recv().unwrap();
        assert_eq!(
            conn.connection
                .local_addr()
                .unwrap()
                .as_pathname()
                .unwrap()
                .as_os_str(),
            si.as_str()
        );
        tx.send(()).unwrap();
        remove_file(si).unwrap();
    }

    #[test]
    fn test_listening_unix_local_addr_string() {
        let si = "/tmp/".to_owned() + &random_filename() + ".socket";
        let server = UnixListener::bind(&si).unwrap();
        let got = server.local_addr_string();
        remove_file(&si).unwrap();
        assert_eq!(got, si);
    }

    #[test]
    fn test_persistent_connection_expire_reuse_count() {
        let si = "/tmp/".to_owned() + &random_filename() + ".socket";
        let _listener = UnixListener::bind(&si).unwrap();
        let socket = UnixStream::connect(&si).unwrap();
        let mut pconn = dummy_persistent_connection(socket, 60);
        pconn.expire();
        assert_eq!(pconn.count, pconn.options.max_reuse_count);
        assert_eq!(pconn.count, 42);
        assert!(pconn.expired());
        remove_file(&si).unwrap();
    }

    #[test]
    fn test_persistent_connection_reuse() {
        let si = "/tmp/".to_owned() + &random_filename() + ".socket";
        let _listener = UnixListener::bind(&si).unwrap();
        let socket = UnixStream::connect(&si).unwrap();
        let mut pconn = dummy_persistent_connection(socket, 60);
        for rc in 0..41 {
            assert_eq!(rc, pconn.count);
            assert!(pconn.reuse());
        }
        assert!(!pconn.reuse());
        assert_eq!(42, pconn.count);
        assert!(!pconn.reuse());
        remove_file(&si).unwrap();
    }

    #[test]
    fn test_persistent_connection_timeout() {
        let si = "/tmp/".to_owned() + &random_filename() + ".socket";
        let _listener = UnixListener::bind(&si).unwrap();
        let socket = UnixStream::connect(&si).unwrap();
        let mut pconn = dummy_persistent_connection(socket, 1);
        for rc in 0..2 {
            assert_eq!(rc, pconn.count);
            assert!(pconn.reuse());
            thread::sleep(Duration::from_secs_f32(0.4));
        }
        thread::sleep(Duration::from_secs_f32(0.2));
        assert_eq!(2, pconn.count);
        assert!(pconn.expired());
        assert!(!pconn.reuse());
        assert!(pconn.expired());
        assert!(!pconn.reuse());
        assert!(pconn.expired());
        remove_file(&si).unwrap();
    }
}
