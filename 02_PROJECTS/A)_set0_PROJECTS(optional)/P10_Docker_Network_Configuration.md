# Project 10: Docker Network Configuration and Management

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P10
> 
> **Related:** [P12 (Microservices Load Balancing)](P12_Docker_Microservices_Load_Balancing.md)

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Project assessment takes place EXCLUSIVELY at the faculty, with mandatory physical attendance.**

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md) | [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-10`

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | Network types, IP schemes, service discovery |
| Architecture diagrams | 20 | Network topology, container relationships |
| Implementation plan | 15 | Realistic timeline |
| Repository initialised | 15 | GitHub configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic networks working | 35 | Bridge and custom networks |
| Code quality | 25 | Clean docker-compose, documented |
| Container communication | 15 | Containers can reach each other |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete functionality | 40 | All network types + management tool |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Network connectivity tests |
| Documentation | 10 | Complete docs |
| Performance analysis | 5 | Network latency measurements |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: Network policies** | +10 | Traffic isolation rules (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Networks work, containers communicate |
| Technical presentation | 25 | Explains Docker networking |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | All members know code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Bridge + custom networks + basic management |
| **2 persons** | + Multiple network types + DNS resolution |
| **3 persons** | + Network policies + monitoring dashboard |

---

## 📚 Project Description

Create a Docker network management system that demonstrates different network types (bridge, host, overlay, macvlan), implements custom network configurations and provides tools for monitoring and troubleshooting container connectivity. This project teaches container networking fundamentals essential for modern DevOps and cloud deployments.

Docker networking is fundamental to microservices architecture. Understanding how containers communicate — both with each other and the outside world — is crucial for deploying scalable applications.

### 🎯 Learning Objectives

- **LO1:** Configure different Docker network types (bridge, host, overlay)
- **LO2:** Implement custom bridge networks with specific subnets
- **LO3:** Enable container-to-container communication via DNS
- **LO4:** Troubleshoot network connectivity issues
- **LO5:** Create a management tool for network operations
- **LO6:** Analyse network performance and latency

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Docker** | Container runtime | [docs.docker.com](https://docs.docker.com) |
| **Docker Compose** | Multi-container orchestration | [docs.docker.com/compose](https://docs.docker.com/compose) |
| **Python docker SDK** | Programmatic Docker control | [docker-py.readthedocs.io](https://docker-py.readthedocs.io) |
| **iperf3** | Network performance testing | [iperf.fr](https://iperf.fr) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **Bridge Network** | Default isolated network for containers |
| **Host Network** | Container shares host's network stack |
| **Overlay Network** | Multi-host container communication |
| **Macvlan** | Containers get real MAC addresses |
| **Docker DNS** | Automatic name resolution for containers |
| **Network Driver** | Plugin that implements network type |
| **Subnet** | IP address range for a network |
| **Gateway** | Router for external communication |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST create at least 3 different network types
- [ ] MUST demonstrate container DNS resolution
- [ ] MUST implement network isolation
- [ ] MUST provide CLI management tool
- [ ] MUST log all network operations
- [ ] MUST pass all smoke tests

### MUST NOT (Forbidden)
- [ ] MUST NOT use `--network host` for all containers
- [ ] MUST NOT hardcode container IPs
- [ ] MUST NOT expose unnecessary ports
- [ ] MUST NOT leave orphaned networks

### SHOULD (Recommended)
- [ ] SHOULD implement network monitoring
- [ ] SHOULD support network creation via config file
- [ ] SHOULD measure network latency

---

## 🎯 Concept Analogies

### Docker Bridge Network = Apartment Building

🏠 **Real-World Analogy:**  
An apartment building has internal hallways (bridge network). Residents (containers) can visit each other through these hallways without going outside. A doorman (gateway) handles visitors from outside. Each apartment has an intercom number (IP address) and a name plate (DNS name).

🖼️ **Visual Representation:**
```
        ┌─────────── Building (Bridge Network) ───────────┐
        │                                                  │
        │   ┌──────────┐    ┌──────────┐    ┌──────────┐  │
        │   │ Apt 101  │    │ Apt 102  │    │ Apt 103  │  │
        │   │ (web)    │◄──►│ (api)    │◄──►│ (db)     │  │
        │   │ 172.18.  │    │ 172.18.  │    │ 172.18.  │  │
        │   │ 0.2      │    │ 0.3      │    │ 0.4      │  │
        │   └──────────┘    └──────────┘    └──────────┘  │
        │                       │                         │
        │              ┌────────▼────────┐               │
        │              │    Doorman      │               │
        │              │   (Gateway)     │               │
        │              │   172.18.0.1    │               │
        │              └────────┬────────┘               │
        └───────────────────────┼────────────────────────┘
                                │
                        Outside World (Host)
```

💻 **Technical Mapping:**
- Building = Docker bridge network
- Apartments = Containers
- Hallways = Internal network
- Doorman = Gateway/NAT
- Intercom numbers = IP addresses
- Name plates = Container DNS names

⚠️ **Where the analogy breaks:** In real buildings, everyone can hear you in the hallway. In Docker, traffic is isolated per network — containers on different networks can't communicate without explicit connection.

---

### Network Isolation = Gated Communities

🏠 **Real-World Analogy:**  
Different gated communities (networks) are isolated from each other. Residents can only visit other communities if they have access (container connected to multiple networks).

💻 **Technical Mapping:**
- Gated community = Docker network
- Resident = Container
- Access card to multiple communities = Container attached to multiple networks

---

## 🗳️ Peer Instruction Questions

### Question 1: Default Bridge vs Custom Bridge

> 💭 **PREDICTION:** What's the main advantage of custom bridge networks?

**Options:**
- A) Better performance
- B) Automatic DNS resolution between containers ✓
- C) More IP addresses
- D) Stronger security

**Correct answer:** B

**Explanation:** On the default bridge, containers can only communicate by IP. Custom bridge networks provide automatic DNS — containers can reach each other by name (e.g., `ping db` instead of `ping 172.17.0.3`).

**Misconception targeted:** Students think all bridge networks have DNS.

---

### Question 2: Host Network Mode

> 💭 **PREDICTION:** When would you use `--network host`?

**Options:**
- A) For better isolation
- B) When container needs host's exact network stack ✓
- C) For multi-container applications
- D) For security

**Correct answer:** B

**Explanation:** Host mode removes network isolation — container uses host's IP directly. Useful for performance-critical applications or when binding to specific host interfaces. But it sacrifices isolation.

---

### Question 3: Container IP Persistence

> 💭 **PREDICTION:** Does a container keep the same IP after restart?

**Options:**
- A) Yes, always
- B) No, IP can change ✓
- C) Only with Docker Compose
- D) Only on custom networks

**Correct answer:** B

**Explanation:** Container IPs are dynamically assigned. After restart, a container might get a different IP. This is why DNS-based discovery (by container name) is preferred over hardcoded IPs.

---

### Question 4: Overlay Network Purpose

> 💭 **PREDICTION:** When do you need an overlay network?

**Options:**
- A) For containers on the same host
- B) For containers on different hosts (Swarm/Kubernetes) ✓
- C) For internet access
- D) For better performance

**Correct answer:** B

**Explanation:** Overlay networks span multiple Docker hosts, enabling containers on different machines to communicate as if on the same network. Required for Docker Swarm and distributed deployments.

---

## ❌ Common Misconceptions

### 🚫 "Containers on the same host can always communicate"

**WRONG:** Just being on the same host doesn't enable communication.

**CORRECT:** Containers must be on the same Docker network OR have port mappings. Two containers on different bridge networks cannot reach each other directly.

**Evidence:** Create two containers on different networks and try to ping between them — it fails.

---

### 🚫 "Port mapping is required for container-to-container communication"

**WRONG:** You need `-p 8080:80` for containers to talk to each other.

**CORRECT:** Port mapping (`-p`) exposes ports to the HOST. Containers on the same network can communicate directly on any port without mapping.

---

### 🚫 "docker0 bridge is the best option"

**WRONG:** The default bridge (docker0) is sufficient for everything.

**CORRECT:** The default bridge lacks automatic DNS and has limited isolation options. User-defined bridge networks are recommended for any multi-container application.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **Bridge Network** | Virtual network connecting containers on one host |
| **Host Network** | Container shares host's network namespace |
| **Overlay Network** | Network spanning multiple Docker hosts |
| **Macvlan** | Network giving containers MAC addresses on physical network |
| **Docker DNS** | Built-in DNS server resolving container names |
| **Network Driver** | Plugin implementing network type |
| **IPAM** | IP Address Management for Docker networks |
| **Subnet** | Range of IP addresses (e.g., 172.18.0.0/16) |
| **Gateway** | Router IP for external communication |
| **docker0** | Default bridge network interface |

---

## 🔨 Implementation Stages

### Stage 2 (Week 9) — Prototype

**Code Example — Network Manager:**

```python
#!/usr/bin/env python3
"""
Docker Network Manager
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import docker
from typing import List, Dict, Optional
import logging

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_MANAGER
# ═══════════════════════════════════════════════════════════════════════════════
class NetworkManager:
    """
    Manage Docker networks programmatically.
    
    # 💭 PREDICTION: Why use Docker SDK instead of subprocess?
    # Answer: Type safety, error handling and cleaner API
    """
    
    def __init__(self):
        self.client = docker.from_env()
        self.logger = logging.getLogger(__name__)
    
    def create_network(
        self,
        name: str,
        driver: str = "bridge",
        subnet: Optional[str] = None,
        gateway: Optional[str] = None
    ) -> docker.models.networks.Network:
        """
        Create a Docker network.
        
        Args:
            name: Network name
            driver: Network driver (bridge, overlay, macvlan)
            subnet: CIDR notation (e.g., "172.20.0.0/16")
            gateway: Gateway IP
            
        Returns:
            Created network object
        """
        ipam_config = None
        if subnet:
            ipam_pool = docker.types.IPAMPool(
                subnet=subnet,
                gateway=gateway
            )
            ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        
        network = self.client.networks.create(
            name=name,
            driver=driver,
            ipam=ipam_config
        )
        
        self.logger.info(f"Created network '{name}' with driver '{driver}'")
        return network
    
    def list_networks(self) -> List[Dict]:
        """List all networks with details."""
        networks = []
        for net in self.client.networks.list():
            networks.append({
                'name': net.name,
                'id': net.short_id,
                'driver': net.attrs['Driver'],
                'scope': net.attrs['Scope'],
                'containers': len(net.attrs.get('Containers', {}))
            })
        return networks
    
    def connect_container(self, network_name: str, container_name: str) -> None:
        """Connect a container to a network."""
        network = self.client.networks.get(network_name)
        container = self.client.containers.get(container_name)
        network.connect(container)
        self.logger.info(f"Connected '{container_name}' to '{network_name}'")
    
    def test_connectivity(self, container1: str, container2: str) -> bool:
        """
        Test if container1 can reach container2.
        
        # 💭 PREDICTION: What command tests connectivity?
        # Answer: ping or nc (netcat)
        """
        container = self.client.containers.get(container1)
        result = container.exec_run(f"ping -c 1 {container2}")
        return result.exit_code == 0
```

**docker-compose.yml Example:**

```yaml
version: '3.8'

networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/24
          gateway: 172.20.0.1
  
  backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/24
          gateway: 172.21.0.1

services:
  web:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "8080:80"
  
  api:
    image: python:3.11-slim
    networks:
      - frontend
      - backend
    # API connects to both networks
  
  db:
    image: postgres:15-alpine
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD: secret
    # DB only on backend network
```

---

## 📋 Expected Outputs

### Scenario 1: Create Custom Network

**Input:**
```bash
python src/main.py create-network --name mynet --subnet 172.25.0.0/24
```

**Expected output:**
```
[INFO] Creating network 'mynet' with subnet 172.25.0.0/24
[INFO] Network created successfully
Network ID: a1b2c3d4e5
Driver: bridge
Subnet: 172.25.0.0/24
Gateway: 172.25.0.1
```

### Scenario 2: Test Connectivity

**Input:**
```bash
python src/main.py test-connectivity web api
```

**Expected output:**
```
[INFO] Testing connectivity: web → api
[SUCCESS] web can reach api (1.23ms latency)
```

---

## ❓ Frequently Asked Questions

**Q: Why can't my containers ping each other?**

A: Check they're on the same network:
```bash
docker network inspect mynetwork
```

**Q: How do I find a container's IP?**

A: Use inspect:
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name
```

**Q: DNS doesn't work between containers?**

A: Only custom networks have DNS. Default bridge doesn't. Create a user-defined network.

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 10 | `10enWSL/` | Docker basics, containers |
| 11 | `11enWSL/` | Docker networking |
| 2 | `02enWSL/` | IP addressing fundamentals |

---

## 📚 Bibliography

1. **[OFFICIAL]** Docker Networking Overview  
   URL: https://docs.docker.com/network/  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** Docker Python SDK  
   URL: https://docker-py.readthedocs.io/  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
