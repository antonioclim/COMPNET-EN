# 🗿 Rosetta Stone: Python for Network Programming
## Side-by-Side Comparison with C, JavaScript, Java and Kotlin

> **Purpose:** If you know one of these languages, you already know Python's networking logic.
> **Format:** Same algorithm, five implementations.
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
struct sockaddr_in addr = {AF_INET, htons(8080), INADDR_ANY};
bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
listen(server_fd, 5);

while (1) {
    int client_fd = accept(server_fd, NULL, NULL);
    char buffer[1024];
    int n = recv(client_fd, buffer, 1024, 0);
    send(client_fd, buffer, n, 0);  // Echo back
    close(client_fd);
}
```

### JavaScript (Node.js)
```javascript
const net = require('net');
const server = net.createServer((socket) => {
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
            int n = client.getInputStream().read(buffer);
            client.getOutputStream().write(buffer, 0, n);  // Echo
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
            val n = client.getInputStream().read(buffer)
            client.getOutputStream().write(buffer, 0, n)  // Echo
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
            data = client.recv(1024)
            client.sendall(data)  # Echo back
```

### Key Observations

| Aspect | C | JS | Java | Kotlin | Python |
|--------|---|----|----|--------|--------|
| Lines of code | ~15 | ~8 | ~12 | ~10 | ~10 |
| Manual memory | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| Resource cleanup | Manual close() | Callbacks | try-with-resources | .use {} | `with` statement |
| Byte order | `htons()` | Automatic | Automatic | Automatic | Automatic |

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
short port = buf.getShort();
int ip = buf.getInt();
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
try {
    await socket.connect(host, port);
} catch (error) {
    console.error('Connection failed:', error.message);
}
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
