### The network layer
### IP, IPv4/IPv6, CIDR, subnetting and VLSM

---

### Learning objectives
By the end of the lecture, students should be able to:
- Explain the role of the network layer and the difference between MAC and IP
- Identify protocol types at the network layer (routable vs routing)
- Explain the basic structure of IPv4 and IPv6 and key fields (TTL/Hop Limit and Next Header)
- Work with CIDR (prefix /n) and compute: network, broadcast and host range
- Perform IPv4 subnetting with a fixed-length mask (FLSM) and with a variable-length mask (VLSM)
- Identify address types and communication types (unicast, multicast and broadcast/anycast)
- Understand essential IPv6 notions: link-local, global, multicast and shortening rules

---

### Network layer functions
- Fragmentation of datagrams (where applicable) and reassembly at the destination
- Routing packets from source to destination

[FIG] assets/images/fig-l3-role.png

---

### Types of network-layer protocols
- Routable protocols
  - carry data from upper layers (e.g., IP)
- Routing protocols
  - help determine routes (e.g., OSPF, RIP) (mentioned here for context)

---

### Why IP and not MAC?
- MAC (Layer 2): local significance (within an L2 domain)
- IP (Layer 3): hierarchical significance (network + host) and globally routable

[FIG] assets/images/fig-mac-vs-ip.png

---

### IP: the core idea
- The fundamental protocol of the Internet
- Best effort (no delivery guarantees)
- Logical addressing and routing

---

### IP versions
- IPv4: 32-bit, very widespread
- IPv6: 128-bit, a large address space and simplifications

---

### IPv4 vs IPv6 (quick comparison)
| IPv4 | IPv6 |
|---|---|
| 32 bits | 128 bits |
| variable header + header checksum | fixed header (extensions) and no header checksum |
| broadcast exists | no broadcast (replaced by multicast) |
| fragmentation can occur in the network | fragmentation only at the source (via extensions) |
| NAT is common in practice | supports end-to-end again (in principle) |

---

### IPv4 communication types
- unicast: one host → one host
- multicast: one host → a group
- broadcast: one host → all hosts in a segment

---

### IPv4 packet format (key fields)
[FIG] assets/images/fig-ipv4-header.png

---

### IPv4: essential fields (part 1)
- Version (4): 4
- IHL: header length
- DSCP/ECN: QoS and congestion notification (conceptually)
- Total Length: header + data

---

### IPv4: essential fields (part 2)
- Identification + Flags (DF/MF) + Fragment Offset: fragmentation
- TTL: decreases at each hop, prevents infinite loops
- Protocol: what is encapsulated (TCP=6, UDP=17, ICMP=1)

---

### IPv4: essential fields (part 3)
- Header Checksum: header only
- Source/Destination Address: 32 bits
- Options: rare in practice

---

### IPv6 format (fixed header + extensions)
[FIG] assets/images/fig-ipv6-header.png

---

### IPv6: essential fields
- Version: 6
- Traffic Class + Flow Label
- Payload Length
- Next Header (similar to 'Protocol', but also for extensions)
- Hop Limit (similar to TTL)
- Source/Destination: 128 bits

---

### IPv4 addressing: network + host
- An IPv4 address has:
  - the network part (prefix)
  - the host part
- The mask/prefix separates the two parts

[FIG] assets/images/fig-prefix-mask.png

---

### IPv4 classes (historical context)
- An older model, replaced by CIDR
- Class A/B/C, D multicast, E reserved

Note: in practice we work with CIDR, not classes.

---

### CIDR
- Classless allocation
- Notation /n = number of 1 bits in the mask
- Example: 255.255.0.0 = /16

[SCENARIO] assets/scenario-cidr-basic/

---

### IPv4 subnetting (FLSM)
- Split a network into equal-size subnets
- Borrow bits from the host part and move them into the prefix

[SCENARIO] assets/scenario-subnetting-flsm/

---

### VLSM (IPv4)
- Subnets of different sizes allocated efficiently
- Typical steps:
  1) sort requirements in descending order (hosts)
  2) allocate blocks of powers of two
  3) check alignment to the prefix

[SCENARIO] assets/scenario-vlsm/

---

### Special IPv4 addresses
- 0.0.0.0 (default / 'all interfaces' for bind)
- 255.255.255.255 (limited broadcast)
- loopback: 127.0.0.0/8 (commonly 127.0.0.1)
- link-local: 169.254.0.0/16
- private: 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16

---

### IPv6 representation and shortening
- hexadecimal, 8 groups
- remove leading zeros within a group
- a single :: compression for the longest sequence of zeros

[SCENARIO] assets/scenario-ipv6-shortening/

---

### IPv6: common address types
- loopback: ::1
- global unicast: 2000::/3
- link-local: fe80::/10
- multicast: ff00::/8
- default route: ::/0

---

### IPv6 communication types
- unicast
- multicast
- anycast (the same address on multiple nodes, delivered to the 'nearest' one)

---

### IPv6 scopes (concept)
- link-local: on the link only
- unique local: internal (typically)
- global: globally routable
- multicast: scope is included in the address (conceptually)

---

### Subnetting in IPv6 (in practice)
- you receive a prefix (e.g., /48)
- you allocate subnets by extending the prefix (often /64 for LANs)
- the number of /64 subnets in a /48 is 2^(64-48)=65,536

---

### IPv6 in URLs
- `http://[2001:db8::1]`
- with port: `http://[2001:db8::1]:8080`

---

### Summary
- Layer 3 role: addressing, routing and TTL/Hop Limit
- IPv4: CIDR, subnetting and VLSM
- IPv6: address types, shortening and prefixes

---

### Preparation for Lecture 6
- NAT/PAT, ICMP, DHCP and BOOTP
- the link between L2 (ARP) and L3 (IP), then L3→L4 (ports)
