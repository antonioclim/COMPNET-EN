# S12 — Portainer Guide: Client–Server Messaging with TLS

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `tls-server` | Messaging server with TLS (your code) | **5443 → 5443** |
| `tls-client` | Client (your code or tester-driven) | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Three containers. The server listens on 5443 with TLS; the client connects, authenticates and exchanges messages over the encrypted channel.

## What to Watch in Portainer

### TLS Handshake Verification

Open `tls-server` → **Logs**. Watch for:

1. "Listening on 0.0.0.0:5443" — server is ready.
2. TLS handshake events — cipher negotiated, client certificate verified (if mutual TLS).
3. Application-layer messages after the handshake completes.

If the handshake fails, the log should show the OpenSSL/TLS library error (e.g. "certificate verify failed", "unknown CA").

### Certificate Inspection

Open **Console** on `tls-server`:

```sh
# Verify certificates are mounted correctly
ls -la /app/certs/
openssl x509 -in /app/certs/server.crt -noout -subject -dates
```

### Phase 0 Comparison (Optional)

If you kept the plain-text port (5002) for Phase 0 comparison, Portainer shows both ports in the container detail. You can verify that the unencrypted version is disabled in the E2 configuration.

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Client gets "connection refused" | Server not binding to 0.0.0.0 or TLS context failed to initialise | Server **Logs**: startup traceback |
| Handshake fails with "certificate verify" | CA certificate mismatch or self-signed cert not trusted | Verify client trusts the server's CA; check cert paths |
| Messages encrypted but PCAP shows plaintext | tcpdump captured on loopback inside the container, not on the network interface | Verify capture interface in the tester config |
| Authentication fails | Username/password or token not matching | Server **Logs**: authentication error details |
