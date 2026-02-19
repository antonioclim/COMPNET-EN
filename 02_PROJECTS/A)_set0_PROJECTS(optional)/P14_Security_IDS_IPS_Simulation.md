# Project 14: Security IDS/IPS Simulation

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P14
> 
> **Related:** [P03 (IDS Traffic Monitoring)](P03_IDS_Traffic_Monitoring_Python.md) | [P07 (Firewall IDS)](P07_Firewall_IDS_Traffic_Monitoring.md)

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md) | [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-14`

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | Detection rules, attack signatures |
| Architecture diagrams | 20 | Detection pipeline, alert flow |
| Implementation plan | 15 | Realistic timeline |
| Repository initialised | 15 | GitHub configured |
| MANIFEST.txt | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic detection working | 35 | Detects at least 3 attack types |
| Code quality | 25 | Clean, typed, documented |
| Alert generation | 15 | Proper alert format and logging |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete implementation | 40 | IDS + IPS mode + 5+ signatures |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Detection accuracy tests |
| Documentation | 10 | Complete signature docs |
| False positive analysis | 5 | Accuracy metrics |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: ML anomaly detection** | +10 | Statistical anomaly detection (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Detects simulated attacks |
| Technical presentation | 25 | Explains detection methods |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | All members know code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Port scan + SYN flood + brute force detection |
| **2 persons** | + Automatic blocking (IPS) + signature management |
| **3 persons** | + Anomaly detection + real-time dashboard |

---

## 📚 Project Description

Build a network Intrusion Detection and Prevention System (IDS/IPS) that monitors traffic, detects common attacks and optionally blocks malicious activity. Implement both signature-based detection (matching known patterns) and threshold-based detection (identifying anomalies like too many connections).

### 🎯 Learning Objectives

- **LO1:** Implement signature-based attack detection
- **LO2:** Design threshold-based anomaly detection
- **LO3:** Generate security alerts with proper severity levels
- **LO4:** Implement automatic blocking (IPS mode)
- **LO5:** Evaluate detection accuracy (true/false positives)
- **LO6:** Manage and update detection signatures

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Scapy** | Packet capture and analysis | [scapy.readthedocs.io](https://scapy.readthedocs.io) |
| **iptables** | Packet blocking (IPS) | Linux man pages |
| **nmap** | Attack simulation | [nmap.org](https://nmap.org) |
| **hping3** | Packet crafting | [hping.org](http://www.hping.org) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **IDS** | Intrusion Detection System — detects and alerts |
| **IPS** | Intrusion Prevention System — detects and blocks |
| **Signature** | Known pattern of malicious traffic |
| **Threshold** | Limit triggering anomaly detection |
| **Port Scan** | Probing multiple ports to find services |
| **SYN Flood** | DoS attack using incomplete TCP handshakes |
| **Brute Force** | Repeated login attempts |
| **False Positive** | Alert on legitimate traffic |
| **False Negative** | Missed actual attack |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST detect at least 5 different attack types
- [ ] MUST log all alerts with timestamp, severity, details
- [ ] MUST support configurable detection thresholds
- [ ] MUST implement both IDS (alert) and IPS (block) modes
- [ ] MUST handle high traffic volumes without crashing
- [ ] MUST pass all smoke tests

### MUST NOT (Forbidden)
- [ ] MUST NOT scan or attack systems without permission
- [ ] MUST NOT hardcode detection signatures
- [ ] MUST NOT block without logging
- [ ] MUST NOT ignore malformed packets

### SHOULD (Recommended)
- [ ] SHOULD calculate false positive rate
- [ ] SHOULD support signature hot-reload
- [ ] SHOULD provide statistics dashboard

---

## 🎯 Concept Analogies

### IDS vs IPS = Security Camera vs Guard

🏠 **Real-World Analogy:**  
IDS is like a security camera — it records everything and alerts security, but doesn't stop intruders. IPS is like a security guard — detects threats AND takes action (blocks entry).

💻 **Technical Mapping:**
- Camera = IDS (passive monitoring)
- Guard = IPS (active blocking)
- Recording = Packet capture/logging
- Alert to security = Alert notification
- Physical intervention = iptables DROP rule

---

### Signature Detection = Wanted Poster Matching

🏠 **Real-World Analogy:**  
Police use wanted posters with specific features (height, scar, tattoo). They match suspects against these known patterns. Similarly, IDS matches packets against known attack signatures.

💻 **Technical Mapping:**
- Wanted poster = Signature (pattern definition)
- Features = Packet characteristics (flags, payload)
- Match = Detection event
- Limitation = Can't catch unknown criminals (zero-day)

---

## 🗳️ Peer Instruction Questions

### Question 1: SYN Flood Detection

> 💭 **PREDICTION:** How do you detect a SYN flood attack?

**Options:**
- A) Count HTTP requests
- B) Count SYN packets without corresponding ACKs ✓
- C) Check payload content
- D) Monitor bandwidth usage

**Correct answer:** B

**Explanation:** SYN flood sends many TCP SYN packets (connection requests) without completing the handshake (no ACK). Detection: track half-open connections per source IP; alert when threshold exceeded.

---

### Question 2: Threshold Tuning

> 💭 **PREDICTION:** What happens with a too-low detection threshold?

**Options:**
- A) Miss more attacks
- B) More false positives ✓
- C) Better detection
- D) Less CPU usage

**Correct answer:** B

**Explanation:** Low threshold = more sensitive = more false alarms. Normal traffic variations trigger alerts. High threshold = fewer false positives but might miss real attacks.

---

### Question 3: IPS Blocking

> 💭 **PREDICTION:** Why not block all detected attacks automatically?

**Options:**
- A) Too slow to respond
- B) False positives would block legitimate users ✓
- C) Can't modify traffic
- D) Violates privacy

**Correct answer:** B

**Explanation:** No detection is 100% accurate. Automatic blocking with false positives = blocking legitimate users. IPS mode requires careful tuning and monitoring.

---

### Question 4: Evasion Techniques

> 💭 **PREDICTION:** How might an attacker evade signature detection?

**Options:**
- A) Use encryption
- B) Fragment packets to split signature ✓
- C) Attack faster
- D) Attack slower

**Correct answer:** B

**Explanation:** If the signature "ATTACK" is in payload, splitting across fragments makes it invisible to simple signature matching. Advanced IDS reassembles fragments before checking.

---

## ❌ Common Misconceptions

### 🚫 "IDS prevents attacks"

**WRONG:** Having an IDS stops attacks.

**CORRECT:** IDS only DETECTS — it alerts humans who must take action. For automatic prevention, you need IPS and even then it only blocks known patterns.

---

### 🚫 "More signatures = better security"

**WRONG:** Add every possible signature for maximum protection.

**CORRECT:** More signatures = more processing time = higher latency. Also increases false positive potential. Quality over quantity.

---

### 🚫 "Anomaly detection catches everything"

**WRONG:** Statistical anomaly detection catches all attacks.

**CORRECT:** Anomaly detection has high false positive rates and can be evaded with "low and slow" attacks that stay within normal thresholds.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **IDS** | Intrusion Detection System |
| **IPS** | Intrusion Prevention System |
| **Signature** | Pattern matching known attacks |
| **Anomaly** | Deviation from baseline behaviour |
| **Port Scan** | Discovering open ports |
| **SYN Flood** | DoS with incomplete TCP handshakes |
| **Threshold** | Limit triggering detection |
| **False Positive** | Alert on legitimate traffic |
| **False Negative** | Missed attack |
| **Zero-day** | Unknown attack (no signature) |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""IDS/IPS with Multiple Detection Methods"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from scapy.all import sniff, IP, TCP, ICMP
from dataclasses import dataclass, field
from typing import Dict, List, Callable
from collections import defaultdict
from datetime import datetime, timedelta
import logging
import subprocess
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════════
# TYPES
# ═══════════════════════════════════════════════════════════════════════════════
class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Alert:
    """Security alert."""
    timestamp: datetime
    severity: Severity
    attack_type: str
    source_ip: str
    target_ip: str
    details: str

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTORS
# ═══════════════════════════════════════════════════════════════════════════════
class PortScanDetector:
    """
    Detect port scanning activity.
    
    # 💭 PREDICTION: What threshold indicates a port scan?
    # Answer: 10+ different ports from same source in 60 seconds
    """
    
    def __init__(self, threshold: int = 10, window_seconds: int = 60):
        self.threshold = threshold
        self.window = timedelta(seconds=window_seconds)
        self.port_history: Dict[str, List[tuple]] = defaultdict(list)
    
    def check(self, packet) -> Alert | None:
        if IP not in packet or TCP not in packet:
            return None
        
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport
        now = datetime.now()
        
        # Add to history
        self.port_history[src_ip].append((now, dst_port))
        
        # Clean old entries
        cutoff = now - self.window
        self.port_history[src_ip] = [
            (t, p) for t, p in self.port_history[src_ip] if t > cutoff
        ]
        
        # Count unique ports
        unique_ports = set(p for _, p in self.port_history[src_ip])
        
        if len(unique_ports) >= self.threshold:
            return Alert(
                timestamp=now,
                severity=Severity.HIGH,
                attack_type="PORT_SCAN",
                source_ip=src_ip,
                target_ip=packet[IP].dst,
                details=f"Scanned {len(unique_ports)} ports: {sorted(unique_ports)[:10]}..."
            )
        
        return None


class SYNFloodDetector:
    """Detect SYN flood attacks."""
    
    def __init__(self, threshold: int = 100, window_seconds: int = 10):
        self.threshold = threshold
        self.window = timedelta(seconds=window_seconds)
        self.syn_history: Dict[str, List[datetime]] = defaultdict(list)
    
    def check(self, packet) -> Alert | None:
        if IP not in packet or TCP not in packet:
            return None
        
        # Check for SYN flag (without ACK)
        tcp = packet[TCP]
        if not (tcp.flags & 0x02) or (tcp.flags & 0x10):  # SYN but not ACK
            return None
        
        src_ip = packet[IP].src
        now = datetime.now()
        
        self.syn_history[src_ip].append(now)
        
        # Clean old entries
        cutoff = now - self.window
        self.syn_history[src_ip] = [t for t in self.syn_history[src_ip] if t > cutoff]
        
        if len(self.syn_history[src_ip]) >= self.threshold:
            return Alert(
                timestamp=now,
                severity=Severity.CRITICAL,
                attack_type="SYN_FLOOD",
                source_ip=src_ip,
                target_ip=packet[IP].dst,
                details=f"{len(self.syn_history[src_ip])} SYN packets in {self.window.seconds}s"
            )
        
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# IDS_ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
class IDSEngine:
    """Main IDS/IPS engine."""
    
    def __init__(self, ips_mode: bool = False):
        self.ips_mode = ips_mode
        self.detectors = [
            PortScanDetector(),
            SYNFloodDetector(),
        ]
        self.alerts: List[Alert] = []
        self.blocked_ips: set = set()
        self.logger = logging.getLogger(__name__)
    
    def process_packet(self, packet) -> None:
        """Process single packet through all detectors."""
        for detector in self.detectors:
            alert = detector.check(packet)
            
            if alert:
                self.alerts.append(alert)
                self._handle_alert(alert)
    
    def _handle_alert(self, alert: Alert) -> None:
        """Handle detected alert."""
        self.logger.warning(
            f"[{alert.severity.name}] {alert.attack_type} from {alert.source_ip}: "
            f"{alert.details}"
        )
        
        # IPS mode: block source
        if self.ips_mode and alert.severity.value >= Severity.HIGH.value:
            self._block_ip(alert.source_ip)
    
    def _block_ip(self, ip: str) -> None:
        """Block IP using iptables."""
        if ip in self.blocked_ips:
            return
        
        try:
            subprocess.run([
                "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"
            ], check=True)
            self.blocked_ips.add(ip)
            self.logger.info(f"[IPS] Blocked IP: {ip}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to block {ip}: {e}")
    
    def start(self, interface: str = "eth0") -> None:
        """Start packet capture."""
        self.logger.info(f"Starting IDS on {interface} (IPS mode: {self.ips_mode})")
        sniff(iface=interface, prn=self.process_packet, store=False)
```

---

## 📋 Expected Outputs

### Scenario 1: Port Scan Detection

**Simulate with nmap:**
```bash
nmap -sS 192.168.1.100
```

**Expected alert:**
```
[WARNING] [HIGH] PORT_SCAN from 192.168.1.5: Scanned 15 ports: [22, 80, 443, 3306, ...]
```

### Scenario 2: SYN Flood Detection

**Simulate with hping3:**
```bash
sudo hping3 -S --flood 192.168.1.100
```

**Expected alert:**
```
[WARNING] [CRITICAL] SYN_FLOOD from 192.168.1.5: 500 SYN packets in 10s
[INFO] [IPS] Blocked IP: 192.168.1.5
```

---

## ⚠️ ETHICAL WARNING

**⚠️ Only scan or test systems you OWN or have EXPLICIT PERMISSION to test!**

Unauthorised network scanning is illegal in most jurisdictions. Use these techniques only in controlled lab environments.

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 7 | `07enWSL/` | Packet capture, Wireshark |
| 13 | `13enWSL/` | Network security |
| 14 | `14enWSL/` | Security protocols |

---

## 📚 Bibliography

1. **[OFFICIAL]** Scapy Documentation  
   URL: https://scapy.readthedocs.io/  
   Verified: 2026-01-24 ✓

2. **[ACADEMIC]** NIST Guide to IDS/IPS  
   URL: https://csrc.nist.gov/publications/detail/sp/800-94/rev-1/final  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
