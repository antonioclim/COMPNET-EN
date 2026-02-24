# S07 — Portainer Guide: UDP DNS Resolver

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `resolver` | DNS resolver (your code) | **5300 → 5300/udp** |
| `upstream-stub` | Simulated upstream DNS (or real) | 53/udp (exposed) |
| `tester` | pytest runner + tcpdump | — (internal) |

Three containers. The tester sends DNS queries to `resolver:5300`, which answers from its local zone or forwards to `upstream-stub:53`.

## What to Watch in Portainer

### Three Query Types in the Logs

Your E2 PCAP must evidence three distinct behaviours. In the resolver **Logs**, watch for:

1. **Local-zone hit** — query for a name in the configured zone. The resolver answers immediately; no upstream traffic.
2. **Forwarded query** — query for an external name. The resolver forwards to `upstream-stub` and relays the response.
3. **Cache hit** — repeat of a previously forwarded query. The resolver answers from cache; no upstream packet.

Open **two** tabs: `resolver` logs and `upstream-stub` logs. On the third query (cache test), `upstream-stub` should show **no** new incoming request.

### TTL Verification

Open **Console** on `tester`:

```sh
# First query (forwarded)
dig @resolver -p 5300 example.com A

# Immediate repeat (should be cached)
dig @resolver -p 5300 example.com A

# Wait for TTL to expire, then query again (should forward again)
sleep <TTL+1>
dig @resolver -p 5300 example.com A
```

Correlate each step with the resolver log in Portainer: the second query should show "cache hit" and the third (after expiry) should show "forwarding to upstream."

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Resolver exits immediately | UDP socket bind failure | Logs: check for "Address already in use" or permission error |
| All queries forwarded, none cached | Cache not populated on first response | Check that you store the response with its TTL |
| Cache never expires | TTL countdown not implemented | Verify cache eviction logic |
| `NXDOMAIN` not returned for absent names | Error-code handling missing | Check response-code construction for unknown names |
