# S10 — Portainer Observation Tasks

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

Keep Portainer open in a browser tab throughout the session. Complete each task group at the corresponding point in the seminar.

---

## During Part 2 — DNS Containers

### P1 — Network Comparison

After `docker compose up` for the DNS stack:

1. In **Networks**: how many non-default networks exist?  → `____`

2. Click the Compose-created network. Fill in:

   | Container | IP address |
   |-----------|------------|
   | `web` | |
   | `dns-server` | |
   | `debug` | |

3. Open **Console** on `debug`. Run:
   ```sh
   nslookup web 127.0.0.11
   ```
   Does the returned IP match the one shown in Portainer?  → `____`

### P2 — Clean Transition Checkpoint

After `docker compose down` for DNS:

How many containers are running besides `portainer`?  → `____`

If you see anything other than `portainer`, stop it from the dashboard before continuing.

**Expected answer: 0.**

---

## During Part 3 — SSH with Paramiko

### P3 — Port Mapping Analysis

After `docker compose up` for the SSH stack:

1. Click `ssh-server` in Portainer. Find the published port mapping.

   `host_port` : `container_port`  →  `____` : `____`

2. Why is port 22 not published directly as 22 on the host?

   *(Hint: what service typically occupies port 22 on the host operating system?)*

### P4 — Clean Transition Checkpoint (repeat)

After `docker compose down` for SSH: only `portainer` remains?  → ✅ / ❌

---

## During Part 4 — SSH Port Forwarding

### P5 — Isolation Proof

After `docker compose up` for the port-forwarding stack, look at the **Published Ports** column in Portainer:

| Question | Answer |
|---|---|
| Which container has published ports? | |
| Which container has **no** published ports? | |
| Can you access `http://localhost:8000` directly? | works / does not work |
| After the SSH tunnel (`ssh -L 9000:web:8000 ...`), can you access `http://localhost:9000`? | works / does not work |

### P6 — Log Observation Through the Tunnel

1. Click `web` in Portainer → **Logs** → enable auto-refresh.
2. In another window: `curl http://localhost:9000/`
3. Did the web container's log show the HTTP request?  → Yes / No

Explain in one sentence how this is possible, given that `web` has no published ports:

> `__________________________________________________________`

---

## Self-Check

| Concept | Verified through Portainer? |
|---|:---:|
| Docker internal DNS resolves service names to IPs | Task P1 |
| Clean transitions between stacks prevent port conflicts | Tasks P2, P4 |
| Port mapping is explicit — not automatic | Task P3 |
| No published port means no direct host access | Task P5 |
| SSH tunnelling bypasses port isolation | Task P6 |
