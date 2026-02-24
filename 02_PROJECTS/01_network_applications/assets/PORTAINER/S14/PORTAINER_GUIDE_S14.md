# S14 — Portainer Guide: Didactic Distance-Vector Routing in Mininet

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `mininet-host` | Mininet topology + DV routing daemons | varies |
| `tester` | pytest runner + tcpdump | — (internal) |

Two to three containers. The routing logic runs **inside Mininet hosts**, not as separate Docker containers. Portainer's benefit here is limited compared to other projects.

## What Portainer Still Gives You

### Container Health

Even though the interesting work happens inside Mininet, the Docker containers that host Mininet must be running. Portainer confirms:

- `mininet-host` is 🟢 and has not exited due to a privilege error (Mininet requires `--privileged` or `NET_ADMIN`).
- `tester` started after the topology is ready.

### Tester Output

Click `tester` → **Logs** for the pytest output. Since DV convergence is timing-sensitive, test failures often relate to convergence not completing within the expected window.

### Console Access to Mininet

If your Compose file allows it, open **Console** on `mininet-host`:

```sh
# Check Mininet topology
mn --topo=custom --custom /app/topo.py
```

## Honest Assessment

For S14, Portainer is a convenience (quick log access and container state) but adds no architectural insight. The real debugging happens inside Mininet with `xterm`, `pingall` and `tcpdump` on virtual interfaces. Use Portainer for the Docker layer; use Mininet's own tools for the routing layer.
