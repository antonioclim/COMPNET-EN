# S18 — Portainer Guide: Resource Reservation

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `reservation-service` | Hold and reservation service (your code) | **5018 → 5018** |
| `client-a` | Requests the first hold and confirms it | — (internal) |
| `client-b` | Competing client used for overlap refusal | — (internal) |
| `watcher-client` | Observes state changes | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Four to five containers. Portainer helps because the interesting E2 behaviour is distributed across several clients and a time-sensitive server.

## What to Watch in Portainer

### Overlap Refusal

Open **three** tabs:

- Tab A: `reservation-service` → **Logs** — accepted holds, refused overlaps, expiry timers and confirmations
- Tab B: `client-a` → **Logs** — successful `HOLD` and `CONFIRM`
- Tab C: `client-b` → **Logs** — deterministic `OVERLAP` or `REJECT`

Run `make e2` and confirm that:

1. `client-a` obtains a temporary hold.
2. `client-b` is refused for the overlapping interval.
3. The hold becomes a confirmed reservation or expires on schedule.
4. The watcher receives a state change.

### Timer Behaviour

Stop one client mid-scenario or wait for the configured hold timer. The server log should show `EXPIRED`, `RELEASED` or `CANCELLED` without manual cleanup.

### Quick Inspection

Open **Console** on `reservation-service`:

```sh
date -u
env | grep -E 'HOLD|TTL|PORT|PROJECT'
```

If your implementation keeps a local database or JSON snapshot, inspect it to verify that confirmed reservations and expired holds are distinguished correctly.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Overlapping requests are both accepted | Interval-boundary logic is wrong | Add tests for partial overlap, exact overlap and adjacent intervals |
| Holds never expire | Timer manager only runs on explicit commands | Add a periodic expiry sweep or scheduled timers |
| Confirm works for the wrong client | Hold ownership is not checked | Bind hold IDs to the owning session or user |
| Logs cannot be correlated | Server time is not exposed in responses or logs | Emit authoritative timestamps on state changes |
