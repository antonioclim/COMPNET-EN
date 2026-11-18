# 🗿 Rosetta Stone: Python for Network Programming
## Side-by-Side Comparison with C, JavaScript, Java and Kotlin

> **Purpose:** If you know one of these languages, you already know Python's networking logic.
> **Format:** Echo each received byte until EOF. C, Java, Kotlin and Python below serve clients sequentially; the Node event loop can serve several clients. These are core fragments: supply imports, a main function where required and error handling appropriate to the full application.
> **Version:** 4.1 — January 2026

---

## Core Syntax Mapping

### Variables and Types

| Concept | C | JavaScript | Java | Kotlin | Python |
|---------|---|------------|------|--------|--------|
| Integer | `int x = 5;` | `let x = 5;` | `int x = 5;` | `val x = 5` | `x = 5` |
| String | `char* s = "hi";` | `let s = "hi";` | `String s = "hi";` | `val s = "hi"` | `s = "hi"` |
| Array/List | `int arr[] = {1,2};` | `let arr = [1,2];` | `int[] arr = {1,2};` | `val arr = listOf(1,2)` | `arr = [1, 2]` |
| Dictionary | `// use struct` | `{key: val}` | `HashMap<>` | `mapOf(k to v)` | `{key: val}` |
| Null check | `if (ptr != NULL)` | `if (x !== null)` | `if (x != null)` | `x?.let {}` | `if x is not None:` |

### Control Flow

| Concept | C | JavaScript | Java | Kotlin | Python |
|---------|---|------------|------|--------|--------|
| If | `if (x > 0) {...}` | `if (x > 0) {...}` | `if (x > 0) {...}` | `if (x > 0) {...}` | `if x > 0:` |
| For (range) | `for(int i=0;i<n;i++)` | `for(let i=0;i<n;i++)` | `for(int i=0;i<n;i++)` | `for(i in 0 until n)` | `for i in range(n):` |
| For (each) | `// manual` | `for(let x of arr)` | `for(int x : arr)` | `for(x in arr)` | `for x in arr:` |

---

## 1. TCP Echo Server

### C (POSIX Sockets)
```c
int server_fd = socket(AF_INET, SOCK_STREAM, 0);
setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
struct sockaddr_in addr = {0};
addr.sin_family = AF_INET;
addr.sin_port = htons(8080);
addr.sin_addr.s_addr = htonl(INADDR_ANY);
bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
listen(server_fd, 5);

while (1) {
    int client_fd = accept(server_fd, NULL, NULL);
    char buffer[1024];
    if (client_fd < 0) continue;
    ssize_t n;
    while ((n = recv(client_fd, buffer, sizeof buffer, 0)) > 0) {
        ssize_t sent = 0;
        while (sent < n) {
            ssize_t part = send(client_fd, buffer + sent, (size_t)(n - sent), 0);
            if (part <= 0) goto close_client;
            sent += part;
        }
    }
close_client:
    close(client_fd);
}
```

### JavaScript (Node.js)
```javascript
const net = require('net');
const server = net.createServer((socket) => {
    socket.on('error', (error) => { console.error(error.message); socket.destroy(); });
    socket.on('data', (data) => {
        socket.write(data);  // Echo back
    });
});
server.listen(8080, '0.0.0.0');
```

### Java
```java
try (ServerSocket serverSocket = new ServerSocket(8080)) {
    while (true) {
        try (Socket client = serverSocket.accept()) {
            byte[] buffer = new byte[1024];
            int n;
            while ((n = client.getInputStream().read(buffer)) != -1) {
                client.getOutputStream().write(buffer, 0, n);
            }
        }
    }
}
```

### Kotlin
```kotlin
ServerSocket(8080).use { server ->
    while (true) {
        server.accept().use { client ->
            val buffer = ByteArray(1024)
            while (true) {
                val n = client.getInputStream().read(buffer)
                if (n == -1) break
                client.getOutputStream().write(buffer, 0, n)
            }
        }
    }
}
```

### Python ✨
```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)

    while True:
        client, addr = server.accept()
        with client:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                client.sendall(data)  # Echo this chunk; TCP has no message boundary
```

### Key Observations

| Aspect | C | JS | Java | Kotlin | Python |
|--------|---|----|----|--------|--------|
| Execution model | Blocking | Event-driven | Blocking | Blocking | Blocking |
| Manual memory | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| Resource cleanup | Manual close() | Callbacks | try-with-resources | .use {} | `with` statement |
| Port in socket API | `htons()` in sockaddr | Host-order integer | Host-order integer | Host-order integer | Host-order integer |

---

## 2. Binary Protocol Parsing (struct)

**Scenario:** Parse a header: 2-byte port + 4-byte IP address

### C
```c
struct header { uint16_t port; uint32_t ip; } __attribute__((packed));
struct header* h = (struct header*)data;
uint16_t port = ntohs(h->port);
```

### JavaScript
```javascript
const view = new DataView(buffer);
const port = view.getUint16(0, false);  // false = big-endian
const ip = view.getUint32(2, false);
```

### Java
```java
ByteBuffer buf = ByteBuffer.wrap(data).order(ByteOrder.BIG_ENDIAN);
int port = Short.toUnsignedInt(buf.getShort());
long ip = Integer.toUnsignedLong(buf.getInt());
```

### Python ✨
```python
import struct

# '!' = network byte order, 'H' = unsigned short, 'I' = unsigned int
port, ip = struct.unpack('!HI', data)
```

### struct Format Codes (Python)

| Code | C Type | Size | Description |
|------|--------|------|-------------|
| `!` | - | - | Network byte order |
| `B` | unsigned char | 1 | 0-255 |
| `H` | unsigned short | 2 | 0-65535 |
| `I` | unsigned int | 4 | 0-4294967295 |
| `s` | char[] | n | Byte string |

---

## 3. Error Handling

### C
```c
if (connect(sock, &addr, sizeof(addr)) < 0) {
    perror("connect failed");
    exit(1);
}
```

### JavaScript
```javascript
const net = require('net');
function connectTo(host, port) {
    return new Promise((resolve, reject) => {
        const socket = net.createConnection({host, port});
        socket.once('error', reject);
        socket.once('connect', () => resolve(socket));
    });
}
(async () => {
    try {
        const socket = await connectTo('127.0.0.1', 8080);
        // Perform the application exchange here; connect() itself is not a Promise.
        socket.end();
    } catch (error) {
        console.error('Connection failed:', error.message);
    }
})();
```

### Java
```java
try {
    Socket socket = new Socket(host, port);
} catch (IOException e) {
    System.err.println("Connection failed: " + e.getMessage());
}
```

### Python ✨
```python
try:
    with socket.socket() as s:
        s.connect((host, port))
except ConnectionRefusedError:
    print("Connection refused - is the server running?")
except socket.timeout:
    print("Connection timed out")
```

---

## Quick Reference: Resource Cleanup

| Language | Pattern |
|----------|---------|
| C | Manual `close()` in all paths |
| JavaScript | Callbacks or `finally` |
| Java | try-with-resources |
| Kotlin | `.use {}` extension |
| **Python** | `with` statement |

---

## Quick Reference: Bytes vs Strings

| Language | String to Bytes | Bytes to String |
|----------|-----------------|-----------------|
| C | Already bytes | N/A |
| JavaScript | `Buffer.from(str)` | `buffer.toString()` |
| Java | `str.getBytes()` | `new String(bytes)` |
| Kotlin | `str.toByteArray()` | `String(bytes)` |
| **Python** | `str.encode('utf-8')` | `bytes.decode('utf-8')` |

---

*Rosetta Stone for Python Networking — Computer Networks Course*
*ASE Bucharest, CSIE — Version 4.1, January 2026*
