# S03 — Portainer Guide: HTTP/1.1 Raw-Socket Server

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `http-server` | Raw-socket HTTP/1.1 server (your code) | **8080 → 8080** |
| `tester` | pytest runner + tcpdump | — (internal) |

## What to Watch in Portainer

### Server Readiness

Your HTTP server parses raw bytes — no framework, no safety net. Common startup failures include socket-bind errors and malformed response formatting that causes the tester to fail immediately.

1. **Server logs.** Watch for "listening on 0.0.0.0:8080" (or your equivalent). If the container exits, the log shows the traceback.

2. **Live request observation.** Keep the server's **Logs** tab open with auto-refresh. As the tester sends GET requests for static files, you should see each request logged with its path, status code and response size.

### Console Testing

Open **Console** on `http-server`:

```sh
# Verify the server responds to a minimal request
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 8080
```

This tests your parser without involving the full tester suite.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Tester gets connection refused | Server crashed or did not bind to 0.0.0.0 | Verify bind address is not `127.0.0.1` (must be reachable from other containers) |
| Tester gets 400 Bad Request | Response formatting error (missing `\r\n\r\n`) | Server **Logs** + manual curl test |
| Static files return 404 | Working directory mismatch inside the container | **Console**: `ls /app/static/` (or your file root) |
