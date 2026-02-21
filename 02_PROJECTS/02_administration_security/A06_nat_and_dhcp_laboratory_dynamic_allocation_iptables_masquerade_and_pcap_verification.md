# A06 — NAT and DHCP laboratory: dynamic allocation, iptables MASQUERADE and verification via PCAP

## Metadata
- **Group:** 2
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C06, C05, C03 | S05, S06, S07
- **Protocol/default ports (E2):** DHCP (UDP) plus NAT: DHCP server 67/UDP, client 68/UDP (Mininet/namespace); NAT via iptables MASQUERADE.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A06.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You design a Mininet topology with an internal network (clients) and an external network (server), separated by a gateway that performs NAT. Internal clients do not have statically configured IP addresses: they obtain addresses via DHCP and must then reach an external service (for example HTTP) through the NAT gateway.

The emphasis is on administration and verification: iptables MASQUERADE, forwarding rules, DHCP configuration and observing the effect in a capture. A specific goal is to demonstrate, via PCAP, the DHCP DORA sequence and, separately, that packet sources towards the external network are rewritten by NAT.

Bash automation is central: scripts start the topology, configure the gateway, start services, run test requests and collect evidence (iptables ruleset, DHCP leases, PCAP).

The NAT plus DHCP laboratory combines configuration (iptables, routing) with observability (DORA in PCAP). The DHCP server may be minimal but must respect the order DISCOVER→OFFER→REQUEST→ACK and manage a configurable pool with lease time. NAT is assessed through a concrete scenario: a host from an “internal” subnet accesses a service in an “external” subnet and the capture shows address translation (pre/post NAT). Bash is used to set namespaces and rules consistently and to collect artefacts (`iptables-save`, `ip route`).

## Learning objectives
- Configure DHCP in an isolated environment and verify address allocation
- Configure NAT with iptables and understand the difference between DNAT and SNAT/MASQUERADE
- Demonstrate connectivity internal client → external server and default inbound isolation
- Collect configuration and traffic evidence using Bash
- Design automated tests that validate both DHCP and NAT

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe DORA (DHCP) and address rewriting on NAT egress.

### Minimum scenario
- Start a client without static IP and a DHCP server in a local network and capture traffic.
- Run `dhclient` (or equivalent) and identify Discover, Offer, Request, Ack.
- After obtaining the IP, run a ping to a host outside the local network and capture traffic on both gateway interfaces.
- Compare the source address of packets on the internal versus external gateway interface.

### Recommended Wireshark filters
- `bootp` — DHCP is dissected as BOOTP in Wireshark
- `bootp.option.dhcp == 1` — DHCP Discover
- `bootp.option.dhcp == 2` — DHCP Offer
- `bootp.option.dhcp == 3` — DHCP Request
- `bootp.option.dhcp == 5` — DHCP Ack

### Guiding questions
- Which DHCP fields link request and response (transaction ID, chaddr)
- What information the server delivers: IP, gateway, DNS and lease time and where it appears in the capture
- How NAT rewriting is demonstrated by comparing captures from different interfaces
- Which iptables rules are required to enable forwarding and MASQUERADE

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Mininet topology with at least 3 hosts: two internal clients, one gateway and one external server, with two distinct subnets.
- Working DHCP for internal clients: IP allocation, gateway and lease time without manual configuration on clients.
- NAT on the gateway using iptables MASQUERADE so that internal clients can access the external server while inbound access is blocked by default.
- Bash scripts that configure DHCP and NAT, run connectivity tests and collect evidence (PCAP, `iptables-save`, lease file).
- PCAP capture must be taken on the gateway on interface `any` (or on both interfaces) to demonstrate DORA and NAT in the same capture.
- DHCP server clarification: `dnsmasq` is accepted **or** a minimal implementation; in both cases artefacts (config, leases) plus justification are required.

### SHOULD (recommended)
- Port forwarding (DNAT) for a controlled internal service exposed to the external side, with a documented rule.
- DHCP reservations for at least one client (MAC → fixed IP) to facilitate testing.
- Automatically generated E2 report that includes DORA and a NAT comparison (internal versus external).

### MAY (optional)
- Local DNS caching on the gateway for clients, with evidence in the capture of resolutions.
- Traffic limitation (`tc`) on the external link to observe the effect on connections.

## Non-functional requirements
- Reproducibility: topology and configuration are rebuilt entirely through scripts, with no manual steps.
- Security: iptables rules are explicit and do not leave forwarding fully open without justification.
- YAML configuration: subnets, DHCP pool, interfaces, service ports.
- Logs and evidence: each script writes under `artifacts/` what it executed and what results were obtained.
- PCAP capture short enough for easy inspection but complete for DORA and NAT.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Subnet description and addressing plan for clients, gateway and external server.
- DHCP configuration specification: pool, lease time, options (router, DNS).
- iptables rule specification: forwarding, MASQUERADE and optional DNAT.
- Mininet topology and test commands (curl/ping) plus capture points for E2.
- Test plan: obtain IP, external HTTP access, inbound blocking and port forward if present.
- List of Bash scripts and roles.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A06 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Internal client receives IP via DHCP and can access the external server (curl or ping).
- Gateway has iptables rules set by script and exported into artefacts.
- PCAP capture contains DORA and a flow to the external server.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes DHCP Discover/Offer/Request/Ack packets and a data flow to the external server.
- The analysis points to relevant DHCP options and demonstrates NAT through source-address comparison.
- Include BOOTP filters and a filter for traffic to the server (for example `http` or `icmp`).

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A06.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A06.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A06 --pcap artifacts/pcap/traffic_e2.pcap`
- Decode-as used during validation: `udp.port==67,bootp, udp.port==68,bootp`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `bootp.option.dhcp==1` | `>= 1` | DHCP Discover. |
| R2 | `bootp.option.dhcp==2` | `>= 1` | DHCP Offer. |
| R3 | `bootp.option.dhcp==3` | `>= 1` | DHCP Request. |
| R4 | `bootp.option.dhcp==5` | `>= 1` | DHCP Ack. |
| R5 | `ip && (tcp || udp || icmp)` | `>= 10` | IP traffic post-DHCP (NAT test). |

### Deliverables
- Docker Compose with `tester` that runs the Bash scripts and produces `artifacts/pcap/traffic_e2.pcap`.
- Bash scripts under `scripts/` for DHCP, NAT and evidence collection.
- Completed `docs/E2_pcap_analysis.md` plus `artifacts/iptables_rules.txt` and `artifacts/dhcp_leases.txt`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus DNAT/port forwarding or DHCP reservations (recommended).
- Extended tests for lease renewal and behaviour when the DHCP server is stopped.
- Mininet demo: show a client obtaining IP, reaching external, then an inbound attempt blocked by default, with PCAP evidence.
- Documented refactoring and a mini security audit for iptables rules and exposures.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (client1) ---\
                 s1 --- h3 (gateway) --- s2 --- h4 (external_server)
h2 (client2) ---/
```
s1 represents the internal LAN, s2 represents the external network; the gateway has two interfaces.

### Demo steps
- Run DHCP on h1/h2 and show DORA in PCAP.
- Run an HTTP request to h4 and show that the source is rewritten on the gateway external interface.
- Attempt an inbound connection from h4 to an internal client and show that it is blocked by default.

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
- **tester:** Bash orchestration, PCAP capture and result verification
- **external_server:** simple external service if it is containerised for E2

### E2 flow
- Start external service (if containerised) and prepare the topology.
- Run `tester` which configures DHCP and NAT, runs tests and writes `artifacts/pcap/traffic_e2.pcap`.
- Export evidence (iptables rules, leases) and stop the scenario.

## Notes
- The implementation relies on iptables and a standard DHCP server (`dnsmasq` or equivalent). These services are not reimplemented.
- The NAT demonstration may require captures on both internal and external interfaces or a capture on the gateway with `-i any`, depending on design.
- Avoid dependency on the Internet. The external server is inside the Mininet topology.

### Typical pitfalls
- DHCP offers addresses from a subnet that does not match the client interface; clients get an IP but cannot route correctly.
- NAT is applied on the wrong interface or in the wrong direction and traffic is lost without clear evidence.
- Capture is taken only on one interface; translation cannot be demonstrated (only presence of traffic is shown).

### Indicative resources (similar examples)
- [dnsmasq (DHCP/DNS for small networks, practical model)](https://github.com/imp/dnsmasq)
- [ISC DHCP (established DHCP implementation)](https://github.com/isc-projects/dhcp)
