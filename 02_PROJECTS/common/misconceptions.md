# ❌ Common Misconceptions — Computer Networks Projects
## ASE Bucharest, CSIE | by ing. dr. Antonio Clim

> **Purpose:** Document frequent misunderstandings to help you avoid common pitfalls.  
> **Note:** In previous cohorts, these misconceptions caused significant debugging time. Review before starting your project.

---

## SDN and OpenFlow (P01, P06, P11)

### 🚫 Misconception 1: "OpenFlow switches can make independent routing decisions"

**WRONG:** "If the controller is slow, the switch will figure out where to send packets on its own."

**CORRECT:** OpenFlow switches are intentionally "dumb" — they only execute rules installed by the controller. When a packet arrives with no matching flow rule, the switch sends a PacketIn to the controller and waits for instructions. The switch cannot improvise.

| Aspect | Wrong assumption | Reality |
|--------|------------------|---------|
| Decision-making | Switch decides autonomously | Controller decides, switch executes |
| Unknown packets | Switch floods or drops | Switch asks controller (PacketIn) |
| Rule installation | Automatic | Explicit from controller |

**Practical verification:**
```bash
# In Mininet, disconnect controller and observe
mininet> h1 ping h2
# Ping fails because switch has no rules and no controller to ask
```

---

### 🚫 Misconception 2: "The control plane and data plane are on the same device"

**WRONG:** "SDN just means the switch has better software."

**CORRECT:** SDN physically separates control (decision-making) from data (forwarding). The controller runs on a separate machine or VM. This separation is the core architectural principle — not just a software improvement.

**Why this matters:** If you design your project assuming the controller runs on the switch, your topology and communication patterns will be fundamentally wrong.

---

### 🚫 Misconception 3: "Flow rules persist forever once installed"

**WRONG:** "I installed the rule once, so it will always work."

**CORRECT:** Flow rules have configurable timeouts (idle_timeout, hard_timeout). Rules can expire or be explicitly removed. Your controller must handle rule expiration and reinstall as needed.

---

## Docker Networking (P10, P12)

### 🚫 Misconception 4: "All Docker containers can communicate by default"

**WRONG:** "I started two containers, so they can ping each other."

**CORRECT:** Containers can only communicate if they share a network. The default bridge network allows communication by IP but not by container name. For DNS-based discovery, you must create a user-defined network.

**Practical verification:**
```bash
# Default bridge - no DNS
docker run -d --name web1 nginx
docker run -d --name web2 nginx
docker exec web2 ping web1  # FAILS - unknown host

# User-defined network - DNS works
docker network create mynet
docker run -d --name web3 --network mynet nginx
docker run -d --name web4 --network mynet nginx
docker exec web4 ping web3  # WORKS
```

---

### 🚫 Misconception 5: "localhost inside a container refers to the host machine"

**WRONG:** "My container can reach the host's port 5432 via localhost."

**CORRECT:** Inside a container, `localhost` (127.0.0.1) refers to the container itself, not the host. To reach the host from a container, use `host.docker.internal` (Docker Desktop) or the host's actual IP address.

| Reference | Inside container means |
|-----------|----------------------|
| `localhost` | The container itself |
| `host.docker.internal` | The Docker host (Desktop only) |
| Container name | Another container (same network) |

---

### 🚫 Misconception 6: "Exposed ports are automatically accessible from outside"

**WRONG:** "I wrote EXPOSE 8080 in Dockerfile, so I can access it from my browser."

**CORRECT:** `EXPOSE` is documentation only — it tells humans which ports the container uses. To make a port accessible, you must publish it with `-p 8080:8080` when running the container.

---

## Socket Programming (P04, P08, P09)

### 🚫 Misconception 7: "TCP guarantees message boundaries"

**WRONG:** "If I send 'Hello' and then 'World', the receiver gets two separate messages."

**CORRECT:** TCP is a byte stream protocol with no message boundaries. If you send "Hello" and "World", the receiver might get "HelloWorld", "Hel" + "loWorld", or any other split. You must implement your own framing (length prefix, delimiter, fixed size).

**This usually breaks when:** Students test on localhost where messages often arrive intact due to timing, then deploy to a real network where fragmentation occurs.

---

### 🚫 Misconception 8: "Closing a socket is optional"

**WRONG:** "The program exits anyway, so I don't need to close sockets."

**CORRECT:** Unclosed sockets leak file descriptors and may leave ports in TIME_WAIT state, preventing reuse. Always call `socket.close()` or use context managers (`with socket.socket() as s:`).

---

### 🚫 Misconception 9: "bind() is required for client sockets"

**WRONG:** "I need to bind my client socket to a specific port."

**CORRECT:** Client sockets get ephemeral ports automatically when connecting. Only servers need `bind()` to listen on a known port. Binding clients causes port conflicts when running multiple instances.

---

## FTP Protocol (P09)

### 🚫 Misconception 10: "FTP uses a single connection"

**WRONG:** "FTP is simple — one connection for everything."

**CORRECT:** FTP uses two connections: a control channel (port 21) for commands and a separate data channel for file transfers. The data channel is created per-transfer and can use either active (server connects to client) or passive (client connects to server) mode.

**If this feels confusing:** Focus on passive mode first — it works better with firewalls and NAT, which is why modern clients default to it.

---

## Security and IDS (P03, P07, P14)

### 🚫 Misconception 11: "IDS and firewall are the same thing"

**WRONG:** "My IDS will block the attack."

**CORRECT:** IDS (Intrusion Detection System) only detects and alerts — it does not block traffic. IPS (Intrusion Prevention System) can block. A firewall filters based on rules but typically doesn't do deep packet inspection for attack signatures.

| System | Detection | Prevention | Deep inspection |
|--------|-----------|------------|-----------------|
| Firewall | Basic | Yes | Limited |
| IDS | Yes | No | Yes |
| IPS | Yes | Yes | Yes |

---

### 🚫 Misconception 12: "Signature-based detection catches all attacks"

**WRONG:** "I have 1000 signatures, so I'm protected against everything."

**CORRECT:** Signature-based detection only catches known attack patterns. Zero-day attacks and novel variations evade signatures. This is why anomaly detection (statistical deviation from normal) complements signatures.

---

## MQTT and IoT (P15, P20)

### 🚫 Misconception 13: "MQTT QoS 2 is always better than QoS 0"

**WRONG:** "I'll use QoS 2 everywhere for reliability."

**CORRECT:** QoS 2 (exactly once) has significant overhead — multiple round trips per message. For sensor data where occasional loss is acceptable, QoS 0 is more efficient. Choose QoS based on actual requirements:

| QoS | Guarantee | Use case |
|-----|-----------|----------|
| 0 | At most once | Frequent sensor readings |
| 1 | At least once | Important but idempotent events |
| 2 | Exactly once | Financial transactions, commands |

---

### 🚫 Misconception 14: "MQTT topics work like message queues"

**WRONG:** "If no subscriber is online, messages queue up for later."

**CORRECT:** MQTT is pub/sub, not a message queue. Without retained messages or persistent sessions, messages sent when no subscriber is connected are lost. Configure retained messages for last-known-value scenarios.

---

## gRPC (P13)

### 🚫 Misconception 15: "gRPC is just REST with Protocol Buffers"

**WRONG:** "I can design gRPC like REST endpoints."

**CORRECT:** gRPC has fundamentally different patterns: streaming (server, client, bidirectional), built-in deadlines and cancellation. REST is request-response; gRPC supports long-lived streaming connections. Design around these capabilities.

| Feature | REST | gRPC |
|---------|------|------|
| Streaming | Workarounds (SSE, WebSocket) | Native |
| Binary efficiency | JSON overhead | Protobuf compact |
| Code generation | Optional | Required |
| Browser support | Native | Requires proxy |

---

## General Networking

### 🚫 Misconception 16: "ping measures bandwidth"

**WRONG:** "My ping is 10ms, so my connection is fast."

**CORRECT:** ping measures latency (round-trip time), not bandwidth. You can have low latency with low bandwidth or high latency with high bandwidth. Use `iperf` to measure throughput.

---

### 🚫 Misconception 17: "NAT provides security"

**WRONG:** "I'm behind NAT, so I'm protected."

**CORRECT:** NAT provides obscurity by hiding internal addresses, not security. It was designed for address conservation, not protection. Attackers can still reach you through outbound connections you initiate. Use proper firewalls for security.

---

*Misconceptions Document v1.0 — Computer Networks Projects*  
*ASE Bucharest, CSIE — January 2026*
