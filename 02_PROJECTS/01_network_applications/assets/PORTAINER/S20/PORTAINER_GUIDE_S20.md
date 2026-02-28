# S20 — Portainer Guide: Database-backed Object Service

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `object-db-service` | Persistent object service (your code) | **5020 → 5020** |
| `client-a` | Performs query and update operations | — (internal) |
| `client-b` | Watches objects and observes notifications | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Four containers in the baseline design. If the team separates the database into its own container, Portainer becomes even more informative, but the standard E2 baseline assumes a single service container backed by an embedded deterministic store such as SQLite.

## What to Watch in Portainer

### Query, Update and Notification Correlation

Open **three** tabs:

- Tab A: `object-db-service` → **Logs** — query handling, committed updates, deletes and notifications
- Tab B: `client-a` → **Logs** — `QUERY`, `GET`, `UPDATE` and `DELETE`
- Tab C: `client-b` → **Logs** — `WATCH`, `CHANGED` and `DELETED`

Verify that the service notifies only the interested client and that the reported revision or state marker changes after the update.

### Persistence Check

Restart `object-db-service` from Portainer after the scripted E2 flow or during an auxiliary manual run. The retained dataset should remain available if persistence is part of the chosen baseline. If everything disappears, the data path is probably inside the ephemeral container filesystem.

### Quick Inspection

Open **Console** on `object-db-service`:

```sh
ls -lah /app 2>/dev/null || true
find /app -maxdepth 2 -type f | grep -E 'sqlite|db|json' || true
env | grep -E 'PORT|PROJECT|DB|SQLITE'
```

Use these commands to confirm where durable state lives and whether the expected database file exists.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Client B never receives a change notification | Watch state is not stored per session or is dropped too early | Trace watch registration and fan-out selection |
| UPDATE succeeds but a later GET shows stale data | The in-memory index and the persistent store are updated in different orders | Define one authoritative commit order and document it |
| DELETE removes the row but leaves watch state corrupted | Session watch cleanup is coupled incorrectly to object lifetime | Separate session cleanup from persistent object deletion |
| Data disappears after restart | The database file is written inside a non-persistent layer | Mount a persistent path or place the file under the intended durable directory |
