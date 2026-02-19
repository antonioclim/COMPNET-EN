# Project 16: Network Traffic Analyzer (Individual Reserve)

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE  
> **Project type:** Reserve (Individual)

> 📍 **Navigation:** [00PROJ](../README.md) → [RESERVE](./README.md) → P16

---

## 📋 Assessment Overview

| Stage | Week | Score | Deliverables |
|-------|------|-------|--------------|
| **E1** | 5 | 20% | Specifications + Diagrams |
| **E2** | 9 | 25% | Prototype implementation |
| **E3** | 13 | 35% | Final version + Tests |
| **E4** | 14 | 20% | Live demo + Defence |

**Repository:** `https://github.com/[username]/retele-proiect-16`

**Common guides:** [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md) | [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📊 Assessment Rubric Summary

| Stage | Key Criteria |
|-------|--------------|
| **E1** | Protocol analysis design, traffic classification |
| **E2** | Packet capture, basic statistics working |
| **E3** | Complete analysis, visualisation, tests |
| **E4** | Demo with real/simulated traffic |

---

## 📚 Project Description

Build a network traffic analyser that captures packets, extracts protocol information, calculates statistics (bandwidth, packet rates, protocol distribution) and visualises traffic patterns. This tool helps understand network behaviour and diagnose issues.

### 🎯 Learning Objectives

- **LO1:** Capture network packets using Scapy/pyshark
- **LO2:** Parse protocol headers (Ethernet, IP, TCP, UDP, HTTP)
- **LO3:** Calculate traffic statistics (packets/sec, bytes/sec, distributions)
- **LO4:** Visualise traffic patterns in real-time or from captures
- **LO5:** Export analysis results (CSV, JSON)

### 🛠️ Technologies

| Technology | Purpose |
|------------|---------|
| **Scapy/pyshark** | Packet capture |
| **matplotlib** | Visualisation |
| **Python 3** | Core programming |
| **Wireshark (reference)** | Comparison |

---

## ⛔ Constraints

### MUST
- [ ] MUST capture live traffic OR read PCAP files
- [ ] MUST parse at least 5 protocol types
- [ ] MUST calculate bandwidth statistics
- [ ] MUST generate visualisations (graphs/charts)
- [ ] MUST pass smoke tests

### MUST NOT
- [ ] MUST NOT capture sensitive data without permission
- [ ] MUST NOT crash on malformed packets
- [ ] MUST NOT hardcode interface names

---

## 🎯 Concept Analogies

### Traffic Analyzer = Highway Traffic Counter

🏠 **Real-World Analogy:**  
Highway sensors count vehicles, measure speed, classify by type (car, truck). They generate reports: "500 vehicles/hour, 20% trucks, average speed 100 km/h."

💻 **Technical Mapping:**
- Vehicles = Packets
- Counter = Packet capture
- Classification = Protocol parsing
- Report = Statistics output

---

## 🗳️ Peer Instruction Questions

### Question 1: Promiscuous Mode

> 💭 **PREDICTION:** Why is promiscuous mode needed?

**Options:**
- A) Faster capture
- B) Capture all traffic, not just own ✓
- C) Better parsing
- D) Required by law

**Correct answer:** B — Normal NICs only receive packets addressed to them. Promiscuous mode captures ALL packets on the network segment.

---

### Question 2: PCAP vs Live

> 💭 **PREDICTION:** When prefer PCAP files over live capture?

**Options:**
- A) When traffic is encrypted
- B) For reproducible analysis ✓
- C) For faster processing
- D) When network is slow

**Correct answer:** B — PCAP files allow repeated analysis of the same traffic, essential for testing and comparison.

---

## ❌ Common Misconceptions

### 🚫 "Can analyse all traffic on network"

**WRONG:** Connect to any network and see everything.

**CORRECT:** On switched networks, you only see: your traffic, broadcast and traffic to your MAC. Full capture requires mirror port or inline tap.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **PCAP** | Packet Capture file format |
| **Promiscuous** | Capture all packets, not just addressed to host |
| **BPF** | Berkeley Packet Filter (capture filters) |
| **Protocol Distribution** | Percentage of each protocol type |
| **Bandwidth** | Data rate (bits/bytes per second) |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""Network Traffic Analyzer"""

from scapy.all import sniff, IP, TCP, UDP
from collections import Counter, defaultdict
from datetime import datetime
import time

class TrafficAnalyzer:
    """Analyse network traffic statistics."""
    
    def __init__(self):
        self.packet_count = 0
        self.byte_count = 0
        self.protocol_counts = Counter()
        self.start_time = None
    
    def process_packet(self, packet) -> None:
        """Process single packet."""
        if self.start_time is None:
            self.start_time = time.time()
        
        self.packet_count += 1
        self.byte_count += len(packet)
        
        # Classify protocol
        if TCP in packet:
            self.protocol_counts['TCP'] += 1
        elif UDP in packet:
            self.protocol_counts['UDP'] += 1
        elif IP in packet:
            self.protocol_counts['Other IP'] += 1
    
    def get_statistics(self) -> dict:
        """Get current statistics."""
        elapsed = time.time() - self.start_time if self.start_time else 1
        return {
            'packets': self.packet_count,
            'bytes': self.byte_count,
            'packets_per_sec': self.packet_count / elapsed,
            'mbps': (self.byte_count * 8) / (elapsed * 1_000_000),
            'protocols': dict(self.protocol_counts)
        }
```

---

## 📋 Expected Outputs

**Statistics output:**
```
=== Traffic Analysis ===
Duration: 60.0 seconds
Packets: 12,543
Bytes: 8,432,156
Rate: 209 pkt/s, 1.12 Mbps

Protocol Distribution:
  TCP: 8,234 (65.7%)
  UDP: 3,891 (31.0%)
  Other: 418 (3.3%)
```

---

## 📚 Bibliography

1. **[OFFICIAL]** Scapy Documentation — https://scapy.readthedocs.io/  
2. **[OFFICIAL]** Wireshark Developer Guide — https://www.wireshark.org/docs/wsdg_html/

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
