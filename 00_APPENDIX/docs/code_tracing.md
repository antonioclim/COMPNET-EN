# 🔍 Code Tracing Exercises — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Purpose:** Trace code execution step by step without actually running it.
> **Technique:** Complete the tables with variable state after each line.

---

## Why Code Tracing?

Code tracing helps you:
- Aderstand **exactly** what each line of code does
- Detect logic errors before execution
- Build a correct mental model of the programme
- Answer "what will it display?" questions without running the code

**Golden rule:** Be the computer. Don't assume — trace each step.

---

## Exercise T1: TCP Socket — Server Flow

### Code to Trace
```python
import socket

DEFAULT_PORT = 8080
BUFFER_SIZE = 1024

def server(port=DEFAULT_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(5)
        print(f"[SERVER] Listening on port {port}...")

        conn, addr = s.accept()
        print(f"[SERVER] Connection from {addr}")

        with conn:
            data = conn.recv(BUFFER_SIZE)
            if data:
                message = data.decode('utf-8')
                print(f"[SERVER] Received: {message}")
                response = b"OK: " + data.upper()
                conn.sendall(response)
                print(f"[SERVER] Sent: {response}")

server(9000)
```

### Questions

**1. Complete the table with variable state:**

Assume a client sends the message `"test"` from address `('192.168.1.100', 54321)`.

| After line | `port` | `s` (type) | `conn` | `addr` | `data` | `message` | `response` |
|------------|--------|-----------|--------|--------|--------|---------|------------|
| 7 | ? | ? | - | - | - | - | - |
| 10 | ? | ? | - | - | - | - | - |
| 14 | ? | ? | ? | ? | - | - | - |
| 18 | ? | ? | ? | ? | ? | - | - |
| 20 | ? | ? | ? | ? | ? | ? | - |
| 21 | ? | ? | ? | ? | ? | ? | ? |

<details>
<summary>Click for solution</summary>

| After line | `port` | `s` (type) | `conn` | `addr` | `data` | `message` | `response` |
|------------|--------|-----------|--------|--------|--------|---------|------------|
| 7 | 9000 | TCP socket | - | - | - | - | - |
| 10 | 9000 | TCP socket (bound) | - | - | - | - | - |
| 14 | 9000 | TCP socket | TCP socket | ('192.168.1.100', 54321) | - | - | - |
| 18 | 9000 | TCP socket | TCP socket | ('192.168.1.100', 54321) | b'test' | - | - |
| 20 | 9000 | TCP socket | TCP socket | ('192.168.1.100', 54321) | b'test' | 'test' | - |
| 21 | 9000 | TCP socket | TCP socket | ('192.168.1.100', 54321) | b'test' | 'test' | b'OK: TEST' |

</details>

**2. What will the programme display in the console?**

<details>
<summary>Click for solution</summary>

```
[SERVER] Listening on port 9000...
[SERVER] Connection from ('192.168.1.100', 54321)
[SERVER] Received: test
[SERVER] Sent: b'OK: TEST'
```

</details>

**3. What happens if the client sends empty bytes (`b''`)?**

<details>
<summary>Click for solution</summary>

The condition `if data:` is `False` for empty bytes (`b''` is considered falsy in Python), so:
- "Received:" is not displayed
- No response is sent
- Connection closes without processing

</details>

---

## Exercise T2: Bytes vs String — Conversions

### Code to Trace
```python
text = "Hello"
encoded = text.encode('utf-8')
length = len(encoded)
decoded = encoded.decode('utf-8')
is_same = text == decoded

print(f"Original: {text} (type: {type(text).__name__})")
print(f"Encoded: {encoded} (type: {type(encoded).__name__})")
print(f"Bytes length: {length}")
print(f"Decoded: {decoded}")
print(f"Identical: {is_same}")
```

### Questions

**1. Complete the table:**

| Variable | Value | Type |
|----------|-------|------|
| `text` | ? | ? |
| `encoded` | ? | ? |
| `length` | ? | ? |
| `decoded` | ? | ? |
| `is_same` | ? | ? |

<details>
<summary>Click for solution</summary>

| Variable | Value | Type |
|----------|-------|------|
| `text` | 'Hello' | str |
| `encoded` | b'Hello' | bytes |
| `length` | 5 | int |
| `decoded` | 'Hello' | str |
| `is_same` | True | bool |

</details>

**2. If `text = "Ħello"` (with special H), what changes in the table?**

<details>
<summary>Click for solution</summary>

| Variable | Value | Type |
|----------|-------|------|
| `text` | 'Ħello' | str |
| `encoded` | b'\xc4\xa6ello' | bytes |
| `length` | **6** (not 5!) | int |
| `decoded` | 'Ħello' | str |
| `is_same` | True | bool |

**Explanation:** The character "Ħ" takes 2 bytes in UTF-8, not 1. String length in characters is 5, but in bytes it's 6.

</details>

---

## Exercise T3: Struct Parsing — IP Header

### Code to Trace
```python
import struct
import socket

# Simulated IP header (20 bytes)
raw_header = bytes([
    0x45,                    # Version (4) + IHL (5)
    0x00,                    # TOS
    0x00, 0x3c,              # Total Length (60)
    0x1c, 0x46,              # Identification
    0x40, 0x00,              # Flags + Fragment Offset
    0x40,                    # TTL (64)
    0x06,                    # Protocol (TCP = 6)
    0x00, 0x00,              # Checksum (placeholder)
    0xc0, 0xa8, 0x01, 0x64,  # Source IP: 192.168.1.100
    0xc0, 0xa8, 0x01, 0x01   # Dest IP: 192.168.1.1
])

version_ihl = raw_header[0]
version = version_ihl >> 4
ihl = version_ihl & 0x0F
header_length = ihl * 4

ttl = raw_header[8]
protocol = raw_header[9]

src_bytes = raw_header[12:16]
src_ip = socket.inet_ntoa(src_bytes)
```

### Questions

**1. Bit operations — complete:**

| Expression | Calculation | Result |
|------------|-------------|--------|
| `0x45 >> 4` | ? | ? |
| `0x45 & 0x0F` | ? | ? |
| `5 * 4` | ? | ? |

<details>
<summary>Click for solution</summary>

| Expression | Calculation | Result |
|------------|-------------|--------|
| `0x45 >> 4` | 01000101 >> 4 = 00000100 | 4 |
| `0x45 & 0x0F` | 01000101 & 00001111 = 00000101 | 5 |
| `5 * 4` | IHL in units of 4 bytes | 20 |

</details>

**2. What protocol does number 6 represent?**

<details>
<summary>Click for solution</summary>

**TCP** — according to RFC 790, Protocol Numbers:
- 1 = ICMP
- 6 = TCP
- 17 = UDP

</details>

---

## Exercise T4: Context Manager — Resources

### Code to Trace
```python
class ConnectionTracker:
    count = 0

    def __init__(self, name):
        self.name = name
        print(f"[INIT] Created: {name}")

    def __enter__(self):
        ConnectionTracker.count += 1
        print(f"[ENTER] {self.name} — Total: {ConnectionTracker.count}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ConnectionTracker.count -= 1
        print(f"[EXIT] {self.name} — Total: {ConnectionTracker.count}")
        return False

print("Start")
with ConnectionTracker("A") as a:
    print(f"In block A, count = {ConnectionTracker.count}")
    with ConnectionTracker("B") as b:
        print(f"In block B, count = {ConnectionTracker.count}")
    print(f"After B, count = {ConnectionTracker.count}")
print(f"Final, count = {ConnectionTracker.count}")
```

### Questions

**1. In what order are methods called?**

<details>
<summary>Click for solution</summary>

```
Start
[INIT] Created: A
[ENTER] A — Total: 1
In block A, count = 1
[INIT] Created: B
[ENTER] B — Total: 2
In block B, count = 2
[EXIT] B — Total: 1
After B, count = 1
[EXIT] A — Total: 0
Final, count = 0
```

</details>

**2. Why is this pattern important for sockets?**

<details>
<summary>Click for solution</summary>

The context manager guarantees that `__exit__` is called **always**, even if an exception occurs in the block. For sockets, this means:
- The socket is closed correctly
- The port is released for reuse
- No resource leaks occur

Without `with`, if an exception occurs between `socket()` and `close()`, the socket remains open.

</details>

---

## Summary of Tracing Techniques

| Technique | When to Use |
|-----------|-------------|
| Variable table | Track state at each step |
| Flow diagram | Visualise branches (if/else) |
| Call stack | Track function calls |
| Timeline | Aderstand async operation order |

**Final tip:** When you encounter a bug, **manually trace** the code before adding print statements. You'll often find the error without running anything.

---

*Code Tracing Exercises — Week 0*
*Computer Networks — ASE Bucharest, CSIE*
*Version: January 2025*
