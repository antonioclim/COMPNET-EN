# A03 — PCAP report generator: flow statistics, top talkers and TCP indicators

## Metadata
- **Group:** 2
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C13 | S07, S01, S02
- **Protocol/default ports (E2):** offline PCAP analysis

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A03.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will build a PCAP analysis tool that produces a reproducible technical report: top talkers, protocol distribution, TCP/UDP flows, retransmissions, estimated RTT and connection-quality indicators. The goal is to move beyond manual Wireshark inspection and towards an automated summary that can run in a pipeline.

The project includes a Mininet scene that generates mixed traffic (for example ICMP, HTTP, DNS and a TCP transfer). The resulting capture becomes the input to the tool and the output is a Markdown report and a JSON file of metrics, both saved under `artifacts/`.

Bash automation is required: a script starts the topology, runs traffic generation, stops the capture then runs the analysis and produces the report. Traceability is essential: each number in the report must be linked to a `tshark` query or to a clearly defined calculation.

A PCAP report generator is an exercise in measurement: define what a “flow” means, aggregate on the 5‑tuple and compute TCP indicators that can be verified (retransmissions, out-of-order, successful versus failed handshake). To avoid unstable results, E1 fixes the exact metric set and calculation method (time windows, units, treatment of incomplete connections). In E2, the same capture must be usable both for the report and for manual verification in Wireshark (Statistics → Conversations/IO Graph), so that students can correlate tools.

## Learning objectives
- Extract metrics from a PCAP and aggregate them per flow
- Interpret TCP indicators (retransmissions, estimated RTT, bytes in flight)
- Automate capture generation in Mininet and offline analysis
- Design stable report outputs (Markdown/JSON) for assessment
- Validate results by comparing with Wireshark and `tshark` statistics

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** compare Wireshark statistics with what can be extracted automatically via filters and fields.

### Minimum scenario
- Take a short capture with TCP traffic and introduce delay or loss on a link in Mininet.
- In Wireshark inspect `Statistics → Conversations` and `TCP Stream Graphs` for RTT and retransmissions.
- Note Wireshark fields that can be used as filters (for example `tcp.analysis.ack_rtt`).
- Decide which metrics are useful in a report and at which granularity (per host, per flow).

### Recommended Wireshark filters
- `tcp.analysis.retransmission` — TCP retransmissions, an indicator of loss or congestion
- `tcp.analysis.ack_rtt > 0.05` — estimated RTT above a threshold, useful for observing delay
- `frame.len > 1000` — large packets typical of a file transfer
- `dns` — DNS traffic (if present) to report resolution timings
- `http` — HTTP traffic to report status codes and resources

### Guiding questions
- Which metrics are robust on short captures and which become unstable
- How retransmissions should be aggregated correctly: per flow or per host
- How RTT can be estimated from a PCAP without application timestamps
- How to report control traffic (DNS) separately from data traffic (HTTP/TCP transfer)

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- A Mininet scenario that generates mixed traffic and produces a reproducible input PCAP.
- An analysis tool that extracts at minimum: top talkers (bytes), number of flows, TCP retransmissions, estimated RTT (median) per flow.
- Dual output: a Markdown report with tables and a JSON file with raw metrics.
- Bash automation that runs end-to-end: topology → traffic → capture → report, storing outputs under `artifacts/`.
- PCAP parsing uses a library (e.g. `pyshark`, `scapy`, `dpkt`) — a pure wrapper around `tshark` without your own processing is not accepted.
- Deterministic report: generate JSON and (optionally) CSV for top talkers, flows, retransmissions and estimated latencies.

### SHOULD (recommended)
- Simple anomaly detection: flows with many retransmissions, high RTT or unusual packet rates.
- Time-window segmentation to show evolution over time.
- Report validation: for at least one metric include the equivalent `tshark` command as reference.

### MAY (optional)
- HTML export for the report while keeping Markdown for quick review.
- Offline plots (matplotlib) for RTT or retransmission evolution.

## Non-functional requirements
- The tool runs in reasonable time on captures of a few MB without excessive memory use.
- YAML configuration: included fields, anomaly thresholds, input/output paths.
- Reproducibility: the report includes a hash of the analysed PCAP and a generation timestamp.
- Logs for analysis steps and parsing errors.
- Bash scripts do not assume extra privileges beyond what is needed for capture in Mininet.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Metric definitions and formulas: what is computed and how it is aggregated.
- Structure of JSON output and Markdown report (sections and tables).
- Mininet topology and generated traffic types to cover the metrics.
- E2 capture plan: where capture happens and what minimum traffic volume is required.
- Test plan: validation on a small capture with expected outcomes (for example 0 retransmissions).
- List of Bash scripts: traffic generation, capture, report.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A03 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Generate a PCAP containing TCP traffic with at least one source of delay or loss.
- Run the tool and produce the Markdown report and JSON metrics.
- The report includes at least top talkers and a flow identified as high RTT or with retransmissions.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` is the analysed PCAP and is produced automatically by the E2 scenario.
- The analysis (`docs/E2_pcap_analysis.md`) describes two metrics and shows how they appear in the capture (via filters).
- One concrete example is mentioned: a flow with RTT above a threshold.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A03.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A03.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A03 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp` | `>= 50` | At least 50 TCP packets for statistics (flows, retransmissions). |
| R2 | `tcp.analysis.retransmission` | `>= 1` | At least one retransmission (TCP indicator). |
| R3 | `ip` | `>= 50` | At least 50 IP packets (top talkers). |

### Deliverables
- Docker Compose with `pcap_reporter` and `tester` that run the scenario and write artefacts.
- Bash scripts for traffic generation and capture under `scripts/`.
- `artifacts/pcap/traffic_e2.pcap`, Markdown report and JSON plus `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus anomalies and time windows (recommended).
- Extended tests for PCAP parsing and JSON output stability.
- Mininet demo: run two scenarios (good link versus lossy link) and show differences in the report.
- Documented refactoring and a mini security audit for input file handling and path validation.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (client) --- s1 --- h2 (web_server)
                 |
                 +--- h3 (dns_server)
```
Delay/loss is applied on one link to create an observable effect in RTT and retransmissions.

### Demo steps
- Run a set of HTTP requests and a DNS lookup then a larger TCP transfer.
- Generate the report and indicate top talkers and median RTT for the main flow.
- Compare the report between two link settings (with and without loss).

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
- **pcap_reporter:** PCAP analysis tool
- **tester:** runs the scenario and produces `artifacts/pcap/traffic_e2.pcap` and reports

### E2 flow
- Run `tester` which generates the capture then invokes `pcap_reporter` on the resulting PCAP.
- Save via volume `./artifacts:/artifacts` for PCAP and reports.
- Automatically verify output format (Markdown and JSON).

## Notes
- The tool does not need to reimplement all of Wireshark. Focus on carefully chosen metrics that can be explained.
- For consistency, the report must fix units and specify the analysed time interval.
- The capture produced in E2 becomes the input; avoid external PCAP files during assessment.

### Typical pitfalls
- Flows are aggregated only by port rather than by 5‑tuple, so reports mix distinct flows.
- Timestamps are not normalised (timezone, epoch) and plots/time windows become meaningless.
- Retransmission interpretation is done without controlling offloading, creating discrepancies between host and capture.

### Indicative resources (similar examples)
- [Scapy (packet crafting and parsing in Python)](https://github.com/secdev/scapy)
- [Wireshark (sources plus analyser reference)](https://github.com/wireshark/wireshark)
