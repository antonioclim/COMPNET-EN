# C07 — Routing Protocols

Week 7 addresses how routers discover and select paths. The lecture covers static vs. dynamic routing, distance-vector algorithms (RIP, Bellman-Ford, count-to-infinity and split horizon), link-state algorithms (Dijkstra, OSPF areas and LSA flooding), the IGP vs. EGP distinction and a contextual note on BGP. Three scenarios let students implement the algorithms in Python and observe routing behaviour in a Mininet triangle topology.

## File and Folder Index

| Name | Description | Metric |
|------|-------------|--------|
| [`c7-routing-protocols.md`](c7-routing-protocols.md) | Slide-by-slide lecture content | 187 lines |
| [`assets/puml/`](assets/puml/) | PlantUML diagram sources | 9 files |
| [`assets/images/`](assets/images/) | Rendered PNG output | .gitkeep |
| [`assets/render.sh`](assets/render.sh) | Diagram rendering script | — |
| [`assets/scenario-bellman-ford/`](assets/scenario-bellman-ford/) | Bellman-Ford algorithm (Python) | 2 files |
| [`assets/scenario-dijkstra/`](assets/scenario-dijkstra/) | Dijkstra's algorithm (Python) | 2 files |
| [`assets/scenario-mininet-routing/`](assets/scenario-mininet-routing/) | Mininet three-router topology | 2 files |

## Visual Overview

```mermaid
graph LR
    BF["Bellman-Ford (Python)"] --> DJ["Dijkstra (Python)"]
    DJ --> MN["Mininet Triangle Routing"]

    style BF fill:#e1f5fe,stroke:#0288d1
    style DJ fill:#e8f5e9,stroke:#388e3c
    style MN fill:#fff3e0,stroke:#f57c00
```

## PlantUML Diagrams

| Source file | Subject |
|-------------|---------|
| `fig-distance-vector.puml` | Distance-vector algorithm exchange |
| `fig-igp-vs-egp.puml` | IGP vs. EGP scope |
| `fig-l2-l3-changes.puml` | L2/L3 header changes across hops |
| `fig-link-state.puml` | Link-state algorithm (LSA flood) |
| `fig-mininet-triangle.puml` | Three-router Mininet topology |
| `fig-ospf-areas.puml` | OSPF area hierarchy |
| `fig-rip-loop.puml` | RIP count-to-infinity loop |
| `fig-router-role.puml` | Router role in packet forwarding |
| `fig-routing-table.puml` | Routing table structure |

## Usage

Bellman-Ford and Dijkstra implementations:

```bash
cd assets/scenario-bellman-ford && python3 bellman_ford.py
cd ../scenario-dijkstra && python3 dijkstra.py
```

Mininet scenario (requires Mininet and root privileges):

```bash
cd assets/scenario-mininet-routing
sudo python3 tringle-net.py
```

## Pedagogical Context

Students implement both algorithm families from scratch before observing their behaviour in a simulated network. This theory-then-simulation ordering lets students predict routing table entries and then verify predictions against Mininet output, reinforcing the connection between mathematical abstraction and operational reality.

## Cross-References

### Prerequisites

| Prerequisite | Path | Why |
|---|---|---|
| IP addressing and CIDR | [`../C05/`](../C05/) | Routing tables match on CIDR prefixes |
| L3 support protocols | [`../C06/`](../C06/) | ARP, ICMP used in forwarding and diagnostics |

### Lecture ↔ Seminar ↔ Project ↔ Quiz

| Content | Seminar | Project | Quiz |
|---------|---------|---------|------|
| SDN, routing and Mininet topologies | [`S06`](../../04_SEMINARS/S06/) | — | [W07](../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W07_Questions.md) |
| Distance-vector routing in Mininet | — | [S14](../../02_PROJECTS/01_network_applications/S14_didactic_distance_vector_routing_in_mininet_convergence_and_anti_loop.md) | — |
| SDN firewall with OpenFlow | — | [A01](../../02_PROJECTS/02_administration_security/A01_sdn_firewall_filtering_policies_via_openflow_rules.md) | — |
| SDN learning switch | — | [A07](../../02_PROJECTS/02_administration_security/A07_sdn_learning_switch_controller_flow_installation_and_ageing.md) | — |

### Instructor Notes

Romanian outlines: [`roCOMPNETclass_S07-instructor-outline-v2.md`](../../00_APPENDIX/d%29instructor_NOTES4sem/roCOMPNETclass_S07-instructor-outline-v2.md)

### Downstream Dependencies

Routing concepts are assumed by the Mininet-based seminars (S06) and by the SDN-focused administration projects (A01, A07, A08). The Mininet Guide in [`01_GUIDE_MININET-SDN/`](../../01_GUIDE_MININET-SDN/) provides extended reference material for this topic.

### Suggested Sequence

[`C06/`](../C06/) → this folder → [`04_SEMINARS/S06/`](../../04_SEMINARS/S06/) → [`C08/`](../C08/)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C07
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C07`
## Provenance

Course kit version: v13 (February 2026). Author: ing. dr. Antonio Clim — ASE Bucharest, CSIE.
