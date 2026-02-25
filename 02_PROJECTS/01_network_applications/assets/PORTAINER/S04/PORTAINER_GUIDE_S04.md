# S04 — Portainer Guide: Forward HTTP Proxy

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `proxy` | Forward HTTP proxy (your code) | **3128 → 3128** |
| `origin` | Simple origin server (tester-provided or your own) | **8080 → 8080** |
| `tester` | pytest runner + tcpdump | — (internal) |

Three containers. The tester sends requests **through** the proxy to the origin. The PCAP must show two distinct TCP conversations: tester → proxy and proxy → origin.

## What to Watch in Portainer

### Two-Hop Traffic

This is a project where **parallel log observation** matters. Open two Portainer tabs:

- **Tab A:** `proxy` → **Logs** (auto-refresh on)
- **Tab B:** `origin` → **Logs** (auto-refresh on)

Run `make e2`. Watch requests arrive first at the proxy (Tab A), then at the origin (Tab B). The proxy log should show filtering decisions: which URLs were allowed (200) and which were blocked (403).

### Network View

Open **Networks** and click the Compose network. All three containers should be on the same subnet. Note: the tester addresses the proxy by container name (`proxy:3128`), not by IP.

### Filter Policy Verification

Open **Console** on `tester` (or a debug container):

```sh
# Request that should be allowed
curl -x http://proxy:3128 http://origin:8080/allowed-path

# Request that should be blocked
curl -x http://proxy:3128 http://origin:8080/blocked-path
```

The proxy log in Portainer should show `ALLOW` for the first and `BLOCK` (403) for the second.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Tester cannot reach the proxy | Proxy not listening on 0.0.0.0:3128 | Check bind address in your config |
| Proxy reaches origin but returns mangled response | Proxy modifies `Content-Length` or headers incorrectly | Compare origin **Logs** (what was sent) with tester **Logs** (what was received) |
| Filtering does not trigger 403 | Blacklist file not mounted or wrong path inside container | **Console** on `proxy`: `cat /app/config/blacklist.txt` |
| PCAP shows only one TCP conversation | Proxy connects to origin on loopback instead of the Docker network | Verify proxy forwards to `origin:8080`, not `localhost:8080` |
