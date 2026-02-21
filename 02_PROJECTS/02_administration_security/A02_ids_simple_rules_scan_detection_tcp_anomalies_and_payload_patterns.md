# A02 — IDS with simple rules: scan detection, TCP anomalies and payload patterns

## Metadata
- **Group:** 2
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C13, C08, C03 | S07, S13, S04
- **Protocol/default ports (E2):** offline PCAP / IDS sensor (capture-driven).

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A02.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a didactic IDS that analyses captured traffic (live or from a PCAP file) and emits alerts based on a declarative rule set. Rules are intentionally simple to fit within a semester yet expressive enough to capture distinct attack classes: port scanning, incomplete TCP handshakes and suspicious application payload patterns.

The IDS runs in a Mininet laboratory context: you generate benign traffic and controlled malicious traffic and the system must produce reproducible evidence (PCAP, alert log, summary). The project also requires Bash automation: scripts that start the topology, generate traffic, run the IDS and collect results into an artefacts folder.

In the PCAP analysis you highlight an example scan (many SYNs to different ports) and an example payload alert. The goal is not perfect detection but traceability: rule → packets → alert.

An IDS transforms raw traffic into events: aggregation over time windows, simple evaluation rules and structured alerts (JSON) that can be consumed automatically. For scans you track patterns of connection attempts to many ports, for TCP anomalies you can use rates of SYN without completion and for payload you implement a bounded pattern matcher (without claiming full DPI). In E2, controlled scenarios (benign versus “attack” traffic) are required and the capture must justify each alert through concrete packets.

## Learning objectives
- Design an IDS rule format and implement an evaluation engine
- Detect port scanning and basic TCP anomalies using flow statistics
- Detect payload patterns in simple cleartext protocols
- Automate Mininet experiments and evidence collection using Bash
- Build automated tests for at least two rules and one negative case

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe a port scan in PCAP and identify signatures of incomplete TCP handshakes.

### Minimum scenario
- In Mininet, start a victim host with a simple service on one port and an attacker host.
- Run a controlled scan (for example TCP connects to a port list) and capture traffic at the switch.
- Then run benign traffic (an HTTP request or a small transfer) to provide contrast in the capture.
- Note the difference between a SYN without follow-up and a full handshake with SYN/SYN‑ACK/ACK.

### Recommended Wireshark filters
- `tcp.flags.syn == 1 && tcp.flags.ack == 0` — initial SYNs used in scans
- `tcp.analysis.syn_ack_retransmission` — SYN/ACK retransmissions when there is no subsequent ACK
- `tcp.flags.reset == 1` — RSTs, frequent for closed ports or aggressive scans
- `frame contains "DROP TABLE"` — payload pattern marker for a typical injection rule
- `tcp.dstport >= 1 && tcp.dstport <= 1024` — scans towards common ports (range)

### Guiding questions
- How to distinguish in the capture a port scan from a normal client connecting to a single service
- What signal indicates a closed port versus a filtered port (RST versus no reply) and how this affects detection
- How to aggregate events over a time interval to emit a scan alert
- What limitations payload-based detection has for encrypted protocols and what remains detectable

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The IDS can analyse either live traffic (interface capture) or a PCAP file, using the same rule logic.
- Declarative rules support at minimum: match on IP/port, match on TCP flags, match on substring in payload.
- Detection for at least two classes: port scanning (many SYNs to different ports) and a suspicious payload pattern (for example an SQL marker).
- Bash automation: scripts that start the Mininet topology, generate benign traffic and test traffic, run the IDS and save evidence.
- SYN scan detection: define a **time window** (e.g. 5 s) and a threshold (e.g. ≥ N distinct destination ports) that triggers an alert.
- Stated limitation (if applicable): TCP/IP reassembly is not required; specify that signatures are evaluated per packet for the E2 scenario.

### SHOULD (recommended)
- Alert output in JSON Lines with fields: timestamp, source, destination, rule, severity, description.
- Configurable thresholds per rule (window seconds, number of events) and a dry-run mode for tuning.
- Automatically generated summary report (Markdown) with alerts per rule and example packets.

### MAY (optional)
- Correlation between rules (for example scan followed by login attempts) and severity escalation.
- Export of flow statistics (top sources, top ports) in the same report.

## Non-functional requirements
- Performance sufficient for a moderate volume of Mininet traffic without blocking the topology.
- Separation between collection (capture) and analysis so that the PCAP can be re-analysed offline.
- YAML configuration: capture interface, optional BPF filters, thresholds and rule file.
- Logs: capture start/stop, loaded rules, emitted alerts, PCAP parsing errors.
- Explicit limitations: encrypted protocols cannot be inspected at payload level without keys.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Rule-format specification with examples for each type.
- Exact scan detection definition: time window, counting method, false-positive avoidance.
- Mininet topology: attacker, victim, observation/capture point.
- Evidence collection plan: PCAP plus alert log plus summary report, all generated via scripts.
- E2 capture plan: payload marker and one scan episode plus recommended filters.
- Test plan: one positive rule and one negative case (must not alert).

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A02 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- End-to-end run: topology, scan generation, scan alert detection, PCAP saved.
- One payload rule that triggers an alert on a controlled request.
- Automatically generated summary report from Bash scripts.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes a SYN sequence to different ports and a payload containing the rule marker.
- The analysis identifies relevant streams and justifies why the alert is emitted (thresholds, window).
- Include filters for SYN scan and payload pattern.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A02.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A02.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A02 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 10` | At least 10 SYN packets (scan) in the test window. |
| R2 | `tcp.flags.reset==1` | `>= 1` | Observable RST (closed port), distinguishing it from filtered. |
| R3 | `tcp.len>0 && frame contains "GET "` | `>= 1` | Payload with a pattern (e.g. HTTP GET) for a signature rule. |

### Deliverables
- Docker Compose with `ids_sensor` and `tester` (runs the scenario and produces the capture).
- Bash scripts in `scripts/` for topology, traffic and evidence collection.
- Completed `docs/E2_pcap_analysis.md` plus an alerts file in `artifacts/`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus configurable thresholds and stable JSON Lines output.
- Extended tests for rule parsing and time-window aggregation.
- Mininet demo with benign and malicious traffic, showing at least two distinct alerts.
- Documented refactoring and a mini security audit for input validation and script execution.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (attacker) ---\
                 s1 --- h2 (victim)
h3 (sensor)   ---/
```
h3 can run capture or analysis depending on design; traffic crosses s1.

### Demo steps
- Generate a scan from h1 to h2 and show the corresponding alert plus SYN packets in PCAP.
- Send a cleartext request with the payload marker and show the signature alert.
- Show a benign case that does not trigger alerts.

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
- **ids_sensor:** IDS analyser with rules
- **tester:** orchestrates scenario, runs Bash scripts, captures PCAP

### E2 flow
- Start `ids_sensor` or prepare it for offline analysis.
- Run `tester` which executes the scenario and saves `artifacts/pcap/traffic_e2.pcap` via volume.
- Generate report and verify artefacts in `artifacts`.

## Notes
- Scanning and tests are performed only in the laboratory (Mininet), not on real networks.
- Rules must be deterministic and produce reproducible alerts.
- A didactic IDS may have false positives; the project must discuss them and reduce them through thresholds.

### Typical pitfalls
- Thresholds are too low and alerts fire on normal traffic (false positives), which undermines the demonstration.
- Aggregation lacks a time window; it cannot distinguish short bursts from persistent behaviour.
- Payload pattern matching ignores encoding and TCP fragmentation; the signature is not found although the string exists.

### Indicative resources (similar examples)
- [Suricata (open-source IDS/IPS, reference)](https://github.com/OISF/suricata)
- [Zeek (network security monitor, analysis model)](https://github.com/zeek/zeek)
