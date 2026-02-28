# S19 — Portainer Guide: Distributed Auction

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `auction-service` | Authoritative auction service (your code) | **5019 → 5019** |
| `seller-client` | Publishes auction items and observes closure | — (internal) |
| `bidder-a` | Places an early valid bid | — (internal) |
| `bidder-b` | Places a competing higher bid | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Four to five containers. Portainer is especially useful here because accepted bids, outbid events and deadline-driven closure are easier to correlate across parallel log views than from a single terminal.

## What to Watch in Portainer

### Bid Progression and Fan-out

Open **three** tabs:

- Tab A: `auction-service` → **Logs** — auction creation, accepted bids, rejections, closure and winner selection
- Tab B: `seller-client` → **Logs** — `SELL` request and closure notification
- Tab C: `bidder-a` and `bidder-b` → **Logs** — competing `BID` attempts and `OUTBID` handling

Check that only one highest bid exists at any time and that the outbid client is notified after the higher accepted bid is committed.

### Timer-driven Closure

Leave the stack running until the configured deadline expires. The service log should emit `CLOSED` and `WINNER` without manual intervention. If closure happens only after a later command arrives, the timer logic is incomplete.

### Quick Inspection

Open **Console** on `auction-service`:

```sh
ps aux
env | grep -E 'PORT|AUCTION|PROJECT|TIMER'
```

If your implementation stores an append-only event log on disk, inspect it and compare the recorded order with the application log.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| A lower bid replaces a higher bid | Comparison uses `>=` or string ordering | Use a canonical numeric representation and enforce strictly greater bids |
| Late bids are accepted | Deadline is checked with the client timestamp | Use only the server clock for acceptance |
| Two winners appear in the logs | Closure and settlement are not atomic | Guard closure with a single authoritative transition |
| The event log does not match the final state | Log entries are emitted before validation or after a failed commit | Log only committed transitions in the authoritative order |
