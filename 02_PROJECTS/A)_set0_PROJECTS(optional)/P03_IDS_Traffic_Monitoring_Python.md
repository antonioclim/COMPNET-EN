# Project 03: IDS Traffic Monitoring with Python

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

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

**Repository:** `https://github.com/[username]/retele-proiect-03`

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Basic detection (port scan, ping flood) |
| **2 persons** | + Multiple attack types + Alerting system |
| **3 persons** | + Machine learning anomaly detection + Dashboard |

---

## 📚 Project Description

This project implements a simplified Intrusion Detection System (IDS) that captures and analyses network traffic to identify suspicious patterns. Using Python libraries like Scapy or pyshark, you will develop an application capable of detecting common attack patterns such as port scans, ping floods and brute-force attempts.

The system will capture packets, analyse them against defined rules or thresholds and generate alerts when suspicious activity is detected.

### 🎯 Learning Objectives

By completing this project, you will be able to:

- **Capture** network packets using Python libraries
- **Parse** packet headers to extract relevant information
- **Implement** detection rules for common attack patterns
- **Design** alerting mechanisms for security events
- **Evaluate** false positive rates and detection accuracy

### 🛠️ Technologies and Tools

| Technology | Purpose |
|------------|---------|
| **Scapy** | Packet capture and manipulation |
| **pyshark** | Wireshark wrapper for Python |
| **PCAP files** | Stored traffic for analysis |
| **Docker** | Isolated test environment |
| **Wireshark** | Traffic verification |

---

## 🎯 Concept Analogies

### IDS = Security Camera System

🏠 **Real-World Analogy:**  
A building's security camera system records all activity (packet capture), analyses footage for suspicious behaviour (pattern matching) and alerts security guards (alerting) when something unusual is detected. It doesn't stop intruders (that's IPS) but identifies them.

💻 **Technical Mapping:**
- Cameras = Network interface in promiscuous mode
- Recording = PCAP file storage
- Motion detection = Threshold-based detection
- Facial recognition = Signature matching
- Alert system = Log files, notifications

⚠️ **Where the analogy breaks:**  
Unlike cameras that record everything, IDS may sample traffic or focus on specific protocols. Also, network attacks can happen in milliseconds.

### Signature vs Anomaly Detection = Known Faces vs Suspicious Behaviour

🏠 **Real-World Analogy:**  
Security can work two ways: checking faces against a "wanted" list (signature-based) or watching for unusual behaviour like someone trying many doors (anomaly-based).

💻 **Technical Mapping:**
- Wanted list = Signature database (known attack patterns)
- Unusual behaviour = Statistical anomaly (too many connections)

---

## 🗳️ Peer Instruction Questions

### Question 1: Promiscuous Mode

> 💭 **PREDICTION:** If your network interface is NOT in promiscuous mode, what traffic can the IDS capture?

**Options:**
- A) All traffic on the network segment
- B) Only traffic destined to or from the host ✓
- C) Only broadcast traffic
- D) No traffic at all

**Correct answer:** B

**Explanation:** Without promiscuous mode, the NIC only passes packets addressed to its MAC or broadcast/multicast. IDS needs promiscuous mode to see all traffic.

---

### Question 2: Port Scan Detection

**Scenario:** Host 10.0.0.5 sends SYN packets to ports 22, 23, 80, 443, 8080 on 10.0.0.10 within 2 seconds.

**Question:** What pattern indicates a port scan?

**Options:**
- A) Multiple SYN packets (normal for web browsing)
- B) Same source, same destination, many different destination ports ✓
- C) Packets without responses
- D) Large packet sizes

**Correct answer:** B

**Explanation:** Port scans are characterised by one source probing multiple ports on a target in a short time. The number of unique destination ports from a single source is the key metric.

---

### Question 3: False Positives

**Scenario:** Your IDS alerts on "more than 100 connections per minute from single IP."

**Question:** Which legitimate activity might trigger this alert?

**Options:**
- A) Normal web browsing
- B) A web server handling requests ✓
- C) Sending an email
- D) DNS lookup

**Correct answer:** B

**Explanation:** A busy web server legitimately receives many connections. This is why IDS tuning is critical — thresholds must match the environment.

---

## ❌ Common Misconceptions

### 🚫 Misconception 1: "IDS and IPS are the same"

**WRONG:** "My IDS will block the attack."

**CORRECT:** IDS only **detects** and alerts. IPS (Intrusion Prevention System) can **block** traffic. Your project is an IDS — it monitors but doesn't prevent.

---

### 🚫 Misconception 2: "Signature-based detection catches everything"

**WRONG:** "I have signatures for all attacks."

**CORRECT:** Signature-based detection only catches **known** attacks. New (zero-day) attacks need anomaly-based detection or updated signatures.

---

### 🚫 Misconception 3: "More alerts = better security"

**WRONG:** "My IDS generates 1000 alerts/hour, so it's working well."

**CORRECT:** Too many alerts cause "alert fatigue" — operators ignore them. A good IDS has high detection rate with low false positives.

---

### 🚫 Misconception 4: "Encrypted traffic can't be analysed"

**WRONG:** "HTTPS traffic is invisible to my IDS."

**CORRECT:** While payload is encrypted, metadata (IP addresses, ports, packet sizes, timing) is visible. Many attacks can be detected from metadata alone.

---

## 📖 Project Glossary

| Term | Definition |
|------|------------|
| **IDS** | Intrusion Detection System — monitors for suspicious activity |
| **IPS** | Intrusion Prevention System — blocks malicious traffic |
| **Signature** | Known pattern of malicious activity |
| **Anomaly** | Deviation from normal baseline behaviour |
| **False Positive** | Alert triggered by legitimate activity |
| **False Negative** | Attack missed by the system |
| **PCAP** | Packet Capture file format |
| **Promiscuous Mode** | NIC mode capturing all network traffic |
| **Port Scan** | Probing multiple ports to find services |
| **DoS** | Denial of Service attack |

---

## 💭 Prediction Checkpoints

### E2 - Prototype Phase

> 💭 **Before running scan detection:** How many unique destination ports indicate a port scan? 5? 10? 100?
> 
> Consider: What's normal for a web browser?

> 💭 **Before testing with real traffic:** What percentage of alerts do you expect to be false positives?

---

## 🔨 Implementation Stages

### Stage 2 (Week 9) — Prototype

**Example IDS structure:**
```python
#!/usr/bin/env python3
"""
Simple IDS — Port Scan and Ping Flood Detection
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from scapy.all import sniff, IP, TCP, ICMP
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Set
import logging

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
PORT_SCAN_THRESHOLD = 10      # Ports in time window
PORT_SCAN_WINDOW = 60         # Seconds
PING_FLOOD_THRESHOLD = 50     # ICMP packets in time window
PING_FLOOD_WINDOW = 10        # Seconds

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_SETUP
# ═══════════════════════════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ids_alerts.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION_STATE
# ═══════════════════════════════════════════════════════════════════════════════
class DetectionState:
    """Track connection state for anomaly detection."""
    
    def __init__(self):
        self.port_connections: Dict[str, Set[int]] = defaultdict(set)
        self.port_timestamps: Dict[str, datetime] = {}
        self.icmp_counts: Dict[str, int] = defaultdict(int)
        self.icmp_timestamps: Dict[str, datetime] = {}

state = DetectionState()

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION_RULES
# ═══════════════════════════════════════════════════════════════════════════════
def detect_port_scan(packet) -> bool:
    """
    Detect port scan based on unique destination ports.
    
    Args:
        packet: Scapy packet object
        
    Returns:
        True if port scan detected
    """
    if not packet.haslayer(TCP):
        return False
    
    src_ip = packet[IP].src
    dst_port = packet[TCP].dport
    now = datetime.now()
    
    # Reset if window expired
    if src_ip in state.port_timestamps:
        if now - state.port_timestamps[src_ip] > timedelta(seconds=PORT_SCAN_WINDOW):
            state.port_connections[src_ip].clear()
    
    state.port_connections[src_ip].add(dst_port)
    state.port_timestamps[src_ip] = now
    
    # 💭 PREDICTION: What if threshold is too low?
    if len(state.port_connections[src_ip]) > PORT_SCAN_THRESHOLD:
        return True
    
    return False


def detect_ping_flood(packet) -> bool:
    """
    Detect ICMP flood based on packet rate.
    
    Args:
        packet: Scapy packet object
        
    Returns:
        True if ping flood detected
    """
    if not packet.haslayer(ICMP):
        return False
    
    src_ip = packet[IP].src
    now = datetime.now()
    
    # Reset if window expired
    if src_ip in state.icmp_timestamps:
        if now - state.icmp_timestamps[src_ip] > timedelta(seconds=PING_FLOOD_WINDOW):
            state.icmp_counts[src_ip] = 0
    
    state.icmp_counts[src_ip] += 1
    state.icmp_timestamps[src_ip] = now
    
    if state.icmp_counts[src_ip] > PING_FLOOD_THRESHOLD:
        return True
    
    return False

# ═══════════════════════════════════════════════════════════════════════════════
# PACKET_HANDLER
# ═══════════════════════════════════════════════════════════════════════════════
def packet_callback(packet):
    """
    Process each captured packet.
    
    Args:
        packet: Scapy packet object
    """
    if not packet.haslayer(IP):
        return
    
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    
    if detect_port_scan(packet):
        logger.warning(f"🚨 PORT SCAN detected from {src_ip}")
        logger.info(f"   Ports: {state.port_connections[src_ip]}")
    
    if detect_ping_flood(packet):
        logger.warning(f"🚨 PING FLOOD detected from {src_ip} to {dst_ip}")
        logger.info(f"   Count: {state.icmp_counts[src_ip]} in {PING_FLOOD_WINDOW}s")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Start IDS packet capture."""
    logger.info("IDS starting — monitoring for suspicious activity")
    logger.info(f"Port scan threshold: {PORT_SCAN_THRESHOLD} ports in {PORT_SCAN_WINDOW}s")
    logger.info(f"Ping flood threshold: {PING_FLOOD_THRESHOLD} packets in {PING_FLOOD_WINDOW}s")
    
    try:
        # Capture on all interfaces
        sniff(prn=packet_callback, store=False)
    except KeyboardInterrupt:
        logger.info("IDS stopped by user")

if __name__ == "__main__":
    main()
```

---

## ❓ Frequently Asked Questions

**Q: Scapy requires root privileges**

A: Run with sudo or set capabilities:
```bash
sudo python3 ids.py
# Or
sudo setcap cap_net_raw+ep /usr/bin/python3
```

**Q: How do I test port scan detection?**

A: Use nmap from another host:
```bash
nmap -sS -p 1-1000 target_ip
```

**Q: How do I reduce false positives?**

A: Adjust thresholds based on your environment:
- Monitor normal traffic first
- Set thresholds above normal levels
- Consider whitelisting known services

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 7 | `07enWSL/` | Wireshark, Scapy, packet interception |
| 13 | `13enWSL/` | Network security, IDS concepts |
| 4 | `04enWSL/` | Protocol parsing with struct |

---

*Last update: January 2026*  
*Computer Networks — ASE Bucharest*
