# S02 — File transfer server with a control channel and a data channel (passive FTP style)

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C11 | S09, S04, S02
- **Protocol/default ports (E2):** TCP: control 5021/TCP; data 60000–60100/TCP (passive; configurable; the default is used in automated tests).

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S02.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
The aim is to implement a file transfer server that separates the control channel from the data channel following the FTP model. On the control channel you negotiate authentication, directories and operations while on the data channel you transfer the file itself or a directory listing.

Passive mode is mandatory: the server announces a temporary data port and the client initiates the data connection to the server. This requirement forces understanding of the difference between session and transfer as well as the impact of NAT and firewall policies at the port level.

The implementation should support streaming transfers, an integrity check at the end (checksum) and a simple per-user isolation model. In the demonstration it should be clear in the capture that there are two distinct connections and that data transfer has a repeatable structure.

The topic enforces an FTP-like control-plane/data-plane separation: the control session remains request/response while the actual transfer occurs over a separate connection initiated (passively) by the client to a server-advertised port. Beyond the commands, the delicate part is the directory and permission model: the server operates under a configured root (logical chroot), normalises paths and blocks traversal (`..`). In E2, the PCAP must allow clear identification of the two channels and their correlation through logs (for example, a transfer triggered by a `RETR` on the control channel).

## Learning objectives
- Define a coherent subset of control-channel commands and their corresponding responses
- Implement passive mode and data-port negotiation
- Perform streaming file transfers with integrity verification
- Apply file-system security rules (path traversal, minimal permissions)
- Build an automated test set covering upload, download and LIST

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **file transfer CLI client (subset)** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **USER + PASV + LIST + RETR/STOR and verify an SHA‑256 checksum**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: control 5021/TCP; data 60000–60100/TCP (passive; configurable; the default is used in automated tests).
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
**Objective:** observe the two connections (control and data) and the negotiated ports in passive mode.

### Minimum scenario
- Start a standard FTP server in a container or on a Mininet host and use a simple client (for example `ftp` or `lftp`) for a short session.
- Capture traffic on the relevant interface and perform: authentication, `LIST` and `RETR` for a small file.
- Note in the capture the `PASV` command and the server response containing the data port.
- Identify the beginning and end of transfer on the data channel.

### Recommended Wireshark filters
- `frame contains "PASV"` — passive-mode negotiation and the moment the data port is decided
- `frame contains "227"` — typical response containing port information for the data connection
- `tcp.len > 0` — segments that contain commands, responses or data payload
- `tcp.analysis.bytes_in_flight > 0` — file-transfer segments, useful for pacing and window behaviour
- `frame contains "RETR"` — download command, a correlation point with the transfer

### Guiding questions
- How do you identify in the capture that there is a control channel and a data channel
- How is the data port computed from a 227 response and how does it appear in the subsequent connection
- What do you see in the capture when a transfer is interrupted: FIN/RST on the data channel and the effect on the control channel
- What is the volume difference between control traffic and data traffic for a 1–2 MB file

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The server exposes a TCP control channel with authentication (`USER`) and coded responses (OK or ERR with a numeric code).
- Commands supported on control: `PWD`, `CWD`, `LIST`, `RETR`, `STOR`, `QUIT`.
- Passive mode: on client request the server allocates a data port, communicates it in the response and accepts a data connection initiated by the client.
- `RETR` and `STOR` transfers in streaming mode with a configurable size limit and without loading the full file into memory.
- Integrity: after each transfer the server provides a file checksum and the client verifies it and reports the result.
- The required integrity checksum is **SHA‑256 in hex** (64 characters), computed over the file contents.
- Passive mode must be an explicit `PASV` command with a deterministic response (e.g. `227 <port>`) and the data port is selected from a configurable range (default 60000–60100).
- Security: prevent **path traversal** (`..`, symlink escapes). Any path must be normalised and verified to remain under the user root (logical root jail).

### SHOULD (recommended)
- Concurrency: two clients can transfer different files in parallel without corrupting server state.
- A per-user directory policy (logical root) with explicit denial for access outside the root.
- Consistent error messages for missing files, permissions and unknown commands.
- Concurrency test: two simultaneous transfers (STOR/RETR) with independent checksum verification.

### MAY (optional)
- Resume an interrupted transfer via a `REST`-style command (offset) for large files.
- An `INFO` command that reports available space and current limits without exposing sensitive details.

## Non-functional requirements
- Control-channel framing: clear delimitation of commands and responses, tolerant to multiple commands within a single segment.
- Timeout for the data connection and port release if the client does not connect in time.
- File-system security: path traversal prevention, name filtering and limits on characters and length.
- Configuration in `config/config.yaml` for ports, root directory, size limits and timeouts.
- Logs for authentication, file operations, data connections and errors.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Control-channel specification: command list, syntax, response codes and complete examples.
- Passive-mode definition: response format containing the data port and allocation/expiry rules.
- Sequence diagram for `LIST`, `RETR` and `STOR` (including opening and closing the data channel).
- Mininet topology and demo scenario (two clients, parallel transfers).
- E2 capture plan: relevant packets on control and data and what is highlighted in the analysis.
- Test plan: smoke tests for `LIST` and `RETR` plus edge cases for path traversal and large files.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S02 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Authentication plus `PWD` plus `LIST` on the control channel.
- A `RETR` for a small file on the data channel followed by a verified checksum.
- Session closure with `QUIT`.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes the passive-mode initiation command and the associated data connection.
- The analysis shows two distinct TCP flows and correlates `RETR` with payload transfer.
- The negotiated data port and the moment the data channel closes are identified.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S02.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S02.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S02 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5021 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake on the control channel. |
| R2 | `tcp.port==5021 && frame contains "USER"` | `>= 1` | Authentication on the control channel (USER). |
| R3 | `tcp.port==5021 && (frame contains "PASV" || frame contains "227")` | `>= 1` | Passive-mode negotiation (PASV/227). |
| R4 | `tcp.dstport>=60000 && tcp.dstport<=60100 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake on the data channel (port in the passive range). |
| R5 | `tcp.port>=60000 && tcp.port<=60100 && tcp.len>0` | `>= 1` | Actual data transfer (payload) on the data channel. |
| R6 | `tcp.port==5021 && (frame contains "SHA-256" || frame contains "HASH")` | `>= 1` | Checksum reporting (SHA‑256) after the transfer. |

### Deliverables
- Docker Compose with `ftp_server` and `tester`.
- Smoke tests (`pytest -m e2`) that run `LIST` and a verifiable `RETR`.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including `STOR` and checksum verification for upload and download.
- Additional tests for concurrency and errors (missing file, invalid command, access outside the root).
- Mininet demo with two simultaneous clients and a lossy link to observe retransmissions during transfer.
- Documented refactoring and a mini security audit for file operations.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (ftp_server) --- s1 --- h2 (client A)
                   |
                   +--- h3 (client B)
```
The link to h3 can be configured with loss to observe retransmissions during transfer.

### Demo steps
- Run `LIST` from h2 and show in the PCAP the command on control and the data flow for listing.
- Run `RETR` from h3 on the lossy link and highlight in Wireshark the retransmissions and their effect on duration.
- Show the checksum and that the result is verified automatically.

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
- **ftp_server:** passive control and data server with mounted storage
- **tester:** automated client that runs commands and produces a PCAP

### E2 flow
- Start `ftp_server` and prepare the file directory via volumes.
- Run `tester` which initiates commands and transfers then saves `artifacts/pcap/traffic_e2.pcap`.
- Automatically validate capture existence and stop the stack.

## Notes
- The model uses an FTP subset; full compatibility with existing implementations is not required.
- The listing format may be simplified but must be documented and tested.
- Executing commands from input is not accepted; operations must remain strictly limited to files in the project directory.

### Typical pitfalls
- Data-channel negotiation without validation (invalid ports, ports outside the range) complicates testing and may create vulnerabilities.
- Missing path normalisation allows escape from the root directory via `RETR/STOR` (`../`).
- The control channel ends up carrying file payload (channel mixing) which makes tests fragile.

### Indicative resources (similar examples)
- [pyftpdlib (FTP server/framework in Python)](https://github.com/giampaolo/pyftpdlib)
- [SimpleFTPServer (minimal FTP implementation)](https://github.com/kzlecha/SimpleFTPServer)
