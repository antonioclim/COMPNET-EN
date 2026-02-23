# A04 — ARP spoofing detection and mitigation: alerts, evidence and controlled blocking

## Metadata
- **Group:** 2
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C04, C05, C13 | S07, S06, S05
- **Protocol/default ports (E2):** ARP/IPv4

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A04.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
This project targets a classic LAN attack: ARP spoofing (poisoning) to divert traffic through an attacker host. In Mininet you build a topology with a victim, a gateway and an attacker and the system must detect suspicious changes in the IP→MAC mapping.

You implement a detector that monitors ARP (live capture) and maintains an observation table. When a suspicious event occurs (for example a gratuitous ARP that rewrites a stable mapping), the system emits an alert and triggers a controlled mitigation action.

Mitigation may be achieved either through OpenFlow rules in the switch (blocking by MAC) or through static ARP settings on relevant hosts, documented and scripted in Bash. The PCAP capture must include malicious ARP packets plus evidence that subsequent traffic is no longer diverted.

ARP spoofing detection starts from a simple laboratory assumption stated explicitly: within the Mininet segment a legitimate IP↔MAC mapping exists and should not change rapidly. The detector observes ARP replies and gratuitous ARP, maintains state and emits alerts when the same IP is associated with different MACs within a short interval. The mitigation must be reproducible: block through OpenFlow flows or through local rules (for example refuse forwarding to the suspicious MAC), with logs and a rollback mechanism for demo.

## Learning objectives
- Understand ARP and its vulnerability to spoofing in a LAN
- Implement a detection logic based on mapping changes and simple heuristics
- Automate the attack scenario and evidence collection in Mininet
- Apply a deterministic mitigation and justify its effect
- Correlate alerts with ARP packets in PCAP

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** identify normal ARP versus gratuitous ARP and observe how mapping changes appear in the capture.

### Minimum scenario
- In a Mininet topology generate normal traffic towards the gateway to trigger initial ARP resolution.
- Capture ARP traffic and note who asks and who replies.
- Generate a gratuitous ARP (manually or via a utility) and observe that the reply is not preceded by a request.
- Compare IP→MAC mappings before and after the event.

### Recommended Wireshark filters
- `arp` — all ARP traffic
- `arp.opcode == 1` — ARP request
- `arp.opcode == 2` — ARP reply
- `arp.isgratuitous == 1` — gratuitous ARP
- `eth.dst == ff:ff:ff:ff:ff:ff` — broadcast, frequent in ARP requests

### Guiding questions
- What difference exists between request and reply and how a gratuitous ARP can be recognised
- How a rewrite of IP→MAC mapping appears in PCAP and which indicators can be used for detection
- How to demonstrate that traffic was diverted through the attacker (for example by observing transit packets)
- Which mitigations are possible in a LAN and what trade-offs exist (static ARP, switch blocking)

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Mininet topology with victim, gateway, attacker and an observation point (sensor or capture on the switch).
- Reproducible attack scenario: attacker emits ARP spoofing associating the gateway IP with the attacker MAC.
- Detector identifies the suspicious event and produces an alert with context (IP, old MAC, new MAC, timestamp).
- Automatic mitigation triggered via Bash or controller: block traffic from attacker MAC or set static ARP, with evidence that diversion stops.
- Include a mitigation mechanism, e.g. install a rule (OVS/OpenFlow/iptables) that blocks the attacker MAC after detection.
- Avoid false positives: detection rule must be justified and tested on normal traffic.

### SHOULD (recommended)
- Baseline policy: mappings are considered stable only after a learning period to reduce false positives.
- Automatically generated E2 report including alerts, mappings before/after and executed commands.
- Restoration: after mitigation the topology can return to initial state (unblock) through a dedicated script.

### MAY (optional)
- SDN mitigation: install OpenFlow rules that allow ARP replies only from the gateway MAC.
- Additional detection for IP conflict (two MACs claiming the same IP).

## Non-functional requirements
- Clear Bash scripts: `run_attack.sh`, `start_capture.sh`, `apply_mitigation.sh`, `collect_evidence.sh` (names can vary but roles exist).
- Logs and alerts in JSON Lines for automated parsing.
- Input validation: detector must not fail on incomplete ARP packets.
- YAML configuration: gateway IP, trusted MAC list, thresholds and mitigation action.
- Limitation: the scenario is a laboratory scenario; document differences from real networks.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Attack scenario description plus expected mappings before and after spoofing.
- Detector specification: which events generate an alert, which thresholds, which logged fields.
- Mitigation specification: which command is executed and expected effect on traffic.
- Mininet topology and capture point for E2 plus recommended ARP filters.
- Test plan: benign case (normal ARP), malicious case (spoof), mitigation verification.
- List of Bash scripts and responsibilities.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A04 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Run full scenario: normal ARP, spoofing, alert, mitigation.
- PCAP capture containing both normal ARP and spoofing.
- Summary report with mappings before/after and mitigation commands.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes a malicious gratuitous ARP and, afterwards, evidence that diversion is absent after mitigation.
- The analysis identifies the suspicious packets and correlates alert timestamp with PCAP.
- Include ARP filters and a filter for diverted data traffic (for example ICMP between victim and gateway).

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A04.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A04.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A04 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `arp.opcode==1` | `>= 1` | ARP request present (context). |
| R2 | `arp.opcode==2` | `>= 5` | At least 5 ARP replies (spoofing is possible). |
| R3 | `arp` | `>= 10` | Sufficient ARP traffic for analysis. |

### Deliverables
- Docker Compose with `arp_detector` and `tester` that run the scenario and write `artifacts/pcap/traffic_e2.pcap`.
- Bash scripts for attack and mitigation plus evidence (ARP table dumps) in `artifacts/`.
- Completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus baseline and restoration (recommended).
- Extended tests for false positives and for more hosts in the topology.
- Mininet demo: demonstrate diversion (MITM) then blocking with evidence in PCAP and ARP tables.
- Documented refactoring and a mini security audit for scripts and input validation.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (victim) ---\
               s1 --- h2 (gateway)
h3 (attacker) -/
h4 (sensor) ----
```
h4 can be used for capture or for running the detector; traffic crosses s1.

### Demo steps
- Run ping victim→gateway and show normal ARP in PCAP.
- Run spoofing and show the mapping change plus, if MITM is simulated, appearance of transit packets at the attacker.
- Apply mitigation and show that mapping returns or attacker traffic is blocked.

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
- **arp_detector:** ARP monitor and alert generator
- **tester:** scenario orchestration (Bash), PCAP capture and evidence validation

### E2 flow
- Start `arp_detector` (if containerised) or prepare it for analysis.
- Run `tester` which executes the attack and mitigation and writes `artifacts/pcap/traffic_e2.pcap` via volume.
- Collect ARP tables and logs under `artifacts`.

## Notes
- In Mininet there is no physical switch but OVS and namespaces allow a correct ARP demonstration.
- Mitigation must be deterministic and reversible for demo.
- The attack is executed only in the laboratory with controlled hosts.

### Typical pitfalls
- The detector reacts to any variation and oscillates (no hysteresis), especially under legitimate gratuitous ARP.
- Mitigation is too aggressive (drops ARP generically) and breaks connectivity for the whole segment.
- Capture is taken only on the victim; relevant ARP events are broadcast on the segment, not necessarily visible on the victim only.

### Indicative resources (similar examples)
- [ARP Spoofing Detection (simple detection example)](https://github.com/yoelbassin/ARP-Spoofing-Detection)
- [Wireshark display filters documentation (ARP)](https://www.wireshark.org/docs/dfref/a/arp.html)
