### Minimal HTTP Server Implemented Manually with Sockets

In this stage we implement an HTTP server *from scratch*, using only:

- `socket.socket`
- `bind`, `listen`, `accept`
- reading requests from the network
- sending a valid HTTP response

The goal is not to implement the full HTTP standard but rather to understand:

1. what a REAL HTTP request looks like
2. why `Content-Length` is necessary
3. why the status line must be sent
4. how a static file is served

---

### Structure of a Real HTTP Request

The client sends at least:

```

GET /index.html HTTP/1.1
Host: localhost:8000
User-Agent: curl/8.0
Accept: */*

(optional body)

```

We will use ONLY the first line. The remaining headers are ignored at this stage.

---

### Minimal Structure of an HTTP Response

```

HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 42

<content here>
```

If `Content-Length` is wrong, the browser:

* either does not display the page
* or "waits" for the remaining data
* or closes the connection prematurely

**Therefore: Content-Length is mandatory.**

---

### What We Implement in This Stage

1. A TCP server that listens on a port (e.g. 8000)
2. Accepts connections from clients (curl / browser)
3. Reads the request (at least the first line)
4. Parses the method and path
5. Serves the file from the `static/` directory
6. If the file does not exist → sends `404 Not Found`

---

### Advantage

After this stage, students clearly understand:

* the difference between a "real" server and `http.server`
* what "HTTP parsing" means
* how HTTP packets are formed

Then, in Stage 4 we will place this back-end behind nginx as a reverse proxy.
