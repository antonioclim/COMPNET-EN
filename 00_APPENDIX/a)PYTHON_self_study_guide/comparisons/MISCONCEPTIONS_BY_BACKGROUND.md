# 🚧 Common Misconceptions by Programming Background
## Python Pitfalls for Students from C/C++, JavaScript, Java and Kotlin

> **Purpose:** Anticipate and prevent errors based on your prior language experience
> **Version:** 4.1 — January 2026

---

## For C/C++ Programmers

### ❌ Variables Need Type Declarations
```c
// C: int port = 8080;
```
```python
# Python: Just assign!
port = 8080

# Optional type hints (not enforced):
port: int = 8080
```

### ❌ Strings Are Byte Arrays
```c
// C: send(sock, "Hello", 5, 0);  // Works
```
```python
# Python: TypeError if you send str!
sock.send("Hello")      # ❌ TypeError
sock.send(b"Hello")     # ✅ Correct
sock.send("Hello".encode('utf-8'))  # ✅ Also correct
```

### ❌ Manual Memory Management
```c
// C: char* buf = malloc(1024); ... free(buf);
```
```python
# Python: No malloc/free needed
buf = bytearray(1024)  # Garbage collected automatically
```

### ❌ Need htons/htonl for Byte Order
```c
// C: addr.sin_port = htons(8080);
```
```python
# Python socket API handles it:
server.bind(('0.0.0.0', 8080))  # Just use integer

# Only for binary protocols:
import struct
packed = struct.pack('!H', 8080)  # '!' = network order
```

---

## For JavaScript Programmers

### ❌ === vs ==
```javascript
// JS: if (x === 5) { }  // Strict equality
```
```python
# Python: == is already strict (no coercion)
if x == 5:  # Works like ===

# For identity (same object):
if x is None:  # Use 'is', not ==
```

### ❌ const and let
```javascript
// JS: const PORT = 8080;
```
```python
# Python: No const/let keywords
PORT = 8080  # Convention: CAPS for constants
counter = 0  # All variables are reassignable
```

### ❌ Callbacks and Promises
```javascript
// JS: socket.on('data', (data) => {...});
```
```python
# Python sockets are BLOCKING by default
data = socket.recv(1024)  # Waits until data arrives
# No callbacks, no promises, no async (by default)
```

### ❌ Object Literal Dot Notation
```javascript
// JS: const cfg = { port: 8080 }; cfg.port
```
```python
# Python dicts use brackets:
cfg = {"port": 8080}
cfg["port"]  # NOT cfg.port

# For dot notation, use dataclass:
from dataclasses import dataclass
@dataclass
class Config:
    port: int
```

---

## For Java Programmers

### ❌ Class Wrapper Required
```java
// Java: public class Main { public static void main... }
```
```python
# Python: No class needed!
print("Hello")  # Just write code

# Entry point guard:
if __name__ == "__main__":
    main()
```

### ❌ Explicit Access Modifiers
```java
// Java: private int port;
```
```python
# Python: Convention _ prefix
class Server:
    def __init__(self):
        self._port = 8080    # "Private" by convention
        self.host = "0.0.0.0"  # Public
```

### ❌ try-with-resources Syntax
```java
// Java: try (Socket s = new Socket()) { }
```
```python
# Python: 'with' statement (separate from try)
with socket.socket() as s:
    s.connect((host, port))
# Closes automatically!
```

---

## For Kotlin Programmers

### ❌ val/var Declarations
```kotlin
// Kotlin: val port = 8080
```
```python
# Python: Just assign (all reassignable)
port = 8080  # No val/var
```

### ❌ Null Safety (?. and ?:)
```kotlin
// Kotlin: val length = response?.length ?: 0
```
```python
# Python: Explicit checks
length = len(response) if response else 0
```

### ❌ .use {} for Resources
```kotlin
// Kotlin: Socket(host, port).use { ... }
```
```python
# Python: 'with' statement
with socket.socket() as s:
    s.connect((host, port))
```

---

## Universal Networking Misconceptions

### ❌ recv() Returns Complete Message
```python
# TCP is a STREAM - may receive partial data!
data = sock.recv(1024)  # Might get less than sent

# ✅ Loop until complete:
def recv_all(sock, length):
    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError()
        data += chunk
    return data
```

### ❌ Ports <1024 Work Without Privileges
```python
server.bind(('0.0.0.0', 80))  # ❌ Permission denied!
server.bind(('0.0.0.0', 8080))  # ✅ Use 1024+
```

### ❌ localhost == 0.0.0.0
```python
# localhost (127.0.0.1) = local connections only
# 0.0.0.0 = ALL interfaces (remote too)
server.bind(('localhost', 8080))  # Local only
server.bind(('0.0.0.0', 8080))    # All interfaces
```

---

## Quick Diagnostic

| Error | Likely Cause |
|-------|--------------|
| `TypeError: a bytes-like object required` | Forgot `.encode()` |
| `SyntaxError` on `{` | Using braces instead of `:` |
| `NameError: 'const' not defined` | Using JS/Kotlin keywords |
| `AttributeError: no attribute` | Using dot notation on dict |
| `IndentationError` | Mixed tabs/spaces |

---

*Common Misconceptions — Computer Networks Course*
*ASE Bucharest, CSIE — Version 4.1 | January 2026*
