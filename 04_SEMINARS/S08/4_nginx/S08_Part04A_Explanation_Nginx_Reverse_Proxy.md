### Reverse Proxy with nginx and Docker

In this stage we place a reverse proxy nginx, running inside a Docker container,
in front of our Python HTTP server.

Objectives:

- understand what a reverse proxy is
- observe how nginx can sit in front of a Python back-end
- practise using Docker/Docker Compose for a simple service

---

### What Is a Reverse Proxy?

Simplified diagram:

```

client (browser / curl) -> nginx -> backend (Python server)

```

nginx:

- accepts connections from clients on a port (e.g. 8080)
- forwards requests to a back-end (e.g. http://127.0.0.1:8000)
- receives the back-end's response and relays it to the client
- can add/modify headers, perform caching, load balancing etc.

Advantages:

- hides the back-end (the client sees only nginx)
- allows centralising authentication, logging, TLS etc.
- enables running multiple back-ends behind a single entry point

---

### Why Docker?

Instead of installing nginx directly on the system, we use a container:

- official `nginx:alpine` image
- our configuration is mounted into the container
- everything starts with a single command: `docker compose up`

In our laboratory:

- the back-end (Python server) runs on the host, on port 8000
- nginx runs inside a container, but with `network_mode: "host"` for simplicity
  - this way the container can reach the back-end on `127.0.0.1:8000`
  - and directly exposes port 8080 to the host

---

### Laboratory Architecture

Back-end:

- the Python server (e.g. `simple_http_builtin.py`) started on port 8000

Front-end (reverse proxy):

- nginx in Docker, listening on port 8080
- all requests arriving at nginx on 8080 are forwarded to `http://127.0.0.1:8000`

Diagram:

```

curl [http://localhost:8080/](http://localhost:8080/)  -> nginx (8080) -> [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

```

We will:

- test the back-end directly
- test access through nginx
- add a custom header from nginx to demonstrate that traffic passes through the proxy.
