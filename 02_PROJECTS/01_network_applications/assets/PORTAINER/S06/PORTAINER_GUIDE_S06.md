# S06 — Portainer Guide: TCP Pub/Sub Broker

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `broker` | Pub/Sub broker (your code) | **5006 → 5006** |
| `publisher` | Message producer | — (internal) |
| `subscriber1` | Consumer instance 1 | — (internal) |
| `subscriber2` | Consumer instance 2 | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Four to five containers. The broker is the central routing point; publishers and subscribers connect to it by service name.

## What to Watch in Portainer

### Message Routing Observation

Open **three** Portainer tabs:

- Tab A: `broker` → **Logs** — shows SUBSCRIBE registrations, PUBLISH arrivals and routing decisions per topic
- Tab B: `subscriber1` → **Logs** — shows messages received (with topic and payload)
- Tab C: `subscriber2` → **Logs** — same as Tab B

Run `make e2`. Verify:
- Both subscribers receive the same messages for shared topics.
- Messages arrive in the order published (no reordering).
- Each PUBLISH in the broker log has a corresponding delivery to both subscriber logs.

### Disconnect and Reconnect Test

1. In Portainer → select `subscriber1` → **Stop**.
2. From the publisher (or tester), send additional messages.
3. Check `subscriber2` logs: still receiving.
4. **Restart** `subscriber1`.
5. Observe the broker log: does subscriber1 re-register? Does it receive messages published during the downtime? (This depends on your at-least-once vs exactly-once semantics.)

### Topic Matching Verification

Open **Console** on a debug container or `tester`:

```sh
# Manual publish to a specific topic
echo '{"cmd":"PUBLISH","topic":"sensors/temp","payload":"22.5"}' | nc broker 5006
```

Watch the broker log for routing and verify both subscribers (if subscribed to `sensors/temp`) show the message.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Subscribers connect but never receive | Broker routing table not updated on SUBSCRIBE | Broker **Logs**: does the subscription register? |
| Messages delivered to one subscriber but not the other | Per-topic subscriber list incomplete | Broker **Logs**: check subscriber count per topic |
| Messages arrive out of order | Concurrent writes without ordering guarantee | Review broker's per-topic queue implementation |
| Reconnected subscriber misses messages | No message buffering during disconnect | Expected if your semantics are "at-most-once"; document this |
