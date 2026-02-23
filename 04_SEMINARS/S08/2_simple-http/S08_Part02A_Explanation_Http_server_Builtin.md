We now move on to **Stage 2: Basic HTTP Server with `http.server` (Python)**.

This stage provides:

1. **Explanation file** – `index_httpserver_builtin_explanation.md`
2. **Fully commented code** – `simple_http_builtin.py`
3. **Task file** – `index_httpserver_builtin_tasks.md`

---

### HTTP Server Using the Python Standard Library (http.server)

In this stage we start a functional HTTP server using only the Python
standard library. The objective is to understand:

- what a minimal HTTP server looks like
- how static files can be served
- how one can override behaviour to respond to specific endpoints

Python provides two useful classes for a quick server:

- `http.server.SimpleHTTPRequestHandler`
  – automatically serves files from the current directory

- `http.server.BaseHTTPRequestHandler`
  – a base for defining a custom HTTP server

We will start a server that:
- serves files from the current directory
- responds to `/hello`
- responds to `/api/time` with JSON

The server will subsequently be tested with `curl`.

---

### How to Start the Server

Run:

```

python3 simple_http_builtin.py 8000

```

Then test:

```

curl -v [http://localhost:8000/](http://localhost:8000/)
curl -v [http://localhost:8000/hello](http://localhost:8000/hello)
curl -v [http://localhost:8000/api/time](http://localhost:8000/api/time)

```

---

### What Are This Server's Limitations?

- it does not handle concurrent connections efficiently
- it does not use advanced MIME types (only the defaults)
- it does not parse complex requests
- it is not suitable for production

It is, however, excellent as a laboratory server and for understanding how
HTTP works before implementing a server from scratch with sockets.
