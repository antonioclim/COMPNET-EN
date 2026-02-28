# S16 — Collaborative text editing with locking, notifications and versioned saves

## Metadata
- **Group:** 1
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C09 | S03, S04, S09
- **Protocol/default ports (E2):** TCP: 5016/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S16.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a client-server application for collaborative editing of plain-text documents stored on the server. The system is intentionally **not** a full real-time editor with operational transformation or CRDT logic. Instead it focuses on a didactically cleaner model that fits the current COMPNET-EN catalogue: a single active editor per document, concurrent readers, server-authoritative version numbers and explicit network notifications.

The server manages a document directory and keeps, in memory, the current editor, the current version number and the list of connected watchers for each document. A client may list documents, open a document in read-only mode, request an exclusive edit lock, save a full new version and release the lock. When state changes, the server pushes deterministic notifications to interested clients.

This project deserves a place in COMPNET-EN because it is **not** a duplicate of file transfer or file synchronisation. It augments those topics with explicit coordination, lock ownership, version progression and observer notifications. Pedagogically it strengthens protocol design, concurrency control, framing and error handling while remaining simple enough for controlled PCAP-based assessment.

## Learning objectives
- Define a custom application protocol for listing, viewing, locking, saving and releasing documents
- Implement single-writer semantics with many readers and deterministic server-side state
- Propagate notifications to connected clients without corrupting the command stream
- Use version numbers and explicit acknowledgements to prevent stale overwrites
- Build an automated test that demonstrates a refused second lock, a successful save and visible notifications in PCAP

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability rather than only for the team's own client and practise integration across different languages and stacks.

### Proposed component
- A **minimal client** implemented in a language **other than Python** (for example C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates only through the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end in one short scripted scenario covering the project's core control messages.
- Any shortcut such as hardcoding, protocol bypass or direct access to the server's internal files is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 5016/TCP.
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
**Objective:** observe the difference between document retrieval traffic and live collaboration traffic, then extract the minimal ideas needed for a simpler didactic protocol.

### Minimum scenario
- Run an observation-only collaborative editor such as Etherpad Lite or an equivalent shared-note service.
- Open the same document from two browsers or two browser profiles.
- Perform one read-only access, one editing action and one lock-like coordination action if the observed platform exposes it.
- Capture the traffic and identify which exchanges carry state updates and which merely initialise the session.

### Recommended Wireshark filters
- `tcp.len > 0` - frames carrying application payload
- `http` or `websocket` - if the observed platform uses HTTP and WebSocket
- `frame contains "text"` - coarse filter for visible payload markers
- `tcp.analysis.retransmission` - identify transport-level noise that must not be confused with application-level updates

### Guiding questions
- What is the observable difference between initial document fetch and later update traffic
- How does the capture suggest that the server is the authority for ordering updates
- Why is a single-writer model easier to specify and assess than true concurrent editing
- Which fields would you make explicit in your own protocol: document name, version, payload length and lock owner

### Mandatory deliverable
- `docs/E1_phase0_observations.md` with short answers to the guiding questions and a note on the traffic patterns that inspired the final protocol.

## Functional requirements
### MUST (mandatory)
- The server accepts TCP connections and requires a client identifier through `HELLO` or an equivalent command.
- Supported operations: `LIST`, `VIEW <doc>`, `LOCK <doc>`, `SAVE <doc> <version> <length>`, `UNLOCK <doc>`, `WATCH <doc>` and `UNWATCH <doc>` or equivalent.
- At most one client may hold the edit lock for a given document at any time.
- A successful save writes the complete new file to disk, increments the server-side version and generates a notification to watchers.
- A client attempting to lock a document already locked by another client receives a deterministic refusal.
- If the lock owner disconnects unexpectedly, the lock is released automatically and a notification is emitted.
- The project must keep document metadata consistent across all connected clients.

### SHOULD (recommended)
- `CREATE` and `DELETE` commands for documents with corresponding notifications.
- A `WHOLOCKS <doc>` or equivalent diagnostic command for debugging and tests.
- A stale-version refusal rule so that `SAVE` with an obsolete version is rejected.

### MAY (optional)
- Read-only tailing mode for clients that want to see successive versions without reissuing `VIEW`.
- Simple access classes such as read-only users and editor users.

## Non-functional requirements
- The protocol must be framed explicitly so that payload length and document content cannot be confused with command boundaries.
- The save path must avoid partial writes becoming visible as valid final versions.
- Logs must distinguish control-plane events such as lock acquisition from data-plane events such as full document saves.
- Limits for document size, line length and total number of watched documents must be documented in E1.
- The default demonstration must remain feasible on plain Docker and on Mininet without graphical tooling.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format including version or magic where appropriate.

- Protocol specification for `HELLO`, `LIST`, `VIEW`, `LOCK`, `SAVE`, `UNLOCK`, `WATCH` and notifications.
- Exact versioning rule and stale-write policy with one worked example.
- Sequence diagram for one successful editing cycle and one refused competing lock.
- File-system policy: supported file names, persistence rules and maximum document size.
- Mininet topology with one server, one active editor and one watching client.
- E2 capture plan showing where the `LOCK`, `SAVE` and notification messages will appear.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command, recommended `make e2`, that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S16 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Two clients connect to the server and list the same document set.
- Client A acquires a lock on one document.
- Client B attempts to acquire the same lock and is refused deterministically.
- Client A saves a new version and Client B receives a notification or refreshed content marker.

### PCAP requirements
- The capture includes the TCP handshake to port 5016.
- The capture contains one lock request, one refused competing lock and one successful save.
- The capture shows a notification or update message following the save.

### Automatic PCAP criteria (E2)
These criteria are deterministic and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S16.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S16.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S16 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5016 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the editing service. |
| R2 | `tcp.port==5016 && frame contains "LOCK"` | `>= 1` | At least one lock attempt appears in payload. |
| R3 | `tcp.port==5016 && (frame contains "BUSY" || frame contains "ERR_LOCKED" || frame contains "LOCK_DENIED")` | `>= 1` | The competing lock is refused deterministically. |
| R4 | `tcp.port==5016 && frame contains "SAVE"` | `>= 1` | A save command is visible in the session. |
| R5 | `tcp.port==5016 && (frame contains "DOC_UPDATE" || frame contains "UPDATED" || frame contains "VERSION")` | `>= 1` | A post-save update or version marker is visible. |

### Deliverables
- Docker Compose with `editor_server` and `tester` plus optional interactive clients.
- Smoke tests that open a document, enforce lock exclusivity and verify a saved version on disk.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including automatic lock release on disconnect.
- Tests for stale-version save refusal, invalid document name and forced client termination while holding a lock.
- Mininet demo with one editor and one watcher on separate hosts.
- Documented refactoring and a short safety review of file-system input handling.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (editor A) --- s1 --- h3 (editor_server) --- h4 (observer)
                                     +--- h2 (editor B)
```

### Demo steps
- h1 and h2 connect and list documents.
- h1 locks `notes.txt` and h2 receives a refusal when attempting the same action.
- h1 saves a new version and h4, subscribed as watcher, receives an update event.
- h1 disconnects abruptly while holding another lock and the server releases it automatically.

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
- **editor_server:** main service under test
- **tester:** drives the E2 scenario, captures PCAP and validates the deterministic outcome

### E2 flow
- Start the service in the background.
- Run `tester`, which performs the scripted scenario and writes `artifacts/pcap/traffic_e2.pcap`.
- Validate the capture and keep the generated artefacts for E2 and E3 documentation.

## Notes
- Full real-time character-by-character synchronisation is **not** required. Full-document save is acceptable and preferable for deterministic assessment.
- The project should remain text only. Binary attachments or rich-text formatting would move it away from the intended networking focus.
- Portainer is a convenience tool for inspection and log review, not a requirement. The canonical E2 path remains `docker compose` plus automated capture.

### Typical pitfalls
- The command stream and the document payload use the same delimiter and the parser breaks on multi-line content.
- Lock release is performed only on graceful `UNLOCK` rather than also on disconnect.
- The server trusts a client-provided version without checking the current server-side version.
