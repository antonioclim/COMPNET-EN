# Project 17: LAN Design with NAT and DHCP

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Reserve (Individual)

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Network diagram + IP plan | 20% |
| **E2** - Prototype | Week 9 | Basic connectivity | 25% |
| **E3** - Final | Week 13 | Complete configuration | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-17`

---

## 📚 Project Description

Design and implement a local network with NAT for internet access and DHCP for automatic IP assignment using Cisco Packet Tracer or GNS3.

### 🎯 Learning Objectives
- **Design** IP addressing schemes
- **Configure** NAT for address translation
- **Implement** DHCP server
- **Troubleshoot** connectivity issues

---

## 🎯 Concept Analogies

### NAT = Apartment Building Address
🏠 **Analogy:** An apartment building has one street address (public IP). Each apartment has a number (private IP). Mail comes to the building, the doorman (NAT) delivers to the right apartment.

💻 **Technical:** NAT translates between private (192.168.x.x) and public IPs.

### DHCP = Hotel Check-in
🏠 **Analogy:** When you arrive, the hotel assigns you a room (IP address), tells you where the restaurant is (gateway) and how long you can stay (lease time).

---

## 🗳️ Peer Instruction Questions

### Question 1: NAT Types
**Question:** Which NAT type allows multiple internal hosts to share one public IP?
- A) Static NAT
- B) Dynamic NAT
- C) PAT (Port Address Translation) ✓
- D) NAT64

### Question 2: DHCP DORA
**Question:** In DHCP, what does DORA stand for?
- A) Discover, Offer, Request, Acknowledge ✓
- B) Distribute, Open, Relay, Accept
- C) Data, Origin, Route, Address
- D) None of the above

---

## ❌ Common Misconceptions

### 🚫 "NAT provides security"
**CORRECT:** NAT hides internal IPs but is not a security feature. Use firewalls for security.

### 🚫 "DHCP assigns permanent IPs"
**CORRECT:** DHCP leases IPs for a limited time. Devices must renew or may get different IPs.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **NAT** | Network Address Translation |
| **PAT** | Port Address Translation (NAT overload) |
| **DHCP** | Dynamic Host Configuration Protocol |
| **Lease** | Time period for DHCP assignment |
| **Gateway** | Router connecting networks |

---

## 🔨 Implementation Example

```
# ═══════════════════════════════════════════════════════════════════════════════
# CISCO_ROUTER_CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

! Configure NAT
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 ip nat inside

interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.0
 ip nat outside

! 💭 PREDICTION: What does "overload" do?
! Answer: Allows multiple internal IPs to share one external IP (PAT)

ip nat inside source list 1 interface GigabitEthernet0/1 overload
access-list 1 permit 192.168.1.0 0.0.0.255

! Configure DHCP
ip dhcp pool LAN
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 8.8.8.8
 lease 7
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 5 | `05enWSL/` | IP addressing, subnetting, VLSM |
| 6 | `06enWSL/` | NAT/PAT configuration |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
