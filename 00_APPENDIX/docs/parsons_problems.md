# 🧩 Parsons Problems — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Parsons Problems** are code-ordering exercises where you arrange shuffled lines into the correct sequence.
> These build procedural knowledge without the cognitive load of syntax recall.

---

## Instructions

1. Read the problem description carefully
2. Identify the **correct lines** (some may be distractors)
3. Arrange them in the proper order
4. Check your answer against the solution

**Tip:** Think about what each line does before ordering. Consider dependencies between lines.

---

## Problem 1: TCP Server Setup (LO0.5)

**Objective:** Arrange the lines to create a TCP server that listens on port 8080.

**Shuffled Lines:**
```python
A: server_sock.listen(5)
B: server_sock.bind(('0.0.0.0', 8080))
C: import socket
D: server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
E: server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
F: conn, addr = server_sock.accept()
G: server_sock.connect(('0.0.0.0', 8080))  # DISTRACTOR
H: socket.listen(5)  # DISTRACTOR
```

<details>
<summary>💡 Hint</summary>
The server sequence is: import → create socket → set options → bind → listen → accept.
Servers do NOT call connect() — that's for clients!
</details>

<details>
<summary>✅ Solution</summary>

**Correct order:** C → D → E → B → A → F

```python
import socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(('0.0.0.0', 8080))
server_sock.listen(5)
conn, addr = server_sock.accept()
```

**Distractors:**
- G: `connect()` is for clients, not servers
- H: `socket.listen()` is wrong syntax — should be `server_sock.listen()`

**Why this order:**
1. Import the module first
2. Create the socket object
3. Set socket options before binding
4. Bind to address/port
5. Start listening for connections
6. Accept incoming connections
</details>

---

## Problem 2: Bytes Encoding and Sending (LO0.4, LO0.5)

**Objective:** Arrange the lines to send an encoded message over a socket.

**Shuffled Lines:**
```python
A: sock.send(encoded_msg)
B: message = "Hello, Server!"
C: encoded_msg = message.encode('utf-8')
D: sock.connect(('localhost', 8080))
E: import socket
F: sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
G: encoded_msg = message.decode('utf-8')  # DISTRACTOR
H: sock.send(message)  # DISTRACTOR
```

<details>
<summary>💡 Hint</summary>
You must encode a string to bytes BEFORE sending.
Remember: encode() converts str → bytes, decode() converts bytes → str.
</details>

<details>
<summary>✅ Solution</summary>

**Correct order:** E → F → D → B → C → A

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))
message = "Hello, Server!"
encoded_msg = message.encode('utf-8')
sock.send(encoded_msg)
```

**Distractors:**
- G: `decode()` converts bytes→str, not str→bytes
- H: Cannot send a string directly — must be bytes

**Why this order:**
1. Import socket module
2. Create socket
3. Connect to server (client-side)
4. Prepare the message string
5. Encode string to bytes
6. Send the bytes
</details>

---

## Problem 3: Receiving and Decoding Data (LO0.4, LO0.5)

**Objective:** Arrange the lines to safely receive and decode data from a socket.

**Shuffled Lines:**
```python
A: print(f"Received: {text}")
B: data = conn.recv(1024)
C: text = data.decode('utf-8', errors='replace')
D: if not data:
E:     break
F: text = data.encode('utf-8')  # DISTRACTOR
G: data = conn.send(1024)  # DISTRACTOR
H: text = data.decode('utf-8')  # DISTRACTOR (unsafe)
```

<details>
<summary>💡 Hint</summary>
Always use errors='replace' when decoding to handle invalid UTF-8 gracefully.
recv() receives data, send() sends data.
</details>

<details>
<summary>✅ Solution</summary>

**Correct order:** B → D → E → C → A

```python
data = conn.recv(1024)
if not data:
    break
text = data.decode('utf-8', errors='replace')
print(f"Received: {text}")
```

**Distractors:**
- F: `encode()` is wrong direction — we need decode() for received bytes
- G: `send()` doesn't receive data, `recv()` does
- H: Missing `errors='replace'` — could crash on invalid UTF-8

**Why this order:**
1. Receive raw bytes from socket
2. Check if data is empty (connection closed)
3. Break if no data
4. Safely decode bytes to string
5. Use the decoded text
</details>

---

## Problem 4: Complete Echo Server Handler (LO0.5)

**Objective:** Arrange the lines to handle a client connection in an echo server.

**Shuffled Lines:**
```python
A: response = data.upper()
B: conn.sendall(response)
C: data = conn.recv(1024)
D: with conn:
E: conn, addr = server_sock.accept()
F: print(f"Connected by {addr}")
G: response = data.upper().decode()  # DISTRACTOR
H: conn.send(response.encode())  # DISTRACTOR (partially wrong)
```

<details>
<summary>💡 Hint</summary>
recv() returns bytes. The upper() method works on both str and bytes.
sendall() is preferred over send() for complete transmission.
</details>

<details>
<summary>✅ Solution</summary>

**Correct order:** E → F → D → C → A → B

```python
conn, addr = server_sock.accept()
print(f"Connected by {addr}")
with conn:
    data = conn.recv(1024)
    response = data.upper()
    conn.sendall(response)
```

**Distractors:**
- G: `data` is already bytes, `upper()` returns bytes, no need for `decode()`
- H: If response is bytes, don't encode again; also `sendall()` is preferred

**Why this order:**
1. Accept incoming connection
2. Log the connection
3. Use context manager for automatic cleanup
4. Receive data from client
5. Process data (uppercase)
6. Send response back
</details>

---

## Problem 5: Struct Packing for Network Protocol (LO0.5)

**Objective:** Arrange the lines to pack a simple protocol header with version, type and length.

**Shuffled Lines:**
```python
A: header = struct.pack('!BBH', version, msg_type, length)
B: import struct
C: length = len(payload)
D: version = 1
E: msg_type = 0x02
F: sock.sendall(header + payload)
G: payload = b"Hello"
H: header = struct.pack('BBH', version, msg_type, length)  # DISTRACTOR
I: header = struct.pack('!HHH', version, msg_type, length)  # DISTRACTOR
```

<details>
<summary>💡 Hint</summary>
The '!' prefix means network byte order (big-endian).
'B' = unsigned byte (1 byte), 'H' = unsigned short (2 bytes).
Always calculate length AFTER defining the payload.
</details>

<details>
<summary>✅ Solution</summary>

**Correct order:** B → G → D → E → C → A → F

```python
import struct
payload = b"Hello"
version = 1
msg_type = 0x02
length = len(payload)
header = struct.pack('!BBH', version, msg_type, length)
sock.sendall(header + payload)
```

**Distractors:**
- H: Missing '!' for network byte order — will use native byte order
- I: Wrong format — '!HHH' uses 2 bytes each for version and type (should be 1 byte each)

**Why this order:**
1. Import struct module
2. Define the payload first (needed for length)
3. Define protocol constants
4. Calculate payload length
5. Pack header with correct format
6. Send header + payload together
</details>

---

## Difficulty Progression

| Problem | LO | Difficulty | Key Concept |
|---------|-----|------------|-------------|
| P1 | LO0.5 | Basic | Server socket sequence |
| P2 | LO0.4, LO0.5 | Basic | String encoding for network |
| P3 | LO0.4, LO0.5 | Intermediate | Safe decoding with error handling |
| P4 | LO0.5 | Intermediate | Complete connection handler |
| P5 | LO0.5 | Advanced | Binary protocol with struct |

---

## Common Mistakes to Avoid

1. **Calling connect() on a server socket** — Servers bind and listen, clients connect
2. **Forgetting to encode strings before sending** — Sockets only accept bytes
3. **Using decode() without error handling** — Network data may contain invalid UTF-8
4. **Missing network byte order in struct** — Always use '!' prefix for protocols
5. **Using send() instead of sendall()** — send() may not send all data

---

## JSON Export for LMS

This file is also available as `formative/parsons_problems.json` for LMS import (Moodle/Canvas).

---

*Parsons Problems — Week 0 | Computer Networks | ASE-CSIE*
*Version: 1.5.0 | Date: 2026-01-24*
