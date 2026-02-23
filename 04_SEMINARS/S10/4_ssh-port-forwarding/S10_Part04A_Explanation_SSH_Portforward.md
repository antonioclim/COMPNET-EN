### Stage 4 – SSH port forwarding (local tunnel to an HTTP service in containers)

This stage demonstrates how to access an HTTP service that runs inside a container network **through SSH local port forwarding**, as if the service were local.

Scenario:

- container `web`:
  - runs an HTTP server (e.g. `python -m http.server 8000`)
  - does not publish port 8000 to the host (it uses `expose`, not `ports`)
- container `ssh-bastion`:
  - runs `sshd`
  - is reachable from the host on port 2222
  - is on the same Docker network as `web`
- host:
  - connects to `ssh-bastion` using `ssh -L`
  - opens a local port 9000 that is tunnelled to `web:8000` inside the Docker network

Diagram:

```text
browser/curl (host) -> localhost:9000
                      |
                      | (SSH tunnel -L)
                      v
            ssh-bastion container
                      |
                      v
                  web:8000 (HTTP server)
```

---

## 1. What is local port forwarding (`ssh -L`)?

General syntax:

```bash
ssh -L LOCAL_PORT:DEST_HOST:DEST_PORT user@ssh_host
```

Meaning:

- `ssh` establishes a connection to `ssh_host`
- on the **local** machine, it opens `LOCAL_PORT`
- any traffic sent to `localhost:LOCAL_PORT` is tunnelled over SSH and forwarded to
  `DEST_HOST:DEST_PORT` from the perspective of `ssh_host`

In our lab:

```bash
ssh -L 9000:web:8000 labuser@localhost -p 2222
```

- `ssh_host` = `localhost` port 2222 (the `ssh-bastion` container)
- `LOCAL_PORT` = 9000 (on the host)
- `DEST_HOST` = `web` (Docker service name)
- `DEST_PORT` = 8000 (HTTP port inside the `web` container)

---

## 2. Why is this useful?

Real-world uses include:

- accessing internal services that are not publicly exposed
- debugging and testing services inside an internal cluster
- reaching internal UIs (dashboards, databases) without publishing them on the Internet
- security: you expose only SSH, not each service port

---

## 3. What you will do in this stage

1. Start `S10_Part04_Config_Docker_Compose.yml` with:

   - `web` (HTTP server on 8000, internal only)
   - `ssh-bastion` (SSH server, port mapping 2222:22)

2. From inside `ssh-bastion`, verify that `web:8000` is reachable (e.g. `curl web:8000`).

3. From the host, run:

   ```bash
   ssh -L 9000:web:8000 labuser@localhost -p 2222
   ```

4. On the host, test:

   ```bash
   curl http://localhost:9000/
   ```

   The response should come from the HTTP server inside the `web` container.
