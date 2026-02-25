# S11 — Portainer Observation Tasks

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

Keep Portainer open in a dedicated browser tab for the entire seminar.

---

## Part 1 — Nginx Round-Robin

### P1 — Topology Snapshot

After starting the Nginx stack, fill in from Portainer:

| Container     | State | Image | Published Ports | Internal IP |
|---------------|-------|-------|-----------------|-------------|
| `web1`        |       |       |                 |             |
| `web2`        |       |       |                 |             |
| `web3`        |       |       |                 |             |
| `nginx-proxy` |       |       |                 |             |

1. Which container is the only one reachable from your host browser? Why?
2. Open **Networks** → **lbnet**. Sketch the topology: four nodes, one subnet, with IPs.

### P2 — Round-Robin Live Observation

Open three Portainer tabs — one for each backend's **Logs** view (auto-refresh on).

In PowerShell:

```powershell
for ($i = 1; $i -le 9; $i++) {
    curl.exe -s http://localhost:8080/ | Out-Null
    Start-Sleep -Milliseconds 200
}
```

Record which backend handled each request:

| # | Backend |  | # | Backend |  | # | Backend |
|:-:|---------|--|:-:|---------|--|:-:|---------|
| 1 |         |  | 4 |         |  | 7 |         |
| 2 |         |  | 5 |         |  | 8 |         |
| 3 |         |  | 6 |         |  | 9 |         |

Is the distribution uniform? Describe the pattern in one sentence:

> `__________________________________________________________`

### P3 — Failure Resilience

1. In Portainer → select `web2` → click **Stop**.
2. Confirm: `web2` state is now 🔴.
3. Send six more requests. Which backends respond?  → `____`
4. **Restart** `web2` from Portainer.
5. Send six more requests. Does `web2` receive traffic again?  → Yes / No

How does Nginx handle a backend that goes down?

> `__________________________________________________________`

### P4 — Clean Transition

Run `docker compose down`. Verify in Portainer:

- [ ] Only `portainer` remains in the Containers list.

If Part 1 containers are still visible, you likely forgot the `-f` flag.

---

## Part 2 — Custom Python LB

### P5 — Build Status

After starting the custom LB stack:

1. Is `lb-custom` running (🟢) or exited (🔴)?  → `____`
   - If 🔴: open its **Logs**. What error do you see?  → `____`
2. What is different about the **Image** column for `lb-custom` compared to the backends?

### P6 — DNS Resolution from Inside the LB

Open **Console** on `lb-custom`. Run:

```sh
getent hosts web1-lb
getent hosts web2-lb
getent hosts web3-lb
```

Do the IPs match the Networks view in Portainer?  → Yes / No

### P7 — Comparative Failure Test

Repeat the failure test, this time on the Python LB:

1. Stop `web2-lb` from Portainer.
2. Send six requests to `http://localhost:8080/`.
3. Does the Python LB handle the failure as gracefully as Nginx?

| Observation | Nginx (Part 1) | Python LB (Part 2) |
|---|---|---|
| Error messages to the client? | | |
| Noticeable delay? | | |
| Dropped requests? | | |

### P8 — Architecture Comparison

Fill in using information from Portainer and `curl`:

| Dimension | Nginx (Part 1) | Custom LB (Part 2) |
|---|:-:|:-:|
| Proxy image | | |
| Proxy published port | | |
| Number of backends | | |
| Backend image | | |
| Failure behaviour | | |
| Built-in health checks? | | |

---

## Final Self-Check

Mark each statement as true or false:

| Statement | T / F |
|---|:---:|
| A reverse proxy terminates the client connection and opens a new one to the backend | |
| Backends with no published ports are unreachable from the host browser | |
| `docker compose down` removes both containers and the Compose network | |
| Round-robin distributes requests equally regardless of backend load | |
| Docker DNS inside a Compose network resolves container names to IPs | |
