### Network layer: allocation and support mechanisms
### NAT/PAT, ARP, DHCP/BOOTP, NDP and ICMP

---

### Learning objectives
By the end of the lecture, students should be able to:
- Explain why IPv4 led to NAT/PAT and what trade-offs they introduce
- Distinguish between static NAT, dynamic NAT and PAT (NAT overload)
- Understand at a conceptual level how the NAT table works
- Explain ARP and proxy ARP (IPv4) and the IPv6 equivalent via NDP
- Explain DHCP steps (DORA) and the role of a DHCP relay
- Explain the role of ICMP (ping/traceroute and error messages)
- Understand the role of ICMPv6 in NDP

---

### Context: why do we need these mechanisms?
- Layer 3 addressing (IPv4/IPv6) is global and routable
- In practice we need:
  - automatic allocation (DHCP/NDP)
  - IP↔MAC mapping (ARP/NDP)
  - diagnostic and control support (ICMP)
  - compatibility with IPv4 address exhaustion (NAT/PAT)

[FIG] assets/images/fig-l3-support-map.png

---

### IPv4 address exhaustion
- A major IPv4 limitation: a small address space
- Over time, common mitigation approaches:
  - reusable private addresses (RFC1918)
  - NAT/PAT
  - IPv6 transition (slow, but ongoing)

---

### Reusable private addresses (RFC1918)
- 10.0.0.0/8
- 172.16.0.0/12
- 192.168.0.0/16

Note: these are not globally routable; they must be translated or encapsulated to reach the public Internet.

---

### Address translation (NAT)
- Normally, a router forwards packets without changing IP addresses
- NAT: modifies the source and/or destination address
- Requires bidirectional mapping to receive replies

[FIG] assets/images/fig-nat-basic.png

---

### The NAT table (concept)
- The router keeps mappings: internal ↔ external
- Static (configuration) or dynamic (traffic-driven)
- Simple example:
  - 192.168.0.1 → 166.14.133.3

---

### Types of translation
- static NAT (1:1)
- dynamic NAT (a pool of public addresses)
- PAT / NAT overload (many → one public address, distinguished by port)

---

### Static NAT (1:1)
- Problem: a private internal server must be reachable from the outside
- Solution: a fixed mapping between a private IP and a public IP

[FIG] assets/images/fig-nat-static.png

---

### Dynamic NAT (pool)
- Problem: many hosts, few public IP addresses
- Solution: a pool of public IPs allocated temporarily (a lease on the mapping)

[FIG] assets/images/fig-nat-dynamic.png

---

### PAT (Port Address Translation)
- Problem: many hosts, a single public address
- Solution: per-flow mapping using ports on the router

Example table:
- 192.168.0.1:80 → 166.14.133.3:62101
- 192.168.0.2:80 → 166.14.133.3:63105

[FIG] assets/images/fig-pat.png

[SCENARIO] assets/scenario-nat-linux/

---

### Disadvantages of NAT/PAT
- With PAT, inbound connections from the Internet are difficult to initiate without port forwarding
- It breaks the end-to-end principle
- It relies on Layer 4 (ports) to solve a Layer 3 problem
- It can cause issues for certain protocols and for UDP (especially without keepalives)
- It complicates tunnels, VPNs and P2P applications

---

### ARP (IPv4) and why it exists
- In Ethernet, you need the destination MAC address to send a frame
- ARP: IP → MAC on the local network
- ARP request: broadcast
- ARP reply: unicast

[FIG] assets/images/fig-arp.png

[SCENARIO] assets/scenario-arp-capture/

---

### Proxy ARP (concept)
- If the searched IP is in another network
- The router can reply with its own MAC address (instead of the real destination)

[FIG] assets/images/fig-proxy-arp.png

---

### BOOTP (historical context)
- IP configuration via a server
- Does not support true dynamic allocation
- DHCP is the practical extension; DHCP servers can usually support BOOTP clients

---

### DHCP: role
- Automatic allocation of IP configuration and parameters:
  - mask
  - default gateway
  - DNS
  - lease time

[FIG] assets/images/fig-dhcp-dora.png

[SCENARIO] assets/scenario-dhcp-capture/

---

### DHCP DORA (steps)
- Discover: client broadcast (UDP)
- Offer: server proposes an IP and parameters
- Request: client accepts (broadcast to notify other servers)
- Acknowledge: server confirms the lease

---

### DHCP relay
- Discover is a broadcast (it does not cross routers)
- A relay on the router converts and forwards the request to a DHCP server in another network

[FIG] assets/images/fig-dhcp-relay.png

---

### NDP (IPv6)
- In IPv6, several roles that are separate in IPv4 are grouped:
  - neighbour discovery (ARP equivalent)
  - router discovery (gateway)
  - prefix discovery
  - DAD (duplicate address detection)
- NDP uses ICMPv6

[FIG] assets/images/fig-ndp.png

[SCENARIO] assets/scenario-ndp-capture/

---

### Neighbour Solicitation / Advertisement
- NS: solicitation to multicast (instead of broadcast)
- NA: reply (or an unsolicited announcement)

---

### IPv6 autoconfiguration
- Stateless (SLAAC):
  - link-local + DAD
  - prefix from Router Advertisements (RA)
  - the global address is derived from prefix + interface ID (or a random token)
- Stateful:
  - DHCPv6 for additional parameters (DNS etc) and sometimes for the address itself

---

### ICMP: why it exists
- Networks produce errors and need feedback
- ICMP provides:
  - control and error messages
  - ping/traceroute (tools built on top of ICMP)

[FIG] assets/images/fig-icmp-role.png

[SCENARIO] assets/scenario-icmp-traceroute/

---

### ICMPv6
- Similar role to ICMP
- Used extensively by NDP (filtering ICMPv6 wholesale breaks IPv6)

---

### Summary
- NAT/PAT: a practical IPv4 solution with trade-offs
- ARP: IP→MAC (IPv4)
- DHCP: automatic configuration (IPv4)
- NDP: ARP + router/prefix discovery (IPv6)
- ICMP/ICMPv6: diagnostics and control

---

### Preparation for Lecture 7
- Routing: RIP, OSPF and what routing tables mean in practice
