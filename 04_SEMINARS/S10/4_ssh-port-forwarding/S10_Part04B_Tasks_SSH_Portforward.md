### Tasks — SSH port forwarding to an HTTP service in a container

Aim:

- access the HTTP server in the `web` container
- by using an SSH tunnel through the `ssh-bastion` container

Result:

- log file: `ssh_forward_log.txt`

---

## 1. Start the infrastructure

Make sure you have:

- `S10_Part04_Config_Docker_Compose.yml`
- a Dockerfile for `ssh-bastion` (similar to the `ssh-server` image from Stage 3)

Run:

```bash
docker compose up --build
```

---

## 2. Verify internal connectivity (from inside the container)

Enter the `ssh-bastion` container:

```bash
docker compose exec ssh-bastion bash
```

Inside:

```bash
apt-get update && apt-get install -y curl   # if needed
curl http://web:8000/
```

You should see the content served by `web` (for example the directory listing).

Copy the output into `ssh_forward_log.txt` under:

```text
--- DIRECT TEST FROM ssh-bastion ---
<output>
```

Exit the container (`exit`).

---

## 3. Start the SSH tunnel from the host

On the host, run:

```bash
ssh -L 9000:web:8000 labuser@localhost -p 2222
```

Notes:

- `labuser` and `labpass` are the user and password defined in the `ssh-bastion` container
- the command keeps the SSH session open; keep it running while you test curl

---

## 4. Test HTTP access through the tunnel

In **another terminal** on the host:

```bash
curl -v http://localhost:9000/
```

You should see the same content as `curl http://web:8000/` from inside the container.

Copy the output into `ssh_forward_log.txt` under:

```text
--- TEST THROUGH TUNNEL (curl localhost:9000) ---
<output>
```

---

## 5. Reflection questions

At the end of `ssh_forward_log.txt`, answer in a few sentences:

1. What is the role of the `ssh-bastion` container in this scenario?
2. Why can we use `web` as `DEST_HOST` in the `ssh -L` command?
3. What would change if `web` ran on a different machine or IP address?
4. What advantages does port forwarding provide compared with exposing port 8000 directly on the host?

---

### Deliverable (Stage 4)

Submit:

- `S10_Part04_Config_Docker_Compose.yml` (the version used in this stage)
- the Dockerfile for `ssh-bastion` (if it is separate)
- `ssh_forward_log.txt` containing:

  - the direct test from `ssh-bastion`
  - the test through the tunnel (curl localhost:9000)
  - answers to the reflection questions
