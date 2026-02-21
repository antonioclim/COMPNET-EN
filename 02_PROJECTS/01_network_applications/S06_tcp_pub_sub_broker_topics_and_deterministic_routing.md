# S06 — TCP Pub/Sub broker with topics and deterministic routing

## Metadata
- **Group:** 1
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C13 | S03, S04, S02
- **Protocol/default ports (E2):** TCP: 5006/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S06.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a publish/subscribe broker over TCP that mediates communication between producers and consumers through topics. Clients connect, register with an identifier then can publish messages to a topic or subscribe to topics to receive messages asynchronously.

The application protocol is defined by the team and must include framing, acknowledgements and error handling. The broker maintains an internal registry of subscribers per topic and applies clear matching rules (minimum exact match, optional wildcard).

In the demo you focus on role separation: a publisher sends messages at a controlled frequency and two subscribers receive the same sequence, including behaviour on disconnect. The PCAP must contain SUBSCRIBE and PUBLISH commands plus identifiable payload.

The pub/sub broker must implement deterministic routing: a message published on a topic reaches all subscribed connections in the order received by the broker with no duplication. To keep the project testable, E1 must fix the delivery semantics (at least once versus exactly once, with justification) and reconnection behaviour. A typical source of defects is mixing framing with topic semantics: parsing must first extract the complete message then apply rules (authorisation, valid topic, payload limits).

## Learning objectives
- Define a pub/sub protocol with framing and acknowledgements
- Implement a broker with a subscriber registry and topic-based routing
- Manage concurrency among clients and the message queues
- Apply defined delivery guarantees (at most once or at least once)
- Build an automated test that validates routing and message order

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **minimal publisher/subscriber** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **send HELLO, SUBSCRIBE, PUBLISH and receive DELIVER**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 5006/TCP.
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
**Objective:** observe a real publish/subscribe flow and identify subscription and publication events in the payload.

### Minimum scenario
- Run a standard MQTT broker for observation only and start a publisher and a subscriber for the same topic.
- Capture traffic on the relevant interface and send 5–10 short messages.
- Disconnect the subscriber and reconnect it to observe what happens to messages in the meantime.
- Note the difference between control messages (subscribe) and data messages (publish).

### Recommended Wireshark filters
- `frame contains "SUBSCRIBE"` — identify a subscribe command in text protocols or in interpretable payload
- `frame contains "PUBLISH"` — identify publication and topic in payload
- `tcp.len > 0` — segments carrying commands and messages
- `tcp.analysis.out_of_order` — reordering that may appear on lossy links
- `frame contains "topic"` — generic marker for topic fields in JSON payload

### Guiding questions
- What minimal message sequence appears between client and broker during subscription
- How does the capture show the difference between control-plane and data-plane
- How can you verify in the PCAP that messages to two subscribers keep the same order
- What events appear on abrupt subscriber disconnect and how should the broker react

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The broker accepts TCP connections and registers clients via a `HELLO` command or equivalent using a unique ID.
- Supported commands: `SUBSCRIBE <topic>`, `UNSUBSCRIBE <topic>`, `PUBLISH <topic> <payload>` plus OK/ERR responses.
- Routing: a published message is delivered to all matching subscribers without blocking the broker on a slow client.
- A defined and implemented delivery guarantee: at most once or at least once, described in E1 and verifiable in tests.
- Broker logs for connections, subscriptions, publications, deliveries and errors.
- Deterministic routing: define topic matching clearly (exact plus wildcard if present) and the chosen QoS guarantee (at most once/at least once) with observable effects in tests.
- The broker must not block on a slow subscriber: use per-subscriber queues plus a deterministic policy (drop/disconnect) on overflow.

### SHOULD (recommended)
- Topic wildcard support (e.g. `sensors/*`) with documented matching rules.
- Backpressure: queue limit per subscriber and a deterministic overflow policy (drop or disconnect).
- Keepalive messages and timeouts for inactive sessions.

### MAY (optional)
- Retained message per topic (the last message), delivered immediately upon subscription.
- Minimal persistence of the registry in a file for controlled restart.

## Non-functional requirements
- Explicit framing and payload size limits. Messages exceeding the limit are refused with an error.
- Controlled concurrency: separate command acceptance from delivery to subscribers (thread pool, asyncio or queues).
- Socket timeouts and handling of abrupt disconnects, including clean-up of subscriptions.
- YAML configuration: port, queue limits, drop policy, timeouts, wildcard enable/disable.
- Observability: logs include client ID and topic without logging the full payload if large.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Protocol specification: commands, syntax, framing, error codes and complete examples.
- Definition of topic matching rules (exact, wildcard) and delivery guarantee.
- Sequence diagram for subscribe, publish to two subscribers, unsubscribe.
- Mininet topology with broker, two subscribers and one publisher.
- E2 capture plan: subscription commands, a publish and acknowledgements with recommended filters.
- Test plan: message order, multiple topics, slow client.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S06 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- The broker starts in Docker and accepts connections.
- A subscriber subscribes to a topic and receives at least one published message.
- An unsubscribe stops message delivery to that client.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes a complete sequence: subscribe, publish, delivery to subscriber.
- The analysis highlights an application payload and the framing used to delimit it.
- A filter that isolates a subscribe or publish command is stated.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S06.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S06.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S06 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5006 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the broker. |
| R2 | `tcp.port==5006 && (frame contains "HELLO" || frame contains "AUTH")` | `>= 1` | Client registration (HELLO/AUTH). |
| R3 | `tcp.port==5006 && (frame contains "SUBSCRIBE" || frame contains "SUB ")` | `>= 1` | At least one SUBSCRIBE. |
| R4 | `tcp.port==5006 && (frame contains "PUBLISH" || frame contains "PUB ")` | `>= 1` | At least one PUBLISH. |
| R5 | `tcp.port==5006 && (frame contains "DELIVER" || frame contains "MSG ")` | `>= 1` | The broker delivers at least one message to a subscriber (push). |

### Deliverables
- Docker Compose with `broker` and `tester` (which plays publisher and subscriber roles).
- Smoke tests (`pytest -m e2`) that validate delivery to subscriber and the effect of unsubscribe.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including routing to multiple subscribers and behaviour under a slow client.
- Extended tests for wildcard, chosen delivery guarantee and timeouts.
- Mininet demo with two subscribers on different links and delivery evidence in logs.
- Documented refactoring and a mini security audit (input validation, payload limits, timeouts).

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (broker) --- s1 --- h2 (publisher)
                 |
                 +--- h3 (subscriber A)
                 +--- h4 (subscriber B)
```
The link to h4 can have delay to highlight a slow client.

### Demo steps
- Subscribe h3 and h4 to the same topic and publish a numbered message sequence from h2.
- Show in logs that the broker delivers to both and that order is preserved per topic.
- In Wireshark highlight the subscription command and one complete published message.

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
- **broker:** pub/sub server with a topic registry
- **tester:** dual role: subscribe plus publish, verifies delivery and captures PCAP

### E2 flow
- Start `broker` in the background.
- Run `tester` which subscribes, publishes and verifies message reception while writing `artifacts/pcap/traffic_e2.pcap`.
- Stop the stack and verify the capture.

## Notes
- MQTT-style QoS is not required; define a simple guarantee that can be verified automatically.
- Topics are treated as ASCII/UTF-8 strings with validation rules and a maximum length.
- For slow clients, the choice between drop and disconnect must be documented and tested.

### Typical pitfalls
- A slow subscriber blocks delivery to others if the broker does not isolate per client.
- Topic routing is implemented with overly permissive matching (prefix/substring) and messages leak between topics.
- Framing does not handle binary payloads or special characters and the parser breaks on realistic data.

### Indicative resources (similar examples)
- [NATS Server (pub/sub broker, industrial reference)](https://github.com/nats-io/nats-server)
- [RabbitMQ Server (multi-protocol broker, conceptual model)](https://github.com/rabbitmq/rabbitmq-server)
