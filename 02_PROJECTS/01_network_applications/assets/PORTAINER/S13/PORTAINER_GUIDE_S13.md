# S13 — Portainer Guide: gRPC-Based RPC Service

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `grpc-server` | gRPC server (.proto-defined service) | **50051 → 50051** |
| `raw-protobuf-server` | Raw protobuf comparison server | **50052 → 50052** |
| `tester` | pytest runner + tcpdump | — (internal) |

Three containers. Two servers on different ports — one speaks full gRPC (HTTP/2 framing), the other uses raw protobuf over TCP for comparison.

## What to Watch in Portainer

### Dual-Server Observation

Open two log tabs:
- **Tab A:** `grpc-server` → **Logs** — unary and streaming method invocations
- **Tab B:** `raw-protobuf-server` → **Logs** — raw protobuf messages received and decoded

During `make e2`, watch for:
- Unary calls: request in, response out (one log line each).
- Server-streaming calls: one request in, multiple responses out.
- Client-streaming calls: multiple requests in, one response out.

### Port Distinction

In the **Containers** view, verify:
- `grpc-server` publishes **50051** (standard gRPC).
- `raw-protobuf-server` publishes **50052** (custom protocol).

This distinction is important for the PCAP analysis: port 50051 traffic uses HTTP/2 framing; port 50052 uses your custom binary framing.

### Proto Verification

Open **Console** on `grpc-server`:

```sh
# Verify the compiled proto files are present
ls /app/proto/
python3 -c "import your_service_pb2; print('Proto loaded')"
```

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| gRPC client gets "unavailable" | Server not started or wrong port | Server **Logs**: check for startup errors |
| Streaming method returns only one result | Server yields once instead of looping | Check your streaming generator/iterator logic |
| Raw protobuf server receives garbled data | Length-prefix framing mismatch | Verify frame header (message length) matches on both sides |
| PCAP does not decode HTTP/2 on 50051 | Wireshark needs "Decode As → HTTP2" for non-standard ports | Not a Portainer issue — adjust Wireshark settings |
