# Project 02: Hybrid Network with Mininet and Docker

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Project assessment takes place EXCLUSIVELY at the faculty, with mandatory physical attendance.**

- The final presentation (Stage 4) takes place before the instructor/committee
- You must demonstrate understanding of the code and project architecture
- Questions about implementation and theoretical concepts may be asked
- Absence from presentation = project failure

**Common guides (read before starting):**
- [Pair Programming Guide](../docs/common/pair_programming_guide.md)
- [Code Quality Standards](../docs/common/code_quality_standards.md)
- [Git Workflow](../docs/common/git_workflow_detailed.md)
- [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

---

### 🐙 GitHub Publication

**Repository:** `https://github.com/[username]/retele-proiect-02`

#### Required Structure

```
retele-proiect-02/
├── README.md
├── docs/
│   ├── specificatii.md
│   ├── diagrame/
│   ├── raport_progres.md
│   └── documentatie_finala.md
├── src/
│   ├── main.py
│   └── modules/
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── mininet/
│   └── topology.py
├── tests/
├── artifacts/
├── MANIFEST.txt
├── CHANGELOG.md
└── .gitignore
```

---

### 📊 Assessment Rubric

*(Same rubric structure as P01 — see common assessment guide)*

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Basic complete functionality |
| **2 persons** | + Extended testing + Detailed documentation |
| **3 persons** | + Advanced extensions + Performance analysis |

---

## 📚 Project Description

This project creates a hybrid network combining Mininet's virtual network emulation with Docker containers. The goal is to demonstrate how software-defined networks can interact with containerised applications, creating a flexible testing environment for network services.

You will build a topology where Mininet hosts communicate with Docker containers through bridge networks, enabling scenarios like testing microservices, load balancing or distributed applications in an emulated network environment.

### 🎯 Learning Objectives

By completing this project, you will be able to:

- **Design** hybrid network topologies combining virtual and container networks
- **Configure** Docker networking to integrate with Mininet
- **Implement** bridge connections between different network domains
- **Test** network connectivity across hybrid environments
- **Analyse** traffic flow between Mininet hosts and Docker containers

### 🛠️ Technologies and Tools

| Technology | Purpose |
|------------|---------|
| **Mininet** | Virtual network emulation |
| **Docker** | Container runtime |
| **Docker Compose** | Multi-container orchestration |
| **OVS (Open vSwitch)** | Software switch for bridging |
| **Python** | Topology scripting |

---

## 🎯 Concept Analogies

### Hybrid Network = Airport with Multiple Terminals

🏠 **Real-World Analogy:**  
An airport has multiple terminals (Docker networks) connected by a central hub (bridge). Passengers (packets) can transfer between terminals, but each terminal has its own security and services. The airport control tower (controller) coordinates everything.

💻 **Technical Mapping:**
- Terminal A = Docker bridge network
- Terminal B = Mininet virtual network
- Central hub = OVS bridge connecting both
- Passengers = Network packets
- Security checkpoints = Network namespaces

⚠️ **Where the analogy breaks:**  
Unlike airports, network bridges can filter or modify packets and "passengers" (packets) can be duplicated or dropped.

### Container Network = Apartment Building

🏠 **Real-World Analogy:**  
Each apartment (container) has its own address within the building (Docker network). The building has a main entrance (gateway) connecting to the street (host network). Neighbours can visit each other easily, but visitors from outside must go through the entrance.

---

## 🗳️ Peer Instruction Questions

### Question 1: Network Namespace Isolation

> 💭 **PREDICTION:** If you run `ip addr` inside a Docker container and on the Mininet host, will you see the same interfaces?

**Options:**
- A) Yes, they share the same network stack
- B) No, each has its own isolated network namespace ✓
- C) Only if they're on the same bridge
- D) Only root can see all interfaces

**Correct answer:** B

**Explanation:** Both Docker containers and Mininet hosts use Linux network namespaces for isolation. Each namespace has its own interfaces, routing table and firewall rules.

---

### Question 2: Bridge Connectivity

**Scenario:** A Mininet host (h1: 10.0.0.1) needs to reach a Docker container (web: 172.17.0.2).

**Question:** What is required for this communication?

**Options:**
- A) Nothing — Linux routes everything automatically
- B) A bridge connecting both networks with proper routing ✓
- C) Both must be on the same subnet
- D) Docker automatically creates routes to Mininet

**Correct answer:** B

**Explanation:** Different subnets require routing. You need a bridge (OVS or Linux bridge) connected to both networks, plus routing rules to forward traffic.

---

### Question 3: Docker Network Types

**Question:** Which Docker network driver allows containers to share the host's network namespace?

**Options:**
- A) bridge
- B) overlay
- C) host ✓
- D) none

**Correct answer:** C

**Explanation:** The `host` driver removes network isolation — the container uses the host's network directly. This can simplify Mininet integration but loses container isolation.

---

## ❌ Common Misconceptions

### 🚫 Misconception 1: "Docker containers can ping Mininet hosts by default"

**WRONG:** "Once both are running, they can communicate automatically."

**CORRECT:** Docker and Mininet use separate network namespaces and subnets. You must explicitly create a bridge and configure routing for cross-network communication.

---

### 🚫 Misconception 2: "docker0 bridge is the same as OVS bridge"

**WRONG:** "They're both bridges, so they work the same way."

**CORRECT:** docker0 is a Linux bridge for Docker containers. OVS is a more advanced software switch supporting OpenFlow. For SDN integration, you need OVS, not docker0.

---

### 🚫 Misconception 3: "Container IP addresses are permanent"

**WRONG:** "172.17.0.2 will always be my web container."

**CORRECT:** Docker assigns IPs dynamically. Use container names for DNS resolution within Docker networks or assign static IPs in compose files.

---

## 📖 Project Glossary

| Term | Definition |
|------|------------|
| **Network Namespace** | Isolated network stack (interfaces, routes, firewall) |
| **Bridge Network** | Layer 2 connection between network segments |
| **OVS (Open vSwitch)** | Multilayer virtual switch supporting OpenFlow |
| **Docker Bridge** | Default Docker network driver for container communication |
| **veth Pair** | Virtual ethernet pair connecting namespaces |
| **Gateway** | Device routing traffic between networks |

---

## 💭 Prediction Checkpoints

### E2 - Prototype Phase

> 💭 **Before connecting networks:** Can a Mininet host (10.0.0.0/24) ping a Docker container (172.17.0.0/16) without any bridge?
> 
> Expected: No — different subnets, no route

> 💭 **After adding bridge:** What route must be added on the Mininet host?
> 
> Expected: `ip route add 172.17.0.0/16 via [bridge_ip]`

---

## 🔨 Implementation Stages

### Stage 1 (Week 5) — Design

**Tasks:**
1. Design hybrid topology (Mininet + Docker components)
2. Plan IP addressing scheme for both networks
3. Document bridge configuration requirements
4. Create architecture diagrams

---

### Stage 2 (Week 9) — Prototype

**Example bridge setup:**
```python
#!/usr/bin/env python3
"""
Hybrid Network Topology — Mininet + Docker Bridge
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
import subprocess

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
MININET_SUBNET = "10.0.0.0/24"
DOCKER_SUBNET = "172.17.0.0/16"
BRIDGE_NAME = "hybrid-br"

# ═══════════════════════════════════════════════════════════════════════════════
# TOPOLOGY_SETUP
# ═══════════════════════════════════════════════════════════════════════════════
def create_hybrid_topology():
    """
    Create Mininet topology with Docker bridge connection.
    
    Returns:
        Mininet network object
    """
    net = Mininet(controller=Controller, switch=OVSSwitch)
    
    # Add controller
    net.addController('c0')
    
    # Add switch
    s1 = net.addSwitch('s1')
    
    # Add Mininet hosts
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    
    # Connect hosts to switch
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    
    return net

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_BRIDGE
# ═══════════════════════════════════════════════════════════════════════════════
def connect_to_docker(switch_name: str) -> None:
    """
    Connect OVS switch to Docker bridge.
    
    Args:
        switch_name: Name of OVS switch to connect
    """
    # 💭 PREDICTION: What happens if docker0 doesn't exist?
    subprocess.run([
        "ovs-vsctl", "add-port", switch_name, "docker0"
    ], check=True)
    print(f"Connected {switch_name} to Docker bridge")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    setLogLevel('info')
    net = create_hybrid_topology()
    net.start()
    
    # Test connectivity
    print("Testing Mininet internal connectivity:")
    net.pingAll()
    
    CLI(net)
    net.stop()

if __name__ == "__main__":
    main()
```

---

## ❓ Frequently Asked Questions

**Q: Docker containers can't reach Mininet hosts**

A: Check routing on both sides:
```bash
# On Mininet host
ip route add 172.17.0.0/16 via 10.0.0.254

# On Docker container
ip route add 10.0.0.0/24 via 172.17.0.1
```

**Q: OVS bridge won't connect to docker0**

A: Ensure docker0 exists and OVS has permission:
```bash
docker network inspect bridge
sudo ovs-vsctl add-port s1 docker0
```

**Q: How do I test cross-network connectivity?**

A: Use ping from both sides:
```bash
# From Mininet CLI
h1 ping 172.17.0.2

# From Docker container
docker exec web ping 10.0.0.1
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 1 | `01enWSL/` | Docker basics, environment setup |
| 6 | `06enWSL/` | SDN, Docker networking with OVS |
| 11 | `11enWSL/` | Docker Compose, service orchestration |

---

## 📝 Final Notes

- **Always verify** that the GitHub repository is updated before deadlines
- **Test** cross-network connectivity before presentation
- **Document** the IP addressing scheme clearly
- **Review** the [Presentation Guide](../docs/common/presentation_guide.md) before E4

---

*Last update: January 2026*  
*Computer Networks — ASE Bucharest*
