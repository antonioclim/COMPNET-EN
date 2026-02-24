# S08 — Portainer Guide: Minimal Email System (SMTP + POP3)

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `smtp-server` | SMTP server (your code) | **2525 → 2525** |
| `pop3-server` | POP3 server (E3, may share process) | **2110 → 2110** |
| `tester` | pytest runner + tcpdump | — (internal) |

Two to three containers (SMTP and POP3 may run in the same process or separately). In E2, only SMTP is assessed; POP3 is completed in E3.

## What to Watch in Portainer

### SMTP Session Observation

Open `smtp-server` → **Logs**. Watch for the full command sequence as the tester delivers a message:

```
EHLO tester
MAIL FROM:<sender@test.local>
RCPT TO:<recipient@test.local>
DATA
(message body)
.
QUIT
```

Each command should produce a response code (250, 354, 221) visible in the log.

### Storage Verification

After a successful delivery, open **Console** on `smtp-server`:

```sh
# Check the Maildir-style storage
ls -la /app/mailboxes/recipient/
```

Verify the message file was created with the correct content.

### Dual-Protocol Readiness (E3 prep)

When you add POP3 (E3), both servers must be running. Portainer shows both containers green. Open two log tabs to verify that a message delivered via SMTP appears when retrieved via POP3.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Tester gets "connection refused" on 2525 | SMTP server not started or wrong bind address | Server **Logs**: startup traceback |
| `DATA` command hangs | Dot-terminator detection not working | Check your parser for `\r\n.\r\n` |
| Message stored but with wrong content | Encoding issue or headers mixed into body | **Console**: `cat /app/mailboxes/recipient/<file>` |
| Multiple RCPT TO fails | Single-recipient logic only | Server **Logs**: check RCPT TO handler for list support |
