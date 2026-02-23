# S13 — gRPC-based RPC service: .proto definition, unary and streaming methods

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C10, C09 | S12, S07, S04
- **Protocol/default ports (E2):** TCP (HTTP/2 gRPC): gRPC 50051/TCP; raw-protobuf 50052/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S13.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement an RPC service using gRPC, starting from a `.proto` definition authored by the team. The project emphasises strict contracts between client and server, controlled serialisation and error handling through gRPC status codes rather than ad hoc conventions.

Both unary calls (request–response) and at least one streaming method are required to discuss flow control and deadlines. The focus is the design of message types and method semantics so that behaviour can be tested automatically.

In the capture, traffic is HTTP/2. In the PCAP analysis you highlight that gRPC requests and responses are encapsulated in HTTP/2 frames and you discuss which elements can be recognised (headers, path, content-type) even though the payload is binary.

gRPC introduces constraints that affect testing: the contract is proto-first, messages are serialised (Protocol Buffers) and timeouts/deadlines are part of the call semantics. For E2 a coherent minimum chain includes one unary method (request/response) and one stream (server-side or bidirectional) with input validation and typed errors. In the demo it is useful to show what HTTP/2 traffic looks like in PCAP and what framing at stream level means without requiring full interpretation of HTTP/2 frames.

## Learning objectives
- Define a `.proto` contract with coherent types and methods
- Implement a gRPC server and a Python test client
- Use deadlines and status codes for errors and timeouts
- Implement and test a streaming method automatically
- Observe gRPC traffic in Wireshark and correlate it with RPC operations

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **raw-protobuf client** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **connect to the raw port and exchange 1 request/response with the PB1 magic value**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP (HTTP/2 gRPC): gRPC 50051/TCP; raw-protobuf 50052/TCP.
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
**Objective:** identify gRPC signatures in HTTP/2 traffic and characteristic headers.

### Minimum scenario
- Run a simple gRPC example (any local demo) and capture the traffic between client and server.
- In Wireshark filter HTTP/2 and identify request headers: `:path`, `content-type`.
- Observe that payload is binary and message lengths can be seen in frames.
- Send a request with a short deadline and observe an error status.

### Recommended Wireshark filters
- `http2` — HTTP/2 traffic
- `http2.header.value contains "application/grpc"` — identify gRPC flows in headers
- `http2.headers.path` — path of the RPC method
- `grpc` — if the gRPC dissector is active it identifies gRPC messages
- `http2.streamid` — separate HTTP/2 streams used by different RPCs

### Guiding questions
- Which headers are typical for gRPC and how can they be recognised in Wireshark
- How does the capture show the difference between unary and streaming methods (stream duration, number of frames)
- What deadlines mean in gRPC and how they appear as an error status
- How an HTTP/2 streamid correlates with an RPC method from `.proto`

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Define a `.proto` file with one service and at least 3 methods: two unary and one streaming (server streaming or bidirectional).
- Implement the gRPC server in Python and a test client that exercises all defined methods.
- Error handling via gRPC status codes (for example INVALID_ARGUMENT, DEADLINE_EXCEEDED) rather than unstructured text messages.
- Timeouts and deadlines: the client sets a deadline and the server respects cancellation at expiry.
- Reproducible run in Docker with `tester` which generates `artifacts/pcap/traffic_e2.pcap` and validates results.
- In addition to gRPC, implement a mandatory **raw TCP endpoint** with Protocol Buffers messages (without gRPC) to validate framing and interoperability.
- Raw messages include an ASCII magic prefix `PB1` (for deterministic detection in PCAP) plus a length prefix.

### SHOULD (recommended)
- gRPC health check (separate service or method) and use it in tests.
- Logging interceptor with an `X-Request-ID` propagated in metadata, correlatable with logs and PCAP.
- Input validation on server: limits, types and deterministic responses to invalid input.

### MAY (optional)
- gRPC reflection for introspection during demo (if the library supports it) without exposure in production.
- TLS for the gRPC channel as an extension, using local certificates.

## Non-functional requirements
- The `.proto` file is the source of truth and is versioned; changes after E1 are documented.
- Timeout and controlled retry only at the client with a limit; the server must not automatically re-execute non-idempotent operations.
- Logs with request identifier and status code, without logging full binary payload.
- YAML configuration: gRPC port, limit parameters (max message size), timeouts.
- Testability: methods are deterministic for fixed input so tests remain stable.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- `.proto` specification: types, methods, semantics of each method and message examples.
- Design decisions: what is unary, what is streaming and why.
- Sequence diagram for a unary method and for the streaming method.
- Mininet topology with one server and two clients to demonstrate simultaneous streams.
- E2 capture plan: HTTP/2 and gRPC filters and what is tracked (headers, streamid).
- Test plan: unary methods, streaming, deadline exceeded.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S13 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- The gRPC server starts in Docker and exposes at least one functional unary method.
- Tester executes the unary method and the streaming method with a small number of messages.
- A short deadline on one call triggers a verifiable error status.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes HTTP/2 traffic with `application/grpc` header and at least two distinct streams.
- The analysis identifies `:path` for one method and explains what `streamid` means for gRPC.
- The observed error status for a deadline is mentioned.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S13.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S13.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S13 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==50051 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the gRPC endpoint (50051). |
| R2 | `tcp.port==50051 && frame contains "PRI * HTTP/2.0"` | `>= 1` | HTTP/2 preface (gRPC without TLS in E2). |
| R3 | `tcp.port==50051 && tcp.len>0` | `>= 5` | Sufficient HTTP/2 traffic (at least 5 data-bearing segments). |
| R4 | `tcp.dstport==50052 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the raw-protobuf endpoint (50052). |
| R5 | `tcp.port==50052 && frame contains "PB1"` | `>= 1` | Raw protobuf message contains the PB1 magic value (an E1 requirement for determinism). |

### Deliverables
- Docker Compose with `grpc_server` and `tester`.
- Smoke tests (`pytest -m e2`) validating one unary call, one streaming call and a deadline case.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including status codes and cancellation on deadline.
- Extended tests for invalid input and two simultaneous streams.
- Mininet demo: two clients run calls in parallel and distinct streamids are shown in Wireshark.
- Documented refactoring and a mini security audit for message limits and input validation.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (grpc_server) --- s1 --- h2 (client A)
                     |
                     +--- h3 (client B)
```
h2 and h3 run calls in parallel to generate different streams.

### Demo steps
- Execute a unary method from h2 and show `:path` and `content-type` in the HTTP/2 capture.
- Execute the streaming method from h3 and show a longer stream with multiple frames.
- Force a deadline exceeded and show the status code in logs.

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
- **grpc_server:** gRPC server built from `.proto`
- **tester:** automated gRPC client, runs tests and captures PCAP

### E2 flow
- Start `grpc_server` in the background.
- Run `tester` which executes the E2 suite and writes `artifacts/pcap/traffic_e2.pcap` via volume.
- Validate capture and stop the stack.

## Notes
- gRPC libraries are accepted for this project. Document versions and keep `.proto` stable after E1.
- Wireshark may not decode full messages if dissectors are not active; the analysis focuses on headers and streams.
- For streaming, small deterministic messages are recommended so tests remain stable.

### Typical pitfalls
- The `.proto` file changes without versioning; client and server become incompatible and errors are hard to interpret.
- Deadlines/cancellation are not respected; streams remain open and tests become unstable.
- Tests use random payload without a fixed seed; results are not reproducible in CI.

### Indicative resources (similar examples)
- [grpc/grpc (official repository, includes examples)](https://github.com/grpc/grpc)
- [gRPC Python examples (in the same repository, subdirectories)](https://github.com/grpc/grpc/tree/master/examples/python)
