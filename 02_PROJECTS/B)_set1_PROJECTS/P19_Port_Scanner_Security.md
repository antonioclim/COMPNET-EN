# Project 19: Port Scanner for Security Analysis

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Reserve (Individual)

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Scan types specification | 20% |
| **E2** - Prototype | Week 9 | Basic TCP scanner | 25% |
| **E3** - Final | Week 13 | Multiple scan types | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-19`

---

## 📚 Project Description

Implement a port scanning tool supporting multiple scan types (TCP connect, SYN, UDP). Analyse scan results, identify services and document security implications.

⚠️ **ETHICAL WARNING:** Only scan systems you own or have explicit permission to test!

### 🎯 Learning Objectives
- **Implement** different scanning techniques
- **Understand** TCP/UDP behaviour during scans
- **Identify** services from port numbers
- **Analyse** security posture from results

---

## 🎯 Concept Analogies

### Port Scan = Checking Doors
🏠 **Analogy:** Walking through a building trying each door (port). Some are open (listening), some locked (closed), some have signs (banners).

💻 **Technical:** Each open port = potential entry point.

### SYN Scan = Knocking Without Entering
🏠 **Analogy:** You knock (SYN), if someone answers (SYN-ACK), you know they're home but leave without entering (RST instead of ACK).

---

## 🗳️ Peer Instruction Questions

### Question 1: TCP Connect vs SYN
**Question:** Why is SYN scan called "stealth"?
- A) It's invisible
- B) Doesn't complete handshake, less likely logged ✓
- C) Uses encryption
- D) Faster

### Question 2: UDP Scanning
**Question:** Why is UDP scanning difficult?
- A) UDP is encrypted
- B) No response doesn't confirm closed (could be filtered) ✓
- C) UDP ports don't exist
- D) Requires root

---

## ❌ Common Misconceptions

### 🚫 "Closed port = safe"
**CORRECT:** A closed port today may be open tomorrow. Regular scanning is needed.

### 🚫 "Port scanning is illegal"
**CORRECT:** Scanning your own systems is legal. Scanning others without permission may be illegal. Always get authorization.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **TCP Connect Scan** | Full three-way handshake |
| **SYN Scan** | Half-open, sends RST after SYN-ACK |
| **UDP Scan** | Connectionless, unreliable detection |
| **Banner Grabbing** | Identifying service from response |
| **Well-Known Ports** | 0-1023, reserved for common services |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""Port Scanner with Multiple Scan Types"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import concurrent.futures
from typing import List, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# TCP_CONNECT_SCAN
# ═══════════════════════════════════════════════════════════════════════════════
def tcp_connect_scan(host: str, port: int, timeout: float = 1.0) -> Tuple[int, bool]:
    """
    TCP connect scan — full handshake.
    
    Returns:
        Tuple of (port, is_open)
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            # 💭 PREDICTION: What result for closed port?
            # Answer: ConnectionRefusedError (RST received)
            result = sock.connect_ex((host, port))
            return (port, result == 0)
    except:
        return (port, False)

def scan_range(host: str, ports: List[int]) -> List[int]:
    """Scan multiple ports concurrently."""
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(tcp_connect_scan, host, port): port 
                   for port in ports}
        
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"Port {port}: OPEN")
    
    return sorted(open_ports)

# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_IDENTIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
}

def identify_service(port: int) -> str:
    """Get service name for common ports."""
    return COMMON_PORTS.get(port, "Unknown")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: scanner.py <host> [port_range]")
        print("Example: scanner.py 192.168.1.1 1-1000")
        sys.exit(1)
    
    host = sys.argv[1]
    ports = range(1, 1001)  # Default: scan ports 1-1000
    
    print(f"Scanning {host}...")
    open_ports = scan_range(host, list(ports))
    
    print(f"\nFound {len(open_ports)} open ports:")
    for port in open_ports:
        service = identify_service(port)
        print(f"  {port}/tcp - {service}")

if __name__ == "__main__":
    main()
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 2 | `02enWSL/` | Socket programming |
| 7 | `07enWSL/` | Port probing, defensive scanning |
| 13 | `13enWSL/` | Network security concepts |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
