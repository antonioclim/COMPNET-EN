# A05 — Laboratory port scanning: TCP connect scan and minimal service fingerprinting

## Metadata
- **Group:** 2
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C13, C08, C03 | S13, S07, S02
- **Protocol/default ports (E2):** TCP scan (laboratory topology only)

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A05.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a laboratory port scanner, used exclusively inside controlled Mininet topologies. The scanner uses standard TCP connection attempts (connect scan) with configurable timeouts and controlled concurrency to classify ports as open, closed or filtered (no response).

For open ports the scanner applies minimal fingerprinting: banner grabbing (for example SSH), sending a small HTTP request and extracting headers or other lightweight probes. The result is a structured report (JSON) with ports, response times and a service label.

The project requires Bash automation: scripts start a victim host with exposed services (HTTP, SSH mock, etc), run the scan, capture traffic and generate a short summary. The PCAP must contain the connection attempts and at least one banner or an HTTP response.

Port scanning is framed as laboratory inventory, not as a general-purpose tool. In E1 you must define explicitly the permitted scan scope (Mininet subnet, permitted ports, rate limit) and in E2 you demonstrate two techniques: TCP connect scanning and minimal fingerprinting through banner or protocol response. In the PCAP you must show the difference between open ports (SYN/SYN‑ACK/ACK), closed ports (RST) and filtered ports (timeouts with SYN retransmissions).

## Learning objectives
- Understand TCP scan signatures in traffic (SYN, RST, timeouts)
- Implement deterministic TCP scanning with timeouts and controlled concurrency
- Implement minimal fingerprinting for a small set of services
- Generate a reproducible scan report that can be verified
- Collect evidence through PCAP and correlate it with scanner output

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe a TCP scan in Wireshark and distinguish closed ports (RST) from filtered ports (timeout).

### Minimum scenario
- In Mininet, start a victim host with one open port (for example 80) and leave other ports closed.
- Run a series of TCP connections to a port set and capture traffic.
- Add a drop rule for one port (filtered) and repeat to observe lack of response.
- For an open port, read a banner or an HTTP response to observe payload.

### Recommended Wireshark filters
- `tcp.flags.syn == 1 && tcp.flags.ack == 0` — connection initiations to scanned ports
- `tcp.flags.reset == 1` — RST as a signal of a closed port
- `tcp.analysis.retransmission` — SYN retransmissions when no reply exists (filtered port)
- `frame contains "SSH-"` — SSH banner, if a mock SSH service is used
- `http.response.code` — HTTP responses used for fingerprinting

### Guiding questions
- How the capture shows the difference between closed and filtered ports and what it implies for classification
- How to limit concurrency and rate to avoid overloading the laboratory environment
- What probes are sufficient to distinguish an HTTP service from a port that merely accepts a connection
- How to correlate scanner-reported timings with observables in the capture (RTT, retransmissions)

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- TCP connect scanner that accepts a port list or range and produces open/closed/filtered classification with configurable timeouts.
- Controlled concurrency (thread pool or asyncio) and rate limiting to preserve predictability in Mininet.
- Minimal fingerprinting for open ports: at least banner grab (SSH or a mock service) and a simple HTTP request (if the port is HTTP).
- Bash automation: scripts for starting victim services, running the scan, capturing PCAP and saving the report under `artifacts/`.
- Responsible scanning: implement rate limiting (e.g. max 200 probes/s) and a default “polite” mode.
- Minimal fingerprinting: after detecting an open port attempt banner grabbing (e.g. `SSH-2.0`, `HTTP Server:`) with a short timeout.

### SHOULD (recommended)
- Deterministic JSON output with fields: port, state, service_guess, latency_ms, probe_details.
- Exclusions (skip list) and a limit on the number of scanned ports in E2.
- Automatically generated Markdown summary report listing open ports and successful probes.
- (E3 extension) SYN scan with raw packets (Scapy) in the laboratory if the environment permits.

### MAY (optional)
- UDP scanning on one specific port, with the warning that interpretation is ambiguous without a reply.
- Detect a custom laboratory service based on a marker in the banner.

## Non-functional requirements
- Safety: run only in controlled Mininet topologies. Documentation includes this limitation explicitly.
- Timeout and controlled retries: no infinite attempts; each port has a maximum number of probes.
- YAML configuration: timeouts, rate limit, port list/range, probe set.
- Logs: scan progress, socket errors, aggregated results.
- Testability: victim provides deterministic services to minimise fingerprint variability.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Scan algorithm specification: how open/closed/filtered is classified and which timeouts are used.
- Fingerprinting probe specification: which ports are probed and what is extracted (banner, headers).
- Mininet topology: scanner, victim, additional host for benign noise (optional).
- E2 capture plan: SYN, RST and one payload example (banner/HTTP).
- Test plan: open port, closed port, filtered port, plus one rate-limiting case.
- List of Bash scripts: service setup, scan run, capture, report.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A05 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Scan a small range (for example 20 ports) against a victim with 1–2 open services.
- Generate a JSON report and a Markdown summary.
- Produce a PCAP capture containing attempts to closed ports and a response from an open port.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes SYNs to multiple ports, RSTs for closed ports and a full flow to an open port.
- The analysis correlates one open port in the report with packets that show a complete handshake and payload (banner or HTTP).
- Include filters for SYN and for fingerprinting payload.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A05.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A05.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A05 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 20` | At least 20 SYN packets (port scan). |
| R2 | `tcp.flags.syn==1 && tcp.flags.ack==1` | `>= 1` | At least one SYN-ACK (open port). |
| R3 | `tcp.flags.reset==1` | `>= 1` | At least one RST (closed port). |
| R4 | `tcp.len>0 && (frame contains "SSH" || frame contains "HTTP" || frame contains "Server:")` | `>= 1` | Minimal fingerprinting (banner/header). |

### Deliverables
- Docker Compose with `scanner` and `tester` that run the scenario and write `artifacts/pcap/traffic_e2.pcap`.
- Bash scripts in `scripts/` for victim-service setup and capture.
- Completed `docs/E2_pcap_analysis.md` plus JSON report in `artifacts/`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus stable output and demonstrable rate limiting.
- Extended tests for classification (timeout versus RST) and for probes on open ports.
- Mininet demo: compare scanning with small and large rate limits and show the effect in PCAP (SYN/s).
- Documented refactoring and a mini security audit for input validation (range, IP) and error handling.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (scanner) --- s1 --- h2 (victim)
                 |
                 +--- h3 (benign)
```
h3 can generate benign traffic (for example HTTP) to test that the capture does not confuse it with scanning.

### Demo steps
- Start services on h2, run the scan from h1 and show detected open ports.
- Show in PCAP a closed port (RST) and a filtered port (SYN retransmissions).
- Show a banner or HTTP response used for fingerprinting.

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
- **scanner:** TCP connect scanner plus fingerprinting
- **tester:** Bash orchestration, PCAP capture and output verification

### E2 flow
- Start victim services (in Mininet or containers, depending on design).
- Run `tester` which invokes the scanner and writes `artifacts/pcap/traffic_e2.pcap` and reports.
- Validate output format then stop the scenario.

## Notes
- The scanner does not use raw packets or evasion techniques. The scope is didactic and safe.
- For filtered ports, interpretation is probabilistic; the project must explain the conditions.
- Avoid scanning large ranges in E2 to keep captures short.

### Typical pitfalls
- No rate limiting: in topologies with delay/loss results become unreliable (timeouts misinterpreted).
- RST from a middlebox/firewall is interpreted as destination response, making closed/filtered classification incorrect.
- Banner grabbing without timeouts blocks the scanner on services that accept connections but do not answer.

### Indicative resources (similar examples)
- [Nmap (classic scanning reference)](https://github.com/nmap/nmap)
- [masscan (fast scanning, optimisation model)](https://github.com/robertdavidgraham/masscan)
