# 🔧 Troubleshooting Guide
## Python for Networking — Common Issues and Solutions

> **Purpose:** Self-diagnosis for common errors in Python networking code
> **Format:** Symptom → Cause → Fix → Verify
> **Version:** 5.0 — January 2026

---

## Quick Diagnostic Table

| Error Message | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| `TypeError: a bytes-like object is required` | Forgot `.encode()` | Use `b"text"` or `"text".encode()` |
| `ConnectionRefusedError` | Server not running | Start the server first |
| `OSError: Address already in use` | Port occupied | Use `SO_REUSEADDR` or different port |
| `socket.timeout` | Server too slow | Increase timeout value |
| `ModuleNotFoundError: yaml` | PyYAML not installed | `pip install pyyaml` |
| `SyntaxError` on `{` | Using braces instead of colon | Use `:` and indentation |
| `IndentationError` | Mixed tabs and spaces | Use spaces only (4 per level) |
| `NameError: 'const'` | Using JS/Kotlin keywords | Just assign: `PORT = 8080` |
| `AttributeError` on dict | Using dot notation | Use brackets: `d["key"]` |
| `UnicodeDecodeError` | Wrong encoding | Specify encoding or use `errors='replace'` |

---

## Detailed Scenarios

### 1. TypeError: a bytes-like object is required, not 'str'

**When it appears:** Sending data through a socket

**Error example:**
```
TypeError: a bytes-like object is required, not 'str'
```

**Cause:** Python 3 strictly separates bytes from strings. Sockets work ONLY with bytes.

**Fix:**
```python
# ❌ Wrong
sock.send("Hello")

# ✅ Correct options
sock.send(b"Hello")              # bytes literal
sock.send("Hello".encode())      # explicit conversion
sock.send("Hello".encode('utf-8'))  # with encoding specified
```

**Verify:** Run the code — no TypeError appears.

**See also:** [Misconceptions → C/C++ → Strings Are Byte Arrays](../comparisons/MISCONCEPTIONS_BY_BACKGROUND.md#for-cc-programmers)

---

### 2. ConnectionRefusedError: [Errno 111] Connection refused

**When it appears:** Client trying to connect to a server

**Error example:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Cause:** The server is not running or is listening on a different port/address.

**Fix:**
```python
# 1. Start the server FIRST in one terminal:
python server.py

# 2. Then run the client in another terminal:
python client.py

# 3. Verify server is listening:
# Linux/WSL:
netstat -tlnp | grep 8080
# or
ss -tlnp | grep 8080
```

**Verify:** `netstat` shows the server listening on the expected port.

**Common mistakes:**
- Server bound to `127.0.0.1` but client connecting to `0.0.0.0`
- Server on port 8080 but client connecting to 80
- Firewall blocking the connection

---

### 3. OSError: [Errno 98] Address already in use

**When it appears:** Starting a server that was recently stopped

**Error example:**
```
OSError: [Errno 98] Address already in use
```

**Cause:** The port is still in TIME_WAIT state from a previous connection or another process is using it.

**Fix:**
```python
# Add SO_REUSEADDR before bind()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ← Add this
server.bind(('0.0.0.0', 8080))
```

**Alternative:** Find and kill the process using the port:
```bash
# Find process
lsof -i :8080
# or
fuser 8080/tcp

# Kill it
kill -9 <PID>
```

**Verify:** Server starts without error.

---

### 4. socket.timeout: timed out

**When it appears:** Waiting for data that never arrives

**Error example:**
```
socket.timeout: timed out
```

**Cause:** The timeout expired before data was received. The remote end may be slow or not responding.

**Fix:**
```python
# Increase timeout (default is None = wait forever)
sock.settimeout(30.0)  # 30 seconds

# Or handle the timeout gracefully
try:
    data = sock.recv(1024)
except socket.timeout:
    print("Server did not respond in time")
    # Retry or exit gracefully
```

**Verify:** Either data arrives or timeout is handled without crashing.

---

### 5. ModuleNotFoundError: No module named 'yaml'

**When it appears:** Running the quiz or any script that uses YAML

**Error example:**
```
ModuleNotFoundError: No module named 'yaml'
```

**Cause:** PyYAML package is not installed.

**Fix:**
```bash
# Standard installation
pip install pyyaml

# If permission error
pip install --user pyyaml

# On some systems
pip3 install pyyaml

# WSL/Ubuntu with system Python
pip install pyyaml --break-system-packages
```

**Verify:**
```bash
python -c "import yaml; print('OK')"
```

---

### 6. SyntaxError: invalid syntax (on `{` or `}`)

**When it appears:** Writing Python with C/Java/JavaScript habits

**Error example:**
```
  File "script.py", line 3
    if (x > 5) {
               ^
SyntaxError: invalid syntax
```

**Cause:** Python uses indentation for blocks, not braces.

**Fix:**
```python
# ❌ Wrong (C/Java/JavaScript style)
if (x > 5) {
    print("large")
}

# ✅ Correct (Python style)
if x > 5:
    print("large")
```

**Verify:** No SyntaxError on execution.

**See also:** [Misconceptions → JavaScript](../comparisons/MISCONCEPTIONS_BY_BACKGROUND.md#for-javascript-programmers)

---

### 7. IndentationError: unexpected indent

**When it appears:** Mixing tabs and spaces or inconsistent indentation

**Error example:**
```
IndentationError: unexpected indent
```

**Cause:** Python is strict about indentation. Mixing tabs and spaces causes this error.

**Fix:**
```python
# Configure your editor to:
# 1. Use spaces, not tabs
# 2. Use 4 spaces per indentation level
# 3. Show whitespace characters

# In VS Code: Settings → "Editor: Render Whitespace" → "all"
# In PyCharm: Settings → Editor → General → Appearance → "Show whitespaces"
```

**Quick fix for existing file:**
```bash
# Convert tabs to spaces
expand -t 4 script.py > script_fixed.py
```

**Verify:** No IndentationError on execution.

---

### 8. NameError: name 'const' is not defined

**When it appears:** Using JavaScript or Kotlin keywords in Python

**Error example:**
```
NameError: name 'const' is not defined
```

**Cause:** Python does not have `const`, `let`, `var`, `val` keywords.

**Fix:**
```python
# ❌ Wrong (JavaScript/Kotlin style)
const PORT = 8080
let counter = 0
val host = "localhost"

# ✅ Correct (Python style)
PORT = 8080        # Convention: CAPS for constants
counter = 0        # All variables are reassignable
host = "localhost"
```

**Verify:** No NameError on execution.

---

### 9. AttributeError: 'dict' object has no attribute 'port'

**When it appears:** Using dot notation on dictionaries

**Error example:**
```
AttributeError: 'dict' object has no attribute 'port'
```

**Cause:** Python dictionaries use bracket notation, not dot notation.

**Fix:**
```python
# ❌ Wrong (JavaScript style)
config = {"host": "localhost", "port": 8080}
print(config.port)  # AttributeError!

# ✅ Correct (Python style)
print(config["port"])  # Use brackets

# ✅ Alternative: Use dataclass for dot notation
from dataclasses import dataclass

@dataclass
class Config:
    host: str
    port: int

config = Config(host="localhost", port=8080)
print(config.port)  # Works!
```

**Verify:** Attribute access works without error.

---

### 10. UnicodeDecodeError: 'utf-8' codec can't decode byte

**When it appears:** Decoding bytes that are not valid UTF-8

**Error example:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 0
```

**Cause:** The data is not valid UTF-8 (might be binary or different encoding).

**Fix:**
```python
# Option 1: Handle errors gracefully
text = data.decode('utf-8', errors='replace')  # Replace invalid bytes with �
text = data.decode('utf-8', errors='ignore')   # Skip invalid bytes

# Option 2: Try different encoding
text = data.decode('latin-1')  # Never fails for single-byte data
text = data.decode('cp1252')   # Windows encoding

# Option 3: Check if data is actually binary
if data[:4] == b'\x89PNG':
    print("This is a PNG image, not text!")
```

**Verify:** Decoding completes without exception.

---

### 11. recv() returns empty bytes b''

**When it appears:** Reading from a socket after the connection closed

**Symptom:** `sock.recv(1024)` returns `b''` (empty bytes).

**Cause:** The remote end closed the connection. This is NOT an error — it is the normal way to detect connection closure.

**Fix:**
```python
# ✅ Correct handling
while True:
    data = sock.recv(1024)
    if not data:  # Empty bytes = connection closed
        print("Connection closed by remote end")
        break
    process(data)
```

**Common mistake:**
```python
# ❌ Wrong: Infinite loop if connection closes
while True:
    data = sock.recv(1024)  # Returns b'' forever
    print(data)  # Prints b'' infinitely
```

**Verify:** Loop exits gracefully when connection closes.

---

### 12. recv() returns less data than expected

**When it appears:** Receiving large messages over TCP

**Symptom:** Sent 1000 bytes but `recv(1024)` returns only 500 bytes.

**Cause:** TCP is a STREAM protocol. Data may arrive in multiple chunks.

**Fix:**
```python
def recv_exactly(sock: socket.socket, length: int) -> bytes:
    """Receive exactly `length` bytes from socket."""
    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed before receiving all data")
        data += chunk
    return data

# Usage
message = recv_exactly(sock, 1000)  # Guaranteed 1000 bytes
```

**Verify:** All expected bytes are received.

**See also:** [Misconceptions → Universal → recv() Returns Complete Message](../comparisons/MISCONCEPTIONS_BY_BACKGROUND.md#universal-networking-misconceptions)

---

### 13. PermissionError: [Errno 13] Permission denied (port < 1024)

**When it appears:** Binding to ports below 1024 without root privileges

**Error example:**
```
PermissionError: [Errno 13] Permission denied
```

**Cause:** Ports 0-1023 are "privileged ports" and require root/admin access.

**Fix:**
```python
# ❌ Requires root
server.bind(('0.0.0.0', 80))   # HTTP
server.bind(('0.0.0.0', 443))  # HTTPS

# ✅ Works without root
server.bind(('0.0.0.0', 8080))  # Alternative HTTP
server.bind(('0.0.0.0', 8443))  # Alternative HTTPS
```

**Alternative:** Run with elevated privileges (not recommended for learning):
```bash
sudo python server.py
```

**Verify:** Server binds successfully to port ≥ 1024.

---

### 14. struct.error: unpack requires a buffer of N bytes

**When it appears:** Unpacking binary data with wrong size

**Error example:**
```
struct.error: unpack requires a buffer of 4 bytes
```

**Cause:** The data length does not match the format string.

**Fix:**
```python
import struct

# Check format size before unpacking
fmt = '!I'  # Network byte order, unsigned int (4 bytes)
expected_size = struct.calcsize(fmt)  # = 4

data = sock.recv(1024)
if len(data) < expected_size:
    raise ValueError(f"Need {expected_size} bytes, got {len(data)}")

value, = struct.unpack(fmt, data[:expected_size])
```

**Common format sizes:**
| Format | Size | Description |
|--------|------|-------------|
| `!B` | 1 | Unsigned byte |
| `!H` | 2 | Unsigned short (port) |
| `!I` | 4 | Unsigned int (IPv4) |
| `!Q` | 8 | Unsigned long long |

**Verify:** Unpack succeeds with correct data length.

---

### 15. Docker: "Cannot connect to the Docker daemon"

**When it appears:** Running Docker commands in WSL2

**Error example:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Cause:** Docker Desktop is not running or WSL integration is disabled.

**Fix:**
1. Start Docker Desktop on Windows
2. Wait for it to fully start (whale icon stable in system tray)
3. Check WSL integration: Docker Desktop → Settings → Resources → WSL Integration → Enable for your distro

**Verify:**
```bash
docker --version
docker ps
```

---

### 16. WSL2: Operations extremely slow

**When it appears:** File operations or pip install very slow in WSL2

**Cause:** Antivirus scanning WSL filesystem or accessing Windows filesystem from WSL.

**Fix:**
```bash
# 1. Work in Linux filesystem, not /mnt/c/
cd ~  # Use Linux home, not Windows

# 2. Exclude WSL paths from antivirus
# Windows Security → Virus & threat protection → Manage settings
# → Add exclusion → Folder → \\wsl$\Ubuntu\home\

# 3. For pip, use --no-cache-dir
pip install package --no-cache-dir
```

**Verify:** Operations complete in reasonable time.

---

## Getting Help

If your issue is not listed here:

1. **Read the error message carefully** — Python error messages are usually descriptive
2. **Check the line number** — The error points to where Python detected the problem
3. **Search the error message** — Copy the exact error text into a search engine
4. **Ask for help** — Include the full error traceback and relevant code

---

*Troubleshooting Guide — Python for Networking*
*Computer Networks Course — ASE Bucharest, CSIE*
*Version 5.0 — January 2026*
