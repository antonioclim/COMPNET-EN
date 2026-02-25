# S01 — Portainer Guide: Multi-Client TCP Chat

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `chat-server` | TCP chat server (your code) | **5000 → 5000** |
| `tester` | pytest runner + tcpdump | — (internal) |

Two containers on a shared Compose network. The tester connects to `chat-server:5000` by service name.

## What to Watch in Portainer

### Before Running `make e2`

Open Portainer → **Containers**. Verify nothing is left over from a previous run. If old containers linger, select them and click **Remove** (force-remove if needed). A clean slate prevents "address already in use" errors on port 5000.

### During `make e2`

1. **Container startup order.** Your chat server must be listening before the tester attempts to connect. In Portainer, `chat-server` should show 🟢 running for a few seconds before `tester` starts its pytest run. If `tester` exits immediately (🔴, exit code ≠ 0), open its **Logs** — the first lines will tell you whether the connection was refused (server not ready) or a test assertion failed.

2. **Server logs.** Click `chat-server` → **Logs** → enable auto-refresh. Watch for:
   - Client connection events (multiple concurrent clients in E2).
   - LOGIN, MSG and QUIT command processing.
   - Any Python tracebacks — these are your primary debugging signal.

3. **Tester logs.** Click `tester` → **Logs**. The pytest output appears here: which tests passed, which failed and the assertion details for failures.

### After `make e2`

Check whether `artifacts/pcap/traffic_e2.pcap` was generated. If the tester exited before capturing, the PCAP may be empty or missing. Portainer's exit code for `tester` tells you immediately: exit 0 = success, exit 1 = test failure, exit 2 = crash.

## Debugging Checklist

| Symptom in Portainer | Likely cause | What to check |
|---|---|---|
| `chat-server` exits immediately | Crash on startup (import error, bind failure) | Server **Logs**: Python traceback |
| `tester` exits with code 1 | Test assertion failed | Tester **Logs**: pytest output |
| `tester` exits with code 2 | Tester crashed (not a test failure) | Tester **Logs**: exception trace |
| `chat-server` stays green but tester fails | Server running but not responding correctly | Server **Logs**: is it receiving connections? |
| Both containers green, PCAP empty | tcpdump did not capture on the right interface | Check `docker-compose.yml` network name matches tcpdump filter |

## Tip

Since S01 has only one server port (5000/TCP), the Portainer view is simple. Use the **Console** on `chat-server` to run quick checks while the server is live:

```sh
# Verify the server is listening
ss -tlnp | grep 5000
```
