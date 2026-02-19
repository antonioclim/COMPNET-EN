# Project 08: Web Server and Reverse Proxy

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P08
> 
> **Related:** [P12 (Microservices Load Balancing)](P12_Docker_Microservices_Load_Balancing.md)

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Project assessment takes place EXCLUSIVELY at the faculty, with mandatory physical attendance.**

**Common guides (read before starting):**
- [Pair Programming Guide](../docs/common/pair_programming_guide.md)
- [Code Quality Standards](../docs/common/code_quality_standards.md)
- [Git Workflow](../docs/common/git_workflow_detailed.md)
- [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

---

### 🐙 GitHub Publication

**Repository:** `https://github.com/[username]/retele-proiect-08`

#### Required Repository Structure

```
retele-proiect-08/
├── README.md
├── docs/
│   ├── specificatii.md
│   ├── diagrame/
│   ├── raport_progres.md
│   └── documentatie_finala.md
├── src/
│   ├── main.py
│   ├── server/
│   │   ├── __init__.py
│   │   ├── http_server.py
│   │   └── request_handler.py
│   ├── proxy/
│   │   ├── __init__.py
│   │   └── reverse_proxy.py
│   └── utils/
├── static/
│   └── index.html
├── tests/
│   ├── test_smoke.py
│   ├── test_server.py
│   └── test_proxy.py
├── docker/
│   └── docker-compose.yml
├── Makefile
├── requirements.txt
├── MANIFEST.txt
└── CHANGELOG.md
```

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | HTTP methods, routing, proxy rules |
| Architecture diagrams | 20 | Request flow, components |
| Implementation plan | 15 | Realistic timeline |
| Repository initialised | 15 | GitHub configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic HTTP server works | 35 | GET requests, static files |
| Code quality | 25 | Clean, typed, documented |
| Configuration working | 15 | Port, routes configurable |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete functionality | 40 | Server + proxy + headers |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Unit and integration |
| Documentation | 10 | Complete docs |
| Performance analysis | 5 | Requests/second metrics |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: HTTPS support** | +10 | TLS/SSL (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Server responds, proxy forwards |
| Technical presentation | 25 | Explains HTTP, proxy architecture |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | All members know code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | HTTP server + basic reverse proxy |
| **2 persons** | + Request logging + header manipulation |
| **3 persons** | + HTTPS + caching + load balancing |

---

## 📚 Project Description

Build a custom HTTP web server and reverse proxy from scratch using Python sockets. The web server will handle HTTP requests, serve static files and support basic routing. The reverse proxy will forward requests to backend servers, demonstrating how modern web infrastructure works.

This project provides deep understanding of HTTP protocol mechanics — essential knowledge for web development and DevOps roles. You'll see exactly what happens "under the hood" when a browser makes a request.

### 🎯 Learning Objectives

- **LO1:** Implement HTTP request parsing and response generation
- **LO2:** Create a multi-threaded server handling concurrent connections
- **LO3:** Build a reverse proxy that forwards and modifies requests
- **LO4:** Configure routing rules for different URL paths
- **LO5:** Analyse HTTP headers and their role in web communication
- **LO6:** Measure server performance under load

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Python sockets** | Low-level networking | [docs.python.org](https://docs.python.org/3/library/socket.html) |
| **threading** | Concurrent connections | [docs.python.org](https://docs.python.org/3/library/threading.html) |
| **HTTP/1.1** | Web protocol | [RFC 7230](https://tools.ietf.org/html/rfc7230) |
| **curl** | HTTP client testing | [curl.se](https://curl.se) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **HTTP Request** | Method + Path + Headers + Body |
| **HTTP Response** | Status + Headers + Body |
| **Reverse Proxy** | Server that forwards requests to backends |
| **Content-Type** | Header specifying response format |
| **Host Header** | Identifies target server (virtual hosting) |
| **Keep-Alive** | Persistent connections |
| **Status Codes** | 200 OK, 404 Not Found, 502 Bad Gateway |
| **Request Routing** | Mapping URLs to handlers |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST parse HTTP/1.1 requests correctly
- [ ] MUST return proper status codes (200, 404, 500, 502)
- [ ] MUST handle concurrent connections (threading)
- [ ] MUST serve static files (HTML, CSS, JS, images)
- [ ] MUST log all requests with timestamp
- [ ] MUST pass all smoke tests

### MUST NOT (Forbidden)
- [ ] MUST NOT use http.server module (implement from scratch)
- [ ] MUST NOT use Flask/Django (raw sockets only)
- [ ] MUST NOT crash on malformed requests
- [ ] MUST NOT leave connections open indefinitely

### SHOULD (Recommended)
- [ ] SHOULD support chunked transfer encoding
- [ ] SHOULD implement connection keep-alive
- [ ] SHOULD add custom headers (X-Proxy-By)

---

## 🎯 Concept Analogies

### Reverse Proxy = Hotel Receptionist

🏠 **Real-World Analogy:**  
A hotel receptionist receives all guest requests. "I need room service" → routes to kitchen. "I need housekeeping" → routes to cleaning staff. Guests don't contact departments directly; the receptionist manages routing and can also add services (wake-up calls, messages).

🖼️ **Visual Representation:**
```
Guest                RECEPTIONIST           Departments
  │                      │                      │
  ├─── "Room service" ───►│                     │
  │                      ├────► Kitchen ────────┤
  │◄─── "Coming up!" ────┤◄────────────────────┤
  │                      │                      │
  ├─── "Housekeeping" ───►│                     │
  │                      ├────► Cleaning ───────┤
  │◄─── "On the way!" ───┤◄────────────────────┤
```

💻 **Technical Mapping:**
- Guest = Client (browser)
- Receptionist = Reverse Proxy
- Departments = Backend servers
- Request routing = URL path matching
- Added services = Header manipulation, caching

⚠️ **Where the analogy breaks:**  
A receptionist handles one guest at a time. A proxy handles thousands of concurrent requests. Also, proxies can do load balancing — sending requests to different "staff members" based on availability.

---

### HTTP Request/Response = Restaurant Order

🏠 **Real-World Analogy:**  
At a restaurant: you give an order (request) specifying what you want (method: GET food), from which menu (path: /appetizers/soup), with preferences (headers: no onions). The kitchen processes it and returns your meal (response) with a receipt (status: 200 served or 404 not available).

💻 **Technical Mapping:**
- Order = HTTP Request
- Menu section = URL path
- Preferences = Headers
- Kitchen = Server
- Meal = Response body
- Receipt status = Status code

---

## 🗳️ Peer Instruction Questions

### Question 1: HTTP Method Semantics

> 💭 **PREDICTION:** What HTTP method should modify existing data?

**Options:**
- A) GET (retrieves data)
- B) POST (creates new data)
- C) PUT (replaces data) ✓
- D) DELETE (removes data)

**Correct answer:** C

**Explanation:** PUT is idempotent — calling it multiple times has the same effect. It replaces the resource entirely. POST creates new resources (not idempotent), GET only reads, DELETE removes.

---

### Question 2: Reverse Proxy vs Forward Proxy

> 💭 **PREDICTION:** Who configures a reverse proxy?

**Options:**
- A) The client user
- B) The server administrator ✓
- C) The ISP
- D) The browser

**Correct answer:** B

**Explanation:** Reverse proxies sit in front of servers and are configured by server admins to handle incoming requests. Forward proxies are configured by clients to handle outgoing requests.

---

### Question 3: Status Code Meaning

> 💭 **PREDICTION:** What does 502 Bad Gateway mean?

**Scenario:** Proxy receives request, forwards to backend, backend doesn't respond.

**Options:**
- A) Client sent bad request
- B) Resource not found
- C) Proxy couldn't reach backend ✓
- D) Server overloaded

**Correct answer:** C

**Explanation:** 502 means the proxy (gateway) received an invalid response from the upstream server or couldn't connect at all. The problem is between proxy and backend, not client and proxy.

---

### Question 4: Host Header Purpose

> 💭 **PREDICTION:** Why is the Host header required in HTTP/1.1?

**Options:**
- A) For authentication
- B) For virtual hosting (multiple sites on one IP) ✓
- C) For caching
- D) For encryption

**Correct answer:** B

**Explanation:** One IP address can host multiple websites. The Host header tells the server which site the client wants. Without it, the server wouldn't know which site to serve.

---

## ❌ Common Misconceptions

### 🚫 "HTTP is complicated"

**WRONG:** Students think HTTP requires complex libraries.

**CORRECT:** HTTP/1.1 is text-based and simple. A basic request is just:
```
GET /index.html HTTP/1.1\r\n
Host: example.com\r\n
\r\n
```
You can implement a basic server in <100 lines of Python.

---

### 🚫 "Reverse proxy adds latency"

**WRONG:** Another hop means slower responses.

**CORRECT:** Proxies often IMPROVE performance through caching, connection pooling and compression. The small routing overhead is offset by these optimisations.

---

### 🚫 "Content-Length is optional"

**WRONG:** You can skip Content-Length in responses.

**CORRECT:** Without Content-Length or chunked encoding, clients don't know when the response ends. This causes hanging connections or truncated data.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **HTTP** | HyperText Transfer Protocol |
| **Reverse Proxy** | Server forwarding requests to backend servers |
| **Forward Proxy** | Client-side proxy for outgoing requests |
| **Status Code** | 3-digit number indicating response result |
| **Header** | Key-value metadata in HTTP messages |
| **Keep-Alive** | Reusing TCP connections for multiple requests |
| **Virtual Hosting** | Multiple websites on one IP address |
| **MIME Type** | Content-Type value (text/html, image/png) |
| **Request Method** | GET, POST, PUT, DELETE, etc. |
| **URI** | Uniform Resource Identifier (the path) |

---

## 🔨 Implementation Stages

### Stage 2 (Week 9) — Prototype

**Code Example — Basic HTTP Server:**

```python
#!/usr/bin/env python3
"""
Simple HTTP Server using raw sockets.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import threading
from pathlib import Path
from typing import Tuple, Dict, Optional
import logging

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
BUFFER_SIZE = 4096
HTTP_VERSION = "HTTP/1.1"
CRLF = "\r\n"

MIME_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".json": "application/json",
}

# ═══════════════════════════════════════════════════════════════════════════════
# HTTP_SERVER
# ═══════════════════════════════════════════════════════════════════════════════
class HTTPServer:
    """
    Simple HTTP/1.1 server.
    
    # 💭 PREDICTION: Why use threading for connections?
    # Answer: Handle multiple clients concurrently
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080, 
                 static_dir: str = "static"):
        self.host = host
        self.port = port
        self.static_dir = Path(static_dir)
        self.logger = logging.getLogger(__name__)
    
    def start(self) -> None:
        """Start the server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen(5)
            
            self.logger.info(f"Server running on http://{self.host}:{self.port}")
            
            while True:
                client, addr = server.accept()
                thread = threading.Thread(target=self._handle_client, args=(client, addr))
                thread.daemon = True
                thread.start()
    
    def _handle_client(self, client: socket.socket, addr: Tuple[str, int]) -> None:
        """Handle a single client connection."""
        try:
            request = client.recv(BUFFER_SIZE).decode('utf-8')
            if not request:
                return
            
            method, path, headers = self._parse_request(request)
            self.logger.info(f"{addr[0]} - {method} {path}")
            
            response = self._generate_response(method, path)
            client.sendall(response)
            
        except Exception as e:
            self.logger.error(f"Error handling {addr}: {e}")
            client.sendall(self._error_response(500, "Internal Server Error"))
        finally:
            client.close()
    
    def _parse_request(self, request: str) -> Tuple[str, str, Dict[str, str]]:
        """Parse HTTP request into components."""
        lines = request.split(CRLF)
        method, path, _ = lines[0].split(" ")
        
        headers = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key.lower()] = value
        
        return method, path, headers
    
    def _generate_response(self, method: str, path: str) -> bytes:
        """Generate HTTP response."""
        if method != "GET":
            return self._error_response(405, "Method Not Allowed")
        
        # Serve static file
        file_path = self.static_dir / path.lstrip("/")
        if file_path.is_dir():
            file_path = file_path / "index.html"
        
        if not file_path.exists():
            return self._error_response(404, "Not Found")
        
        content = file_path.read_bytes()
        mime_type = MIME_TYPES.get(file_path.suffix, "application/octet-stream")
        
        response = f"{HTTP_VERSION} 200 OK{CRLF}"
        response += f"Content-Type: {mime_type}{CRLF}"
        response += f"Content-Length: {len(content)}{CRLF}"
        response += f"Connection: close{CRLF}"
        response += CRLF
        
        return response.encode() + content
    
    def _error_response(self, code: int, message: str) -> bytes:
        """Generate error response."""
        body = f"<html><body><h1>{code} {message}</h1></body></html>"
        response = f"{HTTP_VERSION} {code} {message}{CRLF}"
        response += f"Content-Type: text/html{CRLF}"
        response += f"Content-Length: {len(body)}{CRLF}"
        response += CRLF
        response += body
        return response.encode()
```

---

## 📋 Expected Outputs

### Scenario 1: Serve Static File

**Input:**
```bash
curl -v http://localhost:8080/index.html
```

**Expected output:**
```
< HTTP/1.1 200 OK
< Content-Type: text/html
< Content-Length: 156
<
<html>...
```

---

### Scenario 2: File Not Found

**Input:**
```bash
curl -v http://localhost:8080/nonexistent.html
```

**Expected output:**
```
< HTTP/1.1 404 Not Found
< Content-Type: text/html
```

---

## ❓ Frequently Asked Questions

**Q: Why not use http.server module?**

A: The goal is learning HTTP internals. Using built-in modules hides the protocol details you need to understand.

**Q: How do I test concurrent connections?**

A: Use tools like `ab` (Apache Bench) or `wrk`:
```bash
ab -n 1000 -c 10 http://localhost:8080/
```

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 8 | `08enWSL/` | HTTP server implementation |
| 11 | `11enWSL/` | Load balancing concepts |
| 2 | `02enWSL/` | Socket programming |

---

## 📚 Bibliography

1. **[OFFICIAL]** HTTP/1.1 RFC 7230  
   URL: https://tools.ietf.org/html/rfc7230  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** Python socket documentation  
   URL: https://docs.python.org/3/library/socket.html  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026*  
*Computer Networks — ASE Bucharest*
