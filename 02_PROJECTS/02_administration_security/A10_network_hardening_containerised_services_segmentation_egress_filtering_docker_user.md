# A10 — Network hardening for containerised services: segmentation and egress filtering with DOCKER-USER

## Metadata
- **Group:** 2
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C13, C05, C06 | S11, S07, S05
- **Protocol/default ports (E2):** Docker networking

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/A10.json`.
- **E3 (40%) — Final plus demo:** complete implementation plus demo (included in E3). **No Flex component** for the A01–A10 series.

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You build a simple containerised application (minimum three services) and apply a network-segmentation policy plus egress filtering. The aim is to demonstrate reproducibly that not all containers can talk to each other and that access towards “outside” is restricted by default, following the least-privilege principle.

The implementation uses separate Docker networks (front/back) plus a set of rules in the `DOCKER-USER` chain (iptables) to control traffic between networks and towards the external host. An explicit connectivity matrix is required: which connections are allowed and which are forbidden, validated automatically.

The project includes a Mininet scenario in which an external host attempts to interact with the services and the policy demonstrates both controlled exposure (for example only frontend is reachable) and blocking of forbidden communications (for example direct access to DB). The PCAP must include at least one permitted flow and one blocked flow.

Docker network hardening is treated as a set of verifiable controls: segmentation on user-defined networks, minimised port publishing, controlled egress and verification that services cannot communicate “implicitly” across segments. Bash plays an operational role: scripts build the scenario, run connectivity tests and collect state (`docker network inspect`, iptables, routes) into artefacts. In E2, PCAP must show explicitly an allowed case and a blocked case (SYN without a full handshake) and in E3 you justify decisions as a mini security audit.

## Learning objectives
- Segment services across distinct Docker networks and control inter-service communication
- Apply egress filtering to reduce attack surface and exfiltration paths
- Use `DOCKER-USER` for stable policies, independent of Docker-generated rules
- Automate configuration and verification using Bash
- Collect evidence (iptables-save, counters, PCAP) for assessment

## Flexible component

**N/A for the A01–A10 series.** Administration/security projects are assessed via configuration, automation, PCAP and a demo; multi-language interoperability is not required.

(Optional extensions in any language are accepted but do not replace the core requirements.)

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe the effect of segmentation and iptables rules on TCP flows between containers.

### Minimum scenario
- Start two containers on different networks and attempt a TCP connection between them.
- Apply a drop rule in `DOCKER-USER` and repeat to observe the difference.
- Capture on the relevant Docker bridge (e.g. `br-...`) and observe SYN without response when traffic is blocked.
- Export `iptables-save` and use counters to check whether rules were hit.

### Recommended Wireshark filters
- `tcp.dstport == 3306` — attempts towards DB (typical port) which should be blocked from frontend
- `tcp.dstport == 8080` — traffic towards backend (application port) which should be permitted from frontend
- `tcp.flags.syn == 1 && tcp.flags.ack == 0` — connection initiation, useful for observing drops
- `tcp.flags.reset == 1` — RST, if blocking is implemented as reject
- `ip.addr == 172.18.0.0/16` — typical Docker network prefix (adjust according to setup)

### Guiding questions
- Why `DOCKER-USER` is an appropriate place for policies and how order appears in iptables
- How to demonstrate in PCAP that a connection is blocked (drop) versus rejected (reject/RST)
- How to define a minimal connectivity matrix for a front–back–db application
- How to verify egress filtering without depending on the Internet (use an external Mininet host)

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Containerised application with at least three services: `frontend`, `backend`, `db` (or equivalent), started via Docker Compose.
- Segmentation into at least two Docker networks: `frontend` in the front network, `db` in the back network, `backend` with controlled access.
- Connectivity policy: `frontend → backend` allowed, `backend → db` allowed, `frontend → db` denied, verified automatically via tests.
- Egress filtering: services cannot initiate connections to an external Mininet host unless explicitly allowed; evidence in iptables and PCAP.
- Implement deterministic egress filtering for containers (iptables/nftables) plus segmentation via separate Docker bridge networks.
- Mandatory artefacts: `iptables-save`/`nft list ruleset`, network diagrams (`docker network inspect`) plus PCAP before/after.

### SHOULD (recommended)
- Logging via iptables counters and periodic export for the report (how many packets were blocked).
- Minimal exposure: only `frontend` is published to a host port; other services are not published.
- Automatically generated E2 report: connectivity matrix, rules, counters plus two PCAP examples.

### MAY (optional)
- Egress rate limiting on the frontend service to demonstrate volume control.
- Explicit rule allowing only DNS to a local resolver in the laboratory (not the Internet).

## Non-functional requirements
- Bash scripts: `network_setup.sh`, `apply_firewall.sh`, `test_matrix.sh`, `collect_evidence.sh` (clear roles).
- YAML configuration: service ports, networks, inter-service allowlist and egress allowlist.
- The policy is reversible: a cleanup script exists that removes added rules.
- Testability: the “external” server is in the Mininet topology, not on the Internet.
- Service logs must not contain secrets; DB credentials are in a local `.env`, not in the repository.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Connectivity matrix plus justification (least privilege).
- Docker network architecture (front/back) and service mapping.
- iptables/DOCKER-USER rule specification: what is allowed and what is blocked.
- Mininet topology for an external host and how egress filtering is tested without the Internet.
- E2 capture plan: allowed flow (frontend→backend) and blocked flow (frontend→db or to external).
- Test plan: four connectivity tests plus counter verification.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap`, then validates the capture: `python tools/validate_pcap.py --project A10 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Services start in Docker Compose and respond to local health checks.
- DOCKER-USER rules are applied via script and the connectivity matrix is validated automatically.
- PCAP capture includes an allowed flow and a blocked flow.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes a complete handshake for the allowed connection and SYN packets without progress for the blocked connection (or RST if reject is used).
- The analysis explains which iptables rule is responsible and shows hit counters.
- Filters for backend and DB ports are included.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/A10.json`
- In the catalogue (template): `00_common/tools/pcap_rules/A10.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project A10 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp || udp` | `>= 10` | Network traffic generated by containers (to evidence egress filtering). |
| R2 | `dns || udp.port==53` | `>= 1` | DNS resolution attempt (allowed/blocked). |
| R3 | `tcp.port==80 || tcp.port==443` | `>= 1` | External HTTP/HTTPS access attempt (allowed/blocked). |

### Deliverables
- Docker Compose with `frontend`, `backend`, `db` and `tester`.
- Bash scripts for policy and testing under `scripts/`.
- `artifacts/pcap/traffic_e2.pcap`, `artifacts/iptables-save.txt`, `artifacts/counters.txt` plus `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus automatic report and counters (recommended).
- Mininet demo: an external host can access only the frontend and egress from containers to external is blocked.
- Extended tests for bypass attempts (for example direct DB access) and blocking confirmation.
- Documented refactoring and a mini security audit for rules and secret management.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (docker_host) --- s1 --- h2 (external)
```
Services run on h1, while h2 plays the “external” role for egress/inbound tests.

### Demo steps
- From h2 attempt direct access to DB and show it is blocked; access to frontend is allowed.
- From containers attempt a connection to h2 (external) and show egress is blocked.
- Show `DOCKER-USER` plus counters then highlight packets in PCAP.

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
- **frontend:** exposed service, communicates only with backend
- **backend:** internal service, communicates with db
- **db:** data service, not published
- **tester:** runs the matrix tests and captures PCAP

### E2 flow
- Start services via Docker Compose then apply iptables rules via script.
- Run `tester` which executes the connectivity matrix and captures traffic on the relevant bridge.
- Export evidence and stop the stack.

## Notes
- Host-level iptables policies can affect other containers; isolate rules using subnet/interface matches.
- Egress filtering is demonstrated without Internet: the external host is in Mininet.
- DOCKER-USER is preferred because it is evaluated before Docker-generated rules for forwarding.

### Typical pitfalls
- Rules are applied on the default `bridge` network but services run on user-defined networks, so no effect is observed.
- Ports are published to the host and testing happens from the host rather than through Docker segmentation, making results inconclusive.
- Capture is taken only inside the container while filtering is applied on the host; evidence is missing for the actual blocking point.

### Indicative resources (similar examples)
- [docker-bench-security (hardening checklist)](https://github.com/docker/docker-bench-security)
- [Containernet (Mininet + Docker, useful for hybrid scenarios)](https://github.com/containernet/containernet)
