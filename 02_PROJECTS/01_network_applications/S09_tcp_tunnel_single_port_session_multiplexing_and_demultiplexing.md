# S09 — TCP tunnel on a single port with session multiplexing and demultiplexing

## Metadata
- **Group:** 1
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C09 | S04, S07, S02
- **Protocol/default ports (E2):** TCP: 9000/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S09.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will build an application-level tunnel that transports multiple logical streams over a single TCP connection. The tunnel exposes one public port to the client then routes traffic to two or more internal services (for example an echo service and an HTTP static service).

Multiplexing is performed at protocol level: each frame contains a header with a session identifier and a service identifier plus a payload length. The tunnel must carry interleaved frames from different sessions without losing framing or per-session order.

In the demonstration you emphasise the distinction between one TCP connection and multiple logical sessions. The PCAP capture must show that there is a single TCP stream while the payload contains frames marked with different IDs and responses return to the correct session.

A single-port tunnel forces design of a multiplexing protocol: several logical flows are encapsulated in frames with a session ID and a length prefix then demultiplexed at the destination. The critical aspect is flow control: if one logical stream generates large traffic, the others must not be blocked indefinitely. E1 must describe a simple policy (fairness and per-session limits). In E2, the PCAP must make the multiplexing header recognisable and show two tunnelled services in parallel (for example echo and file transfer) over the same external TCP connection.

## Learning objectives
- Design a binary protocol with a header and a length prefix for multiplexing
- Implement a client–server tunnel with at least two tunnelled services
- Manage logical sessions and demultiplex responses correctly
- Handle protocol errors (invalid frames, unknown service ID) and timeouts
- Build an automated test that validates two sessions active in parallel

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **tunnel client (mux/demux)** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **open sessions (TNL1O), send DATA (TNL1D) and close (TNL1C)**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 9000/TCP.
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
**Objective:** observe that TCP does not preserve message boundaries and motivate binary framing for multiplexing.

### Minimum scenario
- Open a simple TCP connection with netcat and send two consecutive messages without delay then with a delay to observe that segmentation is not guaranteed.
- Capture traffic and use Follow TCP Stream to observe message concatenation.
- Simulate length-prefix framing manually: send a number (length) then send the payload.
- Note in the capture how a message can be reconstructed when segmentation splits it across segments.

### Recommended Wireshark filters
- `tcp.len > 0` — data-bearing segments, relevant for observing concatenation
- `tcp.stream eq 0` — follow the single stream used by the tunnel
- `frame contains "SID"` — marker for a textual header in the manual framing experiment
- `tcp.analysis.segment_overlap` — anomalies that may appear with incomplete captures
- `tcp.flags.push == 1` — PSH segments, useful for a discussion on buffering

### Guiding questions
- Why can you not assume one message per `recv` and how does this appear in the capture
- How does a length prefix help reconstruct messages and what errors appear if the length is incorrect
- What does application-level multiplexing mean and how does it differ from using multiple TCP connections
- What information must a frame header contain to allow demultiplexing

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Binary protocol with framing: each frame is length-prefixed and includes a header with `session_id`, `service_id` and message type (data, open, close, error).
- Single-port tunnel server that can forward to at least two distinct internal services, configurable.
- Tunnel client that can open two logical sessions in parallel over the same connection and send interleaved payload.
- Correct demultiplexing: responses return to the appropriate session and order is preserved within a session.
- Error handling: unknown service ID, invalid frame, payload too large, timeout, all with an error response and logs.
- Deterministic frame format: every frame starts with ASCII magic `TNL1` plus 1 byte type (`O`/`D`/`C`) plus fixed fields (len, stream_id).
- Implement minimal flow control: per-stream buffer limit and deterministic behaviour on overflow.

### SHOULD (recommended)
- Keepalive and dead-connection detection with configurable timeout and controlled reconnect.
- Limit on the number of simultaneous sessions and a deterministic policy on exceedance.
- Per-session statistics: bytes in/out and duration, exposed via a local endpoint or periodic logs.

### MAY (optional)
- Optional per-frame compression negotiated at connection start.
- A compatibility mode that tunnels a full request–response (for example HTTP GET) as an atomic operation.

## Non-functional requirements
- The header and fields are documented with endianness, sizes and allowed values.
- Timeouts for connecting to internal services and for socket reads; avoid blocking on a slow backend.
- Strict length validation: reject frames larger than a configured limit.
- YAML configuration: tunnel port, mapping `service_id → host:port`, limits, timeouts.
- Logs: session open/close events, protocol errors, aggregated statistics.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Frame specification: header layout, message types, error codes and hex examples.
- Description of mapping to internal services and how sessions are closed.
- Sequence diagram for opening a session, data transfer, closing, plus an error case (unknown service).
- Mininet topology with tunnel server, tunnel client and two internal services.
- E2 capture plan: a single TCP stream with frames from two sessions, highlighted in the analysis.
- Test plan: two simultaneous sessions and demultiplexing validation.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S09 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- The tunnel server starts in Docker and can connect to two internal services.
- The tunnel client opens a session to service A and receives a verifiable response.
- The tunnel client opens a second session to service B on the same connection and receives a response.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes a single TCP stream and payload with two different `session_id` values.
- The analysis describes framing and shows a complete frame example with interpreted fields.
- Filters that isolate the stream and the payload-bearing segments are provided.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S09.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S09.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S09 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==9000 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the tunnel. |
| R2 | `tcp.port==9000 && frame contains "TNL1O"` | `>= 1` | OPEN frame (magic TNL1 plus type O). |
| R3 | `tcp.port==9000 && frame contains "TNL1D"` | `>= 1` | DATA frame (magic TNL1 plus type D). |
| R4 | `tcp.port==9000 && frame contains "TNL1C"` | `>= 1` | CLOSE frame (magic TNL1 plus type C). |
| R5 | `tcp.port==9000 && tcp.len>0` | `>= 5` | Sufficient payload traffic for multiplexing (at least 5 data-bearing segments). |

### Deliverables
- Docker Compose with `tunnel_server`, two internal services and `tester`.
- Smoke tests (`pytest -m e2`) that verify two distinct sessions and correct responses.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including error handling and payload limits.
- Tests for invalid frames, unknown service ID and controlled reconnection.
- Mininet demo where internal services are on distinct hosts and multiplexing is shown in Wireshark.
- Documented refactoring and a mini security audit for binary input and limits.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (tunnel_server) --- s1 --- h2 (tunnel_client)
                        |
                        +--- h3 (service A)
                        +--- h4 (service B)
```
The tunnel is a single TCP stream between h2 and h1 while h1 has separate connections to h3 and h4.

### Demo steps
- Open two logical sessions and send alternating messages to A and B.
- Show in the PCAP that there is a single TCP stream but the payload contains frames with different `session_id` values.
- Stop service B and show an error response for session B without stopping session A.

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
- **tunnel_server:** tunnel server with mapping `service_id → backend`
- **service_a:** internal service A (echo or simple request–response)
- **service_b:** internal service B (distinct from A)
- **tester:** opens sessions, sends frames, validates responses and captures PCAP

### E2 flow
- Start `tunnel_server` and the internal services.
- Run `tester` which creates two sessions in parallel and writes `artifacts/pcap/traffic_e2.pcap` via volume.
- Validate the capture and stop the stack.

## Notes
- Internal services may be minimal; the focus is framing and multiplexing, not backend business logic.
- The protocol is binary. In E1 include a field table and a frame example in hex.
- Encryption is not required. If added justify it and keep the solution testable.

### Typical pitfalls
- The length prefix is computed in characters (UTF‑8) rather than bytes; the tunnel loses synchronisation with non‑ASCII payload.
- A single shared global buffer for all sessions creates interleavings that corrupt per-session traffic.
- Closing a session closes the entire tunnel connection even though other sessions remain active.

### Indicative resources (similar examples)
- [Yamux (stream multiplexing, concept compatible with this project)](https://github.com/hashicorp/yamux)
- [Chisel (TCP/UDP tunnel over a single transport, practical example)](https://github.com/jpillora/chisel)
