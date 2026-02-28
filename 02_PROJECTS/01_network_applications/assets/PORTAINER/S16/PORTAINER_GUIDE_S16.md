# S16 — Portainer Guide: Collaborative Text Editing

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `editor-server` | Collaborative editor service (your code) | **5016 → 5016** |
| `client-a` | Lock owner in the deterministic scenario | — (internal) |
| `client-b` | Competing reader/editor | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Three to four containers. Portainer becomes useful as soon as the lock conflict is exercised because you can watch the lock owner and the competing client in parallel.

## What to Watch in Portainer

### Lock Exclusivity

Open **three** tabs:

- Tab A: `editor-server` → **Logs** — lock acquisition, version increments and watcher notifications
- Tab B: `client-a` → **Logs** — successful `LOCK` and `SAVE`
- Tab C: `client-b` → **Logs** — refused competing `LOCK`

Run `make e2` and confirm:

1. `client-a` obtains the document lock.
2. `client-b` is refused with a deterministic error such as `ERR_LOCKED`.
3. The server logs a version increment after `SAVE`.
4. A post-save update is emitted to watchers or readers.

### Document Persistence

Open **Console** on `editor-server`:

```sh
ls -la /app/documents/
sed -n '1,40p' /app/documents/notes.txt
```

After `SAVE`, verify that the file on disk matches the version reported in the log.

### Abrupt Disconnect Test

Stop `client-a` from Portainer while it owns a lock. The server log should show automatic cleanup. Start `client-a` again and verify that the document is no longer locked indefinitely.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| `client-b` acquires the same lock | Lock table updates are not atomic | Inspect the server log around the two `LOCK` requests |
| Save succeeds but watchers see nothing | Notification fan-out is not triggered after version increment | Check whether watchers are registered before the save |
| Multi-line documents corrupt the protocol | Payload framing collides with command framing | Use a length-prefixed payload and log the parsed length |
| Lock remains after disconnect | Cleanup only happens on `UNLOCK` | Add disconnect hooks in the session manager |
