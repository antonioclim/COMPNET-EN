# A01 — SDN firewall: filtering policies implemented via OpenFlow rules

## Metadata
- **Group:** 2
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C13, C04, C05 | S06, S07, S13
- **Protocol/default ports (E2):** OpenFlow (TCP): 6653/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A01.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will build an SDN-controlled firewall in a Mininet topology with Open vSwitch. A controller (Python application) applies filtering policies and installs OpenFlow rules into switches so that allowed traffic and blocked traffic are demonstrable and measurable.

The policy is external to code: a configuration file describes which host pairs may communicate and which services are permitted (for example ICMP allowed only between selected pairs, HTTP allowed towards one server and the rest blocked). The controller compiles the policy into flow rules and applies them incrementally without restarting the switch.

The project requires Bash automation: start the topology, apply the policy, collect evidence (dump-flows, logs, PCAP) and generate a short report for E2. The PCAP must clearly highlight one allowed flow and one blocked flow.

An SDN firewall relies on a clear separation between decision and enforcement: the controller decides based on policy while the switch enforces via flow entries with priorities and timeouts. In E1 you specify the YAML schema for rules (fields, allowed values, evaluation order) plus a logging format for decisions (allow/deny plus reason). In E2, the PCAP and the flow dump must be correlated: a blocked packet appears in the capture as an attempt (for example SYN without success) and the corresponding installed OVS rule is visible.

## Learning objectives
- Apply SDN concepts: separation between control plane and data plane
- Translate a declarative policy into OpenFlow rules installed in the switch
- Demonstrate filtering via allowed/blocked traffic and via the flow table
- Automate scenarios with Bash and collect reproducible evidence
- Correlate OpenFlow rules with packets observed in the capture

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe control-plane traffic between controller and switch (OpenFlow) and the effect of rules on data traffic.

### Minimum scenario
- Start a Mininet topology with an external controller and an Open vSwitch instance.
- Run `ovs-ofctl dump-flows` before installing any rules to inspect the initial table.
- Send ICMP and HTTP traffic between hosts and capture on the switch interface.
- Install a drop rule manually and observe how traffic and the flow table change.

### Recommended Wireshark filters
- `tcp.port == 6653` — OpenFlow controller–switch traffic (common port)
- `icmp` — ICMP packets used for connectivity testing
- `tcp.flags.syn == 1` — TCP connection initiations, useful for observing blocking
- `arp` — ARP resolution prior to traffic
- `frame contains "OFPT"` — marker for OpenFlow messages in payload if present

### Guiding questions
- What appears in the capture when the switch has no matching rule and asks the controller (packet-in)
- How do you prove that a packet was blocked: lack of reply and absence of an allow flow
- How do you correlate a rule from `dump-flows` with observed traffic (match on IP/port)
- What difference exists between blocking a SYN and blocking later traffic in the same TCP session

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Mininet topology with at least 3 hosts and 1 OVS switch controlled by the project controller.
- External filtering policy (file) defining at least one allowed flow and one blocked flow, distinguishable in tests.
- The controller installs OpenFlow rules consistent with policy and can reload policy without restarting the topology.
- Bash automation: scripts to start topology, apply policy, generate test traffic and collect evidence (flow dump, PCAP, logs).
- Specify the OpenFlow policy with **priorities** (more specific match implies higher priority) and document rule ordering.
- Rules must explicitly handle **return traffic** (e.g. TCP ACK or ICMP reply) according to the chosen policy.

### SHOULD (recommended)
- L4 policies: allow/deny based on ports (HTTP, SSH, etc), not only on IPs.
- Return-traffic rules so permitted flows are bidirectional.
- Automatically generated E2 report (Markdown) including a summary: rules applied, traffic allowed, traffic blocked.

### MAY (optional)
- Support host groups in the declarative policy.
- Decision logs explaining why traffic was blocked, without logging every packet.

## Non-functional requirements
- Reproducibility: the Bash scripts produce the same topology and evidence set on the MININET-SDN station.
- Controlled timeout and retry for controller connection to the switch.
- The policy does not hard-code IP addresses in code; use mapping from topology/config.
- Logs for policy changes and for flow installations (count, priorities).
- Clear separation between controller code, policy config and experiment scripts.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Policy specification: format, examples and validation rules.
- Generated OpenFlow rule specification: match fields, priority, actions (drop/forward).
- Mininet topology description and host → role mapping.
- Evidence collection plan: `ovs-ofctl dump-flows`, PCAP capture and controller logs.
- Test plan: allowed case, blocked case, policy reload.
- List of Bash scripts and responsibilities (start, apply, collect).

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project A01 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- A functional controller that installs a minimal set of rules and blocks a defined flow.
- Bash script that runs one allowed test and one blocked test and collects evidence.
- PCAP capture with permitted ICMP or TCP traffic and blocked traffic.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes one allowed flow (for example ping) and one blocked attempt (for example SYN without reply).
- The analysis explains which packets are missing for the blocked case and how this appears in `dump-flows`.
- Include filters for OpenFlow (if captured) and for data-plane traffic.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A01.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A01.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A01 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.port==6653` | `>= 1` | OpenFlow control-plane traffic (TCP/6653) is present. |
| R2 | `tcp.port==6653 && tcp.len>0` | `>= 5` | At least 5 OpenFlow segments with payload (negotiation plus rule installation). |
| R3 | `ip && (tcp || udp || icmp)` | `>= 5` | Sufficient data-plane traffic to demonstrate filtering. |

### Deliverables
- Docker Compose with `tester` that runs checks and produces `artifacts/pcap/traffic_e2.pcap` (via volume).
- Bash scripts in `scripts/` used by E2 for topology and evidence.
- Completed `docs/E2_pcap_analysis.md` plus a flow-table summary.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus L4 policies and demonstrated reload without restart.
- Mininet demo with real-time policy change and observable effect on traffic.
- Extended tests for conflicting rules and priorities.
- Documented refactoring and a mini security audit for policy validation and scripts.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (client) ---\
               s1 (OVS) --- controller
h2 (server) ---/
h3 (admin) ----
```
h3 may be used for management traffic or for a special allowed flow.

### Demo steps
- Allow h1→h2 on one port and block ICMP; demonstrate by blocked ping and allowed HTTP.
- Change policy to allow ICMP and demonstrate immediate effect.
- Show `dump-flows` before and after the change.

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
- **tester:** runs automated checks and collects `artifacts/pcap/traffic_e2.pcap`
- **controller:** the controller application, executed in a container for E2 if that variant is chosen

### E2 flow
- Start the controller component (if E2 runs in containers) and prepare artefacts.
- Run `tester` which executes the Bash scripts and captures the generated traffic.
- Save `artifacts/pcap/traffic_e2.pcap` via volume and validate automatically.

## Notes
- OpenFlow traffic is visible only if you capture the correct interface; the project must document clearly where capture is performed.
- The policy must be small but sufficient to demonstrate priorities and conflicts.
- Bash scripts are part of the requirement, not an optional detail.

### Typical pitfalls
- Wrong priorities: a general rule shadows a specific rule and behaviour appears random.
- Return traffic is blocked (reverse direction) because match rules ignore ports or direction.
- Capture is taken at one point only and cannot distinguish a drop from a routing issue.

### Indicative resources (similar examples)
- [osrg/ryu (OpenFlow controller, includes examples)](https://github.com/osrg/ryu)
- [Faucet (SDN controller, policy-oriented)](https://github.com/faucetsdn/faucet)
