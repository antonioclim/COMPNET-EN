# S15 — Portainer Guide: IoT Gateway (UDP Telemetry + HTTP API)

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

## Your E2 Stack

| Container | Role | Published Ports |
|---|---|---|
| `iot-gateway` | UDP ingest + HTTP API (your code) | **5515 → 5515/udp**, **8080 → 8080** |
| `sensor-sim` | Simulated sensor (sends UDP datagrams) | — (internal) |
| `tester` | pytest runner + tcpdump | — (internal) |

Three to four containers. The gateway exposes two protocols on two ports: UDP for telemetry ingestion and HTTP for querying stored data.

## What to Watch in Portainer

### Dual-Protocol Observation

Open **two** Portainer tabs:

- **Tab A:** `iot-gateway` → **Logs** — shows both UDP ingestion events and HTTP API requests in a single stream
- **Tab B:** `sensor-sim` → **Logs** — shows datagrams sent (with sequence numbers and sensor IDs)

Run `make e2`. Correlate:
- sensor-sim sends datagram with `sensor_id=IOT1, seq=1` → gateway log shows "accepted: IOT1 seq=1"
- tester queries `GET /latest?sensor=IOT1` → gateway log shows "API: 200 OK, value=22.5"

### Ingestion Rate and Validation

The gateway must validate incoming datagrams (mandatory fields, value ranges, deduplication). In the gateway log, watch for:

- **Accepted** measurements (valid format, within range, unique sequence).
- **Rejected** measurements (missing fields, out of range, duplicate seq).
- **Rate-limited** measurements (if per-sensor rate limits are configured).

### Published Ports Check

In the container detail for `iot-gateway`, verify both ports are published:
- `5515/udp` — telemetry ingestion
- `8080/tcp` — HTTP API

If only one appears, check your `docker-compose.yml` — UDP ports require explicit `protocol: udp` in the port mapping.

### Console-Based Quick Test

Open **Console** on `tester` (or a debug container):

```sh
# Send a test datagram
echo '{"sensor_id":"IOT1","seq":99,"value":42.0}' | nc -u iot-gateway 5515

# Query the API
curl -s http://iot-gateway:8080/latest?sensor=IOT1 | python3 -m json.tool
```

## Debugging Checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Gateway receives nothing on 5515 | UDP port not published or wrong protocol in compose | Verify `"5515:5515/udp"` in `docker-compose.yml` |
| Datagrams received but all rejected | Validation rules too strict or field names mismatched | Gateway **Logs**: check rejection reason per datagram |
| HTTP API returns empty results | Ingested data not stored or wrong sensor_id in query | **Console**: query with a known sensor_id from the sensor-sim log |
| PCAP shows TCP but no UDP | tcpdump filter excludes UDP | Check capture command: should include `udp port 5515` |
| Rate-limiting triggers too early | Per-sensor limit set too low for E2 test rate | Check config: `max_rate_per_sensor` vs sensor-sim send interval |
