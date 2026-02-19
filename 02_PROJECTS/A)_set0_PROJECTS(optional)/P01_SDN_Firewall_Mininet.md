# Project 01: SDN Firewall in Mininet

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

**Intermediate checks (optional, for feedback):** Weeks 3, 6, 8, 11

---

### 🐙 GitHub Publication

**MANDATORY:** The project must be published on GitHub before each stage.

#### Your Repository

```
https://github.com/[username]/retele-proiect-01
```

#### Required Repository Structure

```
retele-proiect-01/
├── README.md                    # Project description, run instructions
├── docs/
│   ├── specificatii.md          # [E1] Technical specifications
│   ├── diagrame/                # [E1] Architecture diagrams
│   ├── raport_progres.md        # [E2] Progress report
│   └── documentatie_finala.md   # [E3] Complete documentation
├── src/
│   ├── main.py                  # Entry point
│   ├── controller/              # SDN controller modules
│   └── utils/                   # Utilities
├── mininet/
│   ├── topology.py              # Mininet topology definition
│   └── configs/                 # Configuration files
├── tests/
│   ├── test_firewall.py
│   └── expected_outputs/
├── artifacts/
│   └── screenshots/
├── MANIFEST.txt
├── CHANGELOG.md
└── .gitignore
```

#### What to Publish at Each Stage

| Stage | Mandatory Files/Folders on GitHub |
|-------|-----------------------------------|
| **E1** | `README.md`, `docs/specificatii.md`, `docs/diagrame/`, `.gitignore` |
| **E2** | + `src/` (partial functional code), `mininet/`, `docs/raport_progres.md` |
| **E3** | + `tests/`, `artifacts/`, `docs/documentatie_finala.md`, `CHANGELOG.md` |
| **E4** | Complete repository + tag `v1.0-final` |

#### Git Commands for Each Stage

```bash
# Stage 1 - After preparing specifications
git add docs/ README.md .gitignore
git commit -m "E1: Initial specifications and design"
git push origin main

# Stage 2 - After implementing prototype
git add src/ mininet/ docs/raport_progres.md
git commit -m "E2: Functional prototype"
git push origin main

# Stage 3 - Final version
git add tests/ artifacts/ docs/documentatie_finala.md CHANGELOG.md
git commit -m "E3: Complete final version"
git tag -a v1.0-final -m "Final project version"
git push origin main --tags

# Stage 4 - Final adjustments before presentation
git add .
git commit -m "E4: Presentation preparation"
git push origin main
```

---

### 📦 Archive Naming Convention

**Format:** `SURNAME_Firstname_GGGG_P01_TT.zip`

| Field | Description | Example |
|-------|-------------|---------|
| SURNAME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Firstname | First name (capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| P01 | Project number | P01 |
| TT | Deliverable type (E1-E4 or SXX) | E1 |

**Examples:**
- `POPESCU_Ion_1098_P01_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P01_E2.zip` — Stage 2

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | All requirements identified and documented |
| Architecture diagrams | 20 | Network topology, data flow, components |
| Implementation plan | 15 | Realistic timeline with milestones |
| Repository initialised | 15 | GitHub correctly configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Partial functionality | 35 | Minimum 50% of functional requirements |
| Code quality | 25 | Clean, commented, structured |
| Mininet configured | 15 | Topology works, controller connects |
| Progress report | 10 | Documents what is done and what remains |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete functionality | 40 | All requirements implemented |
| Final code quality | 20 | Production-ready code |
| Tests | 15 | Unit and integration tests |
| Documentation | 10 | Complete README, code comments |
| Comparative analysis | 5 | Comparison with alternatives |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus extensions** | +10 | Additional features (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Application runs and demonstrates requirements |
| Technical presentation | 25 | Explains architecture and decisions |
| Answers to questions | 20 | Demonstrates deep understanding |
| Team contribution | 15 | Each member knows all the code |
| Time management | 5 | 10-15 minutes per team |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Basic complete functionality |
| **2 persons** | + Extended testing + Detailed documentation |
| **3 persons** | + Advanced extensions + Performance analysis |

---

## 📚 Project Description

This project implements a network firewall using the Software-Defined Networking (SDN) model. Instead of a traditional firewall based on dedicated hardware devices, you will implement a firewall application at the SDN controller level that filters traffic between nodes in a virtual network.

The Mininet emulation platform will be used to create a virtual network topology (computers and OpenFlow switches), controlled by an SDN controller (such as POX or Ryu) programmed in Python. The SDN firewall will inspect packets (based on IP addresses, TCP/UDP ports or protocol type) and apply filtering rules (allow/block) dynamically by installing OpenFlow flows in the network switches.

If Mininet feels confusing at first, focus on the topology definition before touching the controller code. In previous years, students who tried to understand everything simultaneously got overwhelmed — the topology is just Python creating virtual links, which is much simpler than the OpenFlow logic.

### 🎯 Learning Objectives

By completing this project, you will be able to:

- **Explain** the SDN architecture and how it separates control and data planes
- **Implement** firewall rules using OpenFlow flow entries
- **Configure** virtual network topologies in Mininet
- **Analyse** network traffic to verify firewall behaviour
- **Evaluate** the impact of security rules on network performance

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Mininet** | Virtual network emulation | [mininet.org](http://mininet.org) |
| **POX/Ryu** | SDN controller framework | [POX](https://github.com/noxrepo/pox), [Ryu](https://ryu-sdn.org) |
| **Python 3** | Controller programming | [python.org](https://python.org) |
| **OpenFlow** | Switch-controller protocol | [OpenFlow Spec](https://opennetworking.org) |
| **Wireshark** | Packet capture and analysis | [wireshark.org](https://wireshark.org) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **Software-Defined Networking** | Separation of control plane from data plane |
| **OpenFlow Protocol** | Communication between controller and switches |
| **Flow Rules** | Match+Action entries in switch flow tables |
| **PacketIn/PacketOut** | Controller-switch message exchange |
| **Network Firewall** | Packet filtering based on rules |

---

## 🎯 Concept Analogies

### SDN Controller = Air Traffic Control Tower

🏠 **Real-World Analogy:**  
An air traffic control tower coordinates all aircraft. Planes don't decide their own routes — they follow instructions from the tower. The tower has the complete picture and makes all routing decisions.

🖼️ **Visual Representation:**
```
         [Controller/Tower]
          ↙    ↓     ↘
       [S1]   [S2]   [S3]    ← Switches follow orders
        ↓      ↓      ↓
      [H1]   [H2]   [H3]    ← Hosts (endpoints)
```

💻 **Technical Mapping:**
- Tower = SDN Controller (POX/Ryu)
- Planes = Packets flowing through network
- Instructions = Flow rules installed via OpenFlow
- Radar = PacketIn messages informing controller

⚠️ **Where the analogy breaks:**  
Unlike planes, packets can be duplicated, modified or silently dropped. Also, flow rules persist in switches — the controller doesn't need to guide every single packet.

### Flow Table = Restaurant Order System

🏠 **Real-World Analogy:**  
A restaurant kitchen has standing orders: "All orders for Table 5 get extra sauce." New waiters check the order board before asking the manager. If there's no rule, they ask.

💻 **Technical Mapping:**
- Order board = Flow table in switch
- Standing order = Flow rule (match → action)
- Asking manager = PacketIn to controller
- Manager's response = FlowMod installing new rule

---

## 🗳️ Peer Instruction Questions

Use these questions for collaborative learning. Follow the protocol:
1. Read individually (1 min)
2. Vote your answer (30 sec)
3. Discuss with neighbour (2 min)
4. Re-vote (30 sec)
5. Instructor explains (2 min)

### Question 1: PacketIn Trigger

> 💭 **PREDICTION:** Before reading the options, think: when does a switch send a PacketIn message to the controller?

**Scenario:** An OpenFlow switch receives a packet destined for 10.0.0.5, but has no flow entry matching this destination.

**Options:**
- A) The switch drops the packet and logs an error
- B) The switch floods the packet to all ports (like a traditional switch)
- C) The switch sends a PacketIn message to the controller ✓
- D) The switch creates a default "allow all" flow entry

**Correct answer:** C

**Explanation:** In OpenFlow, when no flow rule matches an incoming packet, the switch encapsulates the packet in a PacketIn message and sends it to the controller. The controller then decides what to do and may install a new flow rule.

**Misconception targeted:** Students often confuse OpenFlow behaviour with traditional switch flooding.

---

### Question 2: Drop Action Behaviour

**Scenario:** The controller installs this flow rule:
```
match: ip_src=10.0.0.1, ip_dst=10.0.0.2
action: drop
```

**Question:** What happens to matching packets?

**Options:**
- A) Packets are returned to sender with ICMP "Destination Unreachable"
- B) Packets are silently discarded with no notification ✓
- C) Packets are forwarded to controller for logging
- D) Packets are queued until the flow rule expires

**Correct answer:** B

**Explanation:** The `drop` action silently discards packets. No ICMP message is generated unless explicitly programmed. This is different from a router that might send ICMP unreachable.

---

### Question 3: Flow Rule Persistence

**Scenario:** Host h1 pings h2. The controller installs a flow rule. Then h1 pings h2 again.

**Question:** What happens on the second ping?

**Options:**
- A) Another PacketIn is sent to the controller
- B) The switch processes the packet using the cached flow rule ✓
- C) The switch asks the controller if the rule is still valid
- D) The packet is dropped because the flow expired

**Correct answer:** B

**Explanation:** Once a flow rule is installed, subsequent matching packets are handled directly by the switch without controller involvement. This is the key performance benefit of SDN.

---

### Question 4: Multiple Switches

**Scenario:** A network has three switches: S1 → S2 → S3. A packet needs to travel from h1 (connected to S1) to h3 (connected to S3).

**Question:** How many FlowMod messages does the controller need to send for this path?

**Options:**
- A) 1 (only the first switch)
- B) 2 (entry and exit switches)
- C) 3 (one for each switch in the path) ✓
- D) 0 (switches figure it out themselves)

**Correct answer:** C

**Explanation:** Each switch needs its own flow rule to forward the packet to the correct output port. The controller must install rules in all switches along the path.

---

## ❌ Common Misconceptions

### 🚫 Misconception 1: "OpenFlow switches make routing decisions"

**WRONG:** "The switch decides whether to allow or block traffic based on its own logic."

**CORRECT:** In SDN, switches are "dumb" forwarding devices. They only execute flow rules installed by the controller. All intelligence is centralised in the controller.

**Verification:**
```bash
# Show flow table — only controller-installed rules
sudo ovs-ofctl dump-flows s1
# Output shows rules with "actions=" — no switch logic
```

---

### 🚫 Misconception 2: "PacketIn sends the whole packet to controller"

**WRONG:** "Every byte of large packets goes to the controller, causing performance issues."

**CORRECT:** By default, only the first N bytes (buffer) are sent. The switch keeps the full packet and can be instructed to forward it via PacketOut or the controller can just install a rule for future packets.

**Why it matters:** This design prevents controller overload with large packets.

---

### 🚫 Misconception 3: "Flow rules last forever"

**WRONG:** "Once installed, a flow rule stays in the switch permanently."

**CORRECT:** Flow rules have timeouts (idle_timeout, hard_timeout). After the timeout, the rule is removed. This prevents stale rules from accumulating.

**Verification:**
```bash
# Check timeouts in flow rules
sudo ovs-ofctl dump-flows s1
# Look for "idle_timeout=" and "hard_timeout=" fields
```

---

### 🚫 Misconception 4: "Mininet containers are real VMs"

**WRONG:** "Each Mininet host runs in its own virtual machine."

**CORRECT:** Mininet uses Linux network namespaces, not VMs. Hosts share the same kernel but have isolated network stacks. This makes Mininet lightweight but means all hosts run the same OS.

---

### 🚫 Misconception 5: "The firewall blocks at the switch port"

**WRONG:** "Blocking a host means disconnecting its switch port."

**CORRECT:** SDN firewalls work at the flow level, not port level. You can block specific traffic (e.g., ICMP) while allowing other traffic (e.g., TCP) from the same host.

---

## 📖 Project Glossary

| Term | Definition | Example |
|------|------------|---------|
| **SDN** | Software-Defined Networking — architecture separating control and data planes | Controller decides, switches forward |
| **OpenFlow** | Protocol for controller-switch communication | Version 1.0, 1.3, 1.5 |
| **Flow Rule** | Match criteria + actions in switch table | `match=ip_dst:10.0.0.1 action=output:2` |
| **PacketIn** | Message from switch to controller when no rule matches | Contains packet header + buffer ID |
| **PacketOut** | Message from controller telling switch to send a packet | Used for ARP replies, ICMP |
| **FlowMod** | Message from controller installing/modifying flow rules | Add, modify, delete operations |
| **DPID** | Datapath ID — unique identifier for each switch | 64-bit number |
| **Flow Table** | Collection of flow rules in a switch | Checked in priority order |
| **Match Fields** | Packet header fields to match | in_port, eth_src, ip_dst, tcp_dport |
| **Actions** | What to do with matching packets | output, drop, set_field, goto_table |
| **Mininet** | Network emulator using Linux namespaces | Creates virtual switches and hosts |
| **POX/Ryu** | Python SDN controller frameworks | POX simpler, Ryu more features |
| **OVS** | Open vSwitch — software OpenFlow switch | Default switch in Mininet |

---

## 💭 Prediction Checkpoints

Include these prediction moments in your development process:

### E1 - Design Phase
> 💭 **Before designing topology:** How many switches do you need for your firewall rules? What happens if you use just one switch vs. multiple switches?

### E2 - Prototype Phase
> 💭 **Before running first test:** What will `pingall` show if your firewall blocks ICMP between h1 and h2?
> 
> Expected: h1 → h2 fails, h2 → h1 fails, other pairs succeed

> 💭 **Before checking flows:** How many flow rules will be in switch s1 after `pingall`?
> 
> Verify with: `sudo ovs-ofctl dump-flows s1 | wc -l`

### E3 - Final Phase
> 💭 **Before performance test:** What latency increase do you expect from the firewall?
> 
> Measure with: `h1 ping -c 100 h2` (compare with/without firewall)

---

## 🔨 Implementation Stages

### Stage 1 (Week 5) — Analysis and Design

**Tasks:**
1. Document SDN and OpenFlow concepts
2. Define security policy (what traffic to block/allow)
3. Design Mininet topology (e.g., 2 switches, 4 hosts)
4. Choose controller platform (POX recommended for simplicity)
5. Create repository structure

**Deliverables:**
- `docs/specificatii.md` — Firewall specifications
- `docs/diagrame/` — Network topology diagram
- Repository initialised with README

---

### Stage 2 (Week 9) — Functional Prototype

**Tasks:**
1. Implement Mininet topology
2. Develop controller with at least one filtering rule
3. Test prototype with traffic tests
4. Collect results (Wireshark captures, controller logs)

**Example controller structure:**
```python
#!/usr/bin/env python3
"""
SDN Firewall Controller — Prototype
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from pox.core import core
from pox.lib.packet import ethernet, ipv4, icmp
import pox.openflow.libopenflow_01 as of

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
BLOCKED_HOSTS = [("10.0.0.1", "10.0.0.2")]  # Block ICMP between these
LOG = core.getLogger()

# ═══════════════════════════════════════════════════════════════════════════════
# FIREWALL_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
class SimpleFirewall:
    """
    Simple SDN firewall blocking ICMP between specified hosts.
    
    Attributes:
        connection: OpenFlow connection to switch
        blocked_pairs: List of (src, dst) tuples to block
    """
    
    def __init__(self, connection):
        """Initialise firewall for a switch connection."""
        self.connection = connection
        connection.addListeners(self)
        LOG.info(f"Firewall active on switch {connection.dpid}")
    
    def _handle_PacketIn(self, event):
        """
        Handle packets sent to controller.
        
        Args:
            event: PacketIn event containing packet data
        """
        packet = event.parsed
        
        # 💭 PREDICTION: What type is 'packet' at this point?
        # Answer: pox.lib.packet.ethernet
        
        if packet.type == ethernet.IP_TYPE:
            ip_packet = packet.payload
            
            # Check if this traffic should be blocked
            if self._should_block(ip_packet):
                self._install_drop_rule(event, ip_packet)
                return
        
        # Default: flood packet
        self._flood(event)
    
    def _should_block(self, ip_packet: ipv4) -> bool:
        """Check if packet matches blocking rules."""
        src = str(ip_packet.srcip)
        dst = str(ip_packet.dstip)
        
        for blocked_src, blocked_dst in BLOCKED_HOSTS:
            if src == blocked_src and dst == blocked_dst:
                return True
        return False
    
    def _install_drop_rule(self, event, ip_packet: ipv4) -> None:
        """Install flow rule to drop matching packets."""
        msg = of.ofp_flow_mod()
        msg.match.dl_type = ethernet.IP_TYPE
        msg.match.nw_src = ip_packet.srcip
        msg.match.nw_dst = ip_packet.dstip
        msg.idle_timeout = 60
        msg.hard_timeout = 120
        # No actions = drop
        self.connection.send(msg)
        LOG.info(f"Blocking: {ip_packet.srcip} → {ip_packet.dstip}")
    
    def _flood(self, event) -> None:
        """Flood packet to all ports."""
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def launch():
    """Start the firewall component."""
    def start_firewall(event):
        SimpleFirewall(event.connection)
    
    core.openflow.addListenerByName("ConnectionUp", start_firewall)
    LOG.info("Simple Firewall running")
```

**Deliverables:**
- `src/controller/firewall.py` — Controller code
- `mininet/topology.py` — Topology definition
- `docs/raport_progres.md` — Progress report with test results

---

### Stage 3 (Week 13) — Final Version and Testing

**Tasks:**
1. Extend firewall with full rule set
2. Add logging for blocked packets
3. Create extensive tests
4. Document performance metrics
5. Compare with alternatives

**Deliverables:**
- Complete source code
- Test suite
- Final documentation
- Comparative analysis

---

### Stage 4 (Week 14) — Final Presentation

**Demo checklist:**
```
□ Mininet topology starts correctly
□ Controller connects to switches
□ Allowed traffic passes (show with ping)
□ Blocked traffic is dropped (show with ping)
□ Flow rules visible with ovs-ofctl
□ Logs show firewall decisions
```

**Presentation structure:**
1. Introduction to SDN firewalls (2 min)
2. Architecture explanation (3 min)
3. Live demo (5 min)
4. Challenges and solutions (2 min)
5. Q&A (3 min)

---

## ❓ Frequently Asked Questions

**Q: Mininet won't start — error "cannot create interface"**

A: Clean previous sessions and run with sudo:
```bash
sudo mn -c                                    # Clean up
sudo mn --topo single,3 --controller remote   # Start fresh
```

**Q: Controller doesn't receive PacketIn messages**

A: Check switch-controller connection:
```bash
# In Mininet CLI
dpctl show
# Should show connection to controller IP
```

**Q: How do I verify the firewall is working?**

A: Test allowed and blocked traffic:
```bash
# In Mininet CLI
h1 ping -c 3 h2    # Should fail if blocked
h1 ping -c 3 h3    # Should succeed if allowed

# Check flow rules
sudo ovs-ofctl dump-flows s1
```

**Q: How do I see what the controller is doing?**

A: Check controller logs:
```bash
# POX logging
./pox.py log.level --DEBUG forwarding.l2_learning

# Or add print statements to your controller
```

**Q: Can I use Ryu instead of POX?**

A: Yes. Ryu has more features and better documentation:
```bash
pip install ryu
ryu-manager your_firewall.py
```

---

## 🔗 JavaScript → Python Bridge

You have experience with JavaScript from Web Technologies. Here's how concepts translate:

| JavaScript (TW) | Python (Networks) | Notes |
|-----------------|-------------------|-------|
| `const fn = (x) => x * 2` | `fn = lambda x: x * 2` | Arrow functions → lambda |
| `arr.map(x => x * 2)` | `[x * 2 for x in arr]` | List comprehension |
| `arr.filter(x => x > 0)` | `[x for x in arr if x > 0]` | Filter in comprehension |
| `JSON.parse(str)` | `json.loads(str)` | Parse JSON |
| `async/await` | `async/await` with `asyncio` | Similar syntax |

**Event handling comparison:**
```javascript
// JavaScript event listener
socket.on('data', (data) => {
    console.log(data);
});
```

```python
# Python POX event handler
def _handle_PacketIn(self, event):
    """Handle incoming packet event."""
    packet = event.parsed
    print(packet)
```

---

## 📚 Laboratory References

Consult these resources from the **netENwsl** archive (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 6 | `06enWSL/` | SDN architecture, OpenFlow 1.3, OS-Ken controller |
| 7 | `07enWSL/` | Packet capture with Wireshark, Scapy |
| 2 | `02enWSL/` | Socket programming fundamentals |

---

## 📚 Bibliography

1. Kreutz, D., et al. (2015). Software-Defined Networking: A Thorough Survey. IEEE Communications Surveys & Tutorials, 17(1), 27-51.

2. Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: Rapid prototyping for software-defined networks. HotNets-IX.

3. Hu, H., et al. (2014). FlowGuard: Building solid firewalls for software-defined networks. HotSDN '14.

4. Göransson, P., Black, C., & Culver, T. (2014). Software Defined Networks: A Complete Approach. Morgan Kaufmann.

---

## 📝 Final Notes

- **Always verify** that the GitHub repository is updated before deadlines
- **Test** the application on a clean machine before presentation
- **Prepare** answers for questions about architecture and code
- **Communicate** with team members to coordinate contributions
- **Review** the [Presentation Guide](../docs/common/presentation_guide.md) before E4

---

*Last update: January 2026*  
*Computer Networks — ASE Bucharest*
