# S01 — Multi-client TCP chat with a text protocol and presence

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C09 | S03, S04, S02
- **Protocol/default ports (E2):** TCP: 5000/TCP (configurable; the default is used in automated tests).

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S01.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will build a TCP-based chat server that maintains active sessions for multiple users and applies an application protocol defined by the team. The protocol remains sufficiently small to be implemented fully within the semester while being strict enough not to rely on implicit TCP behaviour.

The core challenge is framing: TCP is a byte stream so message boundaries must be designed and tested explicitly. The server must process concatenated commands in the same segment and fragmented commands split across multiple segments without losing protocol synchronisation.

The system manages user presence (join, left), private messages and broadcast, together with observability: coherent logs, predictable errors and explicit payload limits so that a Mininet demonstration can highlight differences between fast clients and slow clients.

In practice, the project behaves as a protocol-design exercise: the team must define command syntax, validation rules and state transitions (from connected to authenticated then to an active session). In E2, load behaviour is assessed explicitly: clients that send messages quickly, clients that read slowly and situations in which multiple commands arrive in the same TCP segment. The solution becomes robust only if parsing is incremental and the server maintains a per-connection buffer without assuming that a single `recv()` corresponds to a single message.

## Learning objectives
- Define a text protocol with framing and error codes
- Implement a concurrent TCP server for at least 10 clients
- Manage sessions and state (authentication, user list and disconnect)
- Build an automated smoke test that exercises the critical end-to-end path
- Correlate application behaviour with evidence from a PCAP capture

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **cross-platform CLI client** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **connect, perform LOGIN, send MSG and interpret EVENT/LIST/ERROR**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 5000/TCP (configurable; the default is used in automated tests).
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
**Objective:** observe TCP segmentation and the impact of framing (concatenated or fragmented messages) on a simple chat session.

### Minimum scenario
- Start a Mininet topology with 1 server and 2 clients and run a netcat server on the server host.
- Start capture with `tshark` on the switch interface and send two consecutive commands from the same client without delay.
- Repeat the send with a longer message (several hundred bytes) to increase the likelihood of fragmentation.
- Save the capture locally and note where the chosen delimiter (for example newline) appears in the payload.

### Recommended Wireshark filters
- `tcp.flags.syn == 1` — connection initiation for each client
- `tcp.len > 0` — segments that carry data, excluding empty ACKs
- `tcp.stream eq 0` — follow a full flow (Follow TCP Stream)
- `frame contains "LOGIN"` — identify an application command in the payload
- `tcp.analysis.retransmission` — retransmissions that occur on lossy links

### Guiding questions
- Under what conditions do two application commands appear in the same TCP segment and how does that look in Follow Stream
- What happens when a message exceeds the MSS and is fragmented: does the delimiter remain visible in a single segment or can it be split
- What is the difference between a graceful close (FIN) and an abort (RST) in the observed capture
- How do you distinguish simultaneous client connections (source ports, distinct streams)

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Authentication with a unique `username`. On duplicates return a deterministic error without disconnecting other clients.
- Minimum commands: `LOGIN`, `MSG <user|*> <text>`, `LIST`, `QUIT` with a response for each command (OK or ERR).
- Push notifications to clients: `EVENT user_joined` and `EVENT user_left`.
- A concurrent server that can support at least 10 clients connected simultaneously and routes messages correctly.
- Server-side logs for connection, authentication, commands, errors and disconnects with levels and timestamps.
- The application protocol must include a **version** field (e.g. `PROTO 1`) and explicit message delimitation (newline or length).
- Parsing must accept messages **concatenated in the same buffer** (e.g. two commands in the same `recv`) and handle partial frames (fragmentation).
- Strict identity rules: username 1–16 characters `[A-Za-z0-9_-]` (otherwise ERR).

### SHOULD (recommended)
- Rate limiting per user for `MSG` and explicit handling of limit exceedance.
- Rooms with `JOIN`, `LEAVE` commands and room-scoped message routing.
- An MOTD message on login and a negotiated list of capabilities.

### MAY (optional)
- Minimal persistence of the last N messages per user for debugging and demonstration.
- A compatibility mode for slow clients (buffer limit and backpressure).

## Non-functional requirements
- Explicit framing: delimiter or length prefix, documented in E1 and implemented symmetrically by client and server.
- Timeouts for network operations and inactive sessions, configurable in `config/config.yaml`.
- Per-message payload limit and input validation (unknown command, missing arguments, text too long).
- Controlled concurrency: protect concurrent access to the user list and message routing.
- Handling of abrupt disconnects: clean up state, send presence notifications and avoid resource leaks.
- Observability: structured logs, no `print` plus a configurable log level.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Protocol specification: commands, syntax, examples, error codes and response messages.
- Framing decision and justification based on Phase 0 observations.
- State diagram for server and client (at least CONNECTED, AUTH, ACTIVE and CLOSED).
- Sequence diagram for login, broadcast message, private message and quit.
- Proposed Mininet topology and demo scenario (simultaneous traffic, slow link).
- E2 capture plan: which conversation is captured and which fields are checked in the PCAP.
- Test plan: smoke test for E2 and edge cases for E3.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S01 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- The server starts in Docker and accepts TCP connections.
- A client can authenticate and send a broadcast message to at least one other client.
- `QUIT` closes the session and produces a presence event.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes the TCP handshake, a `LOGIN`, a `MSG` and a `QUIT`.
- The analysis highlights the chosen framing and shows an example of a complete message in the payload.
- The analysed stream and the ports used are stated.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S01.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S01.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S01 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5000 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Connection initiation to the server (SYN). |
| R2 | `tcp.srcport==5000 && tcp.flags.syn==1 && tcp.flags.ack==1` | `>= 1` | SYN‑ACK response from the server. |
| R3 | `tcp.port==5000 && frame contains "LOGIN"` | `>= 1` | A LOGIN command is transmitted (correct framing). |
| R4 | `tcp.port==5000 && frame contains "MSG "` | `>= 1` | At least one MSG message is transmitted. |
| R5 | `tcp.port==5000 && frame contains "EVENT "` | `>= 1` | The server sends at least one push event (presence). |
| R6 | `tcp.port==5000 && (tcp.flags.fin==1 || tcp.flags.reset==1)` | `>= 1` | Session closure (FIN or documented RST). |

### Deliverables
- Functional Docker Compose with server and `tester`.
- Smoke tests (`pytest -m e2`) that run login, message and quit and validate responses.
- `artifacts/pcap/traffic_e2.pcap` produced automatically by `tester` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented and documented.
- Extended tests for private messages, listing and error cases (invalid input, payload too large).
- Reproducible Mininet demo showing differences between a fast client and a client with delay or loss.
- Documented refactoring and a mini security audit (input validation, timeouts and limits).
- Final documentation that correlates logs, PCAP and observed behaviour.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (server) ---\
               s1 --- h4 (slow client)
h2 (client) ---/
h3 (client) ----
```
The link to h4 has delay and optionally loss. Other links keep default parameters.

### Demo steps
- Start h2 and h3 as clients and send simultaneous broadcast messages.
- Start h4 with delay and show the difference in delivery order and timing, confirmed by timestamps in the logs.
- In Wireshark show a stream and a complete message with correct delimitation.

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
- **chat_server:** TCP chat server, configured from `config.yaml`
- **tester:** E2 smoke tests, generates PCAP in `/artifacts`

### E2 flow
- Build images and start the server in the background.
- Run `tester` which executes tests and captures the traffic between `tester` and `chat_server`.
- Save `artifacts/pcap/traffic_e2.pcap` via volume and verify with `tools/validate_pcap.py`.

## Notes
- The protocol remains text-based but framing must be treated as a transport-level problem rather than a UI detail.
- Solutions that assume one message per `recv` or one message per `send` are not accepted.
- TLS is not required here; if added use a standard library and document the negotiation.

### Typical pitfalls
- Parsing under the assumption “one `recv()` = one message” causes desynchronisation when multiple commands arrive in the same segment.
- Missing payload limits and timeouts lead to stalls with slow clients or abandoned connections.
- Broadcast without concurrency protection (the client list changes during iteration) produces errors under abrupt disconnects.

### Indicative resources (similar examples)
- [Chat-Room (multi-client client/server)](https://github.com/al-ghaly/Chat-Room)
- [Multithreaded Client-Server Chat Application](https://github.com/Kunal30/Multithreaded-Client-Server-Chat-Application)
