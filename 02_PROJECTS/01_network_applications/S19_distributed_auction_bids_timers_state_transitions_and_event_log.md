# S19 — Distributed auction with bids, timers, state transitions and an event log

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C09 | S03, S04, S02
- **Protocol/default ports (E2):** TCP: 5019/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S19.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a server-based auction platform in which connected clients may publish items, watch active auctions, place bids and receive live updates on state changes. The auction server is the sole authority for accepted bids, current top value, deadline expiry and final winner selection.

The project is stronger than a generic "chat-like" exercise because it forces the team to define a proper state machine, server-authoritative timing and deterministic tie-breaking. It remains sufficiently network-centred to integrate naturally into COMPNET-EN: the most important phenomena are command validation, notification fan-out, event ordering and robustness under competing requests.

This is not a duplicate of the existing pub/sub broker. It shares notification mechanics but adds value semantics, expiry, event logging and authoritative state transitions. It therefore deserves to be treated as a separate network-application project.

## Learning objectives
- Define an application protocol for listing auctions, publishing items and placing bids
- Implement server-authoritative timers and deterministic tie-breaking
- Broadcast state transitions such as outbid, closed and winner notifications
- Maintain an event log that can be used to justify state at the end of an auction
- Build automated tests for valid bid, refused low bid and expired-auction behaviour

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability rather than only for the team's own client and practise integration across different languages and stacks.

### Proposed component
- A **minimal client** implemented in a language **other than Python** (for example C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates only through the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end in one short scripted scenario covering the project's core control messages.
- Any shortcut such as hardcoding, protocol bypass or direct access to the server's internal files is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 5019/TCP.
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
**Objective:** observe a real-time update channel and identify how event fan-out differs from ordinary request-response traffic.

### Minimum scenario
- Run an observation-only live-update service such as a small WebSocket or Server-Sent Events demo.
- Connect two clients to the same stream.
- Emit a series of timestamped events from a producer.
- Capture traffic and identify the observable markers that show one producer and multiple receivers.

### Recommended Wireshark filters
- `tcp.len > 0`
- `websocket` or `http` depending on the chosen observation service
- `frame contains "event"`
- `frame.time_delta_displayed > 1` to spot timer gaps or periodic updates

### Guiding questions
- How can a capture show that the same logical event was delivered to more than one client
- Why must the auction deadline be server-authoritative rather than client-driven
- What information is required to explain the accepted winning bid at the end
- Which event types should your own protocol make explicit: opened, top bid, outbid, closed and winner

### Mandatory deliverable
- `docs/E1_phase0_observations.md` with short answers and the design choices derived from the observation.

## Functional requirements
### MUST (mandatory)
- The server accepts TCP connections and requires unique client identifiers.
- Supported operations: `LIST`, `SELL <item> <starting_price> <duration>`, `BID <auction_id> <amount>`, `WATCH <auction_id>` and equivalent notification messages.
- The server maintains the state of each auction including owner, starting price, current highest bid, bidder and deadline.
- A bid is accepted only if the auction is open and the amount is strictly greater than the current highest accepted value.
- Auction closure is automatic and decided by the server clock.
- The server emits notifications for new auctions, accepted bids, refused bids where appropriate, outbid clients, closure and winner selection.
- An append-only event log is kept for each auction and is referenced in E3 documentation.

### SHOULD (recommended)
- Deterministic tie-breaking if two bids arrive with the same value close together, documented explicitly in E1.
- Reserve price or minimum increment if the team wishes to make bidding rules richer.
- Query for auction history or recent events.

### MAY (optional)
- Settlement acknowledgement after closure.
- Simple auction categories or search by owner.

## Non-functional requirements
- Monetary values must use a representation that avoids floating-point ambiguity.
- Time representation, deadline precision and tie-breaking rule must be fixed in E1.
- Logs must distinguish user intent from accepted state transitions.
- Limits for maximum active auctions per client and maximum auction duration must be documented.
- The system must remain deterministic under competing bids sent within a short interval.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`.

- Protocol specification for item creation, bid submission, watch registration and notifications.
- State machine for `OPEN -> CLOSED -> SETTLED` or the equivalent chosen model.
- Exact rule for deadline handling and for equal-value bids.
- Sequence diagram for one accepted bid and one refused bid after closure or below the top value.
- Mininet topology with one seller, two bidders and one auction server.
- E2 capture plan showing creation, bidding and closure.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command, preferably `make e2`, that runs the E2 scenario end-to-end and validates the capture.

### Minimum demonstrable outcome
- A seller publishes one auction item.
- Bidder A places a valid bid.
- Bidder B places a higher bid and the service updates the current top value.
- The auction closes automatically and the service announces the winner.

### PCAP requirements
- The capture includes item publication, at least two bids and a closure event.
- The capture shows a notification such as `OUTBID`, `TOP_BID`, `CLOSED` or `WINNER`.

### Automatic PCAP criteria (E2)
- Official rules: `tools/pcap_rules/S19.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S19.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S19 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5019 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the auction service. |
| R2 | `tcp.port==5019 && (frame contains "SELL" || frame contains "OPEN")` | `>= 1` | Auction creation or open-state announcement. |
| R3 | `tcp.port==5019 && frame contains "BID"` | `>= 2` | At least two bids are visible in payload. |
| R4 | `tcp.port==5019 && (frame contains "OUTBID" || frame contains "TOP_BID")` | `>= 1` | Competitive update to the highest bid is visible. |
| R5 | `tcp.port==5019 && (frame contains "CLOSED" || frame contains "WINNER")` | `>= 1` | Automatic closure and winner reporting are observable. |

### Deliverables
- Docker Compose with `auction_service` and `tester` plus optional bidder clients.
- Smoke tests that create an auction, place competing bids and verify the final winner.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including event-log persistence for the running service lifetime.
- Tests for refused low bid, refused late bid and tie-breaking if implemented.
- Mininet demo with one seller and two bidders on separate hosts.
- Documented refactoring and a short review of timer handling and ordering guarantees.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (seller) ---                s1 --- h4 (auction_service)
h2 (bidder A) --/
                                   +--- h3 (bidder B)
```

### Demo steps
- h1 publishes one item with a short auction duration.
- h2 and h3 place bids in sequence.
- The server notifies the current top bidder and the outbid client.
- The auction closes automatically and the winner is announced.

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
- **auction_service:** main service under test
- **tester:** drives the E2 scenario, captures PCAP and validates the deterministic outcome

### E2 flow
- Start the service in the background.
- Run `tester`, which performs the scripted scenario and writes `artifacts/pcap/traffic_e2.pcap`.
- Validate the capture and keep the generated artefacts for E2 and E3 documentation.

## Notes
- A real payment system is not required. The project is about network coordination and state, not financial processing.
- Persistent storage is optional unless the team chooses to extend the event log beyond process lifetime.
- Portainer is helpful for observing logs and container restarts but is not required.

### Typical pitfalls
- Bid value comparison uses floating-point values and creates ambiguous ordering.
- The deadline is checked only when a new bid arrives rather than by a proper timer or deterministic comparison on receive.
- Equal bids are accepted inconsistently because no tie-breaking rule was fixed in E1.
