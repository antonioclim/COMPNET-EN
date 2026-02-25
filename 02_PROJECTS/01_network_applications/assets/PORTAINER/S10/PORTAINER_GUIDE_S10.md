# S10 — Portainer Guide: Network File Synchronisation

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `sync-server` | File-sync server (your code) | **5010 → 5010** |
| `sync-client` | Sync client (your code or tester-driven) | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Three containers. The client connects to the server, exchanges manifests (file lists with hashes) and transfers only the changed files.

## What to Watch in Portainer

### Sync Protocol Observation

Open `sync-server` → **Logs**. Watch for:

1. **Manifest exchange** — server sends its file list; client sends its file list.
2. **Diff calculation** — server (or client) determines which files are new, changed or conflicting.
3. **Transfer** — only the differing files are transferred.
4. **Conflict resolution** — if both sides changed the same file, the resolution strategy kicks in (your configured policy).

### File System Inspection

Open **Console** on `sync-server`:

```sh
# Verify files after sync
ls -la /app/sync-root/
md5sum /app/sync-root/*
```

Compare with the client side (open Console on `sync-client` and run the same commands).

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Manifest exchange succeeds but no files transfer | Diff logic finds no differences | Verify hash computation is consistent across server and client |
| Conflict resolution does not trigger | Test scenario does not modify the same file on both sides | Check tester setup — E2 must include a conflict case |
| Large files cause timeout | No streaming/chunked transfer | Server **Logs**: check for timeout errors on large payloads |
