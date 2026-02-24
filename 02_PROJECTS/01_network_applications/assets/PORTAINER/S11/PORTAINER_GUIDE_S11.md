# S11 — Portainer Guide: REST Microservices with Service Registry and API Gateway

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `gateway` | API gateway (routes based on registry) | **8080 → 8080** |
| `registry` | Service registry (heartbeat + expiry) | **8500 → 8500** |
| `svc-a` | Microservice instance A | 5101 (exposed) |
| `svc-b` | Microservice instance B | 5102 (exposed) |
| `svc-c` | Microservice instance C | — (exposed) |
| `discovery` | Multicast discovery agent (Flex component) | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

**Seven containers.** This is the most complex project in the catalogue. Portainer is not optional here — debugging a 7-container distributed system from `docker logs` alone is painful.

## What to Watch in Portainer

### Startup Sequence

Watch the **Containers** list as `make e2` runs. The expected order:

1. `registry` starts first (other services register with it).
2. `svc-a`, `svc-b`, `svc-c` start and register.
3. `discovery` sends UDP multicast announcements.
4. `gateway` starts and reads the registry.
5. `tester` starts last.

If any container exits early (🔴), click it → **Logs** for the error.

### Control Plane vs Data Plane

Open **two** Portainer tabs for the control plane:

- **Tab A:** `registry` → **Logs** — registration events, heartbeats, expiry warnings
- **Tab B:** `gateway` → **Logs** — routing decisions, selected instance per request

And **three** tabs for the data plane:

- **Tab C:** `svc-a` → **Logs** — incoming requests with `instance_id`
- **Tab D:** `svc-b` → **Logs** — same
- **Tab E:** `svc-c` → **Logs** — same

### Failover Test (the critical observation)

1. In Portainer → select `svc-b` → **Stop**.
2. Wait for the heartbeat interval to expire.
3. Check the registry log: `svc-b` should be marked as expired.
4. Send a request to the gateway:
   ```sh
   curl http://localhost:8080/api/resource
   ```
5. Observe the gateway log: it should route to `svc-a` or `svc-c`, not `svc-b`.
6. Send another request. If all remaining instances are down, the gateway should return **503**.
7. **Restart** `svc-b`. Watch the registry log for re-registration. After the configured recovery period, `svc-b` re-enters the routing table.

### Service-Discovery Observation

Open `discovery` → **Logs**. Watch for multicast announcements on `239.10.11.12:5111`. Then check the registry log to see whether the registry received and processed the announcement.

### Network Topology

Open **Networks** and click the Compose network. All seven containers should be on the same subnet. Note the IPs — these are what the registry stores and the gateway uses for routing.

### Request Tracing

If you propagate `X-Request-ID`, follow a single request across:
1. Gateway log: "routing request abc123 to svc-a"
2. svc-a log: "received request abc123"

This correlation is visible in two Portainer tabs simultaneously.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Gateway returns 503 on all requests | No services registered, or registry unreachable | Registry **Logs**: any registrations? Gateway **Logs**: can it reach the registry? |
| Heartbeat expiry too aggressive | Interval shorter than service startup time | Check registry config: increase expiry threshold |
| Gateway routes to expired service | Expiry not propagated to routing table | Gateway **Logs**: when does it refresh the registry? |
| Discovery agent does nothing | Multicast not working inside Docker | Check that the Compose network supports multicast (default bridge does) |
| `X-Request-ID` missing from backend logs | Header not forwarded by the gateway | Gateway code: verify header propagation |
| Tester fails with "connection timed out" | Gateway or registry not ready when tester starts | Add a health-check or startup delay in `docker-compose.yml` |
