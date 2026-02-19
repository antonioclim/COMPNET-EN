# Project 11: Advanced SDN QoS with Mininet and OpenFlow

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P11
> 
> **Related:** [P01 (SDN Firewall)](P01_SDN_Firewall_Mininet.md) | [P06 (SDN Controller)](P06_SDN_Mininet_Controller_OpenFlow.md)

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

**Repository:** `https://github.com/[username]/retele-proiect-11`

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | QoS policies, traffic classes, queue configs |
| Architecture diagrams | 20 | Traffic flow, queue architecture |
| Implementation plan | 15 | Realistic timeline |
| Repository initialised | 15 | GitHub configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic QoS functional | 35 | Traffic classification works |
| Code quality | 25 | Clean, typed, documented |
| Mininet topology works | 15 | Multi-switch with queues |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete QoS implementation | 40 | Prioritisation, rate limiting |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Traffic generation + validation |
| Documentation | 10 | Complete docs |
| Performance analysis | 5 | Latency/throughput comparison |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: Dynamic QoS** | +10 | Adaptive policies (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | QoS prioritisation visible |
| Technical presentation | 25 | Explains QoS mechanisms |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | All members know code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Basic traffic classification + priority queues |
| **2 persons** | + Rate limiting + multiple traffic classes |
| **3 persons** | + Dynamic QoS + real-time monitoring dashboard |

---

## 📚 Project Description

Implement Quality of Service (QoS) policies in an SDN network using OpenFlow meters and queues. The system will classify traffic (VoIP, video, best-effort), assign priorities and enforce bandwidth guarantees. This demonstrates how modern networks ensure critical applications get the resources they need.

QoS is essential in real networks where video calls compete with file downloads. Without QoS, a large download can starve a video call of bandwidth. Your controller will prevent this by intelligently managing traffic.

### 🎯 Learning Objectives

- **LO1:** Implement traffic classification based on ports, protocols, DSCP
- **LO2:** Configure OpenFlow meters for rate limiting
- **LO3:** Design queue structures for traffic prioritisation
- **LO4:** Measure QoS effectiveness (latency, jitter, throughput)
- **LO5:** Analyse trade-offs between fairness and efficiency
- **LO6:** Implement dynamic policy adjustment based on conditions

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Mininet** | Network emulation | [mininet.org](http://mininet.org) |
| **Ryu/OS-Ken** | SDN controller | [ryu-sdn.org](https://ryu-sdn.org) |
| **Open vSwitch** | QoS-capable switch | [openvswitch.org](https://www.openvswitch.org) |
| **iperf3** | Traffic generation | [iperf.fr](https://iperf.fr) |
| **tc (traffic control)** | Linux QoS | Linux man pages |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **QoS** | Quality of Service - traffic management for performance |
| **Traffic Classification** | Identifying traffic types (VoIP, video, data) |
| **Priority Queuing** | Higher priority traffic processed first |
| **Rate Limiting** | Enforcing maximum bandwidth per flow |
| **DSCP** | Differentiated Services Code Point - QoS marking |
| **Meter** | OpenFlow mechanism for rate enforcement |
| **Queue** | Buffer with scheduling priority |
| **Bandwidth Guarantee** | Minimum assured bandwidth |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST classify at least 3 traffic types (high/medium/low priority)
- [ ] MUST implement rate limiting for at least one class
- [ ] MUST demonstrate measurable QoS improvement
- [ ] MUST use OpenFlow meters or OVS queues
- [ ] MUST log QoS decisions and statistics
- [ ] MUST pass all smoke tests

### MUST NOT (Forbidden)
- [ ] MUST NOT hardcode traffic classification (use config file)
- [ ] MUST NOT starve low-priority traffic completely
- [ ] MUST NOT use external QoS tools (implement in controller)
- [ ] MUST NOT ignore meter/queue errors

### SHOULD (Recommended)
- [ ] SHOULD implement hierarchical queuing (parent/child)
- [ ] SHOULD support DSCP marking
- [ ] SHOULD provide statistics dashboard

---

## 🎯 Concept Analogies

### QoS = Hospital Triage

🏠 **Real-World Analogy:**  
In an emergency room, patients are triaged by severity. Heart attacks get immediate attention, broken arms wait longer, minor cuts wait longest. Resources (doctors, beds) are allocated based on urgency, not arrival order.

🖼️ **Visual Representation:**
```
                    TRIAGE
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
    ▼                  ▼                  ▼
┌────────┐        ┌────────┐        ┌────────┐
│CRITICAL│        │ URGENT │        │ MINOR  │
│ (VoIP) │        │(Video) │        │ (Data) │
├────────┤        ├────────┤        ├────────┤
│Priority│        │Priority│        │Priority│
│   1    │        │   2    │        │   3    │
│  10ms  │        │  50ms  │        │ 200ms  │
└────────┘        └────────┘        └────────┘
 Immediate        Within 15min      When available
```

💻 **Technical Mapping:**
- Patients = Packets
- Triage nurse = Classifier
- Severity levels = Traffic classes
- Treatment priority = Queue priority
- Doctor availability = Bandwidth allocation

⚠️ **Where the analogy breaks:** In hospitals, critical patients get MORE resources. In networking, high priority often means FASTER processing, not necessarily more bandwidth.

---

### Traffic Classification = Airport Security Lanes

🏠 **Real-World Analogy:**  
Airports have different security lanes: priority for business class, standard for economy, expedited for crew. Same security check, different waiting times based on classification.

💻 **Technical Mapping:**
- Passenger class = DSCP value / port number
- Security check = Processing
- Queue time = Latency
- Priority lane = High-priority queue

---

## 🗳️ Peer Instruction Questions

### Question 1: Traffic Starvation

> 💭 **PREDICTION:** What happens if high-priority queue always has traffic?

**Scenario:** VoIP traffic constantly fills the high-priority queue. Low-priority downloads are waiting.

**Question:** In strict priority queuing, what happens to downloads?

**Options:**
- A) They get processed during VoIP silence
- B) They never get processed (starvation) ✓
- C) They get equal bandwidth
- D) They timeout and are dropped

**Correct answer:** B

**Explanation:** Strict priority queuing always processes higher queues first. If high-priority never empties, low-priority starves. Solution: Weighted Fair Queuing (WFQ) guarantees minimum bandwidth to all classes.

**Misconception targeted:** Students think "priority" is just about ordering, not realising it can cause starvation.

---

### Question 2: Rate Limiting vs Priority

> 💭 **PREDICTION:** What's the difference between rate limiting and priority queuing?

**Options:**
- A) Same thing, different names
- B) Rate limiting caps bandwidth, priority affects ordering ✓
- C) Priority is for inbound, rate limiting for outbound
- D) Rate limiting is per-packet, priority is per-flow

**Correct answer:** B

**Explanation:** Rate limiting (meters) enforces maximum bandwidth — excess traffic is dropped or marked. Priority queuing determines processing order but doesn't limit bandwidth. You often use both: classify → prioritise → rate limit.

---

### Question 3: DSCP Preservation

> 💭 **PREDICTION:** Is DSCP preserved across network boundaries?

**Options:**
- A) Always preserved
- B) Often reset at network boundaries ✓
- C) Only in IPv6
- D) Only for TCP

**Correct answer:** B

**Explanation:** ISPs often reset DSCP markings at their border (called "re-marking") because they don't trust customer markings. Your internal QoS works, but doesn't guarantee end-to-end QoS across the internet.

---

### Question 4: Queue Depth Trade-off

> 💭 **PREDICTION:** What's the downside of large queue buffers?

**Options:**
- A) More memory usage
- B) Higher latency (bufferbloat) ✓
- C) More packet drops
- D) Lower throughput

**Correct answer:** B

**Explanation:** Large buffers absorb bursts but add queuing delay. For VoIP (latency-sensitive), small buffers are better — drop packets rather than delay them. This is "bufferbloat" — too much buffering hurts interactive traffic.

---

## ❌ Common Misconceptions

### 🚫 "QoS creates bandwidth"

**WRONG:** QoS can't add bandwidth that doesn't exist.

**CORRECT:** QoS manages EXISTING bandwidth, prioritising important traffic. If you need 100 Mbps but have 50 Mbps, QoS ensures the 50 Mbps goes to important traffic first.

**Evidence:** Total throughput before and after QoS is the same — only distribution changes.

---

### 🚫 "Higher priority = more bandwidth"

**WRONG:** Priority queuing gives more bandwidth to high-priority traffic.

**CORRECT:** Priority determines processing ORDER, not amount. A high-priority VoIP call (64 kbps) still uses less bandwidth than a low-priority download (10 Mbps). Priority ensures the VoIP packets are sent first, reducing latency.

---

### 🚫 "QoS works end-to-end automatically"

**WRONG:** Setting QoS on my network affects the entire path.

**CORRECT:** QoS is hop-by-hop. Each network segment must implement compatible policies. Your ISP ignores your DSCP markings unless you have a QoS SLA.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **QoS** | Quality of Service — managing traffic for performance |
| **DSCP** | Differentiated Services Code Point — 6-bit field for marking |
| **Meter** | OpenFlow mechanism to measure and limit bandwidth |
| **Queue** | Buffer with scheduling priority |
| **Strict Priority** | Higher queues always processed first |
| **WFQ** | Weighted Fair Queuing — proportional bandwidth |
| **Rate Limiting** | Enforcing maximum bandwidth |
| **Bandwidth Guarantee** | Minimum assured bandwidth |
| **Jitter** | Variation in packet delay |
| **Bufferbloat** | Excessive buffering causing latency |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""QoS Controller with Traffic Classification"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, tcp, udp
from dataclasses import dataclass
from typing import Dict, Optional
from enum import IntEnum

# ═══════════════════════════════════════════════════════════════════════════════
# TRAFFIC_CLASSES
# ═══════════════════════════════════════════════════════════════════════════════
class TrafficClass(IntEnum):
    """Traffic priority classes."""
    VOICE = 1      # Highest priority (VoIP)
    VIDEO = 2      # High priority (streaming)
    CRITICAL = 3   # Medium priority (database)
    BEST_EFFORT = 4  # Default

@dataclass
class QoSPolicy:
    """QoS policy definition."""
    traffic_class: TrafficClass
    min_rate: int      # kbps guaranteed
    max_rate: int      # kbps maximum
    priority: int      # queue priority

# ═══════════════════════════════════════════════════════════════════════════════
# QOS_CONTROLLER
# ═══════════════════════════════════════════════════════════════════════════════
class QoSController(app_manager.RyuApp):
    """SDN Controller with QoS support."""
    
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    # Traffic classification rules
    CLASSIFICATION_RULES = {
        5060: TrafficClass.VOICE,    # SIP
        5061: TrafficClass.VOICE,    # SIP-TLS
        554: TrafficClass.VIDEO,     # RTSP
        1935: TrafficClass.VIDEO,    # RTMP
        3306: TrafficClass.CRITICAL, # MySQL
        5432: TrafficClass.CRITICAL, # PostgreSQL
    }
    
    # QoS policies per class
    POLICIES = {
        TrafficClass.VOICE: QoSPolicy(TrafficClass.VOICE, 100, 500, 1),
        TrafficClass.VIDEO: QoSPolicy(TrafficClass.VIDEO, 1000, 5000, 2),
        TrafficClass.CRITICAL: QoSPolicy(TrafficClass.CRITICAL, 500, 2000, 3),
        TrafficClass.BEST_EFFORT: QoSPolicy(TrafficClass.BEST_EFFORT, 0, 10000, 4),
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger.info("QoS Controller initialised")
    
    def _classify_packet(self, pkt) -> TrafficClass:
        """
        Classify packet into traffic class.
        
        # 💭 PREDICTION: What if packet doesn't match any rule?
        # Answer: Returns BEST_EFFORT (default class)
        """
        ip = pkt.get_protocol(ipv4.ipv4)
        if not ip:
            return TrafficClass.BEST_EFFORT
        
        # Check TCP/UDP port
        tcp_pkt = pkt.get_protocol(tcp.tcp)
        udp_pkt = pkt.get_protocol(udp.udp)
        
        dst_port = None
        if tcp_pkt:
            dst_port = tcp_pkt.dst_port
        elif udp_pkt:
            dst_port = udp_pkt.dst_port
        
        if dst_port and dst_port in self.CLASSIFICATION_RULES:
            return self.CLASSIFICATION_RULES[dst_port]
        
        # Check DSCP for pre-marked traffic
        dscp = ip.tos >> 2
        if dscp >= 46:  # EF (Expedited Forwarding)
            return TrafficClass.VOICE
        elif dscp >= 34:  # AF41
            return TrafficClass.VIDEO
        elif dscp >= 26:  # AF31
            return TrafficClass.CRITICAL
        
        return TrafficClass.BEST_EFFORT
    
    def _install_qos_flow(self, datapath, match, traffic_class: TrafficClass, 
                          out_port: int) -> None:
        """Install flow with QoS queue assignment."""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        policy = self.POLICIES[traffic_class]
        
        # Output to specific queue
        actions = [
            parser.OFPActionSetQueue(policy.priority),
            parser.OFPActionOutput(out_port)
        ]
        
        instructions = [
            parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)
        ]
        
        # Higher priority = more specific match
        flow_priority = 100 + (5 - policy.priority)
        
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=flow_priority,
            match=match,
            instructions=instructions,
            idle_timeout=60
        )
        
        datapath.send_msg(mod)
        self.logger.info(f"QoS flow installed: class={traffic_class.name}, queue={policy.priority}")
```

---

## 📋 Expected Outputs

### Scenario 1: Traffic Classification

**Test with iperf:**
```bash
# High priority (VoIP port)
iperf3 -c 10.0.0.2 -p 5060 -u -b 100k

# Low priority (default)
iperf3 -c 10.0.0.2 -p 5001 -u -b 10M
```

**Expected log:**
```
[INFO] Packet classified: VOICE (dst_port=5060)
[INFO] QoS flow installed: class=VOICE, queue=1
[INFO] Packet classified: BEST_EFFORT (dst_port=5001)
[INFO] QoS flow installed: class=BEST_EFFORT, queue=4
```

### Scenario 2: Priority Demonstration

**During congestion, measure latency:**
```
Class       | Latency (no QoS) | Latency (with QoS)
------------|------------------|-------------------
VOICE       | 150ms            | 10ms
VIDEO       | 150ms            | 30ms
BEST_EFFORT | 150ms            | 200ms
```

---

## ❓ Frequently Asked Questions

**Q: How do I configure OVS queues?**

A: Use ovs-vsctl:
```bash
ovs-vsctl set port s1-eth1 qos=@newqos -- \
  --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1 -- \
  --id=@q0 create queue other-config:min-rate=1000000 -- \
  --id=@q1 create queue other-config:min-rate=5000000
```

**Q: How do I measure QoS effectiveness?**

A: Compare latency/throughput with and without QoS under congestion:
```bash
# Generate congestion
iperf3 -c 10.0.0.2 -b 100M &

# Measure VoIP latency
ping -c 100 10.0.0.2
```

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 6 | `06enWSL/` | SDN basics, OpenFlow |
| 11 | `11enWSL/` | QoS concepts |
| 14 | `14enWSL/` | Traffic engineering |

---

## 📚 Bibliography

1. **[OFFICIAL]** Ryu QoS Documentation  
   URL: https://ryu.readthedocs.io/en/latest/app/rest_qos.html  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** OVS QoS Configuration  
   URL: https://docs.openvswitch.org/en/latest/howto/qos/  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
