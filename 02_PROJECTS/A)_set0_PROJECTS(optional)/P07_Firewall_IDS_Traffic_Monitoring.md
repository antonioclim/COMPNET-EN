# Project 07: Firewall and IDS Traffic Monitoring

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P07
> 
> **Related:** [P03 (IDS Traffic Monitoring)](P03_IDS_Traffic_Monitoring_Python.md) | [P14 (IDS/IPS Simulation)](P14_Security_IDS_IPS_Simulation.md)

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Project assessment takes place EXCLUSIVELY at the faculty, with mandatory physical attendance.**

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

**Repository:** `https://github.com/[username]/retele-proiect-07`

#### Required Repository Structure

```
retele-proiect-07/
├── README.md
├── docs/
│   ├── specificatii.md
│   ├── diagrame/
│   ├── raport_progres.md
│   └── documentatie_finala.md
├── src/
│   ├── main.py
│   ├── firewall/
│   │   ├── __init__.py
│   │   ├── rules.py
│   │   └── engine.py
│   ├── ids/
│   │   ├── __init__.py
│   │   ├── detector.py
│   │   └── alerts.py
│   └── utils/
├── rules/
│   ├── firewall_rules.yaml
│   └── ids_signatures.yaml
├── tests/
│   ├── test_smoke.py
│   ├── test_firewall.py
│   └── test_ids.py
├── docker/
│   └── docker-compose.yml
├── artifacts/
│   └── pcap/
├── Makefile
├── requirements.txt
├── MANIFEST.txt
└── CHANGELOG.md
```

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | Firewall rules format, IDS signatures, alert format |
| Architecture diagrams | 20 | Packet flow, rule matching, alert pipeline |
| Implementation plan | 15 | Realistic timeline with milestones |
| Repository initialised | 15 | GitHub correctly configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic firewall working | 35 | Rule loading and packet filtering |
| Code quality | 25 | Clean, commented, type hints |
| Traffic capture works | 15 | Can capture and analyse packets |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete functionality | 40 | Firewall + IDS + alerts working |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Unit and integration tests |
| Documentation | 10 | Complete docs |
| False positive analysis | 5 | Document detection accuracy |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: Real-time dashboard** | +10 | Web UI showing alerts (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Block traffic, detect attacks, show alerts |
| Technical presentation | 25 | Explains architecture and detection logic |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | Each member knows all code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Basic firewall + port scan detection |
| **2 persons** | + Multiple attack signatures + logging |
| **3 persons** | + Real-time dashboard + performance metrics |

---

## 📚 Project Description

Implement a software firewall combined with an Intrusion Detection System (IDS) that monitors network traffic, applies filtering rules and detects suspicious patterns. Using Python with Scapy or pyshark, you will build a system that can block unwanted traffic and alert on potential attacks like port scans, brute force attempts and anomalous traffic patterns.

This project combines two essential security functions: preventive (firewall — blocking bad traffic) and detective (IDS — identifying attacks). Understanding both is crucial for network security roles.

### 🎯 Learning Objectives

By completing this project, you will be able to:

- **LO1:** Implement packet filtering rules based on IP, port and protocol
- **LO2:** Capture and parse network packets using Python libraries
- **LO3:** Design detection signatures for common attack patterns
- **LO4:** Implement alert generation and logging systems
- **LO5:** Evaluate detection accuracy (true/false positives)
- **LO6:** Configure rules via external configuration files

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Scapy** | Packet capture and manipulation | [scapy.readthedocs.io](https://scapy.readthedocs.io) |
| **pyshark** | Wireshark wrapper for Python | [github.com/KimiNewt/pyshark](https://github.com/KimiNewt/pyshark) |
| **Python 3** | Core programming | [python.org](https://python.org) |
| **YAML** | Rule configuration | [yaml.org](https://yaml.org) |
| **Docker** | Isolated test environment | [docs.docker.com](https://docs.docker.com) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **Firewall** | Filters traffic based on rules (allow/deny) |
| **IDS** | Detects suspicious patterns without blocking |
| **IPS** | Detects AND blocks (IDS + firewall combined) |
| **Signature-based** | Matches known attack patterns |
| **Anomaly-based** | Detects deviations from normal |
| **False Positive** | Alert on legitimate traffic |
| **False Negative** | Missing actual attack |
| **Promiscuous Mode** | NIC captures all traffic, not just its own |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST use Python 3.10+ with type hints
- [ ] MUST load rules from YAML configuration files
- [ ] MUST log all blocked packets and alerts
- [ ] MUST run in promiscuous mode for full traffic capture
- [ ] MUST handle malformed packets gracefully
- [ ] MUST pass all smoke tests before submission

### MUST NOT (Forbidden)
- [ ] MUST NOT hardcode rules in source code
- [ ] MUST NOT use bare `except:` clauses
- [ ] MUST NOT crash on malformed packets
- [ ] MUST NOT require root for configuration (only for capture)
- [ ] MUST NOT store sensitive data in logs

### SHOULD (Recommended)
- [ ] SHOULD support rule hot-reload without restart
- [ ] SHOULD implement rate limiting for alerts
- [ ] SHOULD provide statistics on blocked/allowed traffic

---

## 🎯 Concept Analogies

### Firewall = Building Security Guard

🏠 **Real-World Analogy:**  
A building security guard checks everyone at the entrance. They have a list of rules: "Allow employees with badges, deny visitors after 6pm, block known troublemakers." They check each person and decide: let through or turn away.

🖼️ **Visual Representation:**
```
Outside          GUARD           Inside
  │                │                │
  │   ┌────────────┴────────────┐   │
  │   │  Rules:                 │   │
  │   │  - Badge? → ALLOW       │   │
  │   │  - After 6pm? → DENY    │   │
  │   │  - Blacklist? → DENY    │   │
  │   └────────────┬────────────┘   │
  │                │                │
[Visitor] ───────► CHECK ──► ALLOW ──► [Building]
                     │
                   DENY
                     │
                     ▼
               [Turned away]
```

💻 **Technical Mapping:**
- Guard = Firewall engine
- Rules list = Firewall rules (YAML config)
- Badge check = IP/port matching
- Blacklist = Deny rules
- Turning away = Dropping packet

⚠️ **Where the analogy breaks:**  
Guards can ask questions and use judgment. Firewalls only match rules mechanically — they can't handle "suspicious but not rule-violating" traffic.

---

### IDS = Security Camera System

🏠 **Real-World Analogy:**  
Security cameras watch everything and alert when they detect suspicious behaviour (motion after hours, someone trying multiple doors). They don't stop anyone — they just alert security personnel who decide what to do.

💻 **Technical Mapping:**
- Cameras = Network interface in promiscuous mode
- Recording = Packet capture / PCAP files
- Motion detection = Threshold-based detection (too many connections)
- Facial recognition = Signature matching (known attack patterns)
- Alert to security = Log entry / notification

⚠️ **Where the analogy breaks:**  
Cameras have limited "understanding" — they detect motion, not intent. Similarly, IDS can miss sophisticated attacks that don't match signatures (zero-day attacks).

---

## 🗳️ Peer Instruction Questions

### Question 1: Firewall Rule Order

> 💭 **PREDICTION:** Think about how rule order affects which packets are blocked.

**Scenario:** A firewall has these rules:
1. ALLOW src=10.0.0.0/8
2. DENY dst_port=22
3. ALLOW ALL

A packet arrives: src=10.0.0.5, dst_port=22

**Question:** Is the packet allowed or denied?

**Options:**
- A) Denied (rule 2 matches)
- B) Allowed (rule 1 matches first) ✓
- C) Allowed (rule 3 matches)
- D) Depends on implementation

**Correct answer:** B

**Explanation:** Most firewalls use first-match processing. Rule 1 matches (source is in 10.0.0.0/8), so the packet is allowed before rule 2 is checked. Rule order matters critically!

**Misconception targeted:** Students think all matching rules are evaluated or that "deny" rules have priority.

---

### Question 2: Port Scan Detection

> 💭 **PREDICTION:** What pattern indicates a port scan?

**Scenario:** Host 10.0.0.5 sends these packets in 2 seconds:
- SYN to 192.168.1.1:22
- SYN to 192.168.1.1:80
- SYN to 192.168.1.1:443
- SYN to 192.168.1.1:3389

**Question:** What makes this a port scan?

**Options:**
- A) SYN packets without completing handshake
- B) Same source, same destination, multiple destination ports ✓
- C) Packets sent too fast
- D) Targeting common service ports

**Correct answer:** B

**Explanation:** The key indicator is one source probing multiple ports on the same destination. SYN-only is also suspicious but could be normal (half-open connections). Speed alone doesn't indicate scanning.

**Misconception targeted:** Students focus on SYN-only or speed, missing the port enumeration pattern.

---

### Question 3: False Positive Impact

> 💭 **PREDICTION:** Which is worse — false positives or false negatives?

**Scenario:** Your IDS has two tuning options:
- Sensitive: 90% detection, 20% false positive rate
- Conservative: 60% detection, 2% false positive rate

**Question:** Which is better for a busy e-commerce site?

**Options:**
- A) Sensitive (catch more attacks)
- B) Conservative (fewer false alarms) ✓
- C) Depends on attack severity
- D) Neither — need both

**Correct answer:** B (with discussion)

**Explanation:** For production environments, false positives cause "alert fatigue" — operators ignore alerts. 20% false positive rate means 1 in 5 alerts is wrong, which quickly becomes unmanageable. Conservative settings with good logging are often better.

**Misconception targeted:** Students think detection rate is the only important metric.

---

### Question 4: Signature vs Anomaly

> 💭 **PREDICTION:** Can signature-based IDS detect new attacks?

**Scenario:** A new vulnerability is discovered. An attacker uses it before signatures are updated.

**Question:** Will signature-based IDS detect this?

**Options:**
- A) Yes, it will match similar attacks
- B) No, it only detects known patterns ✓
- C) Maybe, depends on the attack
- D) Yes, if logging is enabled

**Correct answer:** B

**Explanation:** Signature-based detection requires known patterns. Zero-day attacks (new, unknown) won't match any signature. This is why anomaly-based detection (looking for unusual behaviour) complements signature-based systems.

**Misconception targeted:** Students overestimate signature-based detection capabilities.

---

## ❌ Common Misconceptions

### 🚫 "Firewall blocks all attacks"

**WRONG:** Firewalls only block traffic that matches deny rules. An attack using allowed ports (e.g., HTTP on port 80) passes right through.

**CORRECT:** Firewalls control access, not content. You need IDS/IPS to inspect packet contents and detect attacks within allowed traffic.

**Evidence:** Run a SQL injection attack over HTTP (port 80) — the firewall allows it because port 80 is permitted.

---

### 🚫 "More rules = better security"

**WRONG:** Adding many specific rules creates complexity, increases processing time and makes it harder to audit.

**CORRECT:** Follow "default deny" principle: deny everything, then allow only what's needed. Fewer, well-designed rules are better than many specific ones.

**Evidence:** Compare rule matching time with 10 rules vs 1000 rules — performance degrades with too many rules.

---

### 🚫 "IDS stops attacks"

**WRONG:** IDS (Intrusion Detection System) only detects — it doesn't block.

**CORRECT:** IDS alerts administrators who then take action. IPS (Intrusion Prevention System) can automatically block. Your project can be either, but be clear about which.

**Evidence:** In pure IDS mode, attacks complete even when detected. You're notified after the fact.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **Firewall** | Network security device that filters traffic based on rules |
| **IDS** | Intrusion Detection System — monitors and alerts on suspicious traffic |
| **IPS** | Intrusion Prevention System — monitors, alerts, AND blocks |
| **Signature** | Known pattern of malicious traffic |
| **Anomaly** | Deviation from normal/baseline behaviour |
| **False Positive** | Alert triggered by legitimate traffic |
| **False Negative** | Attack that wasn't detected |
| **Promiscuous Mode** | NIC mode that captures all network traffic |
| **PCAP** | Packet Capture file format |
| **Port Scan** | Technique to discover open ports on a target |

---

## 🔨 Implementation Stages

### Stage 1 (Week 5) — Design

**Tasks:**
1. Design firewall rule format (YAML schema)
2. Design IDS signature format
3. Define alert format and logging strategy
4. Create architecture diagrams

**Example Rule Format:**

```yaml
# firewall_rules.yaml
rules:
  - name: "Allow established"
    action: allow
    state: established
    priority: 100
    
  - name: "Block SSH from external"
    action: deny
    src_net: "0.0.0.0/0"
    dst_port: 22
    protocol: tcp
    priority: 50
    log: true
    
  - name: "Allow internal"
    action: allow
    src_net: "192.168.0.0/16"
    priority: 10
    
  - name: "Default deny"
    action: deny
    priority: 0
    log: true
```

---

### Stage 2 (Week 9) — Prototype

**Tasks:**
1. Implement packet capture with Scapy
2. Implement rule matching engine
3. Basic port scan detection
4. Logging system

**Code Example — Packet Filter:**

```python
#!/usr/bin/env python3
"""
Simple packet filter using Scapy.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from scapy.all import sniff, IP, TCP, UDP
from dataclasses import dataclass
from typing import List, Optional, Callable
import logging
import yaml

# ═══════════════════════════════════════════════════════════════════════════════
# TYPES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class FirewallRule:
    """Represents a firewall rule."""
    name: str
    action: str  # 'allow' or 'deny'
    priority: int = 0
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    protocol: Optional[str] = None
    log: bool = False

# ═══════════════════════════════════════════════════════════════════════════════
# FIREWALL_ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
class FirewallEngine:
    """
    Packet filtering engine.
    
    # 💭 PREDICTION: Why sort rules by priority?
    # Answer: Higher priority rules should match first
    """
    
    def __init__(self, rules: List[FirewallRule]):
        self.rules = sorted(rules, key=lambda r: r.priority, reverse=True)
        self.logger = logging.getLogger(__name__)
        self.stats = {'allowed': 0, 'denied': 0}
    
    def check_packet(self, packet) -> bool:
        """
        Check if packet should be allowed.
        
        Returns:
            True if allowed, False if denied
        """
        if IP not in packet:
            return True  # Non-IP packets allowed
        
        for rule in self.rules:
            if self._matches_rule(packet, rule):
                if rule.log:
                    self._log_match(packet, rule)
                
                allowed = rule.action == 'allow'
                self.stats['allowed' if allowed else 'denied'] += 1
                return allowed
        
        # Default deny
        self.stats['denied'] += 1
        return False
    
    def _matches_rule(self, packet, rule: FirewallRule) -> bool:
        """Check if packet matches rule conditions."""
        ip = packet[IP]
        
        if rule.src_ip and ip.src != rule.src_ip:
            return False
        if rule.dst_ip and ip.dst != rule.dst_ip:
            return False
        
        if rule.protocol:
            if rule.protocol == 'tcp' and TCP not in packet:
                return False
            if rule.protocol == 'udp' and UDP not in packet:
                return False
        
        if rule.dst_port:
            if TCP in packet and packet[TCP].dport != rule.dst_port:
                return False
            if UDP in packet and packet[UDP].dport != rule.dst_port:
                return False
        
        return True
    
    def _log_match(self, packet, rule: FirewallRule) -> None:
        """Log matched packet."""
        ip = packet[IP]
        self.logger.info(
            f"[{rule.action.upper()}] {rule.name}: "
            f"{ip.src} → {ip.dst}"
        )
```

---

### Stage 3 (Week 13) — Final Version

**Tasks:**
1. Complete IDS signatures implementation
2. Add alert rate limiting
3. Complete testing
4. Performance analysis

---

### Stage 4 (Week 14) — Presentation

**Demo checklist:**
```
□ Packet capture running (show interface)
□ Firewall blocks test traffic
□ IDS detects port scan (use nmap)
□ Alerts appear in logs
□ Rule hot-reload works (if implemented)
```

---

## 📋 Expected Outputs

### Scenario 1: Firewall Blocking

**Input:**
```bash
# Start firewall
sudo python src/main.py --interface eth0 --rules rules/firewall_rules.yaml

# Test blocked traffic
nc -zv 192.168.1.1 22
```

**Expected log:**
```
[INFO] Firewall started on interface eth0
[INFO] Loaded 4 rules
[DENY] Block SSH from external: 10.0.0.5 → 192.168.1.1:22
```

---

### Scenario 2: Port Scan Detection

**Input:**
```bash
# From attacker machine
nmap -sS 192.168.1.1
```

**Expected alert:**
```
[ALERT] Port scan detected
  Source: 10.0.0.5
  Target: 192.168.1.1
  Ports scanned: 22, 80, 443, 3389, 8080
  Duration: 2.3 seconds
  Severity: HIGH
```

---

## ❓ Frequently Asked Questions

**Q: Why do I need root/sudo to capture packets?**

A: Promiscuous mode requires elevated privileges. Run with sudo:
```bash
sudo python src/main.py
```

**Q: How do I test without generating real attacks?**

A: Use tools in controlled environment:
```bash
# Port scan (safe in lab)
nmap -sT localhost

# Or replay PCAP files
tcpreplay -i eth0 test.pcap
```

**Q: My rules aren't matching — how to debug?**

A: Add verbose logging and test with known traffic:
```python
# In rule matching
self.logger.debug(f"Checking rule {rule.name} against {packet.summary()}")
```

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 7 | `07enWSL/` | Packet capture, Wireshark, Scapy |
| 13 | `13enWSL/` | Network security concepts |
| 2 | `02enWSL/` | Socket programming |

---

## 📚 Bibliography

### Primary Sources
1. **[OFFICIAL]** Scapy Documentation  
   URL: https://scapy.readthedocs.io/  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** Wireshark User Guide  
   URL: https://www.wireshark.org/docs/wsug_html/  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026*  
*Computer Networks — ASE Bucharest*
