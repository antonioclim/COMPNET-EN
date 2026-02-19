### Computer Networks
### Fundamentals: concepts, components and classifications

---

### Overview
- Motivation
- Learning objectives
- Lecture structure
- Requirements and marking scheme
- Resources and tools

---

### Learning objectives
By the end of the lecture, students should be able to:
- Define a computer network
- Classify networks by size and topology
- Explain the role of transmission media and networking devices
- Understand the notions of protocol, protocol stack and encapsulation
- Conceptually follow the path of a message across a network

---

### What is a computer network?
- A set of interconnected computing systems
- Communication between systems has two components:
  - physical: devices and media
  - logical: protocols

[FIG] assets/images/fig-network-vs-system.png

---

### Why are networks useful?
- Resource sharing
- Access to remote resources
- Long-distance communication
- Coordination of actions
- Scaling processing and storage capacity

---

### Standards in networking
- IEEE (e.g., 802.3, 802.11)
- RFCs (IETF)
- Programming standards (Berkeley sockets API)

---

### Network size
- LAN (Local Area Network)
  - room, building, campus
- WAN (Wide Area Network)
  - region, country, continent
- Internet
  - global interconnection of WANs and LANs

[FIG] assets/images/fig-lan-wan-internet.png

---

### LAN: characteristics
- Small scale
- Low latency
- Low error rates
- Common technologies: Ethernet and Wi‑Fi

---

### WAN: characteristics
- Interconnects multiple LANs
- End hosts are in distinct subnets
- Transmission takes place through packet routing

---

### Network topology
- How nodes are connected
- Physical topology vs logical topology
- Point-to-point vs multipoint
- Symmetric vs asymmetric

---

### Common topologies
[FIG] assets/images/fig-topologies.png

---

### Classification by topology
|               | Symmetric                   | Asymmetric                    |
|--------------|-----------------------------|-------------------------------|
| Point to point | ring, fully connected mesh | star, partial mesh, tree      |
| Multipoint     | bus, ring                  | satellite                     |

---

### Transmission media
- Guided:
  - copper (coaxial, twisted pair)
  - optical fibre
- Unguided:
  - wireless (radio)

[FIG] assets/images/fig-media.png

---

### Transmission parameters
- bandwidth: amount of data per second
- latency: delay
- jitter: delay variation
- loss: packet loss

[SCENARIO] assets/scenario-ping-traceroute/

---

### Transmission mechanisms
- Broadcast
- Point-to-point

---

### Switching types
- Circuit switching
- Packet switching

[FIG] assets/images/fig-circuit-vs-packet.png

---

### Communication devices
- NIC
- repeater
- hub
- switch
- router

[FIG] assets/images/fig-devices.png

---

### Hub vs switch vs router
- hub: forwards to all nodes
- switch: forwards selectively
- router: interconnects networks

[FIG] assets/images/fig-hub-switch-router.png

---

### Logical communication models
- Client–server
- Peer-to-peer

Note: in programming terms, communication is always client–server.

---

### Communication protocols
- Protocol = rules, syntax and behaviour
- Implemented in hardware or software
- Protocols compose and build on one another

---

### Protocol stacks
- Layering and separation of concerns
- Each layer provides services
- Each layer has its own transfer unit

---

### Encapsulation
- Data is wrapped successively
- Each layer adds a header
- Lower layers do not interpret the payload

[FIG] assets/images/fig-encapsulation.png

---

### A brief traffic analysis
- What a real packet looks like
- What we observe during a ping
- What we observe during a DNS query

[SCENARIO] assets/scenario-capture-basics/

---

### Summary
- Classifications (LAN, WAN and the Internet)
- Topologies and media
- Networking devices
- Protocols, stacks and encapsulation

---

### Preparation for Lecture 2
- Architectural models: OSI and TCP/IP
- Formalising layers and responsibilities
