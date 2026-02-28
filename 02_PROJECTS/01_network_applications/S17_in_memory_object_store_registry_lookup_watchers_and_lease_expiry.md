# S17 — In-memory object store with registry, lookup, watchers and lease expiry

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C09 | S03, S04, S02
- **Protocol/default ports (E2):** TCP: 5017/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S17.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement an in-memory object-sharing service in which the server acts as a registry and transfer broker. Each connected client may publish one or more objects under unique keys. A second client may list keys, request a given object and receive it through a brokered transfer coordinated by the server.

The important educational point is that the service is not merely a central key-value database. The server keeps the authoritative key registry and session metadata while the owner remains responsible for the object payload or for refreshing the object lease, depending on the design fixed in E1. This makes the project an excellent bridge between simple client-server applications and more advanced distributed-service ideas such as ownership, expiry and watchers.

This project is worth adding because it is conceptually different from the existing pub/sub broker, REST gateway and file synchroniser. It introduces registry semantics, owner-coupled state and brokered retrieval while preserving good PCAP observability.

## Learning objectives
- Define a protocol for publishing, listing, fetching and deleting keyed objects
- Implement server-side ownership tracking and automatic cleanup on disconnect or lease expiry
- Distinguish control-plane metadata operations from payload transfer operations
- Add watcher notifications so interested clients observe object creation, deletion and expiry
- Build deterministic tests for publication, retrieval and forced owner removal

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability rather than only for the team's own client and practise integration across different languages and stacks.

### Proposed component
- A **minimal client** implemented in a language **other than Python** (for example C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates only through the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end in one short scripted scenario covering the project's core control messages.
- Any shortcut such as hardcoding, protocol bypass or direct access to the server's internal files is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 5017/TCP.
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
**Objective:** observe a simple key-value protocol and identify how commands, payload and expiry-related control messages appear on the wire.

### Minimum scenario
- Run Redis for observation only.
- Issue a few `SET`, `GET` and `EXPIRE`-style operations from a client.
- Capture the session and note which frames carry commands and which carry returned values.
- Relate those observations to the simpler didactic protocol you will later define.

### Recommended Wireshark filters
- `tcp.port == 6379`
- `frame contains "SET"`
- `frame contains "GET"`
- `frame contains "EXPIRE"`
- `tcp.len > 0`

### Guiding questions
- How does the capture separate control operations from returned object content
- What metadata must your own protocol expose explicitly: key, type, size, owner and expiry
- Why is lease expiry preferable to indefinite ownership for a teaching project
- How can watchers be designed so that they are observable and testable in PCAP

### Mandatory deliverable
- `docs/E1_phase0_observations.md` with short answers and a note explaining how the observed protocol influenced the final design.

## Functional requirements
### MUST (mandatory)
- The server accepts TCP connections and registers clients through `HELLO` or an equivalent command.
- Supported operations: `LIST`, `PUBLISH <key> <type> <length>`, `GET <key>`, `DELETE <key>`, `WATCH <key|prefix>` and the corresponding success and error responses.
- Key uniqueness is enforced at server level.
- The server maintains an authoritative mapping from key to owner session plus metadata needed for retrieval and expiry.
- Retrieval is brokered: the server coordinates transfer so that the requester does not contact the owner directly.
- If the owner disconnects unexpectedly or its lease expires, the server removes the key and notifies watchers.
- The payload format may be JSON or binary but must be documented and validated.

### SHOULD (recommended)
- Prefix-based listing or wildcard listing for keys.
- Per-object metadata such as creation time, payload type and advertised size.
- Heartbeat or lease-renewal messages with explicit expiry semantics.

### MAY (optional)
- Cached copy on the server provided the ownership model remains clearly documented.
- Soft delete or tombstone notifications.

## Non-functional requirements
- The protocol must support payloads larger than a single short command line.
- Limits for maximum object size, maximum number of keys per client and lease duration must be fixed in E1.
- The server must log registry changes, retrieval requests, expiry events and invalid operations.
- Automatic cleanup on disconnect must be deterministic and visible to tests.
- The demonstration must remain feasible with plain Docker and with a small Mininet topology.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`.

- Protocol specification for publication, retrieval, deletion, watching and lease renewal.
- Exact ownership model: whether payload stays only at the owner, is cached at the server or follows a hybrid rule.
- Sequence diagram for one publish plus get operation and one owner disconnect case.
- Key naming policy, payload limits and validation rules.
- Mininet topology with one server, one owner and one requester.
- E2 capture plan showing publication, retrieval and at least one watcher or expiry event.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command, recommended `make e2`, that runs the E2 scenario end-to-end and validates `artifacts/pcap/traffic_e2.pcap` via `tools/validate_pcap.py`.

### Minimum demonstrable outcome
- Client A publishes an object under a unique key.
- Client B lists keys and retrieves that object through a server-brokered flow.
- A watcher receives a notification when the object is removed or expires.

### PCAP requirements
- The capture includes one publication, one retrieval request and one retrieval response or transfer marker.
- The capture shows either a lease-renewal message or an expiry/removal notification.

### Automatic PCAP criteria (E2)
- Official rules: `tools/pcap_rules/S17.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S17.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S17 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5017 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the object-store service. |
| R2 | `tcp.port==5017 && frame contains "PUBLISH"` | `>= 1` | Publication of a keyed object. |
| R3 | `tcp.port==5017 && frame contains "GET"` | `>= 1` | Retrieval request for a key. |
| R4 | `tcp.port==5017 && (frame contains "OBJECT" || frame contains "FETCH" || frame contains "VALUE")` | `>= 1` | Brokered retrieval result appears in payload. |
| R5 | `tcp.port==5017 && (frame contains "LEASE" || frame contains "HEARTBEAT" || frame contains "EXPIRED" || frame contains "REMOVED")` | `>= 1` | Lease or cleanup semantics are observable. |

### Deliverables
- Docker Compose with `object_registry` and `tester` plus optional client containers.
- Smoke tests that publish, retrieve and remove a key.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including automatic cleanup on disconnect.
- Tests for duplicate key refusal, unknown-key retrieval and owner termination during service lifetime.
- Mininet demo with one owner, one requester and one watcher.
- Documented refactoring and a short review of payload validation and memory limits.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (owner) --- s1 --- h3 (object_registry) --- h4 (watcher)
                                 +--- h2 (requester)
```

### Demo steps
- h1 publishes two keys.
- h2 lists available keys and retrieves one object.
- h4 watches a chosen key and observes its removal after owner disconnect or lease expiry.

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
- **object_registry:** main service under test
- **tester:** drives the E2 scenario, captures PCAP and validates the deterministic outcome

### E2 flow
- Start the service in the background.
- Run `tester`, which performs the scripted scenario and writes `artifacts/pcap/traffic_e2.pcap`.
- Validate the capture and keep the generated artefacts for E2 and E3 documentation.

## Notes
- This project is intentionally about **registry plus brokered transfer**, not about a fully replicated distributed store.
- Keeping payloads in memory is acceptable and consistent with the original backbone idea, provided limits are documented.
- Portainer can help inspect container state and logs, but it is optional.

### Typical pitfalls
- The registry accepts duplicate keys under concurrent publication because check and insert are not atomic.
- Owner disconnect removes the TCP session but not the registry entries, leaving stale keys visible.
- The implementation confuses metadata retrieval with payload transfer and no longer demonstrates the intended brokered flow.
