# A08 — Encapsulation and tunnelling in Mininet: VXLAN between two sites

## Metadata
- **Group:** 2
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C04, C05, C06 | S06, S05, S07
- **Protocol/default ports (E2):** VXLAN (UDP): VXLAN 4789/UDP (recommended VNI: 1010).

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A08.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will build an encapsulation laboratory using VXLAN to connect two L2 sites over an L3 underlay. Each site contains a local host and a router (VTEP) and between the two VTEPs you create a VXLAN tunnel over UDP.

The goal is twofold: configuration (ip link, bridge, FDB, VNI) and verification through traffic and capture. In the demo, two hosts from different sites communicate as if they were in the same L2 segment and the PCAP must highlight encapsulated packets: external UDP/VXLAN header and the internal frame.

Bash automation is essential: scripts set up the VTEPs, create bridges, attach interfaces, set MTU and collect evidence. The project must also include a troubleshooting scenario (for example insufficient MTU) with evidence in the capture.

VXLAN in Mininet is an infrastructure laboratory project: two separate L2 “sites” are connected through an L3 tunnel, with explicit VNI and configured VTEPs. In E1 define exactly: VTEP addresses, VNI, MTU (accounting for overhead) and the verification method (ping between hosts in different sites, plus a capture showing encapsulation). The PCAP becomes central if you capture on the underlay interface: you observe UDP/4789 (VXLAN) and, in payload, the original Ethernet frame (inner).

## Learning objectives
- Configure a VXLAN tunnel in Linux and integrate it into an L2 bridge
- Understand underlay versus overlay and the effect of encapsulation on MTU
- Demonstrate connectivity over VXLAN and the structure of encapsulated packets
- Fully automate the laboratory using Bash scripts
- Analyse PCAP focusing on the external header and internal frame

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe a VXLAN packet in capture and identify outer and inner headers.

### Minimum scenario
- In an existing VXLAN configuration (or in a laboratory), capture traffic on the underlay interface between VTEPs.
- Send a ping between hosts in different sites and identify the encapsulated packet.
- In Wireshark inspect the outer UDP header, the VXLAN header and then the inner Ethernet frame.
- Verify the UDP port used (usually 4789) and VNI.

### Recommended Wireshark filters
- `vxlan` — VXLAN traffic
- `udp.port == 4789` — standard VXLAN UDP port
- `vxlan.vni` — VNI identifier used in the overlay
- `eth.type == 0x0806` — ARP in the inner frame, useful for L2 bootstrap
- `icmp` — ping inside the overlay

### Guiding questions
- Which fields appear in the VXLAN header and what role VNI has
- How outer IP/UDP differs from the inner Ethernet frame in the capture
- What overhead encapsulation introduces and how it affects MTU and fragmentation
- How to troubleshoot lack of connectivity: FDB, bridge, MTU, ARP

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Mininet topology with two sites, each with a host and a VTEP, connected through an L3 underlay.
- VXLAN configuration via Bash scripts: create vxlan interface, set VNI, add it to a bridge, configure underlay IP and bridge.
- Overlay connectivity: hosts from different sites can communicate at L2/L3 (ping) over the VXLAN tunnel.
- PCAP capture that shows encapsulated VXLAN packets, identifying outer and inner headers and the VNI.
- Fix: competency mapping without C09; specify VNI (e.g. 1010) and MTU (VXLAN overhead) plus verification method.
- Include end-to-end verification (ping/arp) between hosts in different segments through VXLAN.

### SHOULD (recommended)
- MTU scenario: demonstrate a packet that exceeds MTU then fix it by adjusting MTU; evidence in PCAP.
- Diagrams and evidence: `ip link`, `bridge fdb show`, `ip neigh` saved under `artifacts/`.
- A cleanup script that restores the system to initial state.

### MAY (optional)
- Multicast-based VXLAN versus static unicast FDB, explaining the differences.
- Two different VNIs for two overlay segments, demonstrable.

## Non-functional requirements
- Bash scripts are idempotent and check preconditions (available commands, permissions).
- YAML configuration: VNI, port, underlay IPs, MTU, host mapping.
- Logs for each configuration step and for errors.
- Capture is taken on the underlay interface to observe full encapsulation.
- Document explicitly limitations of Mininet relative to real equipment.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Underlay/overlay description: addresses, VNI, port, MTU, flows.
- Specification of Bash steps for VTEP and bridge configuration.
- Mininet topology and demo scenario including a fault case (MTU).
- E2 capture plan: where to capture to see VXLAN and which filters to use.
- Test plan: ping, ARP learning, MTU break/fix.
- List of Bash scripts: setup, test, capture, cleanup.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A08 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- VXLAN tunnel configured automatically by script and ping connectivity between hosts.
- PCAP capture with VXLAN traffic on the underlay.
- Collect configuration evidence (ip link, bridge, fdb) under `artifacts/`.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes VXLAN packets (UDP 4789) with the correct VNI.
- The analysis describes the packet structure: outer IP/UDP, VXLAN header, inner Ethernet then ICMP.
- Include filters `vxlan` and `vxlan.vni` to isolate overlay traffic.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A08.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A08.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A08 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `udp.port==4789` | `>= 5` | VXLAN traffic (UDP/4789) is present. |
| R2 | `arp || icmp` | `>= 1` | L2/L3 traffic transported through the tunnel (ARP/ICMP) is observable. |

### Deliverables
- Docker Compose with `tester` that runs scripts and produces `artifacts/pcap/traffic_e2.pcap`.
- Bash scripts in `scripts/` for setup and evidence collection.
- Completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus MTU scenario and cleanup (recommended).
- Extended tests for two VNIs or configuration change without a full restart.
- Mininet demo with two sites and capture on the underlay, highlighting overhead and MTU.
- Documented refactoring and a mini security audit for scripts (input validation, avoidance of dangerous commands).

## Mininet topology and demo scenario
### Topology (ASCII)
```
Site A: h1 --- r1 (VTEP) ---\
                              s_underlay --- r2 (VTEP) --- h2 : Site B
```
r1 and r2 are VTEPs connected on the underlay; h1 and h2 are in the overlay via VXLAN.

### Demo steps
- Configure VXLAN, run ping h1→h2 and show the VXLAN packet in PCAP.
- Simulate insufficient MTU with a larger payload and show the effect (fragmentation or drop).
- Fix MTU and demonstrate connectivity again.

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
- **tester:** runs setup/test/capture, writes `artifacts/pcap/traffic_e2.pcap` and evidence

### E2 flow
- Run `tester` which invokes the Bash scripts for VXLAN configuration.
- Generate traffic and capture on the underlay, saving via volume.
- Collect evidence (`ip link`, `bridge fdb`) under `artifacts`.

## Notes
- VXLAN is an overlay example. The project must explain clearly what is underlay and what is encapsulated.
- In Mininet, interfaces are namespaces; nevertheless, ip link and bridge work for demonstration.
- It is recommended to keep the VNI and standard port for simplicity.

### Typical pitfalls
- MTU is not adjusted; the overlay works only for small packets while larger ones fragment or are lost.
- VNI/VTEP mismatch between ends; the underlay has UDP 4789 traffic but the overlay has no connectivity.
- Capture is taken on the overlay rather than on the underlay; encapsulation is not visible and the demonstration loses its central evidence.

### Indicative resources (similar examples)
- [Open vSwitch (VXLAN/OVS support)](https://github.com/openvswitch/ovs)
- [iproute2 (Linux utilities for link/vxlan)](https://github.com/iproute2/iproute2)
