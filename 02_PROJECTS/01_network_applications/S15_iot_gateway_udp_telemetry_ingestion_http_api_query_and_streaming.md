# S15 — IoT gateway: UDP telemetry ingestion and an HTTP API for querying and streaming

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C10, C13 | S07, S08, S02
- **Protocol/default ports (E2):** UDP+HTTP: ingest 5515/UDP; API 8080/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S15.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement an IoT gateway that receives telemetry from sensors via UDP and exposes an HTTP API for querying recent values. The model is realistic: simple sensors send short datagrams while the gateway must validate and store efficiently the latest N measurements per sensor.

The telemetry protocol may be JSON or binary but it must be well defined: fields, error codes and size limits. To avoid amplification, the gateway does not automatically respond to every datagram; acknowledgements (if any) are explicit and occur only under certain conditions.

In the demo you follow the full flow: two sensors send values, the gateway collects them and an HTTP client (a simple dashboard) queries `/latest`. The PCAP capture must show both UDP datagrams and HTTP requests to the gateway.

The IoT gateway combines two traffic types with different properties: UDP for ingestion (losses, duplicates) and HTTP/TCP for querying (request/response with status codes). In E1 you define clearly what “accepted measurement” means: mandatory fields, valid ranges, deduplication rules (timestamp/sequence) and per-sensor limits. To avoid amplification effects, it is recommended that UDP ingestion remains predominantly unidirectional and any acknowledgements are rare and conditional (for example only for messages marked as configuration).

## Learning objectives
- Define a UDP telemetry protocol with validation and limits
- Implement a per-sensor bounded queue (ring buffer) for the latest N values
- Expose an HTTP API to query recent data
- Handle UDP loss and duplicate datagrams through application logic
- Build automated tests that send UDP telemetry and verify HTTP responses

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- An **IoT sensor simulator** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **send UDP telemetry (IOT1 plus seq) and validate the HTTP API response**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** UDP+HTTP: ingest 5515/UDP; API 8080/TCP.
- The Flex component must work with the default values (without manual reconfiguration) so that it can be integrated into automated tests.

### Deliverables
- `flex/` directory with sources plus build/run instructions (avoid exotic dependencies where possible).
- `docs/FLEX.md` with:
  - build/run commands
  - the minimal scenario that is demonstrated
  - known limitations
- A minimal automated test (pytest or script) that starts the Flex component and validates the minimal scenario.

### Assessment (clear and measurable)
- The Flex component is assessed in E3 (as part of the E3 score). Its absence limits the maximum possible E3 mark.

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe the difference between UDP (no handshake) and HTTP/TCP in the same demonstration.

### Minimum scenario
- In Mininet, send repeated UDP datagrams from one host to another and capture the traffic.
- In parallel run a simple HTTP server and send `GET` requests to compare handshake and payload.
- Introduce loss on the sensor link and observe missing datagrams in the capture.
- Note that UDP does not retransmit automatically and the application must decide how to treat missing measurements.

### Recommended Wireshark filters
- `udp` — UDP telemetry traffic
- `udp.length < 200` — short datagrams typical of telemetry
- `http.request.method == "GET"` — HTTP requests to the gateway
- `frame contains "sensor_id"` — marker for an identification field in JSON telemetry
- `udp.checksum_bad == 1` — datagrams with an invalid checksum (if present)

### Guiding questions
- What is lost when using UDP instead of TCP and what must be compensated at application level
- How duplicates or out-of-order telemetry can be detected (timestamp, seq)
- How UDP telemetry and HTTP queries can be correlated in PCAP for the same time period
- Which validation policy the gateway applies to avoid storing corrupted data

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The gateway listens on UDP and receives telemetry from sensors in a documented format (mandatory fields: `sensor_id`, `ts`, `value`).
- Validation: refuse malformed datagrams, impossible values (by defined rules) and payload above a limit.
- Local storage: the latest N measurements per sensor in a bounded structure (ring buffer), with N configurable.
- HTTP API exposing at least: list of available sensors and `GET /latest?sensor_id=...` (or equivalent), returning deterministic JSON.
- Automated tests send UDP telemetry then verify via HTTP that data are present and correct.
- UDP telemetry has a deterministic format and starts with ASCII magic `IOT1` plus JSON or TLV; includes mandatory `device_id` and `seq` (monotonic) for deduplication.
- API exposes a streaming endpoint (recommended: SSE) for live metrics, with a documented backpressure policy.

### SHOULD (recommended)
- Deduplication and out-of-order handling: ignore packets older than the last measurement for the same sensor, based on `ts` or `seq`.
- Simple streaming endpoint (SSE or long-poll) that provides near real-time updates to a client.
- Rate limiting per sensor to prevent flooding and keep the demo stable.

### MAY (optional)
- Periodic persistence of recent values to disk for controlled restart.
- Alarms: simple threshold rules generating a logged event when a value crosses a threshold.

## Non-functional requirements
- Separation between control plane (HTTP) and data plane (UDP). Separate logs for ingestion and API.
- Timeouts and limits for HTTP; for UDP limit processing queues and avoid blocking.
- YAML configuration: UDP port, HTTP port, N, validation rules, rate limits.
- Logs include `sensor_id` and refusal reason for invalid datagrams, without logging full payload if it is large.
- Testability: use a deterministic simulator in E2 to reproduce telemetry sequences.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Telemetry protocol specification: format, types, limits, examples and validation rules.
- HTTP API specification: endpoints, JSON responses and error codes.
- Deduplication/out-of-order policy and storage structure (ring buffer).
- Mininet topology: two sensors, gateway, dashboard client.
- E2 capture plan: UDP datagrams and HTTP requests in the same capture.
- Test plan: valid telemetry, invalid telemetry, latest query.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S15 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- The gateway starts in Docker and receives UDP telemetry from `tester`.
- After sending telemetry, `tester` queries the HTTP endpoint and validates the value.
- A capture is produced containing both UDP and HTTP.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes UDP telemetry datagrams and HTTP requests to `GET /latest`.
- The analysis describes which telemetry field is visible in payload and how presence is confirmed in the API.
- Mention the filters used for UDP and for HTTP.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S15.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S15.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S15 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `udp.dstport==5515 && frame contains "IOT1"` | `>= 3` | At least 3 telemetry datagrams (magic IOT1). |
| R2 | `tcp.dstport==8080 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the HTTP API. |
| R3 | `tcp.port==8080 && frame contains "GET /"` | `>= 1` | At least one HTTP query for metrics (GET). |
| R4 | `tcp.port==8080 && frame contains "HTTP/1.1 200"` | `>= 1` | 200 response for the API query. |
| R5 | `udp.dstport==5515 && frame contains "seq"` | `>= 1` | Telemetry contains a sequence field (deduplication/out-of-order handling). |

### Deliverables
- Docker Compose with `iot_gateway` and `tester`.
- Smoke tests (`pytest -m e2`) that send telemetry and validate the HTTP response.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus demonstrable deduplication/out-of-order handling and rate limiting.
- Tests for invalid datagrams, unknown sensor and high telemetry volume.
- Mininet demo: two sensors send values, a client queries and (optional) receives a live stream.
- Documented refactoring and a mini security audit for input validation and limits.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (sensor A) ---\
                  s1 --- h3 (iot_gateway) --- h4 (dashboard)
h2 (sensor B) ---/
```
The link to h2 may have loss to simulate UDP losses.

### Demo steps
- Send telemetry from h1 and h2 and show in logs acceptance and refusal (if any).
- From h4 query `latest` and show the JSON response and recent values.
- In PCAP show UDP datagrams and HTTP requests in the same interval.

## Docker scenario (E2)
### Mandatory requirements for `docker-compose.yml` (E2)

For the PCAP to be **complete** (including internal hops, e.g. proxy→origin or gateway→microservice), `tester` must capture traffic from the **network namespace of the evaluated service** (typically server/proxy/gateway). Recommended deterministic approach:

- `tester` uses:
  - `network_mode: "service:<service_under_test>"` (e.g. `service:server`, `service:proxy`, `service:gateway`)
  - `cap_add: ["NET_ADMIN", "NET_RAW"]` (for `tcpdump`)
  - volume: `./artifacts:/artifacts`
  - env: `PROJECT_CODE=<CODE>` and `PCAP_PATH=/artifacts/pcap/traffic_e2.pcap`
- `tester` starts `tcpdump -i any`, runs `pytest -m e2`, stops the capture then runs `tools/validate_pcap.py`.

The catalogue includes a reference template: `00_common/docker/tester_base/`.

### Services
- **iot_gateway:** receives UDP and exposes HTTP API
- **tester:** simulates sensors, queries the API, captures PCAP

### E2 flow
- Start `iot_gateway` in the background.
- Run `tester` which sends UDP telemetry then issues HTTP requests and writes `artifacts/pcap/traffic_e2.pcap`.
- Stop the stack and verify the capture.

## Notes
- UDP does not guarantee delivery. The project defines explicitly what missing data mean and how they are reported.
- The telemetry format must remain stable after E1 for stable tests.
- For HTTP streaming keep a simple mechanism (SSE/long-poll) and test it deterministically.

### Typical pitfalls
- UDP payload is not validated; a malformed packet can crash the gateway process.
- State is global rather than per sensor; data are mixed between sources and the API becomes incoherent.
- The HTTP API has no limits (rate/size) and can be saturated easily, affecting telemetry ingestion.

### Indicative resources (similar examples)
- [StatsD (classic model: UDP ingestion plus aggregation)](https://github.com/statsd/statsd)
- [Telegraf (collection agent, includes UDP inputs)](https://github.com/influxdata/telegraf)
