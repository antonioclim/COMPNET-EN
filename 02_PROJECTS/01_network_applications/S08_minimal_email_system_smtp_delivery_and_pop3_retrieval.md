# S08 — Minimal email system: SMTP server for delivery and POP3 server for reading

## Metadata
- **Group:** 1
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C12 | S04, S02, S07
- **Protocol/default ports (E2):** TCP: SMTP 2525/TCP; POP3 2110/TCP (POP3 is assessed in E3).

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S08.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a minimal email system composed of two services: an SMTP server that accepts messages and stores them and a POP3 server that provides mailbox access. The aim is not full compatibility with the entire email ecosystem but understanding application protocols with state machines and response codes.

SMTP enforces a strict sequence of commands (HELO, MAIL FROM, RCPT TO, DATA) while POP3 uses a session model and operations on stored messages (LIST, RETR, DELE). The implementation must handle SMTP body delimitation (`
.
` terminator) and apply limits on size and recipient count.

In the demonstration, one client sends a message to a local user and another client downloads it via POP3. The PCAP capture must show state transitions, the DATA command and message payload as well as the deletion operation.

The system is centred on two state machines: one for SMTP (sequential commands, DATA terminator, response codes) and one for POP3 (authentication, listing, retrieval, deletion). Storing messages in a Maildir-like layout simplifies the concurrency discussion: each message is a file and the server must avoid name collisions and offer consistency for `RETR/DELE`. In E2, the PCAP must contain the full SMTP session (including DATA) while POP3 is completed in E3 so that the end-to-end delivery and consumption flow can be demonstrated robustly.

## Learning objectives
- Implement two application protocols with explicit state machines (SMTP and POP3)
- Store messages in a simple and safe format (maildir per user)
- Handle SMTP body delimitation and dot-stuffing
- Implement POP3 operations over stored messages and consistency after DELE
- Build an automated end-to-end test: send mail → retrieve mail (E3)

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- An **SMTP client** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **send a full message (MAIL/RCPT/DATA with dot-stuffing)**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: SMTP 2525/TCP; POP3 2110/TCP (POP3 is assessed in E3).
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
**Objective:** observe SMTP sequences in a capture and identify message delimiters.

### Minimum scenario
- Using netcat or telnet, connect to a test SMTP server and execute a short session: HELO, MAIL FROM, RCPT TO, DATA, message, QUIT.
- Connect to a test POP3 server and execute: USER, PASS, LIST, RETR, QUIT.
- Capture both sessions and follow the DATA command and the end-of-message terminator.
- Note response codes and protocol-specific prefixes (for example `+OK` in POP3).

### Recommended Wireshark filters
- `frame contains "MAIL FROM"` — beginning of SMTP transaction and sender address
- `frame contains "RCPT TO"` — recipient, showing difference between sender and recipient
- `frame contains "\r\n.\r\n"` — SMTP end-of-body terminator
- `pop.request.command == "RETR"` — POP3 message retrieval
- `smtp.response.code >= 500` — SMTP error (if an error case is forced)

### Guiding questions
- Which responses does an SMTP client receive after each command and how can they be identified in the capture
- How do you recognise the DATA terminator and how is dot-stuffing handled
- What do POP3 `+OK` and `-ERR` responses mean and where do they appear in the flow
- How can deletion (DELE) be observed and what happens after QUIT

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Minimal SMTP server supporting `HELO` or `EHLO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT` with coherent response codes.
- Message storage in a Maildir-like layout per user (configurable directory structure) with path-traversal prevention for usernames.
- Correct handling for DATA delimitation (terminator) including dot-stuffing and a configurable size limit.
- Minimal POP3 server supporting `USER`, `PASS` (simple authentication), `LIST`, `RETR`, `DELE`, `QUIT` operating over the same storage area (completed in E3).
- End-to-end test: send a message through SMTP and retrieve through POP3 (E3) with evidence in PCAP and logs.
- Staged scope: in **E2** you implement SMTP plus storage; POP3 is completed in **E3** (to keep difficulty realistic).
- SMTP: handle DATA termination with `\r\n.\r\n` and implement **dot-stuffing** (lines starting with '.' are escaped on transmit and unescaped on storage).
- Storage: use Maildir atomicity or an equivalent documented approach.

### SHOULD (recommended)
- Support multiple recipients within a single SMTP session with a configurable limit.
- Specific error messages: unknown user, authentication failure, message too large.
- A simple mailbox lock to avoid inconsistencies under simultaneous access.

### MAY (optional)
- An administrative utility that lists mailboxes and message counts without reading contents.
- A test mode that injects an invalid message intentionally to validate error responses.

## Non-functional requirements
- Explicit state machines for both protocols with documented transitions and refusal of commands in the wrong state.
- Timeouts for inactive sessions, configurable; connections close gracefully.
- Input validation: maximum lengths for addresses and lines, filtering of disallowed characters.
- Separate logs for SMTP and POP3 with correlation via session ID and user.
- No command execution or unsafe interpretation of message contents.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- SMTP specification: command sequence, response codes, DATA delimitation and errors.
- POP3 specification: commands, response formats, DELE semantics and commit on QUIT.
- Storage format (maildir): directory structure and naming rules.
- Mininet topology: sender client, servers and receiver client.
- E2 capture plan: what is captured for SMTP and what marker is highlighted (DATA, terminator).
- Test plan: send/retrieve, incorrect authentication, message too large.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S08 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Full SMTP session for a small message addressed to a local user.
- On-disk storage verified by the existence of a maildir file (without exposing contents in logs).

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes the `DATA` command and terminator (dot) for a locally delivered message.
- The analysis describes state transitions and observed response codes.
- Filters to isolate SMTP in the capture are provided.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S08.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S08.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S08 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==2525 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Client → SMTP handshake. |
| R2 | `tcp.port==2525 && (frame contains "EHLO" || frame contains "HELO")` | `>= 1` | SMTP greeting (EHLO/HELO). |
| R3 | `tcp.port==2525 && frame contains "MAIL FROM"` | `>= 1` | MAIL FROM present. |
| R4 | `tcp.port==2525 && frame contains "RCPT TO"` | `>= 1` | RCPT TO present. |
| R5 | `tcp.port==2525 && frame contains "DATA"` | `>= 1` | DATA command present. |
| R6 | `tcp.port==2525 && (frame contains "\r\n.\r\n" || frame contains "\n.\n")` | `>= 1` | The data terminator (dot) appears in the payload (dot-stuffing is demonstrable). |

### Deliverables
- Smoke tests (`pytest -m e2`) that send a message and verify storage plus validate one error case.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including POP3 (USER/PASS/LIST/RETR/DELE) and commit on QUIT.
- Extended tests for wrong command ordering and concurrent mailbox access.
- Mininet demo with two clients: one sends, one reads, with the flows observable in PCAP.
- Documented refactoring and a mini security audit for parsing and storage.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (smtp_server) --- s1 --- h3 (pop3_server)
                   |
                   +--- h2 (sender)
                   +--- h4 (receiver)
```
Servers may run on separate hosts to highlight distinct connections to two ports.

### Demo steps
- From h2 send a message via SMTP and show in the capture the full sequence up to QUIT.
- From h4 list and download the message via POP3 and show `+OK` responses and message contents.
- Show in logs the session IDs and mailbox used.

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
- **smtp_server:** accepts messages and stores them in maildir
- **pop3_server:** exposes POP3 access to maildir (E3)
- **tester:** sends a message (E2) and, in E3, retrieves it, capturing PCAP

### E2 flow
- Start `smtp_server` (and optionally `pop3_server`) with a shared storage volume.
- Run `tester` which performs the SMTP sequence and writes `artifacts/pcap/traffic_e2.pcap`.
- Verify the capture and stop the stack.

## Notes
- Authentication can be simple (user/password in config) but credentials must not be logged.
- SMTP extensions (TLS, complex AUTH) or IMAP are not required. The scope is controlled.
- A subset of headers is acceptable but DATA delimitation must be correct.

### Typical pitfalls
- SMTP is implemented without a state machine; the server accepts commands in the wrong order and enters inconsistent states.
- Message storage is not atomic; under concurrent access (two POP3 sessions) loss or duplication appears.
- There is no DATA size limit which can exhaust storage or memory quickly in the laboratory.

### Indicative resources (similar examples)
- [aiosmtpd (SMTP server in Python, reference)](https://github.com/aio-libs/aiosmtpd)
- [MailHog (SMTP testing server, useful laboratory model)](https://github.com/mailhog/MailHog)
