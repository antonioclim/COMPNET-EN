# S14 — Didactic distance-vector routing in Mininet with convergence and anti-loop

## Metadata
- **Group:** 1
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C05, C06, C07 | S06, S05, S07
- **Protocol/default ports (E2):** UDP: DV updates 5014/UDP; overlay data 5015/UDP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Mininet script plus automation), `pytest -m e2` (or equivalent test), capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S14.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
This project asks you to implement a didactic distance-vector routing algorithm in a Mininet topology. The focus is on the algorithm itself (periodic updates, neighbour exchange, convergence) rather than on kernel-level routing.

Routers are implemented as user-space agents that exchange routing updates over UDP and maintain a local routing table. For demonstrability, data packets are not routed by the OS but through an overlay: packets are encapsulated into a UDP “data” format and forwarded hop-by-hop according to the computed routing table.

Anti-loop behaviour is mandatory: you must implement split horizon or poison reverse and provide evidence in PCAP and logs that it is active. In the demo you show convergence after a link failure and the routing-table change that follows.

Distance-vector is one of the classical routing families. In this didactic variant you make routing state explicit and observable: periodic DV update packets include the advertised distances and next hops and the overlay data packets include a magic value that allows deterministic detection in captures. The goal is not production-grade routing but a rigorous experiment: the topology is small, the update interval is controlled and failure is injected at a known time so the convergence behaviour can be assessed repeatedly.

## Learning objectives
- Implement a distance-vector update protocol over UDP (periodic and triggered updates)
- Maintain and update routing tables based on neighbour advertisements
- Handle convergence and detect invalid routes after failure
- Implement an anti-loop technique (split horizon or poison reverse)
- Forward overlay data packets hop-by-hop based on the computed routes

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **router agent** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust) that can participate in the DV update exchange.
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **send DV1 updates and forward one DATA1 packet as a router**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** UDP: DV updates 5014/UDP; overlay data 5015/UDP.
- The Flex component must work with the default values (without manual reconfiguration) so that it can be integrated into automated tests.

### Deliverables
- `flex/` directory with sources plus build/run instructions (avoid exotic dependencies where possible).
- `docs/FLEX.md` with:
  - build/run commands
  - the minimal scenario that is demonstrated
  - known limitations
- A minimal automated test (pytest or script) that starts the Flex component and validates the minimal scenario.

### Assessment (clear and measurable)
- The Flex component is assessed in E3 (as part of the E3 score). Its absence limits the maximum possible E3 mark.

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe convergence behaviour and loop-prevention markers in a distance-vector simulation.

### Minimum scenario
- Run a small topology with 3 routers and 2 hosts and use any DV simulation tool or a toy implementation.
- Capture DV update packets periodically and extract the advertised distances.
- Shut down one link and observe triggered updates and convergence.
- Note how poison reverse or split horizon appears in an update (in a simplified protocol).

### Recommended Wireshark filters
- `udp.port == 5014` — DV update traffic
- `udp.port == 5015` — overlay data traffic
- `frame contains "DV1"` — marker for DV updates in a custom payload
- `frame contains "POISON"` — poison reverse markers
- `icmp` — optional end-to-end pings through the overlay environment

### Guiding questions
- What indicates convergence in a capture: stable periodic updates with unchanged costs
- How quickly does the algorithm react after a link failure and what triggers the update
- How poison reverse or split horizon prevents loops and how that is observed
- How overlay forwarding differs from OS routing and what is visible in a PCAP

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Implement DV update messages over UDP, sent periodically (fixed interval) and optionally triggered on significant changes.
- Routers maintain a routing table and compute next hops based on neighbour advertisements.
- Overlay data forwarding: send a UDP packet with a magic `DATA1` and forward it hop-by-hop according to the routing table.
- Link failure handling: when a neighbour becomes unreachable, routes through that neighbour are invalidated.
- Anti-loop: implement split horizon or poison reverse and provide evidence (payload markers, logs) that it is active.
- Deterministic message formats: DV update messages start with ASCII magic `DV1` and data packets start with `DATA1` for deterministic capture validation.
- Expose the routing table on demand (CLI command or endpoint) and log changes with timestamps.

### SHOULD (recommended)
- Triggered updates on failure and recovery rather than relying solely on periodic intervals.
- Hold-down timer or route expiry to avoid oscillations.
- A deterministic convergence time measurement (log when stable state is reached).

### MAY (optional)
- Support for unequal costs (link weights) rather than constant hop count.
- Simple route aggregation for networks with multiple subnets.

## Non-functional requirements
- Update interval, timeouts and hold-down timers configured in a YAML file.
- Deterministic behaviour: fixed seeds and explicit timing to make captures reproducible.
- Concurrency control: routing table updates protected against concurrent reads during forwarding.
- Logging: periodic summaries, convergence events, loop-prevention actions.
- Testability: automated scripts can start the topology, inject failure and assert reachability.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Protocol specification for DV1 updates: fields, encoding, neighbour list and example in hex or JSON.
- Update rules: periodic interval, triggered update conditions, expiry policy.
- Anti-loop mechanism description with a concrete example.
- Mininet topology with at least 3 routers and 2 hosts; specify link costs.
- E2 capture plan: periodic updates, a forwarded overlay data packet and anti-loop evidence.
- Test plan: reachability before failure, failover, convergence and reachability after recovery.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: starts Mininet topology, runs a controlled failure sequence, generates `artifacts/pcap/traffic_e2.pcap` then validates: `python tools/validate_pcap.py --project S14 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- At least 3 DV1 update messages exchanged between routers.
- A DATA1 packet forwarded through at least one intermediate router.
- Anti-loop evidence in an update after a link failure.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes periodic DV updates and at least one overlay data packet.
- The analysis identifies the failure moment and describes convergence (routing-table change).
- Loop-prevention evidence is shown (poison reverse or split horizon marker).

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S14.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S14.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S14 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `udp.port==5014 && frame contains "DV1"` | `>= 3` | At least 3 DV messages (magic DV1), periodic updates. |
| R2 | `udp.port==5015 && frame contains "DATA1"` | `>= 1` | At least one forwarded overlay data packet (magic DATA1). |
| R3 | `udp.port==5014 && (frame contains "POISON" || frame contains "SPLITH")` | `>= 1` | Anti-loop evidence (poison reverse/split horizon) in the payload or logs. |
| R4 | `icmp || udp.port==5015` | `>= 1` | Demonstrative end-to-end traffic (data/ping) in the topology. |

### Deliverables
- Mininet script (`topology.py`) plus automation script to start, run scenario and stop.
- Smoke tests (`pytest -m e2`) that check reachability and convergence by reading router state.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus support for configurable link weights and more complex topology.
- Tests for multiple failure scenarios and prevention of count-to-infinity under a loop condition.
- Mininet demo with a link failure and recovery, with routing-table prints and PCAP evidence.
- Documented refactoring and a mini security audit for untrusted DV updates (validation, length limits).

## Mininet topology and demo scenario
### Topology (ASCII)
```
hA --- r1 --- r2 --- r3 --- hB
          \         /
           +--- r4 --+
```
The topology includes at least one alternative path so failover can be demonstrated.

### Demo steps
- Show that hA can reach hB through overlay data forwarding.
- Disable the link r2–r3 and observe convergence and an alternative path through r4.
- Show in the PCAP: DV1 periodic updates, POISON/SPLITH marker and one DATA1 forwarded packet.

## Docker scenario (E2)
This project is Mininet-based. Use scripts rather than Docker for the main topology, but you may use Docker for auxiliary services (logging, artefact collection).

## Notes
- The aim is an educational routing protocol, not full IP routing.
- Keep message formats simple and deterministic; include magic strings for PCAP validation.
- Anti-loop is mandatory: without it the algorithm is incomplete.

### Typical pitfalls
- Lack of anti-loop causes routing loops and count-to-infinity which can be observed as increasing metrics.
- Update packets are not validated; invalid lengths or unknown neighbour IDs corrupt state.
- Timing is not controlled; captures are not reproducible between runs.

### Indicative resources (similar examples)
- [RIP (distance-vector routing protocol, RFC 2453)](https://www.rfc-editor.org/rfc/rfc2453)
- [Mininet examples (topologies and scripts)](https://github.com/mininet/mininet)
