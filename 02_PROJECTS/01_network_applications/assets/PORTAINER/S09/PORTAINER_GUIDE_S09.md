# S09 — Portainer Guide: TCP Tunnel with Session Multiplexing

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `tunnel-server` | Multiplexing tunnel endpoint (your code) | **9000 → 9000** |
| `echo-svc` | Internal echo backend | — (exposed only) |
| `http-svc` | Internal HTTP backend | — (exposed only) |
| `tester` | pytest runner + tcpdump | — (internal) |

Four containers. The tester connects to `tunnel-server:9000` on a single TCP connection, then opens multiple logical sessions routed to different backend services.

## What to Watch in Portainer

### Session Correlation Across Three Logs

This is where parallel log observation proves its worth. Open **three** tabs:

- Tab A: `tunnel-server` → **Logs** — shows session IDs, service routing decisions, frame demultiplexing
- Tab B: `echo-svc` → **Logs** — shows payloads arriving from session N (echo-bound traffic)
- Tab C: `http-svc` → **Logs** — shows HTTP requests arriving from session M (http-bound traffic)

Run `make e2`. Correlate:
- Tunnel-server log: "session 1 → echo-svc, session 2 → http-svc"
- echo-svc log: payload received, echo returned
- http-svc log: GET request received, response sent

### Single TCP Stream Verification

Open **Networks** and click the Compose network. The tunnel-server has a published port (9000); the backends do not. Only the tunnel is reachable from outside — the backends are isolated. This is the whole point of the project.

### Frame Inspection

Open **Console** on `tester`:

```sh
# Verify the tunnel accepts raw connections
nc tunnel-server 9000
```

Type a framed message (per your protocol: session ID + length + payload). Watch the tunnel-server log for parsing and routing.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Tunnel-server exits immediately | Bind failure on port 9000 | **Logs**: check for "Address already in use" |
| Session opens but data never reaches the backend | Demux logic routes to wrong service ID | Tunnel **Logs**: verify service-ID → backend mapping |
| Backend receives data but response never reaches the tester | Response framing broken (missing session ID in return frame) | Tunnel **Logs**: check return-path multiplexing |
| PCAP shows multiple TCP streams instead of one | Tunnel opens new connections per session instead of multiplexing | Verify your tunnel reuses a single outbound TCP connection |

## Note on Port 9000

Port 9000 is also used in S10 seminar (SSH tunnel exercise). There is no conflict — the seminar containers are stopped by the time you work on projects. Portainer runs on 9050 and is unaffected.
