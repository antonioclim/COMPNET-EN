## Stage 2 – Building an architecture with 3 backends and an nginx reverse proxy (Docker Compose)

### Objectives

This stage builds a fully working environment using Docker Compose:

- three simple backend servers, each running `python -m http.server 8000`
- an nginx container configured as a reverse proxy and load balancer
- verification with `curl` that load balancing works (round robin)
- preparation for the next stage (replacing nginx with a custom Python load balancer)

---

## 1. Architecture structure

You will have the following containers:

```text
nginx (reverse proxy)
 ├── web1:8000
 ├── web2:8000
 └── web3:8000
```

Clients will access the system through:

```text
http://localhost:8080
```

---

## 2. Starting the architecture

In a terminal:

```bash
docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml up --build
```

Then, in another terminal, test:

```bash
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

You should observe output similar to:

```html
<h1>Hello from web1</h1>
<h1>Hello from web2</h1>
<h1>Hello from web3</h1>
<h1>Hello from web1</h1>
...
```

This indicates round-robin distribution.

---

## 3. Important observation

The backend services are **not visible from outside** (they have no ports mapped on the host).
Only nginx is exposed on `localhost:8080`.

This is typical in architectures that use a reverse proxy.

---

## 4. What follows next?

In the next stage you will replace nginx with a Python load balancer that:

- listens for HTTP connections
- receives requests
- forwards them to the backends
- implements a round-robin algorithm

You will then compare its behaviour with nginx.
