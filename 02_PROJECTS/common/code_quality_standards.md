# 💻 Code Quality Standards
## Computer Networks Projects — ASE Bucharest, CSIE

> **Purpose:** Standards for Python code in all network projects.  
> **Applies to:** All projects P01-P20

---

## Subgoal Labels (Mandatory)

Every Python file must use subgoal labels to mark logical sections:

```python
# ═══════════════════════════════════════════════════════════════════════════════
# SECTION_NAME_IN_CAPS
# ═══════════════════════════════════════════════════════════════════════════════
```

### Standard Sections

| Section | When to use |
|---------|-------------|
| `IMPORTS` | All import statements |
| `CONSTANTS` | Configuration values, magic numbers |
| `SETUP_ENVIRONMENT` | Initial configuration |
| `PARSE_ARGUMENTS` | Command-line argument handling |
| `VERIFY_PREREQUISITES` | Check Docker, network, dependencies |
| `CORE_LOGIC` | Main functionality |
| `HELPER_FUNCTIONS` | Utility functions |
| `ERROR_HANDLING` | Exception handlers |
| `CLEANUP` | Resource cleanup |
| `MAIN` | Entry point |

### Example Structure

```python
#!/usr/bin/env python3
"""
Module description here.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import sys
from typing import Optional, Tuple, List

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_PORT = 8080
BUFFER_SIZE = 4096
TIMEOUT_SECONDS = 30

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def validate_port(port: int) -> bool:
    """Check if port number is valid."""
    return 1 <= port <= 65535

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def create_server(host: str, port: int) -> socket.socket:
    """Create and configure a TCP server socket."""
    ...

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Entry point."""
    ...

if __name__ == "__main__":
    sys.exit(main())
```

---

## Type Hints (Mandatory)

All functions must have type hints for parameters and return values.

### Basic Types

```python
def process_packet(data: bytes, length: int) -> str:
    ...

def get_config(key: str) -> Optional[str]:
    ...

def list_containers() -> List[str]:
    ...
```

### Complex Types

```python
from typing import Dict, Tuple, Callable, Union

def parse_headers(raw: bytes) -> Dict[str, str]:
    ...

def get_address() -> Tuple[str, int]:
    ...

def register_handler(callback: Callable[[bytes], None]) -> None:
    ...
```

### Common Network Types

```python
# Type aliases for clarity
IPAddress = str
Port = int
SocketAddress = Tuple[IPAddress, Port]

def connect(address: SocketAddress) -> socket.socket:
    ...
```

---

## Docstrings (Mandatory)

Use Google-style docstrings for all functions and classes.

### Function Docstring Template

```python
def send_packet(sock: socket.socket, data: bytes, timeout: float = 5.0) -> int:
    """
    Send data packet through socket with timeout.
    
    Sends the complete data buffer, handling partial sends automatically.
    Raises exception if send fails or times out.
    
    Args:
        sock: Connected socket object
        data: Bytes to send
        timeout: Maximum time to wait in seconds (default: 5.0)
        
    Returns:
        Number of bytes actually sent
        
    Raises:
        socket.timeout: If send exceeds timeout
        ConnectionError: If connection is lost
        
    Example:
        >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        >>> sock.connect(('localhost', 8080))
        >>> bytes_sent = send_packet(sock, b'Hello')
        >>> print(f"Sent {bytes_sent} bytes")
    """
    ...
```

### Class Docstring Template

```python
class PacketParser:
    """
    Parse network packets from raw bytes.
    
    Handles TCP and UDP packet parsing with support for
    custom protocol headers.
    
    Attributes:
        protocol: Protocol type ('tcp' or 'udp')
        buffer_size: Maximum buffer size in bytes
        
    Example:
        >>> parser = PacketParser(protocol='tcp')
        >>> header = parser.parse(raw_data)
        >>> print(header.source_port)
    """
    
    def __init__(self, protocol: str = 'tcp', buffer_size: int = 4096):
        """
        Initialise packet parser.
        
        Args:
            protocol: Protocol to parse ('tcp' or 'udp')
            buffer_size: Maximum buffer size (default: 4096)
        """
        ...
```

---

## Error Handling

### Always Use Specific Exceptions

```python
# ✗ BAD — too broad
try:
    sock.connect((host, port))
except Exception as e:
    print(f"Error: {e}")

# ✓ GOOD — specific exceptions
try:
    sock.connect((host, port))
except socket.timeout:
    print(f"Connection timed out after {timeout}s")
except ConnectionRefusedError:
    print(f"Connection refused — is the server running?")
except OSError as e:
    print(f"Network error: {e}")
```

### Use Context Managers

```python
# ✗ BAD — manual cleanup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((host, port))
    # ... use socket
finally:
    sock.close()

# ✓ GOOD — context manager
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    # ... use socket (auto-closed)
```

### Logging Instead of Print

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use throughout code
logger.info(f"Connected to {host}:{port}")
logger.warning(f"Slow response: {elapsed:.2f}s")
logger.error(f"Connection failed: {e}")
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `packet_count`, `source_ip` |
| Functions | snake_case | `send_packet()`, `parse_header()` |
| Classes | PascalCase | `PacketParser`, `TcpServer` |
| Constants | UPPER_SNAKE | `MAX_BUFFER`, `DEFAULT_PORT` |
| Private | _prefix | `_internal_buffer`, `_validate()` |
| Module | snake_case | `network_utils.py` |

### Meaningful Names

```python
# ✗ BAD
def proc(d):
    for i in d:
        if i > t:
            return True

# ✓ GOOD
def has_packets_above_threshold(packet_sizes: List[int], threshold: int) -> bool:
    for size in packet_sizes:
        if size > threshold:
            return True
    return False
```

---

## Prediction Prompts in Code

Add prediction prompts before important operations:

```python
# 💭 PREDICTION: What will happen if the server is not running?
# Your answer: _______________
try:
    sock.connect((host, port))
except ConnectionRefusedError:
    print("Cannot connect — server not running")

# 💭 PREDICTION: How many packets will this capture in 10 seconds?
# Your answer: _______________
packets = capture_traffic(interface='eth0', duration=10)
print(f"Captured {len(packets)} packets")

# 💭 PREDICTION: What HTTP status code will this return?
# Your answer: _______________
response = requests.get('http://localhost:8080/api/status')
print(f"Status: {response.status_code}")
```

---

## File Organisation

### Standard Project Structure

```
src/
├── __init__.py
├── main.py              # Entry point
├── server.py            # Server implementation
├── client.py            # Client implementation
├── protocol.py          # Protocol handling
└── utils/
    ├── __init__.py
    ├── network.py       # Network utilities
    ├── parsing.py       # Data parsing
    └── validation.py    # Input validation
```

### Import Order

```python
# 1. Standard library imports
import os
import sys
import socket
from typing import Optional, List

# 2. Third-party imports
import requests
import docker

# 3. Local imports
from .utils import network
from .protocol import PacketParser
```

---

## Code Review Checklist

Before submitting, verify:

```
□ All functions have type hints
□ All functions have docstrings
□ Subgoal labels mark each section
□ No bare except clauses
□ Context managers used for resources
□ Meaningful variable names
□ No magic numbers (use constants)
□ Logging instead of print (for production code)
□ Prediction prompts in exercises
□ British spelling in comments (analyse, behaviour, colour)
```

---

## Complete Example

```python
#!/usr/bin/env python3
"""
TCP Echo Server — demonstrates proper code structure.

This server accepts connections and echoes back any received data.
Used for testing network connectivity and message handling.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import logging
import socket
import sys
from typing import Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 8080
BUFFER_SIZE = 4096
MAX_CONNECTIONS = 5

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_SETUP
# ═══════════════════════════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def validate_port(port: int) -> bool:
    """
    Check if port number is within valid range.
    
    Args:
        port: Port number to validate
        
    Returns:
        True if port is valid (1-65535), False otherwise
    """
    return 1 <= port <= 65535


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """
    Handle a single client connection.
    
    Receives data from client and echoes it back until
    the client disconnects.
    
    Args:
        conn: Client socket connection
        addr: Client address tuple (ip, port)
    """
    logger.info(f"Client connected: {addr[0]}:{addr[1]}")
    
    try:
        while True:
            # 💭 PREDICTION: What happens if client sends empty data?
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            
            logger.info(f"Received {len(data)} bytes from {addr[0]}")
            conn.sendall(data)
            
    except ConnectionResetError:
        logger.warning(f"Client {addr[0]} disconnected unexpectedly")
    finally:
        conn.close()
        logger.info(f"Connection closed: {addr[0]}:{addr[1]}")


def run_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """
    Start the echo server.
    
    Args:
        host: Interface to bind to (default: all interfaces)
        port: Port to listen on (default: 8080)
        
    Raises:
        OSError: If port is already in use
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(MAX_CONNECTIONS)
        
        logger.info(f"Server listening on {host}:{port}")
        
        while True:
            conn, addr = server.accept()
            handle_client(conn, addr)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Entry point for echo server.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    port = DEFAULT_PORT
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if not validate_port(port):
                logger.error(f"Invalid port: {port}")
                return 1
        except ValueError:
            logger.error(f"Port must be a number: {sys.argv[1]}")
            return 1
    
    try:
        run_server(port=port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except OSError as e:
        logger.error(f"Server error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

*Code Quality Standards v1.0 — Computer Networks, ASE Bucharest*
