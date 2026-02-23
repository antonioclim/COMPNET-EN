# S10 — Network file synchronisation with manifest, hashes and conflict resolution

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C11 | S09, S04, S07
- **Protocol/default ports (E2):** TCP: 5010/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S10.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will design a file synchronisation service between two replicas with difference detection through a manifest and hashes. A replica scans a directory, constructs a manifest (name, size, hash, timestamp) then compares it with the manifest of the other replica to decide which files must be transferred.

The synchronisation protocol must separate the control phase (manifest exchange and decisions) from the transfer phase (actual file payload). To avoid ambiguity an explicit conflict policy is required: what happens when the same file has been modified on both sides between two sync operations.

In the demo you cover a standard sync case and a conflict case. The PCAP capture must include the manifest exchange and transfer of a file with identifiable payload and application-level acknowledgements.

File synchronisation is assessed on two axes: correctness (what “same state” means) and efficiency (what is transferred). In E1 you define the manifest: format, per-file hash, minimal metadata (size, mtime) plus conflict rules (different contents under the same name). To remain testable a deterministic approach is recommended: a fixed file set, controlled modification scenarios and conflict resolutions that produce the same result on rerun.

## Learning objectives
- Define a synchronisation protocol with control and transfer phases
- Implement manifest construction and comparison based on hashes
- Apply a deterministic conflict-resolution policy
- Perform selective transfer: only changed files, not the whole directory
- Build automated tests for synchronisation, deletion and conflicts

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **sync client** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **request MANIFEST and trigger a deterministic PUSH/PULL**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 5010/TCP.
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
**Objective:** observe a file transfer and the fact that an application checksum enables end-to-end validation.

### Minimum scenario
- Transfer a file of several hundred KB between two hosts using a simple tool (for example a local HTTP server or a minimal TCP transfer).
- Capture traffic and identify the beginning and end of transfer in the payload.
- Compute a local hash before and after transfer and note that the network does not provide an application checksum.
- Observe retransmissions in the capture if you introduce loss on the link.

### Recommended Wireshark filters
- `tcp.len > 0` — segments that carry transfer payload
- `tcp.analysis.retransmission` — retransmissions on lossy links
- `frame contains "SHA256"` — marker for a hash field in the control protocol
- `frame contains "MANIFEST"` — marker for the manifest exchange
- `tcp.analysis.bytes_in_flight > 0` — hint on streaming and window in the transfer

### Guiding questions
- Why an application-level hash is needed even though TCP guarantees byte ordering
- How the protocol can separate the control phase (manifest) from the transfer phase (payload)
- How conflicts can be detected based on timestamp and hash and what resolution policy is acceptable
- What appears in the capture when the link has loss and how it affects sync duration

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Two clear roles: a component that initiates synchronisation and a component that responds, both able to generate a local-directory manifest.
- Manifest exchange with hashes (minimum SHA‑256) and deterministic decisions on which files must be transferred.
- File transfer in streaming mode with an integrity confirmation (verified hash) at the end.
- Bidirectional support: synchronisation can run in both directions with an explicit conflict policy (for example rename with suffix).
- Deletions: detect deleted files and propagate the deletion or a tombstone according to the defined policy.
- Standard hash: SHA‑256 in hex to identify contents; manifest includes relative path, hash and size.
- Deterministic conflict policy (fixed in E1): e.g. last-writer-wins with monotonic timestamp or prefer server.
- Atomic writes on update (tmp plus rename) to avoid corruption.

### SHOULD (recommended)
- Exclusion filters (e.g. `*.tmp`) configurable and applied to the manifest.
- Bandwidth limit or file limit per sync to control demo duration.
- Logging: sync report with file counts transferred, skipped, conflicts and errors.

### MAY (optional)
- Chunking for large files with resumption of a failed chunk without retransferring the full file.
- Optional compression for payload negotiated in the control phase.

## Non-functional requirements
- Clear framing for control messages (manifest, transfer requests) and for data messages (chunks).
- Timeouts and controlled retries for transfer with attempt limits and logs.
- Security: path-traversal prevention and refusal of suspicious filenames; access only within the root directory.
- YAML configuration: directories, scan interval (if present), limits, conflict policy, delete policy.
- Testability: baseline scenarios reproducible in Docker without manual intervention.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Manifest specification: fields, format, order, hash algorithm and path normalisation rules.
- Control protocol specification: request/response for difference listing and transfer initiation.
- Conflict and deletion policy with examples and the final file-system outcome.
- Mininet topology with two replicas and a third host acting as a second modification source.
- E2 capture plan: one manifest exchange and one transfer with a visible marker in payload.
- Test plan: simple sync, conflict, delete.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S10 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Manifest exchange between client and server and identification of a file missing on one side.
- Transfer of that file and hash verification at the end.
- Automatic capture generation and completed analysis.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes a MANIFEST message and a file transfer within the same session.
- The analysis highlights the hash field and the integrity confirmation.
- A filter that isolates control messages versus payload is mentioned.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S10.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S10.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S10 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5010 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the synchronisation service. |
| R2 | `tcp.port==5010 && frame contains "MANIFEST"` | `>= 1` | Manifest transfer/request. |
| R3 | `tcp.port==5010 && (frame contains "SHA256" || frame contains "sha256")` | `>= 1` | A SHA-256 hash appears in the manifest or response. |
| R4 | `tcp.port==5010 && (frame contains "PUSH" || frame contains "PULL" || frame contains "GET" || frame contains "PUT")` | `>= 1` | At least one synchronisation operation (push/pull). |
| R5 | `tcp.port==5010 && (tcp.flags.fin==1 || tcp.flags.reset==1)` | `>= 1` | Controlled session closure. |

### Deliverables
- Docker Compose with `sync_peer` (or client/server) and `tester`.
- Smoke tests (`pytest -m e2`) that create a file, run synchronisation and verify presence on the other side.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including conflict and delete, demonstrable in Mininet.
- Tests for minimal concurrency (two consecutive sync runs) and errors (interrupted transfer).
- Mininet demo: modify the same file on two hosts and show the conflict-policy outcome.
- Documented refactoring and a mini security audit for filenames and resource limits.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (replica A) --- s1 --- h2 (replica B)
                   |
                   +--- h3 (editor)
```
h3 simulates a second source of modifications to one replica (controlled conflict).

### Demo steps
- Create a file on h1 and sync to h2; verify hash and presence.
- Modify the same file on h1 and h2 and run bidirectional sync; show conflict resolution.
- Show in the PCAP the MANIFEST messages and a complete transfer.

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
- **sync_node:** synchronisation component (one role or both roles)
- **tester:** prepares files, runs synchronisation, verifies results and captures PCAP

### E2 flow
- Start `sync_node` and mount volumes for working directories.
- Run `tester` which creates files, initiates synchronisation and writes `artifacts/pcap/traffic_e2.pcap`.
- Stop the stack and verify the capture.

## Notes
- Delta encoding is not required. Full-file transfer is acceptable if the transfer decision is correct.
- The conflict policy must be deterministic and must not lose data (rename, suffix, conflicts folder).
- For deletions, document clearly whether the project propagates delete or only reports it.

### Typical pitfalls
- The “file modified” decision uses only mtime; between containers clock drift may cause needless sync.
- Writing to disk is not atomic (a partial file is visible) and the next scan treats it incorrectly.
- Limits for size and file count are missing; a large directory severely degrades timings.

### Indicative resources (similar examples)
- [Rsync (delta transfer, algorithmic reference)](https://github.com/RsyncProject/rsync)
- [Syncthing (distributed file sync, conceptual model)](https://github.com/syncthing/syncthing)
