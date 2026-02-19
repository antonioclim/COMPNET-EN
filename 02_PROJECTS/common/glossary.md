# 📖 Glossary — Computer Networks Projects
## ASE Bucharest, CSIE | by ing. dr. Antonio Clim

> **Purpose:** Central reference for technical terms used across all projects (P01-P20).  
> **Usage:** Consult when encountering unfamiliar terms in project specifications.

---

## SDN and OpenFlow Terms

| Term | Definition | Context |
|------|------------|---------|
| **SDN** | Software-Defined Networking — architecture separating control plane from data plane | P01, P06, P11 |
| **Control Plane** | Network intelligence layer making routing decisions | P01, P06 |
| **Data Plane** | Packet forwarding layer executing control plane decisions | P01, P06 |
| **OpenFlow** | Protocol for communication between SDN controller and switches | P01, P06, P11 |
| **Flow Rule** | Entry in switch flow table specifying match criteria and actions | P01, P06 |
| **Flow Table** | Collection of flow rules in an OpenFlow switch | P01, P06 |
| **PacketIn** | Message from switch to controller when packet has no matching rule | P01, P06 |
| **PacketOut** | Message from controller to switch instructing packet handling | P01, P06 |
| **Mininet** | Network emulator creating virtual hosts, switches and links | P01, P02, P06, P11 |
| **POX** | Python-based SDN controller framework | P01 |
| **Ryu** | Component-based SDN controller framework in Python | P06, P11 |
| **QoS** | Quality of Service — traffic prioritisation mechanisms | P11 |
| **DPID** | Datapath ID — unique identifier for OpenFlow switches | P06, P11 |

---

## Docker and Container Terms

| Term | Definition | Context |
|------|------------|---------|
| **Container** | Lightweight, isolated runtime environment sharing host kernel | P10, P12 |
| **Image** | Read-only template for creating containers | P10, P12 |
| **Dockerfile** | Script defining steps to build a Docker image | P10, P12 |
| **Docker Compose** | Tool for defining multi-container applications in YAML | P10, P12 |
| **Volume** | Persistent storage mechanism for container data | P10, P12 |
| **Bridge Network** | Default Docker network allowing container communication | P10 |
| **Overlay Network** | Multi-host Docker network for swarm services | P10, P12 |
| **Port Mapping** | Binding container port to host port (`-p 8080:80`) | P10, P12 |
| **Service** | Replicated container definition in Docker Compose/Swarm | P12 |
| **Health Check** | Container command verifying service availability | P12 |
| **Load Balancer** | Component distributing requests across backend services | P12 |

---

## Socket and Protocol Terms

| Term | Definition | Context |
|------|------------|---------|
| **Socket** | Endpoint for network communication (IP + port) | P04, P08, P09 |
| **TCP** | Transmission Control Protocol — reliable, ordered delivery | P04, P08, P09 |
| **UDP** | User Datagram Protocol — connectionless, best-effort delivery | P15 |
| **Three-Way Handshake** | TCP connection establishment (SYN, SYN-ACK, ACK) | P08, P09 |
| **Bind** | Associate socket with specific address and port | P08, P09 |
| **Listen** | Mark socket as passive, ready to accept connections | P08, P09 |
| **Accept** | Block until client connects, return new socket | P08, P09 |
| **HTTP** | Hypertext Transfer Protocol — web communication standard | P08 |
| **FTP** | File Transfer Protocol — file transfer over TCP | P09 |
| **Control Channel** | FTP command connection (port 21) | P09 |
| **Data Channel** | FTP data transfer connection (port 20 or ephemeral) | P09 |
| **Active Mode** | FTP mode where server initiates data connection | P09 |
| **Passive Mode** | FTP mode where client initiates data connection | P09 |

---

## Security Terms

| Term | Definition | Context |
|------|------------|---------|
| **IDS** | Intrusion Detection System — monitors for malicious activity | P03, P07, P14 |
| **IPS** | Intrusion Prevention System — blocks detected threats | P14 |
| **Signature** | Pattern matching rule for detecting known attacks | P03, P07, P14 |
| **Anomaly Detection** | Identifying deviations from normal behaviour | P14 |
| **Firewall** | Network security device filtering traffic by rules | P01, P07 |
| **ACL** | Access Control List — ordered rules permitting/denying traffic | P01, P07 |
| **TLS** | Transport Layer Security — encryption protocol | P04, P15 |
| **Certificate** | Digital document binding public key to identity | P04 |
| **Symmetric Encryption** | Same key for encryption and decryption (AES) | P04 |
| **Asymmetric Encryption** | Public/private key pair (RSA) | P04 |
| **Port Scanning** | Probing host to discover open services | P19 |
| **SYN Scan** | Half-open scan sending SYN packets | P19 |

---

## RPC and Messaging Terms

| Term | Definition | Context |
|------|------------|---------|
| **RPC** | Remote Procedure Call — invoking functions on remote systems | P13 |
| **gRPC** | Google's RPC framework using Protocol Buffers | P13 |
| **Protocol Buffers** | Binary serialisation format for structured data | P13 |
| **Unary RPC** | Single request, single response pattern | P13 |
| **Server Streaming** | Single request, multiple responses | P13 |
| **Client Streaming** | Multiple requests, single response | P13 |
| **Bidirectional Streaming** | Multiple requests and responses concurrently | P13 |
| **MQTT** | Message Queuing Telemetry Transport — lightweight pub/sub | P15, P20 |
| **Broker** | MQTT server managing message routing | P15, P20 |
| **Topic** | Hierarchical string for message routing (`sensors/temp/room1`) | P15 |
| **QoS Level** | MQTT delivery guarantee (0=at most once, 1=at least once, 2=exactly once) | P15 |
| **Retained Message** | Last message stored by broker for new subscribers | P15 |
| **Last Will** | Message sent by broker when client disconnects unexpectedly | P15 |

---

## Tools and Commands

| Command | Purpose | Context |
|---------|---------|---------|
| `docker run` | Create and start container | P10, P12 |
| `docker compose up` | Start services defined in compose file | P10, P12 |
| `docker network create` | Create user-defined network | P10 |
| `docker logs` | View container output | P10, P12 |
| `docker exec -it` | Run command inside running container | P10, P12 |
| `mn` | Start Mininet with default topology | P01, P06, P11 |
| `pingall` | Mininet command testing all-pairs connectivity | P01, P06 |
| `dpctl` | OpenFlow switch control utility | P06, P11 |
| `tcpdump` | Command-line packet capture | P03, P07 |
| `tshark` | Terminal-based Wireshark | P03, P07 |
| `scapy` | Python packet manipulation library | P03, P07, P14 |
| `mosquitto_pub` | MQTT publish command | P15 |
| `mosquitto_sub` | MQTT subscribe command | P15 |
| `grpcurl` | Command-line gRPC client | P13 |

---

## Acronyms Quick Reference

| Acronym | Full Form |
|---------|-----------|
| ACK | Acknowledgement |
| ARP | Address Resolution Protocol |
| CIDR | Classless Inter-Domain Routing |
| DHCP | Dynamic Host Configuration Protocol |
| DNS | Domain Name System |
| ICMP | Internet Control Message Protocol |
| IP | Internet Protocol |
| JSON | JavaScript Object Notation |
| LAN | Local Area Network |
| MAC | Media Access Control |
| NAT | Network Address Translation |
| REST | Representational State Transfer |
| RTT | Round-Trip Time |
| SMTP | Simple Mail Transfer Protocol |
| SNMP | Simple Network Management Protocol |
| SSH | Secure Shell |
| SYN | Synchronise |
| VLAN | Virtual Local Area Network |
| VPN | Virtual Private Network |
| WSL | Windows Subsystem for Linux |
| YAML | YAML Ain't Markup Language |

---

*Glossary v1.0 — Computer Networks Projects*  
*ASE Bucharest, CSIE — January 2026*
