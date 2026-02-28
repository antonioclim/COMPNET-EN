# S20 — Database-backed object service with selection, update, delete and notifications

## Metadata
- **Group:** 1
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C09 | S04, S02, S07
- **Protocol/default ports (E2):** TCP: 5020/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S20.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a network service that exposes a collection of structured objects stored persistently in a database. Clients connect to the service, query objects by key or by a simple criterion, update selected objects, delete objects and subscribe for notifications about objects they previously selected.

This project preserves the spirit of the legacy backbone while upgrading it to the COMPNET-EN standard. Its value lies in the interaction between persistent state, network protocol design and selective notification. Unlike the existing REST registry and gateway project, this one is centred on object selection, change propagation and durable state rather than on routing between services.

The recommended baseline is a custom TCP application protocol backed by SQLite for deterministic local persistence, though another documented database choice is acceptable. The server remains the sole authority for committed state and for deciding which subscribed clients must be notified after an update or delete operation.

## Learning objectives
- Design a query and update protocol for structured objects with persistent backing storage
- Keep in-memory state and durable state consistent under concurrent client requests
- Track client subscriptions or selections so that only relevant updates are pushed back
- Validate object mutation, deletion and error cases without corrupting persistent state
- Build automated tests for selection, update, delete and restart persistence

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability rather than only for the team's own client and practise integration across different languages and stacks.

### Proposed component
- A **minimal client** implemented in a language **other than Python** (for example C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates only through the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end in one short scripted scenario covering the project's core control messages.
- Any shortcut such as hardcoding, protocol bypass or direct access to the server's internal files is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 5020/TCP.
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
**Objective:** observe the network signature of read-modify-read behaviour in a simple database-backed API and derive a more controlled didactic protocol.

### Minimum scenario
- Run a small observation-only CRUD service backed by SQLite or another lightweight database.
- Issue one query for an object, one update and a second query for the same object.
- Capture the traffic and note which fields make the state transition observable.
- Relate those observations to the final custom protocol.

### Recommended Wireshark filters
- `tcp.len > 0`
- `frame contains "GET"` or `frame contains "QUERY"`
- `frame contains "UPDATE"` or `frame contains "PATCH"`
- `frame contains "DELETE"`

### Guiding questions
- What makes a state transition observable rather than merely inferred
- Why should the server remember which clients have selected a given object
- What consistency risks appear if memory and persistent storage are updated in different orders
- Which explicit notifications should your own protocol define: changed, deleted and not-found

### Mandatory deliverable
- `docs/E1_phase0_observations.md` with short answers and the final design decisions that emerged from the observation.

## Functional requirements
### MUST (mandatory)
- The server accepts TCP connections and registers clients through `HELLO` or an equivalent command.
- Supported operations: `QUERY`, `GET <key>`, `UPDATE <key> <payload>`, `DELETE <key>`, `WATCH <key|criterion>` and equivalent success and error responses.
- Objects are stored in a real database and remain available after service restart.
- The server keeps enough session metadata to notify clients that previously selected or watched an object when that object changes or is deleted.
- Update and delete are validated against current state and produce deterministic error codes for unknown keys or invalid payload.
- The implementation keeps persistent state and any in-memory cache or index consistent.
- Disconnecting a client removes only its watch state and must not corrupt stored data.

### SHOULD (recommended)
- Range or prefix queries on the primary key.
- Object schema validation with required fields and type checks.
- Explicit revision number per object so that update history is easier to explain.

### MAY (optional)
- Insert operation for creating new objects if the team wants a richer dataset lifecycle.
- Soft delete or audit trail beyond the mandatory notification mechanism.

## Non-functional requirements
- The default database choice should favour deterministic local execution. SQLite is recommended for E2.
- Database schema, key format and payload size limits must be fixed in E1.
- The service must log query, update, delete and notify events with enough context for debugging.
- Update order between memory and persistent store must be documented and justified.
- The E2 scenario must remain fully automatable with Docker and should not require manual database initialisation.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`.

- Protocol specification for query, retrieval, update, delete, watch and notifications.
- Database schema or object model with one worked example object.
- Consistency policy between memory and durable storage.
- Sequence diagram for query -> update -> notification and for query -> delete -> notification.
- Mininet topology with one server and two interested clients.
- E2 capture plan showing query, update and notification traffic.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command, preferably `make e2`, that runs the E2 scenario end-to-end and validates the capture.

### Minimum demonstrable outcome
- Client A queries one object.
- Client B also watches or selects the same object.
- Client A updates the object and Client B receives a notification.
- A second action deletes the object and the service responds deterministically.

### PCAP requirements
- The capture includes one query, one update and one notification or changed-state marker.
- The capture includes one delete operation or delete-notification pair.

### Automatic PCAP criteria (E2)
- Official rules: `tools/pcap_rules/S20.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S20.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S20 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5020 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the object service. |
| R2 | `tcp.port==5020 && (frame contains "QUERY" || frame contains "GET")` | `>= 1` | A selection or retrieval request appears in payload. |
| R3 | `tcp.port==5020 && frame contains "UPDATE"` | `>= 1` | Update operation is visible in the session. |
| R4 | `tcp.port==5020 && (frame contains "NOTIFY" || frame contains "CHANGED" || frame contains "UPDATED")` | `>= 1` | Change notification is visible to another client. |
| R5 | `tcp.port==5020 && frame contains "DELETE"` | `>= 1` | Delete operation is visible in the session. |

### Deliverables
- Docker Compose with `object_db_service` and `tester` plus optional client containers.
- Smoke tests that verify query, update, notification and persistence after restart.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including persistent restart behaviour.
- Tests for unknown-key update, invalid payload, watched-object notification and restart persistence.
- Mininet demo with two clients observing the same object across one update cycle.
- Documented refactoring and a short review of consistency, transaction ordering and input validation.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (client A) --- s1 --- h3 (object_db_service)
                                     +--- h2 (client B)
```

### Demo steps
- h1 queries an object and h2 watches the same key.
- h1 updates the object and h2 receives a notification.
- h1 deletes the object and both clients observe the resulting state.
- The service restarts and the retained dataset is checked if persistence is part of the chosen design.

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
- **object_db_service:** main service under test
- **tester:** drives the E2 scenario, captures PCAP and validates the deterministic outcome

### E2 flow
- Start the service in the background.
- Run `tester`, which performs the scripted scenario and writes `artifacts/pcap/traffic_e2.pcap`.
- Validate the capture and keep the generated artefacts for E2 and E3 documentation.

## Notes
- A custom TCP protocol is recommended because it keeps the networking emphasis sharp and avoids overlap with the existing REST gateway project.
- SQLite is recommended for E2 because it makes the persistence requirement deterministic and portable.
- Portainer remains optional and useful mainly for log inspection and restart testing.

### Typical pitfalls
- The database is updated but the in-memory index is not, leaving stale notifications.
- Client watch state is never removed and the server keeps notifying dead sessions.
- Query syntax grows too complex and shifts the project from networking design towards database engineering.
