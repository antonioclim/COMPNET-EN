# S02 — Portainer Guide: File Transfer Server (FTP-Style)

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `ftp-server` | Control + passive data server (your code) | **5021 → 5021** (control) |
| `tester` | pytest runner + tcpdump | — (internal) |

The passive data-port range (60000–60100) is exposed internally but does not need host-level publishing — the tester connects within the Docker network.

## What to Watch in Portainer

### Dual-Channel Observation

FTP-style transfers use two TCP connections: one for commands (control, port 5021) and one for data (passive, negotiated at runtime). This is where Portainer's log view pays off.

1. **Server logs.** Click `ftp-server` → **Logs**. Watch for:
   - `PASV` command handling — your server announces a data port (e.g. 60042).
   - `RETR` or `STOR` triggering the data connection.
   - Transfer completion and integrity-check results (checksum).

2. **Port verification.** In the container detail for `ftp-server`, check that port 5021 is published. The passive range (60000–60100) should appear under "Exposed Ports" (not "Published Ports") since it is internal to the Docker network.

### Console-Based Quick Tests

Open **Console** on `tester` (or a separate debug container if you have one):

```sh
# Quick control-channel test
nc ftp-server 5021
```

Type `HELO` or your protocol's greeting and verify the response. This is faster than re-running the full E2 suite when debugging a single command.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Tester cannot connect to 5021 | Server not listening or bind failure | Server **Logs**: check for `Address already in use` or traceback |
| Control works but data transfer fails | Passive port not within exposed range | Verify `docker-compose.yml` exposes 60000–60100 |
| Checksum mismatch in tester output | File corruption during transfer | Server **Logs**: check for incomplete writes or encoding issues |
| PCAP shows control traffic but no data channel | Data connection on a different network interface | Verify tcpdump captures on the Compose network, not `lo` |
