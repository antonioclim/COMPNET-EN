# S17 — Portainer Guide: In-Memory Object Store

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `object-registry` | Registry and brokered transfer service (your code) | **5017 → 5017** |
| `owner-client` | Publishes objects and renews leases | — (internal) |
| `requester-client` | Lists keys and retrieves objects | — (internal) |
| `watcher-client` | Watches for expiry or removal | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Four to five containers. Portainer is especially useful for correlating registry state with the behaviour of the publishing and requesting clients.

## What to Watch in Portainer

### Registry State

Open **three** tabs:

- Tab A: `object-registry` → **Logs** — publication, retrieval coordination, lease expiry and watcher notifications
- Tab B: `owner-client` → **Logs** — `PUBLISH` and `HEARTBEAT`
- Tab C: `requester-client` → **Logs** — `GET` and received `VALUE`

Verify that the requester does not contact the owner directly. The server should log a brokered `FETCH` or equivalent internal coordination step.

### Lease Expiry

Stop `owner-client` from Portainer after publication. The registry log should remove the key after the configured grace period and the watcher should receive `EXPIRED` or `REMOVED`.

### Quick Inspection

Open **Console** on `object-registry`:

```sh
ps aux
env | grep -E 'LEASE|PORT|PROJECT'
```

If the implementation exposes a debug command or an admin endpoint, use it to list currently registered keys and lease timers.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Duplicate keys appear | Publish path checks uniqueness without locking | Make the check-and-insert sequence atomic |
| Requester waits indefinitely | Registry never asks the owner for the payload | Inspect the server log for the brokered fetch step |
| Keys remain after owner disconnect | Session cleanup does not purge ownership metadata | Trace disconnect handling and lease cancellation |
| Watchers never fire | Prefix matching is wrong or watcher registration is not persisted | Compare watched prefixes with emitted object keys |
