# ❌ Common Misconceptions — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists the most common misunderstandings and how to correct them.
> **Use it for self-assessment** and to avoid typical pitfalls.

---

## WSL and Virtualisation

### 🚫 Misconception 1: "WSL2 emulates Linux"

**WRONG:** "WSL2 translates Linux commands into Windows commands, like an emulator."

**CORRECT:** WSL2 runs a **real Linux kernel** (not emulated) in a lightweight virtual machine managed by Hyper-V. Unlike WSL1 which translated system calls, WSL2 offers complete compatibility with Linux syscalls.

| Aspect | WSL1 | WSL2 |
|--------|------|------|
| Kernel | Syscall translation | Real Linux kernel |
| Compatibility | ~80% syscalls | 100% syscalls |
| Linux file performance | Slow | Fast |
| Windows file performance | Fast | Slower |
| Native Docker | No | Yes |

**Practical verification:**
```bash
uname -r
# Output: 5.15.x.x-microsoft-standard-WSL2
# Note "-microsoft-standard-WSL2" = real kernel, customised
```

---

### 🚫 Misconception 2: "Docker Desktop is required for Docker on Windows"

**WRONG:** "I must install Docker Desktop to use Docker on Windows."

**CORRECT:** You can install Docker **natively in WSL2** without Docker Desktop. Native WSL2 installation:
- Consumes fewer resources
- Does not require a licence for commercial use
- Offers more granular control

**Practical verification:**
```bash
docker info 2>/dev/null | grep -i "operating system"
# Output: Operating System: Ubuntu 22.04.x LTS
```

---

## Docker: Images and Containers

### 🚫 Misconception 3: "Container and image are the same thing"

**WRONG:** "I downloaded the nginx container" or "I deleted the image so the containers no longer exist."

**CORRECT:**
- **Image** = read-only template (like an ISO or a mould)
- **Container** = runnable instance created from an image (like a VM started from ISO)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           IMAGE                                              │
│  (nginx:latest — read-only, ~140MB)                                         │
│                                                                              │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                    │
│    │  Container 1 │  │  Container 2 │  │  Container 3 │                    │
│    │    web1      │  │    web2      │  │    web3      │                    │
│    │  (running)   │  │  (stopped)   │  │  (running)   │                    │
│    └──────────────┘  └──────────────┘  └──────────────┘                    │
│                                                                              │
│    Each container has its own writable layer                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 🚫 Misconception 4: "Stopping the container deletes data"

**WRONG:** "If I stop the container, I lose everything I saved in it."

**CORRECT:** `docker stop` does **NOT** delete the container or its data. The container remains on disc in "Exited" state. Data is lost only when:
1. You run `docker rm` (deletes the container)
2. You run `docker run --rm` (auto-remove on stop)
3. You did **NOT** use volumes for persistent data

---

## Docker Networking

### 🚫 Misconception 5: "Container port is automatically accessible from outside"

**WRONG:** "Nginx listens on port 80, so I can access `localhost:80` from my browser."

**CORRECT:** Container ports are **isolated by default**. You must map them explicitly with `-p`:

```bash
# ❌ Does NOT work from browser:
docker run -d nginx

# ✅ Works from browser:
docker run -d -p 8080:80 nginx
# Maps: localhost:8080 (host) → container:80
```

---

### 🚫 Misconception 6: "Localhost is the same everywhere"

**WRONG:** "If Portainer runs on `localhost:9000`, I can access `localhost:9000` from any container."

**CORRECT:** Each container has its **own network namespace**. `localhost` in a container refers to the container itself, not the host.

**Solution:** Use `host.docker.internal` to access host services from a container.

---

### 🚫 Misconception 7: "Docker starts automatically after Windows restart"

**WRONG:** "I configured everything, after restart it will work the same."

**CORRECT:** In native WSL2 (without Docker Desktop), the Docker service does **NOT start automatically**. WSL2 does not have systemd enabled by default, so services do not initialise at boot.

**Immediate solution:**
```bash
sudo service docker start
```

---

### 🚫 Misconception 8: "Portainer manages Docker"

**WRONG:** "Portainer controls Docker. If I delete Portainer, containers disappear."

**CORRECT:** Portainer is just a **management interface** (web UI). Docker Engine is what actually runs and manages containers. You can:
- Delete Portainer → containers remain
- Stop Docker → Portainer (and all containers) stop
- Use only CLI → Portainer becomes useless but Docker works

---

## Python: Bytes and Strings

### 🚫 Misconception 9: "encode() and decode() do the same thing"

**WRONG:** "I'll just use encode() or decode() — they're interchangeable."

**CORRECT:** These methods have **opposite directions**:
- `encode()`: str → bytes (preparing text for network transmission)
- `decode()`: bytes → str (interpreting received network data)

```python
# ✅ CORRECT usage
text = "Hello"
wire_data = text.encode('utf-8')      # str → bytes (for sending)
received_text = wire_data.decode('utf-8')  # bytes → str (after receiving)

# ❌ WRONG — this will raise AttributeError
b"Hello".encode()  # bytes object has no encode()
"Hello".decode()   # str object has no decode()
```

**Memory aid:** "ENcode puts data ON the wire, DEcode takes data OFF the wire"

---

### 🚫 Misconception 10: "All bytes can be decoded as UTF-8"

**WRONG:** "I'll just call `.decode('utf-8')` on any bytes I receive."

**CORRECT:** Network data may contain **invalid UTF-8 sequences** (binary protocols, corrupted data, different encodings). Always use error handling:

```python
# ❌ DANGEROUS — may raise UnicodeDecodeError
text = data.decode('utf-8')

# ✅ SAFE — replaces invalid bytes with �
text = data.decode('utf-8', errors='replace')

# ✅ SAFE — ignores invalid bytes
text = data.decode('utf-8', errors='ignore')

# ✅ FOR DEBUGGING — shows hex escapes
text = data.decode('utf-8', errors='backslashreplace')
```

**Practical verification:**
```python
# This will crash without error handling:
binary_data = b'\x80\x81\x82'  # Invalid UTF-8
text = binary_data.decode('utf-8')  # UnicodeDecodeError!

# Safe version:
text = binary_data.decode('utf-8', errors='replace')  # Returns '���'
```

---

## Python: Socket Programming

### 🚫 Misconception 11: "Server and client use the same socket sequence"

**WRONG:** "Both sides do socket → connect → send → recv."

**CORRECT:** Server and client have **different sequences**:

```
SERVER SEQUENCE:              CLIENT SEQUENCE:
┌─────────────────────┐      ┌─────────────────────┐
│ socket()            │      │ socket()            │
│       ↓             │      │       ↓             │
│ setsockopt()        │      │ connect() ←─────────┼─── to server
│       ↓             │      │       ↓             │
│ bind()              │      │ send()/recv()       │
│       ↓             │      │       ↓             │
│ listen()            │      │ close()             │
│       ↓             │      └─────────────────────┘
│ accept() ←──────────┼─── blocks until client connects
│       ↓             │
│ send()/recv()       │
│       ↓             │
│ close()             │
└─────────────────────┘
```

**Key difference:** Server needs `bind()` + `listen()` + `accept()`, client only needs `connect()`.

**Common error:**
```python
# ❌ WRONG — client trying to bind and listen
client_sock.bind(('', 0))      # Not needed for client!
client_sock.listen(5)           # Client doesn't listen!
client_sock.connect((host, port))

# ✅ CORRECT — client just connects
client_sock.connect((host, port))
```

---

### 🚫 Misconception 12: "recv() always returns the complete message"

**WRONG:** "If I send 1000 bytes, recv(1024) will get all 1000 at once."

**CORRECT:** TCP is a **stream protocol** — it doesn't preserve message boundaries. `recv()` may return:
- Less data than sent (partial read)
- Data from multiple sends combined
- Empty bytes (connection closed)

```python
# ❌ WRONG — assumes complete message
data = sock.recv(1024)
process(data)  # May be incomplete!

# ✅ CORRECT — loop until complete message
def recv_exactly(sock, n):
    """Receive exactly n bytes."""
    chunks = []
    received = 0
    while received < n:
        chunk = sock.recv(n - received)
        if not chunk:
            raise ConnectionError("Socket closed prematurely")
        chunks.append(chunk)
        received += len(chunk)
    return b''.join(chunks)
```

**Solution strategies:**
1. **Length-prefix:** Send message length first, then message
2. **Delimiter:** Use special character (e.g., `\n`) to mark end
3. **Fixed-size:** All messages same length (pad if needed)

---

## Quick Summary

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | WSL2 emulates Linux | Real Linux kernel in lightweight VM |
| 2 | Docker Desktop required | Native Docker in WSL2 works |
| 3 | Container = Image | Image = template, Container = instance |
| 4 | Stop deletes data | Stop preserves data, rm deletes |
| 5 | Ports auto-exposed | Must be mapped explicitly with -p |
| 6 | Localhost is global | Each container has its own localhost |
| 7 | Docker auto-starts | Must be configured manually in WSL2 |
| 8 | Portainer = Docker | Portainer is just UI, Docker is the engine |
| 9 | encode() = decode() | Opposite directions: str↔bytes |
| 10 | All bytes are UTF-8 | Use errors='replace' for safety |
| 11 | Same sequence client/server | Server: bind→listen→accept; Client: connect |
| 12 | recv() returns complete msg | TCP is a stream, may return partial data |

---

*Misconceptions Document — Week 0: Lab Environment Setup*
*Computer Networks — ASE Bucharest, CSIE*
*Version: 1.5.0 | January 2026*
