# S18 — Resource reservation with holds, leases, wait queue and consistency

## Metadata
- **Group:** 1
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C09 | S03, S04, S02
- **Protocol/default ports (E2):** TCP: 5018/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S18.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a reservation service for named resources such as laboratory devices, rooms or shared execution slots. Clients connect to a central server, inspect resource availability, request a temporary hold for a time interval, confirm a reservation, modify or cancel their own reservations and observe updates from other clients.

The project is pedagogically strong because it introduces authoritative time semantics, interval overlap checks, short-lived holds, lease expiry and a deterministic waiting model. Unlike the existing catalogue items, it is neither simple file transfer nor pure message routing. It is a protocol-design exercise centred on concurrency, fairness and consistent shared state.

The most important design decision is that the server is the only authority for time and reservation validity. Clients do not negotiate directly and do not decide whether intervals overlap. This keeps the problem sharply focused on network protocol, state transitions and observable server decisions.

## Learning objectives
- Specify interval-based reservation operations with clear ownership and authority rules
- Implement temporary holds with automatic expiry and promotion to confirmed reservations
- Prevent overlapping reservations through deterministic server-side validation
- Notify interested clients about holds, confirmations, cancellations and expiry
- Build automated tests for conflict, timeout and reconnect scenarios

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability rather than only for the team's own client and practise integration across different languages and stacks.

### Proposed component
- A **minimal client** implemented in a language **other than Python** (for example C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates only through the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end in one short scripted scenario covering the project's core control messages.
- Any shortcut such as hardcoding, protocol bypass or direct access to the server's internal files is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 5018/TCP.
- The Flex component must work with the default values without manual reconfiguration so that it can be integrated into automated tests.

### Deliverables
- `flex/` directory with sources plus build and run instructions.
- `docs/FLEX.md` with:
  - build and run commands
  - the minimal scenario that is demonstrated
  - known limitations
- A minimal automated test or script that starts the Flex component and validates the minimal scenario.

### Assessment
- The Flex component is assessed in E3 as part of the E3 score. Its absence limits the maximum possible E3 mark.

## Phase 0 — Study and observation (Wireshark)
**Objective:** observe a small lease-based coordination workflow and identify the network signatures of acquisition, renewal and expiry.

### Minimum scenario
- Run Redis for observation only and use a short lease command pattern such as `SET key value NX EX 15` followed by `TTL` and `DEL`.
- Capture one successful acquisition and one failed competing acquisition.
- Observe what changes when the lease is renewed or allowed to expire.
- Translate those observations into a cleaner reservation-specific protocol.

### Recommended Wireshark filters
- `tcp.port == 6379`
- `frame contains "SET"`
- `frame contains "TTL"`
- `frame contains "DEL"`
- `tcp.len > 0`

### Guiding questions
- Why must the server rather than the client decide whether a hold is still valid
- What explicit fields are needed for interval reservations: resource, start, end, owner and hold expiry
- How should the service distinguish a temporary hold from a confirmed reservation
- What evidence in PCAP would demonstrate a refused overlapping request

### Mandatory deliverable
- `docs/E1_phase0_observations.md` with the observed lease semantics and the design choices adopted for the final protocol.

## Functional requirements
### MUST (mandatory)
- The server accepts TCP connections and requires a client identifier through `HELLO` or an equivalent command.
- Supported operations: `LIST`, `HOLD <resource> <start> <end>`, `CONFIRM <hold_id>`, `CANCEL_HOLD <hold_id>`, `MODIFY <reservation_id> ...`, `DELETE <reservation_id>` and `WATCH <resource>` or equivalent.
- The server validates interval consistency and refuses overlaps deterministically.
- A hold has a finite server-defined lifetime and expires automatically if not confirmed.
- Active holds belonging to a disconnected client are released automatically.
- Confirmed reservations are owned and may be modified or deleted only by their owner unless E1 documents an administrator role.
- Notifications are emitted for hold creation, hold expiry, reservation confirmation, modification and deletion.

### SHOULD (recommended)
- A waiting queue for requests that cannot be served immediately, with deterministic ordering documented in E1.
- Explicit server timestamps in responses so that client logs can be correlated with the authoritative timeline.
- Query by resource and by interval for debugging and verification.

### MAY (optional)
- Priority classes for resources provided the ordering rule remains deterministic.
- Bulk listing of all reservations for a given day or laboratory.

## Non-functional requirements
- Time format, timezone assumptions and the canonical overlap rule must be fixed in E1.
- The service must not depend on local client clocks for correctness.
- The server must log state transitions clearly: hold created, hold expired, reservation confirmed, reservation changed and reservation deleted.
- Limits for maximum hold lifetime, maximum future interval and maximum number of active holds per client must be documented.
- The system must remain deterministic under concurrent requests from at least two clients.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`.

- Protocol specification for listing, holding, confirming, cancelling, modifying, deleting and watching.
- Exact interval representation and overlap rule with at least three examples.
- State diagram for `AVAILABLE -> HELD -> RESERVED -> RELEASED`.
- Sequence diagram for one successful confirmation and one refused overlap.
- Mininet topology with one server and two competing clients.
- E2 capture plan showing a refused overlap and one expiry or release event.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command, recommended `make e2`, that runs the E2 scenario end-to-end and validates the capture.

### Minimum demonstrable outcome
- Client A acquires a hold for one resource and interval.
- Client B attempts an overlapping hold and is refused deterministically.
- Client A confirms the hold into a reservation.
- A second scenario shows hold expiry or explicit cancellation with visible notification.

### PCAP requirements
- The capture includes one `HOLD`, one refusal for overlap and one `CONFIRM`.
- The capture includes either `EXPIRED`, `RELEASED` or `CANCELLED` for a temporary hold.

### Automatic PCAP criteria (E2)
- Official rules: `tools/pcap_rules/S18.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S18.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S18 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5018 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the reservation service. |
| R2 | `tcp.port==5018 && frame contains "HOLD"` | `>= 1` | At least one hold request appears in payload. |
| R3 | `tcp.port==5018 && (frame contains "BUSY" || frame contains "OVERLAP" || frame contains "REJECT")` | `>= 1` | Overlapping request is refused deterministically. |
| R4 | `tcp.port==5018 && frame contains "CONFIRM"` | `>= 1` | Promotion from hold to reservation is visible. |
| R5 | `tcp.port==5018 && (frame contains "EXPIRED" || frame contains "RELEASED" || frame contains "CANCELLED")` | `>= 1` | Hold release semantics are observable. |

### Deliverables
- Docker Compose with `reservation_service` and `tester` plus optional interactive clients.
- Smoke tests that validate overlap refusal and successful confirmation.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including automatic release on disconnect.
- Tests for malformed intervals, unauthorised modification and wait-queue promotion if implemented.
- Mininet demo with two competing clients on separate hosts.
- Documented refactoring and a short robustness review centred on race conditions and time handling.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (client A) --- s1 --- h3 (reservation_service)
                                     +--- h2 (client B)
```

### Demo steps
- h1 requests a hold for `lab-pc-01` for a fixed interval.
- h2 requests an overlapping hold and receives a refusal.
- h1 confirms the reservation.
- h1 later disconnects while holding another interval and the server releases it automatically.

## Docker scenario (E2)
### Mandatory requirements for `docker-compose.yml` (E2)

For the PCAP to be **complete** including internal hops, `tester` should capture traffic from the **network namespace of the evaluated service**. Recommended deterministic approach:

- `tester` uses:
  - `network_mode: "service:<service_under_test>"`
  - `cap_add: ["NET_ADMIN", "NET_RAW"]` for `tcpdump`
  - volume: `./artifacts:/artifacts`
  - environment variables such as `PROJECT_CODE=<CODE>` and `PCAP_PATH=/artifacts/pcap/traffic_e2.pcap`
- `tester` starts `tcpdump -i any`, runs `pytest -m e2`, stops the capture then runs `tools/validate_pcap.py`.

The catalogue already includes a reference template in `00_common/docker/tester_base/`.

### Services
- **reservation_service:** main service under test
- **tester:** drives the E2 scenario, captures PCAP and validates the deterministic outcome

### E2 flow
- Start the service in the background.
- Run `tester`, which performs the scripted scenario and writes `artifacts/pcap/traffic_e2.pcap`.
- Validate the capture and keep the generated artefacts for E2 and E3 documentation.

## Notes
- Persistence is optional. A purely in-memory implementation is acceptable if the semantics are correctly specified and observable.
- The point of the project is not calendar UI. A console client is entirely acceptable.
- Portainer may be used for service inspection and log reading, but it is not part of the assessment contract.

### Typical pitfalls
- Overlap logic is implemented incorrectly at interval boundaries.
- Expired holds are checked lazily and remain visible long after they should disappear.
- Client clocks are used to decide validity, which produces inconsistent behaviour across hosts.
