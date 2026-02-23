# A07 — SDN learning-switch controller with flow installation and ageing

## Metadata
- **Group:** 2
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C04, C03, C13 | S06, S07, S01
- **Protocol/default ports (E2):** OpenFlow (TCP): 6653/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A07.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement an SDN controller that provides the functionality of an L2 learning switch. The controller learns the MAC→port mapping from observed packets then installs OpenFlow rules in the switch so that, after the learning phase, the controller is no longer involved for every packet.

The project targets basic control-plane mechanisms: packet-in, flow-mod, timeouts and ageing. In the demonstration you show that the first packets are flooded (unknown destination) but after learning traffic becomes unicast and can be observed in the flow table.

Bash automation is required to run repeatable scenarios: pingall, ARP generation, dump-flows, table resets and PCAP capture. The PCAP analysis must include the initial ARP broadcast and then unicast traffic after rule installation.

An SDN learning switch has two parts: learning logic in the controller (MAC→port table) and flow installation in OVS to reduce subsequent PacketIn messages. In E1 you fix the ageing policy (entry expiry) and how broadcast is treated (controlled ARP flooding). E2 requires correlation between: (1) traffic in PCAP, (2) controller logs and (3) installed flow entries, to demonstrate the transition from “reactive” forwarding to forwarding based on flow-table entries.

## Learning objectives
- Implement an SDN controller handling packet-in and flow-mod
- Learn MAC→port mappings and install OpenFlow rules with timeouts
- Observe the flood → unicast transition and correlate it with the flow table
- Automate Mininet experiments using Bash
- Build automated tests for learning and ageing

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe OpenFlow messages and the effect of flow-mod on L2 traffic in Mininet.

### Minimum scenario
- Start a Mininet topology with an OVS switch and an external controller.
- Run `pingall` and capture traffic on the switch interface.
- In parallel run periodic `ovs-ofctl dump-flows` to see when rules appear.
- Let entries expire (idle timeout) and repeat to observe ageing.

### Recommended Wireshark filters
- `tcp.port == 6633` — OpenFlow controller–switch traffic (frequently used alternative port)
- `arp.opcode == 1` — initial broadcast ARP request
- `eth.dst == ff:ff:ff:ff:ff:ff` — L2 broadcast
- `eth.type == 0x0800` — IPv4 unicast traffic after learning
- `icmp` — ping used in tests

### Guiding questions
- How the PCAP shows that first packets are flooded then become unicast
- Which rules appear in dump-flows after learning and which match fields they use
- How to verify ageing: what happens after idle timeout
- How a port change for the same MAC (MAC move) is treated

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The controller implements a learning switch: learn MAC→port from packets and maintain an internal table.
- Install OpenFlow rules for known destinations and use flooding only for unknown destinations, with configurable timeouts.
- Ageing: entries in the internal table expire after an interval and the controller adapts to new traffic.
- Bash scripts for starting the topology, running tests, dumping flows and capturing PCAP, saved under `artifacts/`.
- Deterministic ageing: fix a `MAC ageing time` (e.g. 60 s) and demonstrate entry expiry in demo/PCAP/logs.

### SHOULD (recommended)
- MAC move handling: if the same MAC appears on another port, update the table and invalidate old flows.
- Flood limiting: avoid unnecessary flooding through temporary rules or rapid learning.
- Automatic E2 report including the MAC table exported and flow dump before/after.

### MAY (optional)
- Didactic VLAN tagging support if the topology includes VLANs.
- Periodic statistics: PacketIn count, flow-mod count, learning rate.

## Non-functional requirements
- Reproducibility: the same topology and commands produce the same evidence.
- YAML configuration: idle timeout, hard timeout, flood mode, parameters for exporting the MAC table.
- Controller logs: learning events, flow installs, expiries and errors.
- Bash scripts are idempotent (can be run multiple times without breaking the environment).
- Clear separation between controller code and laboratory scripts.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Behaviour specification: when flooding occurs, when a flow is installed, which timeouts are used.
- MAC table structure and ageing policy.
- Mininet topology and demo scenario for flood→unicast plus expiry.
- E2 capture plan: ARP broadcast, ICMP unicast, correlated flow dump.
- Test plan: learning for 3 hosts and expiry after timeout.
- List of Bash scripts and their roles.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A07 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Functional controller plus a 3-host topology where hosts can communicate after learning.
- Dump-flows shows rules installed for at least two MAC pairs.
- PCAP capture shows initial ARP broadcast then ICMP unicast.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes an ARP broadcast request and ICMP packets between hosts.
- The analysis explains the transition from flooding to unicast and correlates it with installed flows.
- Include filters for broadcast and unicast plus a note on OpenFlow messages if captured.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A07.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A07.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A07 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.port==6653` | `>= 1` | OpenFlow traffic (TCP/6653) present. |
| R2 | `tcp.port==6653 && tcp.len>0` | `>= 5` | At least 5 OpenFlow segments with payload (learning plus flow installation). |
| R3 | `arp || icmp || ip` | `>= 5` | L2/L3 traffic in the network (to trigger learning). |

### Deliverables
- Docker Compose with `controller` and `tester` that run scripts and produce `artifacts/pcap/traffic_e2.pcap`.
- Bash scripts in `scripts/` for topology, test and flow-dump collection.
- Completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus MAC move handling and automatic report (recommended).
- Extended tests for expiry and concurrent traffic cases.
- Mininet demo: show learning, flow install, expiry and re-learning, with evidence in dump-flows and PCAP.
- Documented refactoring and a mini security audit for input validation and robustness.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 ---\
      s1 (OVS) --- controller
h2 ---/
h3 ----
```
Three hosts on the same switch suffice to observe flooding and unicast.

### Demo steps
- Ping h1→h2 and show initial ARP broadcast plus later flow install.
- Ping h2→h3 and show that the MAC table is completed incrementally.
- Wait for expiry and repeat a ping to show re-learning.

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
- **controller:** SDN learning-switch controller
- **tester:** runs the scenario, captures PCAP and validates flow dump

### E2 flow
- Start the controller (if containerised) and prepare the topology.
- Run `tester` which executes `pingall`, collects dump-flows and writes `artifacts/pcap/traffic_e2.pcap`.
- Stop the scenario and verify artefacts.

## Notes
- The controller must install rules, not merely forward packets in software.
- Choose timeouts so expiry is observable in the demo without taking too long.
- If an SDN library is used, document version and API.

### Typical pitfalls
- The controller floods permanently and does not install flows; the demo “works” but learning is not shown.
- Ageing is missing; the MAC table grows and stale state appears after reconnections or topology changes.
- OVS default L2 learning is confused with controller-driven learning and results become ambiguous.

### Indicative resources (similar examples)
- [osrg/ryu (example simple_switch_13)](https://github.com/osrg/ryu/blob/master/ryu/app/simple_switch_13.py)
- [os-ken (Ryu-derived OpenFlow controller)](https://github.com/openstack/os-ken)
