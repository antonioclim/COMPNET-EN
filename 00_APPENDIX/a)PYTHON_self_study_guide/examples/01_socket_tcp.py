#!/usr/bin/env python3
"""
Example 1: Basic TCP Server and Client
======================================
Demonstrates fundamental socket programming concepts.

Course: Computer Networks - ASE Bucharest, CSIE
Author: ing. dr. Antonio Clim
Version: 2.2 — with refactored helpers for maintainability

💡 ANALOGY: Socket as a Landline Telephone
------------------------------------------
| Socket Operation | Telephone Equivalent                  |
|------------------|---------------------------------------|
| socket()         | You buy a new telephone               |
| bind()           | You get assigned a phone number (port)|
| listen()         | You plug in the phone, wait for calls |
| accept()         | You pick up the receiver when it rings|
| connect()        | You dial someone's number             |
| send()/recv()    | You speak / You listen                |
| close()          | You hang up the phone                 |

Learning objectives:
- Understanding the client-server model
- Proper handling of network errors
- Context manager pattern for resources
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import sys
import logging
from typing import Optional, Tuple

__all__ = ['server', 'client', 'DEFAULT_HOST', 'DEFAULT_PORT', 'BUFFER_SIZE']

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_HOST: str = '0.0.0.0'
DEFAULT_PORT: int = 8080
BUFFER_SIZE: int = 1024
SOCKET_TIMEOUT: float = 30.0
MAX_CONNECTIONS: int = 5


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def _create_server_socket(port: int) -> socket.socket:
    """Create and configure a server socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # HACK: SO_REUSEADDR allows quick rebind after restart
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((DEFAULT_HOST, port))
    s.listen(MAX_CONNECTIONS)
    return s


def _handle_client_data(conn: socket.socket, addr: Tuple) -> None:
    """Process data from a connected client."""
    conn.settimeout(SOCKET_TIMEOUT)
    
    try:
        data: bytes = conn.recv(BUFFER_SIZE)
        
        if not data:
            logger.warning(f"Client {addr} sent empty data")
            return
        
        decoded = data.decode('utf-8', errors='replace')
        print(f"[SERVER] Received: {decoded}")
        logger.info(f"Received from {addr}: {decoded[:50]}...")
        
        response: bytes = b"OK: " + data.upper()
        conn.sendall(response)
        print(f"[SERVER] Sent: {response.decode('utf-8', errors='replace')}")
        
    except socket.timeout:
        logger.warning(f"Timeout reading from {addr}")
        print(f"[SERVER] Timeout - client {addr} did not send data")
        
    except UnicodeDecodeError as e:
        logger.error(f"Decode error from {addr}: {e}")
        print(f"[SERVER] Decode error: {e}")
        conn.sendall(b"ERROR: Invalid encoding")


def _handle_connection(conn: socket.socket, addr: Tuple) -> None:
    """Handle a single client connection."""
    logger.info(f"New connection from {addr}")
    print(f"[SERVER] Connection from {addr}")
    
    with conn:
        try:
            _handle_client_data(conn, addr)
        except ConnectionResetError:
            logger.warning("Client disconnected abruptly")
            print("[SERVER] Client disconnected abruptly")
        except ConnectionAbortedError:
            logger.warning("Connection aborted")
            print("[SERVER] Connection aborted")


def _handle_server_error(e: OSError) -> None:
    """Handle server startup errors with helpful messages."""
    logger.error(f"Cannot start server: {e}")
    print(f"[ERROR] Cannot start server: {e}")
    
    if "Address already in use" in str(e):
        print("  → The port is already in use!")
        print("  → Solutions:")
        print("    1. Wait ~60 seconds and try again")
        print("    2. Use a different port: python script.py server 8081")
        print("    3. Check what's using the port: ss -tlnp | grep 8080")


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

def server(port: int = DEFAULT_PORT) -> None:
    """Start a simple TCP server that echoes messages.
    
    Args:
        port: The port to listen on (default 8080)
    """
    try:
        with _create_server_socket(port) as s:
            logger.info(f"Server started on port {port}")
            print(f"[SERVER] Listening on port {port}...")
            print("[SERVER] Stop with Ctrl+C")
            
            while True:
                conn, addr = s.accept()
                _handle_connection(conn, addr)
                    
    except OSError as e:
        _handle_server_error(e)
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        print("\n[SERVER] Stopped at user's request (Ctrl+C)")


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def _send_and_receive(sock: socket.socket, message: str) -> Optional[str]:
    """Send message and receive response."""
    print(f"[CLIENT] Sending: {message}")
    sock.sendall(message.encode('utf-8'))
    
    response: bytes = sock.recv(BUFFER_SIZE)
    
    if not response:
        logger.warning("Server closed connection without response")
        print("[CLIENT] Server did not send a response")
        return None
        
    response_str = response.decode('utf-8', errors='replace')
    print(f"[CLIENT] Response: {response_str}")
    logger.info(f"Response received: {response_str[:50]}...")
    
    return response_str


def _handle_client_error(e: Exception, host: str, port: int) -> None:
    """Handle client connection errors with helpful messages."""
    if isinstance(e, socket.timeout):
        logger.error(f"Timeout connecting to {host}:{port}")
        print("[ERROR] Timeout - server not responding within 10 seconds")
        print("  → Check if the server is running")
        
    elif isinstance(e, ConnectionRefusedError):
        logger.error(f"Connection refused by {host}:{port}")
        print(f"[ERROR] Connection refused by {host}:{port}")
        print("  → Server is not running or port is wrong")
        print("  → Start the server: python 01_socket_tcp.py server")
        
    elif isinstance(e, socket.gaierror):
        logger.error(f"DNS error for {host}: {e}")
        print(f"[ERROR] Cannot resolve address '{host}': {e}")
        
    else:
        logger.error(f"Network error: {e}")
        print(f"[ERROR] Network problem: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

def client(host: str = '127.0.0.1', port: int = DEFAULT_PORT, 
           message: str = 'Test') -> Optional[str]:
    """Send a message to the server and return the response.
    
    Args:
        host: Server IP address or hostname
        port: Server port (default 8080)
        message: Message to send (default 'Test')
        
    Returns:
        Server response as string, or None if failed
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10.0)
            
            logger.info(f"Connecting to {host}:{port}")
            s.connect((host, port))
            print(f"[CLIENT] Connected to {host}:{port}")
            
            return _send_and_receive(s, message)
            
    except (socket.timeout, ConnectionRefusedError, 
            socket.gaierror, OSError) as e:
        _handle_client_error(e, host, port)
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# USER_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def print_usage() -> None:
    """Display usage instructions."""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║  01_socket_tcp.py - TCP Server/Client Example                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║  USAGE:                                                               ║
║    Server:  python 01_socket_tcp.py server [port]                     ║
║    Client:  python 01_socket_tcp.py [message]                         ║
║    Client:  python 01_socket_tcp.py client [host] [port] [message]    ║
║                                                                       ║
║  EXAMPLES:                                                            ║
║    python 01_socket_tcp.py server              # Server on 8080       ║
║    python 01_socket_tcp.py server 9000         # Server on 9000       ║
║    python 01_socket_tcp.py "Hello world"       # Client to 8080       ║
║    python 01_socket_tcp.py client 192.168.1.5 8080 "Test"             ║
║                                                                       ║
║  DEBUGGING:                                                           ║
║    - Check port: ss -tlnp | grep 8080                                 ║
║    - Enable debug: export LOG_LEVEL=DEBUG                             ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point — parses arguments and executes."""
    if len(sys.argv) < 2:
        print_usage()
        return 0
        
    if sys.argv[1] == 'server':
        port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
        server(port)
        return 0
        
    elif sys.argv[1] == 'client':
        host = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_PORT
        msg = ' '.join(sys.argv[4:]) if len(sys.argv) > 4 else 'Hello'
        result = client(host, port, msg)
        return 0 if result else 1
        
    elif sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        return 0
        
    else:
        message = ' '.join(sys.argv[1:])
        result = client(message=message)
        return 0 if result else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
