# 🐍 Python Quick Reference — Networking

> **Cheatsheet** for Computer Networks Lab
> Version: January 2025

---

## Data Types

### Bytes vs Strings

```python
# String (text for humans)
text = "Hello"

# Bytes (what's sent on network)
data = b"Hello"

# Conversions
data = text.encode('utf-8')     # str → bytes
text = data.decode('utf-8')     # bytes → str
```

### Dataclasses

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class PacketInfo:
    src_ip: str
    dst_ip: str
    protocol: int
    length: int
    payload: Optional[bytes] = None
```

---

## Sockets

### TCP Server

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8080))
    s.listen(5)

    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        conn.sendall(b"Response")
```

### TCP Client

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 8080))
    s.sendall(b"Request")
    response = s.recv(1024)
```

### UDP Server

```python
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('0.0.0.0', 8080))
    data, addr = s.recvfrom(1024)
    s.sendto(b"Response", addr)
```

### UDP Client

```python
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Request", ('127.0.0.1', 8080))
    response, _ = s.recvfrom(1024)
```

---

## Binary Parsing (struct)

### Format Codes

| Code | Type | Bytes | Description |
|------|------|-------|-------------|
| `!` | - | - | Network byte order (big-endian) |
| `B` | unsigned char | 1 | 0-255 |
| `H` | unsigned short | 2 | 0-65535 |
| `I` | unsigned int | 4 | 0-4294967295 |
| `Q` | unsigned long long | 8 | Large numbers |
| `s` | char[] | n | Byte string |

### Examples

```python
import struct

# Pack
header = struct.pack('!HH', 8080, 443)  # 4 bytes

# Apack
src_port, dst_port = struct.unpack('!HH', header)
```

---

## CLI Arguments (argparse)

```python
import argparse

parser = argparse.ArgumentParser(description="Port Scanner")
parser.add_argument("host", help="Target host")
parser.add_argument("--port", "-p", type=int, default=80)
parser.add_argument("--verbose", "-v", action="store_true")

args = parser.parse_args()
print(f"Scanning {args.host}:{args.port}")
```

---

## Threading

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_port(host, port):
    # ... implementation
    return port, is_open

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = {executor.submit(check_port, host, p): p for p in ports}
    for future in as_completed(futures):
        port, is_open = future.result()
```

---

## Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

logger.debug("Debug info")
logger.info("General info")
logger.warning("Warning")
logger.error("Error!")
```

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `TypeError: bytes-like object required` | Sent str instead of bytes | Use `.encode()` |
| `Address already in use` | Port occupied | Use `SO_REUSEADDR` |
| `Connection refused` | Server not running | Start server first |
| `Permission denied` | Port <1024 or docker | Use sudo or add to docker group |

---

*Python Quick Reference — Computer Networks Lab*
*ASE Bucharest, CSIE*
