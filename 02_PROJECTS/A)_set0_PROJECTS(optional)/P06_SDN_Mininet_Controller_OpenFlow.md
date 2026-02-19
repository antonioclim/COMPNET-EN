# Project 06: SDN with Mininet and OpenFlow Controller

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P06
> 
> **Related:** [P01 (SDN Firewall)](P01_SDN_Firewall_Mininet.md) | [P11 (Advanced SDN)](P11_Advanced_SDN_Mininet_OpenFlow.md)

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

**Repository:** `https://github.com/[username]/retele-proiect-06`

#### Required Repository Structure

```
retele-proiect-06/
├── README.md                    # Project description, run instructions
├── docs/
│   ├── specificatii.md          # [E1] Technical specifications
│   ├── diagrame/                # [E1] Architecture diagrams
│   ├── raport_progres.md        # [E2] Progress report
│   └── documentatie_finala.md   # [E3] Complete documentation
├── src/
│   ├── main.py                  # Entry point
│   ├── controller/              # SDN controller modules
│   │   ├── __init__.py
│   │   ├── learning_switch.py   # L2 learning switch
│   │   └── topology.py          # Topology discovery
│   └── utils/                   # Utilities
├── mininet/
│   ├── topology.py              # Custom topology
│   └── configs/                 # Mininet configurations
├── tests/
│   ├── test_smoke.py            # Smoke tests
│   ├── test_controller.py       # Controller unit tests
│   └── expected_outputs/
├── artifacts/
│   └── screenshots/
├── Makefile
├── requirements.txt
├── MANIFEST.txt
├── CHANGELOG.md
└── .gitignore
```

#### Git Commands for Each Stage

```bash
# Stage 1 - After preparing specifications
git add docs/ README.md .gitignore
git commit -m "E1: Initial specifications and design"
git push origin main

# Stage 2 - After implementing prototype
git add src/ mininet/ docs/raport_progres.md
git commit -m "E2: Functional prototype - learning switch"
git push origin main

# Stage 3 - Final version
git add tests/ artifacts/ docs/documentatie_finala.md CHANGELOG.md
git commit -m "E3: Complete final version"
git tag -a v1.0-final -m "Final project version"
git push origin main --tags
```

---

### 📦 Archive Naming Convention

**Format:** `SURNAME_Firstname_GGGG_P06_TT.zip`

**Examples:**
- `POPESCU_Ion_1098_P06_E1.zip` — Stage 1
- `POPESCU_Ion_1098_P06_E2.zip` — Stage 2

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | All requirements identified and documented |
| Architecture diagrams | 20 | Network topology, controller components, data flow |
| Implementation plan | 15 | Realistic timeline with milestones |
| Repository initialised | 15 | GitHub correctly configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Learning switch functional | 35 | MAC learning and forwarding works |
| Code quality | 25 | Clean, commented, type hints present |
| Mininet topology works | 15 | Custom topology runs, controller connects |
| Progress report | 10 | Documents what is done and what remains |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete functionality | 40 | Learning switch + topology discovery + statistics |
| Final code quality | 20 | Production-ready, well-documented |
| Tests | 15 | Unit tests for controller, integration tests |
| Documentation | 10 | Complete README, architecture docs |
| Performance analysis | 5 | Flow table size, convergence time |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: QoS implementation** | +10 | Traffic prioritisation (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Mininet + controller works, traffic flows |
| Technical presentation | 25 | Explains OpenFlow, controller architecture |
| Answers to questions | 20 | Demonstrates deep understanding |
| Team contribution | 15 | Each member knows all the code |
| Time management | 5 | 10-15 minutes per team |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Learning switch + basic topology discovery |
| **2 persons** | + Flow statistics + Multiple topologies |
| **3 persons** | + QoS policies + Performance benchmarking |

---

## 📚 Project Description

Build an SDN controller that manages network topology discovery, implements learning switch functionality and provides basic traffic engineering capabilities using OpenFlow. The controller will run on a Mininet virtual network, communicating with Open vSwitch instances via the OpenFlow protocol.

Software-Defined Networking (SDN) separates the network's control plane (decision-making) from the data plane (packet forwarding). This project implements the control plane as a Python application that instructs switches how to handle traffic. You will learn how modern networks are programmed and gain hands-on experience with network virtualisation.

This project has direct industry relevance — SDN is used by major cloud providers (Google, Amazon, Microsoft) and enterprises to manage their networks programmatically.

### 🎯 Learning Objectives

By completing this project, you will be able to:

- **LO1:** Explain the SDN architecture and the role of the controller
- **LO2:** Implement a learning switch using OpenFlow flow rules
- **LO3:** Develop topology discovery using LLDP packets
- **LO4:** Monitor network state through flow statistics
- **LO5:** Analyse flow table behaviour and convergence time
- **LO6:** Design custom network topologies in Mininet

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Mininet** | Virtual network emulation | [mininet.org](http://mininet.org) |
| **POX/Ryu/OS-Ken** | SDN controller framework | [Ryu SDN](https://ryu-sdn.org) |
| **Open vSwitch** | Software switch implementation | [openvswitch.org](https://www.openvswitch.org) |
| **Python 3** | Controller programming | [python.org](https://python.org) |
| **OpenFlow 1.3** | Switch-controller protocol | [OpenFlow Spec](https://opennetworking.org) |
| **Wireshark** | Packet analysis | [wireshark.org](https://wireshark.org) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **SDN Controller** | Central brain that manages network switches |
| **OpenFlow Protocol** | Standard for controller-switch communication |
| **Flow Table** | List of rules in switch: match → action |
| **Flow Rule** | Single entry: if packet matches X, do Y |
| **PacketIn** | Switch sends unknown packet to controller |
| **FlowMod** | Controller installs rule in switch |
| **LLDP** | Link Layer Discovery Protocol for topology |
| **Learning Switch** | Learns MAC-port mappings dynamically |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST use Python 3.10+ syntax
- [ ] MUST include type hints on ALL public functions
- [ ] MUST use subgoal labels for code sections
- [ ] MUST handle OpenFlow connection errors gracefully
- [ ] MUST log all flow rule installations
- [ ] MUST pass all smoke tests before submission (`make smoke`)
- [ ] MUST work with Mininet's default Open vSwitch

### MUST NOT (Forbidden)
- [ ] MUST NOT use bare `except:` clauses
- [ ] MUST NOT hardcode MAC addresses (learn dynamically)
- [ ] MUST NOT install permanent flows without idle_timeout
- [ ] MUST NOT flood packets after learning is complete
- [ ] MUST NOT leave debug print statements in final code

### SHOULD (Recommended)
- [ ] SHOULD implement flow statistics collection
- [ ] SHOULD support multiple switch connections
- [ ] SHOULD use event-driven architecture
- [ ] SHOULD implement graceful shutdown

---

## 🎯 Concept Analogies

### Learning Switch = Library Card System

🏠 **Real-World Analogy:**  
A library learns which shelf each book belongs to by tracking returns. When someone returns "Introduction to Networks" to Shelf A, the librarian notes this. Next time someone requests that book, the librarian knows exactly where to find it — no need to search all shelves.

🖼️ **Visual Representation:**
```
First request for "Networks" book:
┌─────────────┐
│  LIBRARIAN  │  "I don't know where this is..."
│  (Switch)   │  → Search all shelves (FLOOD)
└─────────────┘

Return observed:
┌─────────────┐
│  LIBRARIAN  │  "Ah! 'Networks' goes to Shelf A"
│  (Switch)   │  → Updates notebook (MAC table)
└─────────────┘

Next request:
┌─────────────┐
│  LIBRARIAN  │  "I know! Shelf A!"
│  (Switch)   │  → Direct lookup (forwarding)
└─────────────┘
```

💻 **Technical Mapping:**
- Librarian = Switch
- Notebook = MAC address table (flow table)
- Book title = MAC address
- Shelf = Switch port
- "Search all shelves" = Flood packet to all ports
- Learning from returns = Learning source MAC from incoming packets

⚠️ **Where the analogy breaks:**  
Unlike a library where books stay on shelves, network hosts can move (laptop changes ports). MAC tables need timeouts to handle this — entries expire if not refreshed.

---

### SDN Controller = Air Traffic Control Tower

🏠 **Real-World Analogy:**  
An air traffic control tower doesn't fly planes — it tells pilots where to go. The tower has radar (network view) showing all aircraft. When a new plane enters airspace, the tower assigns it a flight path. Planes follow instructions without making their own routing decisions.

🖼️ **Visual Representation:**
```
         ┌──────────────┐
         │   CONTROL    │  ← Has complete view
         │    TOWER     │  ← Makes all decisions
         │ (Controller) │  ← Issues instructions
         └──────┬───────┘
                │ OpenFlow
    ┌───────────┼───────────┐
    │           │           │
┌───▼───┐   ┌───▼───┐   ┌───▼───┐
│  S1   │   │  S2   │   │  S3   │  ← Follow orders
│(Switch)│   │(Switch)│   │(Switch)│  ← Don't think
└───────┘   └───────┘   └───────┘
```

💻 **Technical Mapping:**
- Control tower = SDN Controller
- Radar = Topology discovery (LLDP)
- Flight path = Flow rules
- Radio communication = OpenFlow protocol
- Planes = Packets
- Autopilot following path = Switch executing flow rules

⚠️ **Where the analogy breaks:**  
Packets can be duplicated (multicast), which planes cannot. Also, switches can have local rules that persist — they don't need constant radio contact like planes do.

---

## 🗳️ Peer Instruction Questions

Use these questions for collaborative learning. Follow the protocol:
1. Read individually (1 min)
2. Vote your answer (30 sec)
3. Discuss with neighbour (2 min)
4. Re-vote (30 sec)
5. Instructor explains (2 min)

### Question 1: Flow Priority

> 💭 **PREDICTION:** Before reading options, think: if two flow rules match a packet, how does OpenFlow decide which one to apply?

**Scenario:** A switch has two flow rules:
- Rule A: priority=100, match: any → action: flood
- Rule B: priority=200, match: dst=10.0.0.1 → action: output:2

A packet arrives destined for 10.0.0.1.

**Question:** Which rule is applied?

**Options:**
- A) Rule A (first installed wins)
- B) Rule B (higher priority) ✓
- C) Both rules (packet duplicated)
- D) Neither (ambiguity causes drop)

**Correct answer:** B

**Explanation:** OpenFlow uses an explicit priority field. When multiple rules match, the one with the highest priority value wins. Rule B has priority 200 > 100, so it's applied. This is unlike traditional switches where first-match or longest-prefix-match is used.

**Misconception targeted:** Students often think flow tables work like ACLs (first match wins) or routing tables (longest prefix wins).

---

### Question 2: Table-Miss Entry

> 💭 **PREDICTION:** What happens when a packet doesn't match ANY flow rule?

**Scenario:** A new switch connects to the controller. It has an empty flow table. A packet arrives.

**Question:** What is the default behaviour in OpenFlow 1.3?

**Options:**
- A) Flood to all ports
- B) Drop the packet ✓
- C) Send to controller automatically
- D) Queue until rule is installed

**Correct answer:** B

**Explanation:** In OpenFlow 1.3+, the default action for a table-miss (no matching flow) is to DROP the packet. You must explicitly install a table-miss flow rule (priority=0, match=*, action=send-to-controller) to get PacketIn messages. This is a security-by-default design.

**Misconception targeted:** Students expect switches to flood by default like traditional L2 switches or assume PacketIn is automatic.

---

### Question 3: Learning Switch Behaviour

> 💭 **PREDICTION:** When does a learning switch need to ask the controller?

**Scenario:** Host A (port 1) sends to Host B (port 2). The switch has already learned both MAC addresses.

**Question:** Does the switch send a PacketIn to the controller?

**Options:**
- A) Yes, always for the first packet of each flow
- B) No, the installed flow rule handles it directly ✓
- C) Yes, for logging purposes
- D) Only if the packet is ICMP

**Correct answer:** B

**Explanation:** Once a flow rule is installed (match: src_mac=A, dst_mac=B → output:2), the switch handles all matching packets locally. The controller is only involved when no rule matches. This is the performance benefit of SDN — controller handles setup, switches handle forwarding at line rate.

**Misconception targeted:** Students think the controller sees every packet, not realising that flow rules offload work to switches.

---

### Question 4: Flow Idle Timeout

> 💭 **PREDICTION:** What happens when idle_timeout expires?

**Scenario:** Controller installs a flow rule with idle_timeout=60 seconds. Traffic matches the rule for 30 seconds, then stops.

**Question:** What happens 60 seconds after the last matching packet?

**Options:**
- A) Rule remains permanently
- B) Rule is deleted, next packet causes PacketIn ✓
- C) Rule priority decreases
- D) Switch reboots

**Correct answer:** B

**Explanation:** idle_timeout specifies how long a rule survives without matching traffic. After 60 seconds of no matches, the switch deletes the rule. The next packet for that flow will cause a PacketIn, triggering re-learning. This handles host mobility and prevents stale entries.

**Misconception targeted:** Students confuse idle_timeout (no traffic) with hard_timeout (absolute time since installation).

---

## ❌ Common Misconceptions

### 🚫 "Learning switch = the benefit of SDN"

**WRONG:** A learning switch is basic functionality that traditional switches already do. Implementing it in an SDN controller doesn't provide new capabilities.

**CORRECT:** The real SDN benefit is programmability — you can implement ANY forwarding logic (firewalls, load balancers, traffic engineering) by changing controller code, not replacing hardware. The learning switch is just a simple example to understand the architecture.

**Evidence:** Try adding a rule to block traffic between specific hosts — this would require expensive firewall hardware traditionally, but is just a few lines of code in SDN.

---

### 🚫 "Controller handles every packet"

**WRONG:** Having the controller process every packet would be impossibly slow (millions of packets/second vs. controller processing thousands/second).

**CORRECT:** The controller only handles the FIRST packet of each flow (or table-miss packets). It then installs rules so switches handle subsequent packets at hardware speed. This is called "reactive flow installation."

**Evidence:** Check switch flow tables with `ovs-ofctl dump-flows s1` — you'll see rules that handle traffic without controller involvement.

---

### 🚫 "LLDP is for finding hosts"

**WRONG:** LLDP discovers switch-to-switch links, not host locations.

**CORRECT:** LLDP (Link Layer Discovery Protocol) discovers network topology — which switch ports connect to other switches. Hosts are discovered when they send traffic (via PacketIn). These are separate mechanisms.

**Evidence:** In Mininet, LLDP only reveals links between switches (s1-s2, s2-s3). Hosts (h1, h2) are only discovered when they generate traffic.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **SDN (Software-Defined Networking)** | Architecture separating control plane from data plane |
| **OpenFlow** | Protocol for controller-switch communication (port 6653) |
| **Flow Table** | Ordered list of flow rules in a switch |
| **Flow Rule** | Match conditions + actions + priority + timeouts |
| **PacketIn** | Message from switch to controller with unknown packet |
| **FlowMod** | Message from controller to switch to add/modify/delete flow |
| **LLDP** | Link Layer Discovery Protocol for topology mapping |
| **DPID** | Datapath ID — unique identifier for each switch |
| **Learning Switch** | Switch that learns MAC→port mappings from traffic |
| **Table-Miss** | When a packet doesn't match any flow rule |

---

## 🔨 Implementation Stages

### Stage 1 (Week 5) — Design

**Tasks:**
1. Design controller architecture (modules, events, data structures)
2. Define OpenFlow messages to use (PacketIn, FlowMod, StatsRequest)
3. Design network topology (minimum 3 switches, 4 hosts)
4. Create sequence diagrams for learning switch operation
5. Document flow rule format and timeout strategy

**Deliverables:**
- `docs/specificatii.md` — Technical specifications
- `docs/diagrame/` — Architecture and sequence diagrams
- `README.md` — Project overview

---

### Stage 2 (Week 9) — Prototype

**Tasks:**
1. Implement basic learning switch
2. Handle PacketIn events
3. Install flow rules with proper timeouts
4. Create custom Mininet topology
5. Test basic connectivity

**Code Example — Learning Switch:**

```python
#!/usr/bin/env python3
"""
Learning Switch Controller using Ryu/OS-Ken framework.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
from typing import Dict, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
IDLE_TIMEOUT = 60  # seconds before rule expires without traffic
HARD_TIMEOUT = 300  # maximum rule lifetime

# Type aliases
MacAddress = str
PortNumber = int
DatapathId = int
MacTable = Dict[MacAddress, PortNumber]

# ═══════════════════════════════════════════════════════════════════════════════
# LEARNING_SWITCH
# ═══════════════════════════════════════════════════════════════════════════════
class LearningSwitch(app_manager.RyuApp):
    """
    OpenFlow 1.3 Learning Switch Controller.
    
    Learns MAC addresses from incoming traffic and installs
    forwarding rules to enable direct communication.
    
    Attributes:
        mac_tables: MAC→port mapping per switch (by DPID)
    """
    
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    def __init__(self, *args, **kwargs):
        """Initialise controller with empty MAC tables."""
        super().__init__(*args, **kwargs)
        self.mac_tables: Dict[DatapathId, MacTable] = {}
        self.logger.info("Learning Switch Controller initialised")
    
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev) -> None:
        """
        Handle new switch connection.
        
        Installs table-miss flow rule to send unknown packets to controller.
        
        # 💭 PREDICTION: Why do we need this rule?
        # Answer: OpenFlow 1.3 drops packets by default without a table-miss rule
        """
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # Initialise MAC table for this switch
        self.mac_tables[datapath.id] = {}
        self.logger.info(f"Switch {datapath.id} connected")
        
        # Install table-miss flow rule
        match = parser.OFPMatch()  # Match everything
        actions = [parser.OFPActionOutput(
            ofproto.OFPP_CONTROLLER,
            ofproto.OFPCML_NO_BUFFER
        )]
        
        self._add_flow(datapath, priority=0, match=match, actions=actions)
        self.logger.info(f"Installed table-miss rule on switch {datapath.id}")
    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev) -> None:
        """
        Handle PacketIn event — unknown packet arrived at switch.
        
        # 💭 PREDICTION: What two things must we do here?
        # Answer: 1) Learn source MAC→port, 2) Forward or flood packet
        """
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        
        # Parse packet
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        
        if eth is None:
            return
        
        src_mac = eth.src
        dst_mac = eth.dst
        dpid = datapath.id
        
        # Learn source MAC
        self.mac_tables[dpid][src_mac] = in_port
        self.logger.debug(f"Learned: {src_mac} is on port {in_port} (switch {dpid})")
        
        # Determine output port
        if dst_mac in self.mac_tables[dpid]:
            # Known destination — forward directly
            out_port = self.mac_tables[dpid][dst_mac]
            
            # Install flow rule for future packets
            match = parser.OFPMatch(eth_dst=dst_mac)
            actions = [parser.OFPActionOutput(out_port)]
            self._add_flow(datapath, priority=1, match=match, actions=actions)
            self.logger.info(f"Installed flow: {dst_mac} → port {out_port}")
        else:
            # Unknown destination — flood
            out_port = ofproto.OFPP_FLOOD
            self.logger.debug(f"Unknown destination {dst_mac}, flooding")
        
        # Send this packet out
        actions = [parser.OFPActionOutput(out_port)]
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data if msg.buffer_id == ofproto.OFP_NO_BUFFER else None
        )
        datapath.send_msg(out)
    
    def _add_flow(self, datapath, priority: int, match, actions,
                  idle_timeout: int = IDLE_TIMEOUT,
                  hard_timeout: int = HARD_TIMEOUT) -> None:
        """
        Add a flow rule to the switch.
        
        Args:
            datapath: Switch connection
            priority: Rule priority (higher = more important)
            match: Match conditions
            actions: Actions to perform
            idle_timeout: Seconds without traffic before expiry
            hard_timeout: Maximum lifetime in seconds
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        instructions = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions
        )]
        
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=instructions,
            idle_timeout=idle_timeout,
            hard_timeout=hard_timeout
        )
        
        datapath.send_msg(mod)
```

**Deliverables:**
- `src/controller/learning_switch.py` — Learning switch implementation
- `mininet/topology.py` — Custom topology
- `docs/raport_progres.md` — Progress report with test results

---

### Stage 3 (Week 13) — Final Version

**Tasks:**
1. Add topology discovery using LLDP
2. Implement flow statistics collection
3. Add proper logging and monitoring
4. Create thorough tests
5. Document performance metrics

**Deliverables:**
- Complete source code
- Test suite
- Final documentation
- Performance analysis (flow table size, convergence time)

---

### Stage 4 (Week 14) — Presentation

**Demo checklist:**
```
□ Mininet topology starts correctly
□ Controller connects to all switches (check logs)
□ Ping between hosts works (h1 ping h2)
□ Flow rules visible: ovs-ofctl dump-flows s1
□ Traffic stops when controller stops (control plane test)
□ Topology discovery works (show discovered links)
```

**Presentation structure:**
1. SDN introduction (2 min)
2. Architecture explanation (3 min)
3. Live demo (5 min)
4. Challenges and solutions (2 min)
5. Q&A (3 min)

---

## 📋 Expected Outputs

### Scenario 1: Normal Operation

**Input:**
```bash
# Terminal 1: Start controller
ryu-manager src/controller/learning_switch.py

# Terminal 2: Start Mininet
sudo mn --controller=remote --topo=tree,2,2
```

**Expected controller output:**
```
[INFO] Learning Switch Controller initialised
[INFO] Switch 1 connected
[INFO] Installed table-miss rule on switch 1
[INFO] Switch 2 connected
[INFO] Installed table-miss rule on switch 2
```

**Expected Mininet test:**
```
mininet> h1 ping -c 3 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=5.23 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.45 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.38 ms
```

---

### Scenario 2: Flow Rules Verification

**Input:**
```bash
sudo ovs-ofctl dump-flows s1 -O OpenFlow13
```

**Expected output:**
```
cookie=0x0, duration=45.123s, table=0, n_packets=100, n_bytes=8400, 
  priority=1,dl_dst=00:00:00:00:00:02 actions=output:2
cookie=0x0, duration=120.456s, table=0, n_packets=500, n_bytes=42000,
  priority=0 actions=CONTROLLER:65535
```

---

## ❓ Frequently Asked Questions

**Q: Mininet won't connect to controller?**

A: Check controller is running and listening:
```bash
# Verify controller is listening
netstat -tlnp | grep 6653

# Start Mininet with explicit controller IP
sudo mn --controller=remote,ip=127.0.0.1,port=6653
```

**Q: "Connection refused" error from Mininet?**

A: The controller must be started BEFORE Mininet:
```bash
# 1. First start controller
ryu-manager learning_switch.py

# 2. Then start Mininet (in another terminal)
sudo mn --controller=remote
```

**Q: How do I verify learning is working?**

A: Check the flow table before and after traffic:
```bash
# Before any traffic
sudo ovs-ofctl dump-flows s1 -O OpenFlow13
# Should show only table-miss rule

# Generate traffic
mininet> h1 ping h2

# After traffic
sudo ovs-ofctl dump-flows s1 -O OpenFlow13
# Should show new forwarding rules
```

**Q: Can I use POX instead of Ryu?**

A: Yes, POX works but Ryu/OS-Ken is recommended (better maintained):
```bash
# POX (if preferred)
cd pox
./pox.py forwarding.l2_learning
```

**Q: How to clean up Mininet after crash?**

A: Run cleanup command:
```bash
sudo mn -c
```

---

## 🔗 JavaScript → Python Bridge

For students with Web Technologies background:

| JavaScript (TW) | Python (Networks) | Notes |
|-----------------|-------------------|-------|
| Event listeners | Decorators (`@set_ev_cls`) | Similar event-driven pattern |
| `socket.on('data', fn)` | `packet_in_handler(self, ev)` | Async event handling |
| `Map()` | `dict` | MAC table storage |
| `class Component {}` | `class LearningSwitch` | OOP similar |
| `console.log()` | `self.logger.info()` | Use logging module |

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 6 | `06enWSL/` | SDN architecture, OpenFlow 1.3, OS-Ken controller |
| 7 | `07enWSL/` | Packet capture with Wireshark |
| 2 | `02enWSL/` | Socket programming fundamentals |

---

## 📚 Bibliography

> ⚠️ **IMPORTANT:** Use ONLY verified sources. Do NOT invent references!

### Primary Sources (Mandatory)
1. **[OFFICIAL]** Ryu SDN Framework Documentation  
   URL: https://ryu.readthedocs.io/en/latest/  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** Open vSwitch Documentation  
   URL: https://docs.openvswitch.org/  
   Verified: 2026-01-24 ✓

3. **[OFFICIAL]** Mininet Walkthrough  
   URL: http://mininet.org/walkthrough/  
   Verified: 2026-01-24 ✓

### Secondary Sources
4. **[ACADEMIC]** Kreutz, D., et al. (2015). Software-Defined Networking: A Complete Survey.  
   DOI: 10.1109/COMST.2014.2330167

---

## 📝 Final Notes

- **Always verify** that the GitHub repository is updated before deadlines
- **Test** the controller on a clean Mininet instance before presentation
- **Prepare** to explain flow rule format and OpenFlow messages
- **Practice** the demo multiple times — Mininet can be unpredictable
- **Review** the [Presentation Guide](../docs/common/presentation_guide.md) before E4

---

*Last update: January 2026*  
*Computer Networks — ASE Bucharest*
