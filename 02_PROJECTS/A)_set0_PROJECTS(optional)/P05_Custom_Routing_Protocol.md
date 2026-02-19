# Project 05: Custom Routing Protocol Implementation

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

---

## 📋 Assessment and Delivery Guide

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md) | [Troubleshooting](../docs/common/troubleshooting_common.md)

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-05`

---

## 📚 Project Description

Implement a simplified routing protocol (Distance Vector or Link State) that allows nodes in a simulated network to discover paths and forward packets. Nodes exchange routing information and build routing tables dynamically.

### 🎯 Learning Objectives

- **Implement** routing algorithms (Bellman-Ford or Dijkstra)
- **Design** routing message formats and exchange protocols
- **Handle** topology changes and route convergence
- **Analyse** routing table construction and updates

### 🛠️ Technologies

| Technology | Purpose |
|------------|---------|
| **Python sockets** | Node communication |
| **UDP** | Routing updates (connectionless) |
| **Graph algorithms** | Path computation |

---

## 🎯 Concept Analogies

### Distance Vector = Asking Neighbours for Directions

🏠 **Real-World Analogy:**  
You ask your neighbours "How far is the post office?" Each neighbour tells you their best known distance. You pick the shortest path through the neighbour with lowest total distance.

💻 **Technical Mapping:**
- Neighbours = Directly connected routers
- Distance = Hop count or metric
- Asking = Sending routing updates
- Picking shortest = Bellman-Ford algorithm

### Link State = Having a Complete Map

🏠 **Real-World Analogy:**  
Everyone shares their local connections with everyone else. Each person builds a complete map and calculates the best path themselves using GPS (Dijkstra).

---

## 🗳️ Peer Instruction Questions

### Question 1: Count to Infinity

> 💭 **PREDICTION:** In Distance Vector, if a link fails, what can happen?

**Options:**
- A) Routes converge immediately
- B) Routes may temporarily loop and "count to infinity" ✓
- C) All routes are dropped
- D) Only the failed link is affected

**Correct answer:** B

**Explanation:** Without techniques like split horizon or poison reverse, nodes may keep incrementing metrics thinking they can reach destination through each other, creating loops.

---

### Question 2: Convergence Time

**Question:** Which converges faster after a topology change?

**Options:**
- A) Distance Vector
- B) Link State ✓
- C) Both are identical
- D) Depends on network size

**Correct answer:** B

**Explanation:** Link State floods updates immediately and each node computes independently. Distance Vector must wait for iterative updates through neighbours.

---

## ❌ Common Misconceptions

### 🚫 Misconception 1: "Routing protocols forward packets"

**WRONG:** "OSPF forwards my HTTP request."

**CORRECT:** Routing protocols build **routing tables**. The forwarding plane uses these tables to actually move packets.

### 🚫 Misconception 2: "Shortest path = fewest hops"

**WRONG:** "3 hops is always better than 4 hops."

**CORRECT:** Metrics can include bandwidth, delay, cost. A 4-hop path through fast links may be "shorter" than 3 hops through slow links.

---

## 📖 Project Glossary

| Term | Definition |
|------|------------|
| **Distance Vector** | Routing based on neighbour-reported distances |
| **Link State** | Routing based on complete topology knowledge |
| **Routing Table** | Maps destinations to next-hop and metric |
| **Convergence** | All routers have consistent, correct routes |
| **Split Horizon** | Don't advertise route back to source |
| **Bellman-Ford** | Algorithm for Distance Vector |
| **Dijkstra** | Algorithm for Link State |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""
Distance Vector Routing Node
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import json
import threading
from typing import Dict, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
INFINITY = 16
UPDATE_INTERVAL = 5  # seconds

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTING_TABLE
# ═══════════════════════════════════════════════════════════════════════════════
class RoutingTable:
    """
    Distance Vector routing table.
    
    Attributes:
        node_id: This node's identifier
        table: Dict mapping destination to (next_hop, distance)
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.table: Dict[str, Tuple[str, int]] = {node_id: (node_id, 0)}
    
    def update_from_neighbour(self, neighbour: str, their_table: Dict, link_cost: int) -> bool:
        """
        Update table based on neighbour's advertisement.
        
        Returns:
            True if table changed
        """
        changed = False
        
        for dest, their_dist in their_table.items():
            new_dist = their_dist + link_cost
            
            if new_dist >= INFINITY:
                continue
            
            current = self.table.get(dest)
            
            # 💭 PREDICTION: When do we update?
            if current is None or new_dist < current[1]:
                self.table[dest] = (neighbour, new_dist)
                changed = True
        
        return changed
    
    def get_advertisement(self) -> Dict[str, int]:
        """Get distance vector for advertising to neighbours."""
        return {dest: info[1] for dest, info in self.table.items()}
```

---

## ❓ Frequently Asked Questions

**Q: How do I simulate multiple nodes on one machine?**

A: Use different UDP ports for each node:
```python
node_a = ("localhost", 5001)
node_b = ("localhost", 5002)
```

**Q: How do I handle node failures?**

A: Use timeouts — if no update from neighbour in N seconds, mark routes through them as infinity.

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 5 | `05enWSL/` | IP addressing, routing concepts |
| 6 | `06enWSL/` | Network protocols, SDN routing |
| 2 | `02enWSL/` | Socket programming for protocol implementation |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
