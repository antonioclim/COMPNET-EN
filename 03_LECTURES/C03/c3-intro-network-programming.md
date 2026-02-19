### Introduction to network application programming

---

### Learning objectives
By the end of the lecture, students should be able to:
- Explain the difference between building an application over HTTP and programming directly with sockets at the transport layer
- Use TCP and UDP sockets (client and server)
- Understand typical issues: framing, concurrency, timeouts and sessions
- Understand what RAW sockets are and when they are appropriate

---

### General considerations (protocol design)
- Transfer units: format, size and representation (bytes vs text)
- Communication protocols: commands, responses and errors
- Unidirectional vs bidirectional
- Stateful vs stateless
- Error signalling (codes, messages and retries)
- Extensibility (versions and optional fields)
- Security (authentication, encryption and integrity)

---

### Abstractions above the application layer
- We treat an existing application protocol as the underlying channel
- We ignore layers below the application layer
- Example: HTTP for remote object access (REST) or RPC

[FIG] assets/images/fig-app-over-http.png

---

### Programming at the transport layer
- We use TCP or UDP as the channel
- We implement servers that respect an application protocol (e.g., a minimal HTTP)
- Or we define custom protocols

At the foundation: Berkeley sockets.

---

### What is a socket?
- A structure/object that represents a communication endpoint
- On Unix, it is similar to a file (a descriptor)
- Identified by: IP address + port + protocol (TCP/UDP)

---

### Socket types
- TCP (stream sockets)
- UDP (datagram sockets)
- RAW sockets (below the transport layer)

---

### TCP: characteristics
- Connection-oriented
- A byte stream (not 'messages')
- In-order delivery (under normal conditions)
- Flow control and retransmissions (handled by TCP)
- Application concern: message delimitation (framing)

---

### The flow of a TCP server (accept loop)
[FIG] assets/images/fig-tcp-server-flow.png

---

### TCP: issue 1 – framing (stream ≠ message)
- `recv(1024)` does not guarantee that you receive a complete message
- Common solutions:
  - delimiter (e.g., newline)
  - length prefix
  - TLV-style formats

[SCENARIO] scenario-tcp-framing/

---

### TCP: issue 2 – concurrency
- A simple server blocks on a single client
- Common solutions:
  - thread per client
  - process per client
  - async/event loop (select, epoll)

[FIG] assets/images/fig-tcp-concurrency.png

[SCENARIO] scenario-tcp-multiclient/

---

### TCP: timeouts and connection closure
- Timeouts for connect/recv
- The client can close the connection (`recv` returns 0 bytes)
- Robust error handling is essential

---

### UDP: characteristics
- Connectionless
- One message = one datagram (size limits apply)
- No guarantees of delivery, ordering or uniqueness
- The server does not 'accept', it uses `recvfrom`/`sendto`

---

### The flow of a UDP server
[FIG] assets/images/fig-udp-server-flow.png

---

### UDP: common pitfalls
- 'Sessions' at the application layer (client identification)
- Acknowledgements (ACK) and retransmissions at the application layer
- Multi-step commands (state)

[SCENARIO] scenario-udp-session-ack/

---

### RAW sockets (below the transport layer)
- You send and receive packets 'below' TCP/UDP
- Requires privileges (root/admin)
- Used for tooling (diagnostics), research and custom implementations

[FIG] assets/images/fig-raw-layering.png

---

### Scapy (packet construction)
- Enables construction and transmission of L3/L2 packets
- Useful for learning: IP/ICMP, simple DNS and similar examples

[SCENARIO] scenario-scapy-icmp/

---

### Summary
- HTTP as an application-layer abstraction vs direct socket programming
- TCP: streams, framing and concurrency
- UDP: datagrams and sessions/ACKs in the application
- RAW sockets/Scapy: below transport with elevated privileges

---

### Preparation for the next lecture
- In Lecture 4: the physical layer and the data link layer
- We will connect the concepts: frames, MAC, switches and collisions/CSMA (conceptually)
