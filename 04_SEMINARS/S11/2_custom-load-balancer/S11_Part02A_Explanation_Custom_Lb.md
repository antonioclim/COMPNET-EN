## Part B – Implementing a simple HTTP load balancer in Python

This part of the seminar tasks you with implementing a minimal reverse proxy / load balancer in Python using sockets.

The purpose is didactic: to understand what a load balancer does internally, not to reproduce the full behaviour of nginx.

---

## Learning objectives

By the end of this part, you should be able to:

- explain the role of a load balancer as an HTTP reverse proxy
- implement a basic round-robin algorithm across multiple backends
- forward an HTTP request from a client to a selected backend
- return the backend response to the client
- reason about limitations of a naïve implementation compared with nginx

---

## What the load balancer will do

Your custom load balancer:

- listens on port **8080**
- accepts HTTP connections from clients (curl or a browser)
- forwards each request to one of the backend servers:
  - `web1:8000`
  - `web2:8000`
  - `web3:8000`
- uses a round-robin algorithm to select the backend
- returns the backend's response to the client

At a conceptual level:

```text
client -> custom LB -> web1/web2/web3
```

---

## What we intentionally do not implement

This script is deliberately simple. It does not implement:

- persistent connections (keep-alive)
- chunked transfer encoding
- TLS termination (HTTPS)
- advanced header manipulation
- streaming large files efficiently

These topics are handled by production-grade proxies such as nginx, HAProxy or Envoy.

---

## Files in this part

- `S11_Part02_Script_Simple_Lb.py` — the custom load balancer (to complete)
- `S11_Part02_Config_Docker_Compose_Lb_Custom.yml` — Docker Compose setup with web1/web2/web3 and the LB
- `web1/`, `web2/`, `web3/` — backend services (simple HTTP servers)

---

## Next step

You will complete the TODO sections in `S11_Part02_Script_Simple_Lb.py` and then run the full setup with Docker Compose.
