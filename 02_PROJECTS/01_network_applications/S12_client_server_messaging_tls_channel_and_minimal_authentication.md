# S12 — Client–server messaging with a TLS channel and minimal authentication

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C13 | S02, S07, S04
- **Protocol/default ports (E2):** TCP/TLS: TLS 5443/TCP (E2/E3); optional plain 5002/TCP for Phase 0 comparison.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S12.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
This project requires a messaging application over TCP where transport is secured via TLS using the standard `ssl` library. The goal is a clear separation between the problem of securing the channel and the problem of the application protocol: the protocol remains simple but complete, with framing and errors.

A key component is server identity verification: the client does not connect blindly but validates the certificate through a local CA or via pinning. In addition, the project includes a minimal security policy (timeouts, input limits, logs without sensitive data).

In PCAP, the TLS handshake is observable but the application payload becomes opaque. In the analysis you explain what can still be deduced from metadata (SNI, negotiated suites, sizes) and what is no longer visible after the channel is established.

TLS shifts attention away from “hand-made cryptography” towards key and certificate management: who signs, what is verified, what is logged and what is refused. In E1 you must state explicitly the policy: server authentication required, optional mutual TLS and how the client validates hostname and expiry. For Wireshark, the project becomes particularly instructive if you use `SSLKEYLOGFILE` to decrypt traffic in the laboratory and show the difference between encrypted payload and interpretable payload when following a TLS stream.

## Learning objectives
- Configure a TLS server with certificate and key without hardcoding secrets in source code
- Implement a TLS client that verifies the server certificate correctly
- Define a minimal application protocol over TLS with framing and error codes
- Capture and interpret the TLS handshake in Wireshark
- Build automated tests for secure connection establishment and a minimal message exchange

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **TLS client** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **connect, validate the server certificate and exchange at least one application message**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP/TLS: TLS 5443/TCP (E2/E3); optional plain 5002/TCP for Phase 0 comparison.
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
**Objective:** identify the TLS handshake stages and the difference between handshake and application data in a capture.

### Minimum scenario
- Run a test TLS server (for example `openssl s_server`) and a TLS client (`openssl s_client`) on a controlled network.
- Capture traffic and identify `ClientHello`, `ServerHello` and certificate exchange.
- Send a short text after the handshake and observe that the payload is no longer readable.
- Note which fields remain visible: SNI, TLS version, cipher suite.

### Recommended Wireshark filters
- `tls.handshake.type == 1` — ClientHello
- `tls.handshake.type == 2` — ServerHello
- `tls.handshake.ciphersuite` — negotiated cipher suites
- `tls.record.content_type == 23` — TLS Application Data (encrypted payload)
- `ssl.handshake.extensions_server_name` — SNI if used

### Guiding questions
- What difference exists between handshake and application data and how it appears in Wireshark
- How a server certificate should be validated correctly and what happens with an invalid certificate
- What information can still be observed from a TLS stream without decryption
- Which minimum security settings should be enforced (version, timeouts, prohibitions)

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The server accepts TLS connections using certificate and key provided via configured files, not embedded as strings in code.
- The client validates the identity of the server (local CA or pinning) and refuses to connect when the certificate is invalid.
- Application protocol over TLS with framing and minimal commands (for example authenticate user and send a message) plus OK/ERR responses.
- Logs include connection events and TLS errors without logging plaintext payload or keys.
- Automated tests validate TLS connection and a request–response exchange, producing a PCAP capture.
- Authentic TLS: the server certificate is signed by a laboratory CA and the client validates the chain (no `verify=False`).
- Document in E1 the authentication policy: server-auth only (minimum) or mutual TLS (E3).

### SHOULD (recommended)
- Mutual TLS (client certificate) as a configurable option, with mapping certificate → user.
- Timeout and limit policy (payload, number of connections) to prevent blocking or excessive resource use.
- Explicit prohibitions: old TLS versions and weak cipher suites, documented in E1.

### MAY (optional)
- Periodic certificate rotation in the demo (reload on signal or on interval).
- An audit mode that lists the negotiated TLS parameters for each connection.

## Non-functional requirements
- Separation between TLS layer and application protocol: distinct functions and separate tests.
- Framing and input limits applied after decryption, refusing oversized messages.
- Timeout for handshake and reads; incomplete connections close deterministically.
- Safe handling of key files: do not commit them to Git; generate locally or inside containers.
- YAML configuration: port, paths to certificates, CA path, mutual TLS on/off, timeouts.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- TLS specification: accepted versions, certificate validation method, required files and local generation steps.
- Application protocol specification: commands, framing, error codes and examples.
- Sequence diagram: TLS handshake (conceptual) followed by an application message exchange.
- Mininet topology with server and two clients with capture on the switch.
- E2 capture plan: handshake visible and application data opaque, with recommended TLS filters.
- Test plan: valid connection, refused connection (invalid cert), application message.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S12 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- The TLS server starts in Docker with certificate available in the container.
- The tester connects with certificate validation and executes one application request with an OK response.
- PCAP includes a complete TLS handshake and at least one application-data record.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` highlights `ClientHello` and `ServerHello` and certificate exchange.
- The analysis shows the transition to `TLS Application Data` and explains why application payload is not readable.
- Mention negotiated parameters (version, cipher suite) observed in the capture.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S12.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S12.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S12 --pcap artifacts/pcap/traffic_e2.pcap`
- Decode-as used during validation: `tcp.port==5443,tls`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==5443 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | TCP handshake to the TLS service. |
| R2 | `tls.handshake.type==1` | `>= 1` | ClientHello in the TLS handshake. |
| R3 | `tls.handshake.type==2` | `>= 1` | ServerHello in the TLS handshake. |
| R4 | `tls.handshake.type==11 || tls.handshake.certificate` | `>= 1` | Server certificate transmitted. |
| R5 | `tcp.port==5443 && tcp.len>0` | `>= 3` | Application traffic over TLS (data-bearing segments). |

### Deliverables
- Docker Compose with `tls_server` and `tester`.
- Smoke tests (`pytest -m e2`) verifying handshake and a minimal message exchange.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus a controlled failure scenario for an invalid certificate.
- Additional tests for mutual TLS (if implemented) and timeouts.
- Mininet demo with two clients: one valid, one with wrong CA (refused), with evidence in logs.
- Documented refactoring and a mini security audit for TLS configuration and key handling.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (tls_server) --- s1 --- h2 (valid client)
                    |
                    +--- h3 (invalid client)
```
h3 uses a wrong CA or an invalid certificate to demonstrate refusal.

### Demo steps
- From h2 connect and exchange one application message; show handshake and application data in PCAP.
- From h3 attempt to connect and show refusal with an error in logs and no established session.
- Show in Wireshark the TLS filters used in the analysis.

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
- **tls_server:** application server over TLS, configured with certificates
- **tester:** automated TLS client, validates certificate and captures PCAP

### E2 flow
- Start `tls_server` with certificate files mounted or generated at build time.
- Run `tester` which executes handshake and one application request, writing `artifacts/pcap/traffic_e2.pcap`.
- Validate capture and stop the stack.

## Notes
- Do not implement your own cryptography. Use TLS via standard libraries.
- Certificates and keys must not be committed in the team repository.
- For application messages, framing remains mandatory even if transport is secured.

### Typical pitfalls
- The client disables certificate verification (`CERT_NONE`) and TLS becomes merely formal rather than secure.
- Certificates/keys are treated as generic files and accidentally end up in the repository or logs.
- TLS handshake errors are confused with application errors; logs do not clearly distinguish the two classes.

### Indicative resources (similar examples)
- [Python ssl documentation (TLS over sockets)](https://docs.python.org/3/library/ssl.html)
- [pyca/cryptography (cryptographic primitives and recipes)](https://github.com/pyca/cryptography)
