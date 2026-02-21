# A09 — SDN IPS: dynamic blocking via OpenFlow triggered by IDS detection

## Metadata
- **Group:** 2
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C13, C04, C08 | S07, S06, S13
- **Protocol/default ports (E2):** OpenFlow+IDS: 6653/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A09.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
This project combines detection with active response: an IDS sensor identifies suspicious behaviour (for example a port scan) and triggers the installation of a blocking rule in an SDN switch. The system becomes a didactic IPS where the detect–decide–enforce loop is explicit and demonstrable.

The IDS operates on thresholds (many SYN packets to different ports within a time window) and emits a block event. The controller receives the event via a simple interface (for example local HTTP) and installs an OpenFlow rule that blocks traffic from the attacker source for a configured interval.

In the demo, the attack begins, the IDS alerts, then traffic is blocked. The PCAP must show the before/after difference and the flow dump must include the installed rule. Expiry (unblock) is also observed if a temporary-block policy is chosen.

An SDN IPS ties detection to enforcement: an IDS module produces an event and the controller installs temporary drop rules for the suspect source or flow. To prevent accidental blocking, E1 defines an expiry policy (hard/idle timeout) and a whitelisting mechanism for management traffic. In E2, the demonstration must include: detection, flow insertion, effect on traffic in PCAP and recovery after expiry, with complete logs.

## Learning objectives
- Integrate IDS detection with an SDN enforcement mechanism (OpenFlow)
- Define an IDS→controller event interface (API) and an action model
- Install and expire blocking rules in the switch with correct priorities
- Automate the full Mininet scenario with Bash and collect evidence
- Analyse the blocking effect in PCAP and in the flow table

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** identify the before/after difference when a drop rule is applied and observe control messages to the controller.

### Minimum scenario
- In Mininet run a controlled scan from attacker to victim and capture traffic.
- Apply a manual OpenFlow drop rule for the attacker and repeat the scan.
- Observe in PCAP that packets no longer reach the victim after blocking.
- If a local API exists, capture also the HTTP traffic to the controller for the block command.

### Recommended Wireshark filters
- `tcp.flags.syn == 1 && tcp.flags.ack == 0` — SYN packets used in scanning
- `http.request.uri contains "/block"` — block event sent to controller (if HTTP is used)
- `tcp.port == 6653` — OpenFlow control plane, if captured
- `tcp.analysis.retransmission` — retransmitted SYN when filtered
- `frame contains "BLOCK"` — marker for a control message in payload, if present

### Guiding questions
- How to prove that traffic is blocked at the switch, not at the victim (drop versus RST)
- Which priority a block rule must have relative to normal forward rules
- How block duration is defined and how expiry is demonstrated
- Which minimum information an IDS event must contain to block correctly

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- IDS detects a scan event (or another defined behaviour) based on configurable thresholds and emits a block alert.
- The controller receives the event and installs an OpenFlow rule that blocks source traffic (IP or MAC) towards the victim or the network, according to policy.
- Blocking is observable: flow dump shows the installed rule and a PCAP capture shows behaviour change before/after.
- Bash automation: full scenario of attack, detection, blocking and evidence collection saved under `artifacts/`.
- IDS→controller integration: specify the interface (REST/gRPC) and action semantics (block `<src_ip>` for T seconds).
- Define a block timeout (e.g. 30 s) and an automatic unblocking mechanism.

### SHOULD (recommended)
- Temporary blocking with automatic expiry and an unblock log.
- Whitelist for management traffic (for example controller access) that cannot be blocked accidentally.
- Rate limiting as an alternative to drop, configurable per rule.

### MAY (optional)
- L4 blocking (port-based) rather than total blocking to reduce impact.
- Minimal persistence of IDS events and applied actions (audit log).

## Non-functional requirements
- IDS→controller interface is locally authenticated (simple token) or isolated within the laboratory network.
- Strict input validation in the control API to avoid installing incorrect rules.
- YAML configuration: IDS thresholds, block duration, victim target, match fields for flow.
- Correlatable logs: IDS alert, controller command, flow install and observed effect.
- Bash scripts are deterministic and include cleanup (remove rules, stop processes).

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Detection specification: thresholds, time window, alert conditions, event format.
- Control API specification: endpoints, request/response, local authentication (if present).
- OpenFlow rule specification: match, priority, timeout, actions.
- Mininet topology: attacker, victim, switch, controller, capture point.
- E2 capture plan: before/after block sequence and flow dump before/after.
- Test plan: valid event, invalid event, block expiry.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A09 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Full run: scan → alert → block with no manual steps.
- Flow dump shows the installed blocking rule.
- PCAP capture contains scan traffic before and after blocking.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes SYN packets before blocking and then lack of progress after blocking (retransmissions or absence of reply).
- The analysis correlates alert time with rule installation and with the traffic change.
- Include filters for SYN, for `/block` API (if present) and for control plane (optional).

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A09.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A09.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A09 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.port==6653` | `>= 1` | OpenFlow control-plane traffic present. |
| R2 | `tcp.port==6653 && tcp.len>0` | `>= 5` | At least 5 OpenFlow segments with payload (blocking installation). |
| R3 | `tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 10` | Scan/attack traffic (SYN). |
| R4 | `icmp || tcp` | `>= 1` | Legitimate traffic (contrast) in the same capture. |

### Deliverables
- Docker Compose with `ids_sensor`, `controller` and `tester`.
- Bash scripts for scenario and flow-dump collection.
- `artifacts/pcap/traffic_e2.pcap`, alert logs and completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus automatic expiry and whitelist (recommended).
- Extended tests for multiple rules and for avoiding blocking of benign traffic.
- Mininet demo: run attack, show blocking then recovery after expiry, with evidence.
- Documented refactoring and a mini security audit for the control API and scripts.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (attacker) ---\
                 s1 (OVS) --- controller
h2 (victim)   ---/
h3 (sensor)   ----
```
h3 runs the IDS and communicates with the controller via a management network on the same switch.

### Demo steps
- Start the scan from h1 towards h2 and show the IDS alert in logs.
- Show the rule installation in `ovs-ofctl dump-flows` and that traffic no longer reaches h2.
- If blocking expires, show recovery and explain the timeout policy.

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
- **ids_sensor:** scan detection and event emission
- **controller:** receives events and installs flows
- **tester:** Bash orchestration, PCAP capture and artefact validation

### E2 flow
- Start `controller` and `ids_sensor` in containers or as processes, depending on design.
- Run `tester` which triggers the scan, waits for blocking and writes `artifacts/pcap/traffic_e2.pcap`.
- Collect flow dump and logs, then stop the stack.

## Notes
- The project is laboratory-only. It must not be used on real networks.
- The blocking rule should be as specific as possible to minimise impact.
- Temporary blocking is recommended to demonstrate expiry and to avoid persistent disruption in demo.

### Typical pitfalls
- Blocking is too general (global `ip.src`) and affects management traffic or legitimate tests.
- Drop flows have no timeout; a test event blocks permanently until manual reset.
- IDS event and IPS action are not time-correlated; without synchronised logs and PCAP, the demonstration becomes questionable.

### Indicative resources (similar examples)
- [os-ken (OpenFlow controller, useful for inserting flows)](https://github.com/openstack/os-ken)
- [Faucet (examples of policies plus flow control)](https://github.com/faucetsdn/faucet)
