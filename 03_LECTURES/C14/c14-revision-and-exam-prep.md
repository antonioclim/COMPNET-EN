### Lecture 14 – Revision and examination preparation
### Integrating the stack: from physical links to application services

---

### Why a revision lecture?

This final lecture has three aims:

* consolidate the conceptual map of the protocol stack
* connect lecture content to seminar practice and project deliverables
* practise the style of reasoning expected in an examination setting

The focus is on clarity and justification at the correct layer rather than memorising lists.

---

### Learning objectives

By the end of this lecture, students should be able to:

* explain how layering supports interoperability and diagnosis
* identify which layer a question is really asking about
* reason about reliability, performance and security trade-offs
* justify protocol choices using constraints, evidence and expected behaviour
* prepare a revision plan based on the weekly question bank and seminar artefacts

---

### A revision map of the course

[FIG] assets/images/fig-course-map.png

Use this diagram as a navigation tool:

* top-down: start from an application requirement and derive lower-layer needs
* bottom-up: start from an observed packet trace and infer higher-layer behaviour

---

### Layering: what it gives you

Layering is not an abstract modelling choice.
It is a method of controlling complexity.

Key consequences:

* specifications can be independently implemented and still interoperate
* a fault can often be localised to a layer using observable symptoms
* security controls can be expressed at multiple layers, each with different strength

---

### What exam questions typically assess

An examination question in networking rarely asks for a definition in isolation.
It usually tests whether you can connect:

* a requirement to a protocol mechanism
* a packet trace to a protocol state machine
* a failure symptom to a plausible root cause

If your answer stays at the wrong layer, it is usually marked as incomplete.

---

### Physical and link layer: revision anchors

If a question mentions signal quality, timing or medium constraints, start here.

Revision anchors:

* line coding and modulation describe how bits are represented on a medium
* framing turns a bit stream into bounded units with structure and error detection
* switching is a forwarding decision based on link-layer addresses

Common confusion to avoid:

* a switch does not route, it forwards frames inside a broadcast domain
* bandwidth is not latency, throughput is not goodput

---

### Network layer: revision anchors

If a question mentions reachability, addressing or path selection, start here.

Revision anchors:

* IPv4 and IPv6 address structure and scope
* subnetting, CIDR and VLSM as allocation and aggregation tools
* forwarding based on a routing table, not on application intent
* NAT and PAT as translation mechanisms with operational trade-offs

Common confusion to avoid:

* ARP and NDP resolve link-layer next hop information, they are not routing protocols
* ICMP is not an error, it is a control and diagnostic channel

---

### Transport layer: revision anchors

If a question mentions reliability, ordering or congestion behaviour, start here.

Revision anchors:

* TCP provides a byte stream with reliability and flow control
* UDP provides datagrams with minimal semantics
* TLS provides confidentiality and integrity above the transport abstraction
* connection management is a state machine and traces can reveal state

Common confusion to avoid:

* TCP is not faster by definition, it is more robust in loss and reordering
* encryption is not authentication, certificates bind identities to public keys

---

### Application layer: revision anchors

If a question mentions semantics, message structure or operational roles, start here.

Revision anchors:

* HTTP is a request response protocol with intermediaries and caches
* DNS is a distributed naming system with caching and delegation
* SMTP moves mail between servers, POP3 and IMAP retrieve mail to a client
* SSH provides secure remote control and tunnelling
* IoT scenarios typically use publish subscribe messaging (MQTT)

Common confusion to avoid:

* DNS is not a database, it is a cache heavy hierarchy with distinct consistency rules
* REST is an architectural style, it is not a synonym for JSON over HTTP

---

### Security reasoning across layers

Security is not a single protocol.
It is a set of controls that must compose.

When answering a security question, separate:

* the threat model (what the attacker can do)
* the control (what mechanism exists)
* the residual risk (what remains possible)

Examples:

* link layer: segmentation and containment (VLANs)
* network layer: filtering and routing policy
* transport layer: encryption, integrity and endpoint authentication (TLS)
* application layer: input validation, authorisation and secure defaults

---

### Revision workflow: evidence based study

Efficient revision is anchored in artefacts.
Use what you have already produced.

Recommended workflow:

1. Re-run seminar code and regenerate PCAP captures.
2. Re-read each lecture and link every claim to at least one trace or configuration.
3. Use the weekly question bank to practise short answers.

The question bank is located at:

* `00_APPENDIX/c)studentsQUIZes(multichoice_only)/`

---

### Short answer practice: protocol selection

**Question**
You need to stream sensor readings to a local collector and you can tolerate occasional loss.
Which transport protocol is appropriate and why?

**Model answer**
UDP is appropriate if occasional loss is acceptable because it avoids retransmission delay and does not impose stream ordering. If the application needs basic reliability it can add sequence numbers and acknowledgements at the application layer.

---

### Short answer practice: NAT and inbound services

**Question**
Why does NAT complicate inbound connections and why does FTP highlight this limitation?

**Model answer**
NAT rewrites addresses and ports so an inbound connection has no stable mapping unless a static rule exists. FTP is sensitive because it uses a separate data channel and that channel may be initiated from the server side in active mode which fails when the client is behind NAT or a firewall.

---

### Short answer practice: DNS caching

**Question**
What is the role of TTL in DNS and what failure does it prevent?

**Model answer**
TTL limits how long a resolver may cache a record. It prevents indefinite use of stale mappings after an address change and it bounds the time window during which incorrect cached data persists.

---

### Worked scenario: small organisation network design

You are asked to propose a design for a small organisation:

* 40 users across two floors
* one public web service
* a mail service hosted externally
* remote administration for IT staff
* a requirement for separation between staff and guest devices

Reasoning outline:

* link layer: separate staff and guest using VLANs and switch port policies
* network layer: allocate subnets per VLAN and define routing policy between them
* network edge: use NAT for outbound Internet access and a static mapping for the public service
* transport and application: terminate TLS at the web service, use SSH for administration
* observability: capture representative traffic and validate expected behaviour with traces

---

### Checklist before the examination

* Can you explain each diagram in C01–C13 without reading the slide text?
* Can you interpret a TCP three-way handshake and a TLS handshake from a trace?
* Can you justify when to use TCP or UDP based on a requirement?
* Can you explain why DNS caching exists and what it trades off?
* Can you describe how an attacker would exploit a misconfiguration and how to harden it?

---

### Closing note

In networking, correct answers are usually structured.
State the layer, state the mechanism and state the consequence.

If you do this consistently, your answers become both correct and readable.

---

## Week 14 integration lab (recommended)

If you want a single end-to-end rehearsal before the exam, run:

- [`c14-week14-integration-lab.md`](c14-week14-integration-lab.md)
- [`assets/scenario-week14-integration-lab/`](assets/scenario-week14-integration-lab/)

