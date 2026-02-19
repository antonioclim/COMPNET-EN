### Computer Networks
### Architectural models: OSI and TCP/IP

---

### Overview
- Why we need architectural models
- The role of layering in managing complexity
- The connection to real-world protocols

---

### Learning objectives
By the end of the lecture, students should be able to:
- Explain the purpose of a network architectural model
- Describe the role of each layer in the OSI model
- Associate concrete protocols with OSI and TCP/IP layers
- Compare the OSI model with the TCP/IP model
- Follow the encapsulation process across layers

---

### Why architectural models?
- Networks are complex systems
- Layering:
  - reduces complexity
  - enables interoperability
  - allows independent development
- A layer:
  - offers services to the layer above
  - uses services from the layer below

---

### Key concepts (recap from Lecture 1)
- protocol
- protocol stack
- transfer unit
- encapsulation

This lecture formalises these notions.

---

### Historical network models
- Various proprietary models (e.g., IPX/SPX)
- Lack of interoperability
- The need for a standardised model

---

### The OSI model: introduction
- OSI = Open Systems Interconnection
- Created by ISO (International Organization for Standardization)
- A theoretical model
- Aim: a complete description of network communication
- Independent of hardware and operating system

---

### OSI model structure
- A model organised into 7 layers
- Fine granularity
- Each layer has a clearly defined role

[FIG] assets/images/fig-osi-layers.png

---

### Layer 1 – Physical
Role:
- Transmitting bits over the physical medium

Transfer unit:
- bit

Functions:
- signal modulation
- bit-level synchronisation
- transmission rate control
- physical medium configuration

Examples:
- Ethernet cable
- electrical, optical or radio signal

---

### Layer 2 – Data link
Role:
- Frame transfer between directly connected nodes

Transfer unit:
- frame

Functions:
- physical addressing (MAC)
- error detection (CRC)
- flow control
- frame delimitation

Sublayers:
- MAC (Media Access Control)
- LLC (Logical Link Control)

---

### Layer 3 – Network
Role:
- Delivering packets across different networks

Transfer unit:
- packet

Functions:
- logical addressing (hierarchical)
- routing
- fragmentation and reassembly

Examples:
- IP

---

### Layer 4 – Transport
Role:
- process-to-process communication

Transfer unit:
- segment (TCP) / datagram (UDP)

Functions:
- ports
- flow control
- error control
- reordering
- acknowledgements (for connection-oriented protocols)

---

### Layer 5 – Session
Role:
- Managing the dialogue between applications

Functions:
- session establishment
- session maintenance
- session termination
- dialogue control (half/full duplex)

Note:
- often implemented implicitly in modern applications

---

### Layer 6 – Presentation
Role:
- Data representation

Functions:
- encoding and decoding
- format conversions
- compression
- encryption

Examples:
- TLS (conceptually)
- UTF‑8, JSON, ASN.1

---

### Layer 7 – Application
Role:
- The interface to the user or the application

Functions:
- file transfer
- email
- remote resource access

Examples:
- HTTP
- FTP
- SMTP
- DNS

---

### Communication between OSI layers
- Layers communicate only with adjacent layers
- Communication:
  - vertical (within a system)
  - horizontal (between peer layers)

[FIG] assets/images/fig-osi-communication.png

---

### Encapsulation in the OSI model
- Data is encapsulated progressively
- Each layer adds its own header
- At the receiver, the process is reversed

[FIG] assets/images/fig-osi-encapsulation.png

---

### Where layers are implemented
- Lower layers: hardware and drivers
- Transport: operating system
- Upper layers: applications

[FIG] assets/images/fig-osi-implementation.png

---

### Limitations of the OSI model
- A theoretical model
- Rarely implemented as-is
- Some layers are difficult to separate in practice

---

### The TCP/IP model: introduction
- The practical model of the Internet
- Developed before OSI
- Based on real protocols, not an idealised model

---

### TCP/IP model structure
- 4 main layers

[FIG] assets/images/fig-tcpip-layers.png

---

### Network access layer (TCP/IP)
- Equivalent to:
  - Physical + Data link (OSI)
- Provides connectivity to the network

Examples:
- Ethernet
- Wi‑Fi

---

### Internet layer (TCP/IP)
Role:
- Delivering IP packets

Characteristics:
- connectionless protocol
- no delivery guarantees
- independent routing

Protocols:
- IP
- ICMP

---

### Transport layer (TCP/IP)
Fundamental protocols:
- TCP (connection-oriented)
- UDP (connectionless)

TCP provides:
- acknowledgements
- flow control
- error control
- reordering

UDP provides:
- simplicity
- minimal overhead
- performance

---

### Application layer (TCP/IP)
- Combines:
  - Session
  - Presentation
  - Application (OSI)

Examples:
- HTTP
- DNS
- SMTP
- FTP
- SSH

---

### OSI vs TCP/IP: comparison
- OSI:
  - theoretical model
  - 7 layers
  - strict separation
- TCP/IP:
  - practical model
  - 4 layers
  - flexible separation

---

### OSI–TCP/IP equivalences
[FIG] assets/images/fig-osi-vs-tcpip.png

---

### Why do we use both models?
- OSI:
  - analysis
  - learning
  - conceptual troubleshooting
- TCP/IP:
  - real-world implementation
  - programming
  - the Internet

---

### The link to network programming
- Applications use:
  - sockets
  - ports
- The operating system implements:
  - transport
  - IP
- Hardware implements:
  - network access

---

### Summary
- The role of models
- OSI layers
- TCP/IP layers
- Differences and equivalences
- Layered encapsulation

---

### Preparation for Lecture 3
- Network programming
- Sockets
- TCP vs UDP in practice
