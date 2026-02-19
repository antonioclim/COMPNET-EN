### Routing protocols
### RIP, EIGRP (context), OSPF and link-state ideas

---

### Learning objectives
By the end of the lecture, students should be able to:
- Explain the role of a router and what 'forwarding' vs 'routing' means
- Explain what a routing table contains and how a 'next hop' is chosen
- Distinguish static routes from dynamic routes and when each is useful
- Understand the difference between distance-vector and link-state approaches
- Briefly explain RIP (hop count, timers and typical issues)
- Briefly explain OSPF (LSDB, hello, DR/BDR, SPF/Dijkstra and areas)
- Run examples: Bellman–Ford, Dijkstra and Mininet with static routing

---

### What is the role of a router?
- A router connects two or more networks
- It receives packets and decides on which interface to forward them
- It can also provide secondary functions: filtering, NAT, QoS and tunnelling (context)

[FIG] assets/images/fig-router-role.png

---

### Routing vs forwarding
- Forwarding: the local decision 'send out via interface X to next hop Y'
- Routing: how we learn and maintain the information that drives forwarding (static routes or protocols)

---

### The routing process (concept)
- The router maintains a routing table
- For each known prefix: next hop, interface, metric and source (static/dynamic)
- Directly connected routes appear automatically

---

### Route types
- Static (manual):
  - precise control
  - simple and useful for stub networks
  - not scalable
- Dynamic (via protocols):
  - scalable
  - adapts to failures (depending on the protocol)

---

### Routing metrics
- hop count (simple)
- latency, bandwidth, reliability, load and administrative cost (depending on the protocol)
- multiple routes can exist with the same metric (ECMP)

---

### What changes along a path (L2 vs L3)
- Source and destination IP remain the same
- Source and destination MAC change at each hop
- TTL/Hop Limit decreases at each hop

[FIG] assets/images/fig-l2-l3-changes.png

---

### Routing tables
- Hosts also have routing tables, not only routers
- Stored in RAM
- Contains:
  - directly connected routes
  - static routes
  - dynamic routes
  - the default route

[FIG] assets/images/fig-routing-table.png

---

### Network classification from a router perspective
- connected (directly connected)
- known (static/dynamic)
- unknown (default route or drop)

---

### Asymmetric routing
- each router decides locally
- there is no guarantee that the outbound and return paths are identical

---

### IGP vs EGP
- IGP: inside an autonomous system (RIP, OSPF, EIGRP, IS-IS)
- EGP: between autonomous systems (BGP) (mentioned here for context)

---

### Distance-vector (idea)
- the router does not know the full topology
- it knows a 'distance' to networks and a next hop
- periodic (classic) or incremental updates (protocol dependent)
- associated algorithm: Bellman–Ford (conceptually)

[FIG] assets/images/fig-distance-vector.png

[SCENARIO] assets/scenario-bellman-ford/

---

### RIP (Routing Information Protocol)
- metric: hop count
- maximum hop count: 15 (16 = infinity)
- runs over UDP port 520
- RIPv1: no mask (no CIDR/VLSM)
- RIPv2: includes the mask, multicast 224.0.0.9 and can use authentication
- RIPng: for IPv6

---

### RIP issue: routing loops and count-to-infinity
- under certain failures, metrics 'grow' towards infinity
- classic mechanisms:
  - split horizon
  - route poisoning
  - holddown
  - timeout/flush

[FIG] assets/images/fig-rip-loop.png

---

### RIP timers (concept)
- update timer
- invalid timer
- flush timer
- holddown timer

---

### Link-state (idea)
- each router builds a topology database (LSDB)
- it computes optimal routes locally (SPF)
- associated algorithm: Dijkstra (conceptually)

[FIG] assets/images/fig-link-state.png

[SCENARIO] assets/scenario-dijkstra/

---

### OSPF (Open Shortest Path First)
- link-state IGP
- uses hello messages and LSAs (conceptually)
- uses multicast (depending on network type)
- splits the network into areas with a backbone (Area 0)

[FIG] assets/images/fig-ospf-areas.png

---

### OSPF operation (briefly)
- hello: neighbour discovery and adjacency maintenance
- LSDB synchronisation between neighbours
- DR/BDR election on multi-access segments
- route calculation: SPF (Dijkstra) based on the LSDB

---

### Where Mininet fits in the course
- We use a simple topology with three routers
- We assign addresses and static routes
- We inspect routing tables and verify connectivity

[SCENARIO] assets/scenario-mininet-routing/

---

### Summary
- Static routes are useful for stub networks and simple topologies
- RIP: simple, hop count, limitations and convergence issues
- OSPF: link-state, scalable, SPF and areas
- BGP: a different context (inter-AS) and typically covered in Internet operations (optional)
