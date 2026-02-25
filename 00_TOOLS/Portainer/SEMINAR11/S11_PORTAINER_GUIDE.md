# S11 — Portainer Integration (Instructor Notes)

## Context

Seminar 11 is the most Docker-intensive session of the semester. Two load-balancing architectures are deployed back-to-back: an Nginx reverse proxy (Part 1) and a custom Python load balancer (Part 2). Each stack runs four containers on a shared `lbnet` network. The seminar's arc depends on students *seeing* the difference between the two architectures and observing real-time behaviour during deliberate failure tests.

This is where Portainer shifts from "handy shortcut" to "primary observation instrument." Three parallel log streams, one-click stop/start for failure tests and instant topology snapshots — these are all things the CLI can do, but not as fluently when four containers are in play simultaneously.

## Pedagogical Objectives Augmented

| Objective already in the seminar | What Portainer adds |
|---|---|
| Observe round-robin distribution across backends | Three simultaneous log tabs — watch requests land on web1, web2, web3 in rotation |
| Test resilience by stopping a backend | Stop/start a container from the dashboard in one click; the state change is immediately visible |
| Compare Nginx proxy vs custom Python LB | Side-by-side topology snapshots (same 4-container shape, different images and ports) |
| Understand that backends are not directly reachable | Published-ports column: only the proxy has one; backends have none |
| Debug build failures in custom Dockerfile | Exit code and log trace visible on the container card without extra commands |

The round-robin log observation is the highlight. Doing it from the CLI requires three terminals running `docker logs -f web1`, `docker logs -f web2`, `docker logs -f web3` — manageable but clunky. Portainer turns this into three browser tabs with auto-refresh, which students find more intuitive.

## How to Use It — Instructor Perspective

### Pre-seminar checklist

- [ ] Portainer running on 9050
- [ ] No leftover containers from S10
- [ ] Images pre-pulled:
  ```powershell
  docker pull python:3.11-alpine
  docker pull nginx:latest
  ```

---

### Part 1 — Nginx Load Balancer (minutes 8–20)

**Start the stack:**

```powershell
cd 1_nginx-compose
docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml up -d
```

**Topology overview.** In Portainer → Containers:

| Container     | State | Published Ports |
|---------------|-------|-----------------|
| `web1`        | 🟢    | — (expose 8000) |
| `web2`        | 🟢    | —               |
| `web3`        | 🟢    | —               |
| `nginx-proxy` | 🟢    | **8080 → 80**   |

> *▸ "Four containers. Only `nginx-proxy` has a port published on the host. The backends are invisible from the outside — reachable only through the proxy."*

**Network view.** Click **Networks** → **lbnet**. All four containers are on the same subnet. The IPs listed here are what the `upstream` block in `nginx.conf` resolves to.

**Round-robin observation.** This is the centrepiece.

1. Open three Portainer tabs:
   - Tab A: `web1` → **Logs** (auto-refresh on)
   - Tab B: `web2` → **Logs** (auto-refresh on)
   - Tab C: `web3` → **Logs** (auto-refresh on)

2. In PowerShell, send six sequential requests:
   ```powershell
   for ($i = 1; $i -le 6; $i++) {
       curl.exe -s http://localhost:8080/ | Out-Null
       Start-Sleep -Milliseconds 200
   }
   ```

3. Students watch the log lines appear in rotation: web1 gets requests 1 and 4, web2 gets 2 and 5, web3 gets 3 and 6.

> *▸ "Real-time round-robin distribution: each backend receives a request in turn. Without Portainer you would need three PowerShell windows with `docker logs -f`."*

**Failure test.** In Portainer, select `web2` → **Stop**. The card turns red. Repeat the six-request loop. Only web1 and web3 receive traffic.

> *▸ "Nginx detects the failed backend and removes it from the rotation. Notice: web2 is stopped, and its logs are silent."*

Restart `web2` from Portainer. Resume requests — web2 re-enters the rotation.

**Clean transition.** Before Part 2:

```powershell
docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml down
```

Verify in Portainer: only `portainer` remains. If Part 1 containers are still visible, the student likely forgot the `-f` flag (common mistake — Portainer catches it instantly).

---

### Part 2 — Custom Python LB (minutes 22–33)

**Start the stack:**

```powershell
cd ..\2_custom-load-balancer
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml up -d --build
```

**Build verification.** `lb-custom` is built from a Dockerfile. If the build fails, the container appears as red (exited) in Portainer. Click it → **Logs** → the Python traceback or build error is right there.

> *▸ "If `lb-custom` appears in red, open its logs — typically it is an import error or a Python syntax error."*

**Architecture comparison.** Point out the structural parallel in Portainer:

| Container   | Image              | Published Ports |
|-------------|--------------------|--------------------|
| `web1-lb`   | python:3.11-alpine | — (expose 8000) |
| `web2-lb`   | python:3.11-alpine | —                |
| `web3-lb`   | python:3.11-alpine | —                |
| `lb-custom` | *custom build*     | **8080 → 8080**  |

> *▸ "Compare with Part 1: there Nginx listened on internal port 80, published as 8080. Here, the Python load balancer listens directly on 8080. Different implementation, same role."*

**DNS verification.** Open **Console** on `lb-custom`:

```sh
ping -c 1 web1-lb
ping -c 1 web2-lb
```

> *▸ "The load balancer resolves container names via Docker DNS — just like Nginx."*

**Failure test (repeat).** Stop `web2-lb` from Portainer. Send requests. Observe: does the Python LB handle the failure as gracefully as Nginx did? This is the comparison question that closes the seminar.

**Packet capture from the container console.** If `tcpdump` is available in the image:

```sh
tcpdump -i eth0 -c 20 -w /tmp/lb_traffic.pcap &
```

Generate traffic from the host, then copy the capture out:

```powershell
docker cp lb-custom:/tmp/lb_traffic.pcap .
```

---

### Usage Density Summary

Across the full seminar, Portainer is used roughly fifteen times: four state checks, two parallel-log sessions, four stop/start actions, two network inspections, two console accesses and one build-failure diagnosis. This is the peak. Students who are comfortable with Portainer after S11 will use it instinctively for their projects.

## How to Use It — Student Perspective

Students receive `S11_PORTAINER_TASKS.md`, which mirrors the two-part structure. Part 1 tasks focus on topology snapshots, round-robin observation and the failure test. Part 2 adds build verification, DNS checks from inside the LB container and a comparative failure test. The final table asks students to compare the two architectures across six dimensions — all observable through Portainer and `curl` alone.
