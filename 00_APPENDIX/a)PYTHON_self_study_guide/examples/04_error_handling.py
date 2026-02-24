#!/usr/bin/env python3
"""
Example 4: Comprehensive Error Handling for Network Programming
===============================================================
Demonstrates all common error scenarios students will encounter
when working with sockets in Python.

Course: Computer Networks — ASE Bucharest, CSIE
Author: ing. dr. Antonio Clim
Version: 5.0 — January 2026

💡 ANALOGY: Error Handling as a Safety Net
------------------------------------------
| Network Error        | Real-World Analogy                    |
|---------------------|---------------------------------------|
| ConnectionRefused   | Knocking on a door — nobody home      |
| Timeout             | Waiting for a letter that never comes |
| ConnectionReset     | Phone line suddenly cut mid-call      |
| AddressInUse        | Parking space already taken           |
| NetworkUnreachable  | Road closed, cannot reach destination |

Learning objectives:
- Handle connection errors gracefully
- Implement timeouts correctly
- Understand partial receives in TCP
- Use context managers for cleanup
- Write robust retry logic

Run this file directly to see demonstrations:
    python 04_error_handling.py

Or import specific functions:
    from error_handling import connect_with_retry, recv_exactly
"""

import socket
import errno
import time
import logging
from typing import Optional, Tuple
from contextlib import contextmanager


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_TIMEOUT: float = 5.0
DEFAULT_RETRIES: int = 3
BUFFER_SIZE: int = 4096


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECTION HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

def connect_with_retry(
    host: str,
    port: int,
    timeout: float = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_RETRIES,
    retry_delay: float = 1.0
) -> Optional[socket.socket]:
    """
    Attempt to connect to a server with automatic retry on failure.
    
    This function handles common connection errors gracefully and
    provides informative logging for debugging.
    
    Args:
        host: Target hostname or IP address.
        port: Target port number (1-65535).
        timeout: Connection timeout in seconds.
        max_retries: Number of retry attempts before giving up.
        retry_delay: Seconds to wait between retries.
        
    Returns:
        Connected socket if successful, None if all retries failed.
        Caller is responsible for closing the socket.
        
    Example:
        >>> sock = connect_with_retry('localhost', 8080, timeout=3.0)
        >>> if sock:
        ...     try:
        ...         sock.sendall(b'Hello')
        ...     finally:
        ...         sock.close()
    
    Common errors handled:
        - socket.timeout: Server did not respond in time
        - ConnectionRefusedError: Server not running or port blocked
        - OSError (ENETUNREACH): Network is not reachable
        - OSError (EHOSTUNREACH): Host is not reachable
    """
    for attempt in range(1, max_retries + 1):
        sock = None
        try:
            logger.info(f"Attempt {attempt}/{max_retries}: Connecting to {host}:{port}")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            logger.info(f"Connected successfully to {host}:{port}")
            return sock
            
        except socket.timeout:
            logger.warning(f"Attempt {attempt}: Connection timed out after {timeout}s")
            
        except ConnectionRefusedError:
            logger.warning(f"Attempt {attempt}: Connection refused (is server running?)")
            
        except OSError as e:
            if e.errno == errno.ENETUNREACH:
                logger.warning(f"Attempt {attempt}: Network unreachable")
            elif e.errno == errno.EHOSTUNREACH:
                logger.warning(f"Attempt {attempt}: Host unreachable")
            else:
                logger.warning(f"Attempt {attempt}: OS error — {e}")
                
        except Exception as e:
            logger.error(f"Attempt {attempt}: Unexpected error — {type(e).__name__}: {e}")
        
        finally:
            # Clean up failed socket
            if sock is not None:
                try:
                    sock.close()
                except Exception:
                    pass
        
        # Wait before retrying (except on last attempt)
        if attempt < max_retries:
            logger.info(f"Waiting {retry_delay}s before retry...")
            time.sleep(retry_delay)
    
    logger.error(f"All {max_retries} connection attempts failed")
    return None


@contextmanager
def safe_connection(
    host: str,
    port: int,
    timeout: float = DEFAULT_TIMEOUT
):
    """
    Context manager for safe socket connections.
    
    Ensures the socket is always closed, even if an exception occurs.
    
    Args:
        host: Target hostname or IP address.
        port: Target port number.
        timeout: Connection timeout in seconds.
        
    Yields:
        Connected socket.
        
    Raises:
        ConnectionError: If connection fails.
        
    Example:
        >>> try:
        ...     with safe_connection('localhost', 8080) as sock:
        ...         sock.sendall(b'Hello')
        ...         response = sock.recv(1024)
        ... except ConnectionError as e:
        ...     print(f"Could not connect: {e}")
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        sock.connect((host, port))
        yield sock
    finally:
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# DATA RECEPTION
# ═══════════════════════════════════════════════════════════════════════════════

def recv_exactly(sock: socket.socket, length: int) -> bytes:
    """
    Receive exactly the specified number of bytes from a socket.
    
    TCP is a stream protocol — recv() may return fewer bytes than
    requested. This function loops until all bytes are received.
    
    Args:
        sock: Connected socket to receive from.
        length: Exact number of bytes to receive.
        
    Returns:
        Bytes object of exactly `length` bytes.
        
    Raises:
        ConnectionError: If connection closes before all bytes received.
        ValueError: If length is negative.
        
    Example:
        >>> # Receive a 4-byte length prefix
        >>> length_bytes = recv_exactly(sock, 4)
        >>> length = struct.unpack('!I', length_bytes)[0]
        >>> # Now receive the payload
        >>> payload = recv_exactly(sock, length)
    """
    if length < 0:
        raise ValueError(f"Length must be non-negative, got {length}")
    
    if length == 0:
        return b''
    
    chunks = []
    bytes_received = 0
    
    while bytes_received < length:
        remaining = length - bytes_received
        chunk = sock.recv(min(remaining, BUFFER_SIZE))
        
        if not chunk:
            raise ConnectionError(
                f"Connection closed after receiving {bytes_received}/{length} bytes"
            )
        
        chunks.append(chunk)
        bytes_received += len(chunk)
        logger.debug(f"Received {len(chunk)} bytes ({bytes_received}/{length} total)")
    
    return b''.join(chunks)


def recv_until(
    sock: socket.socket,
    delimiter: bytes,
    max_length: int = 65536
) -> bytes:
    """
    Receive data until a delimiter is found.
    
    Useful for protocols that use line endings or other delimiters.
    
    Args:
        sock: Connected socket to receive from.
        delimiter: Bytes sequence marking end of message.
        max_length: Maximum bytes to receive (prevents memory exhaustion).
        
    Returns:
        Received data including the delimiter.
        
    Raises:
        ConnectionError: If connection closes before delimiter found.
        ValueError: If max_length exceeded without finding delimiter.
        
    Example:
        >>> # Receive an HTTP header line
        >>> line = recv_until(sock, b'\\r\\n')
        >>> print(line.decode())
    """
    data = b''
    
    while delimiter not in data:
        if len(data) >= max_length:
            raise ValueError(
                f"Delimiter not found within {max_length} bytes"
            )
        
        chunk = sock.recv(1)  # Read one byte at a time for accuracy
        
        if not chunk:
            raise ConnectionError(
                f"Connection closed before delimiter found (received {len(data)} bytes)"
            )
        
        data += chunk
    
    return data


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER-SIDE ERROR HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

def create_server_socket(
    host: str,
    port: int,
    backlog: int = 5
) -> socket.socket:
    """
    Create and bind a server socket with proper error handling.
    
    Sets SO_REUSEADDR to avoid "Address already in use" errors
    when restarting the server quickly.
    
    Args:
        host: Address to bind to ('0.0.0.0' for all interfaces).
        port: Port number to bind to.
        backlog: Maximum queued connections.
        
    Returns:
        Bound and listening socket.
        
    Raises:
        PermissionError: If port < 1024 and not running as root.
        OSError: If address is already in use (despite SO_REUSEADDR).
        
    Example:
        >>> server = create_server_socket('0.0.0.0', 8080)
        >>> try:
        ...     while True:
        ...         client, addr = server.accept()
        ...         handle_client(client)
        ... finally:
        ...     server.close()
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Allow address reuse (prevents "Address already in use")
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server.bind((host, port))
        server.listen(backlog)
        
        logger.info(f"Server listening on {host}:{port}")
        return server
        
    except PermissionError:
        server.close()
        raise PermissionError(
            f"Cannot bind to port {port}. Ports below 1024 require root privileges. "
            f"Try using port 8080 or higher."
        )
    except OSError as e:
        server.close()
        if e.errno == errno.EADDRINUSE:
            raise OSError(
                f"Port {port} is already in use. "
                f"Check with: lsof -i :{port}"
            )
        raise


def handle_client_safely(
    client: socket.socket,
    addr: Tuple[str, int],
    handler_func
) -> None:
    """
    Wrapper to handle a client connection with proper error handling.
    
    Ensures the client socket is always closed, even if the handler
    function raises an exception.
    
    Args:
        client: Client socket from accept().
        addr: Client address tuple (ip, port).
        handler_func: Function to process the client (takes socket, addr).
        
    Example:
        >>> def echo_handler(sock, addr):
        ...     data = sock.recv(1024)
        ...     sock.sendall(data)
        ...
        >>> client, addr = server.accept()
        >>> handle_client_safely(client, addr, echo_handler)
    """
    try:
        logger.info(f"Handling client from {addr[0]}:{addr[1]}")
        handler_func(client, addr)
        logger.info(f"Client {addr[0]}:{addr[1]} handled successfully")
        
    except socket.timeout:
        logger.warning(f"Client {addr[0]}:{addr[1]} timed out")
        
    except ConnectionResetError:
        logger.warning(f"Client {addr[0]}:{addr[1]} reset connection")
        
    except BrokenPipeError:
        logger.warning(f"Client {addr[0]}:{addr[1]} closed connection unexpectedly")
        
    except Exception as e:
        logger.error(f"Error handling client {addr[0]}:{addr[1]}: {e}")
        
    finally:
        try:
            client.close()
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def demo_connection_retry() -> None:
    """Demonstrate connection retry behaviour."""
    print("\n" + "=" * 60)
    print("DEMO: Connection with Retry")
    print("=" * 60)
    print("\nAttempting to connect to a non-existent server...")
    print("(This will fail but demonstrates error handling)\n")
    
    sock = connect_with_retry(
        host='localhost',
        port=59999,  # Unlikely to have a server here
        timeout=1.0,
        max_retries=2,
        retry_delay=0.5
    )
    
    if sock:
        sock.close()
        print("Unexpectedly succeeded!")
    else:
        print("\nConnection failed as expected (no server on port 59999)")


def demo_recv_exactly() -> None:
    """Demonstrate recv_exactly behaviour."""
    print("\n" + "=" * 60)
    print("DEMO: Receive Exactly N Bytes")
    print("=" * 60)
    
    # Create a simple server-client pair using socketpair
    print("\nUsing socketpair to demonstrate partial receives...")
    
    server_sock, client_sock = socket.socketpair()
    
    try:
        # Server sends 100 bytes
        data = b'X' * 100
        server_sock.sendall(data)
        print(f"Sent {len(data)} bytes")
        
        # Client receives exactly 100 bytes
        received = recv_exactly(client_sock, 100)
        print(f"Received exactly {len(received)} bytes")
        
        assert len(received) == 100, "Did not receive exactly 100 bytes"
        print("✓ recv_exactly works correctly")
        
    finally:
        server_sock.close()
        client_sock.close()


def demo_common_errors() -> None:
    """Demonstrate common socket errors."""
    print("\n" + "=" * 60)
    print("DEMO: Common Socket Errors")
    print("=" * 60)
    
    # 1. Connection Refused
    print("\n1. ConnectionRefusedError:")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        sock.connect(('localhost', 59998))
    except ConnectionRefusedError as e:
        print(f"   Caught: {type(e).__name__}")
        print(f"   This means: No server is listening on that port")
    finally:
        sock.close()
    
    # 2. Timeout
    print("\n2. socket.timeout:")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.001)  # Very short timeout
        sock.connect(('8.8.8.8', 80))  # Will likely timeout
    except socket.timeout as e:
        print(f"   Caught: socket.timeout")
        print(f"   This means: Server did not respond within timeout period")
    except Exception as e:
        print(f"   Caught: {type(e).__name__} (network may have responded)")
    finally:
        sock.close()
    
    # 3. Address Already in Use (simulation)
    print("\n3. Address Already in Use:")
    print("   This occurs when you try to bind to a port that is already bound.")
    print("   Fix: Use SO_REUSEADDR or wait for TIME_WAIT to expire.")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 60)
    print("Error Handling Examples for Network Programming")
    print("=" * 60)
    
    demo_recv_exactly()
    demo_common_errors()
    demo_connection_retry()
    
    print("\n" + "=" * 60)
    print("All demonstrations complete.")
    print("=" * 60)
