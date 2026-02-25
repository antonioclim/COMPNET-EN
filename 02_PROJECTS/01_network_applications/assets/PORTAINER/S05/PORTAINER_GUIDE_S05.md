# S05 — Portainer Guide: Application-Layer HTTP Load Balancer

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `lb` | Load balancer (your code) | **8080 → 8080** |
| `backend1` | HTTP backend instance 1 | 8081 (exposed) |
| `backend2` | HTTP backend instance 2 | 8082 (exposed) |
| `backend3` | HTTP backend instance 3 | 8083 (exposed) |
| `tester` | pytest runner + tcpdump | — (internal) |

Five containers. This is architecturally identical to the S11 seminar exercise — if you completed the Portainer tasks there, you already know the workflow.

## What to Watch in Portainer

### Round-Robin Observation (the main event)

Open **four** Portainer browser tabs:

- Tab A: `backend1` → **Logs** (auto-refresh on)
- Tab B: `backend2` → **Logs** (auto-refresh on)
- Tab C: `backend3` → **Logs** (auto-refresh on)
- Tab D: `lb` → **Logs** (auto-refresh on)

Run `make e2`. Watch requests land on each backend in rotation. The LB log (Tab D) should show routing decisions and the `X-Backend` header assignment.

### Health-Check Verification

Your LB must perform periodic health checks against `/health` on each backend. In the backend logs, you should see these requests arriving at a regular interval (e.g. every 2 seconds). In the LB log, watch for health-check results: pass/fail per backend.

### Failover Test

This is the moment Portainer becomes indispensable:

1. In Portainer → select `backend2` → click **Stop**.
2. `backend2` turns 🔴.
3. Trigger requests (from the host or from the tester console):
   ```sh
   curl http://localhost:8080/work
   ```
4. Observe: only `backend1` and `backend3` receive traffic. The LB log should show `backend2` marked as unhealthy.
5. **Restart** `backend2` from Portainer. After the configured number of consecutive health-check successes, it should re-enter the rotation.

### `/status` Endpoint

Open **Console** on `lb`:

```sh
curl -s http://localhost:8080/status | python3 -m json.tool
```

Verify the JSON reports active/inactive backends, request counts and error counts.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| All requests go to one backend | Round-robin index not advancing | LB **Logs**: is the selection algorithm running? |
| Health checks never appear in backend logs | Wrong health-check endpoint or interval too long | Verify `/health` is implemented and the interval matches your config |
| Stopped backend still receives traffic | LB does not remove failed backends | LB **Logs**: check health-check failure threshold logic |
| `X-Backend` header missing in PCAP | Header not added by the LB | LB **Logs** + `curl -v http://localhost:8080/work` from Console |
| `/status` returns empty or wrong counts | Status tracking not wired to the routing logic | Check that each routed request increments the counter |
