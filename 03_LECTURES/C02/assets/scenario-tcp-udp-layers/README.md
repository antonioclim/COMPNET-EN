### Scenario: TCP vs UDP and layer mapping (OSI and TCP/IP)

#### Objective
- Generate local TCP and UDP traffic
- Observe it in Wireshark or tcpdump
- Map the observed traffic to layers:
  - Application: your message
  - Transport: TCP or UDP
  - Network: IP (visible in the capture)
  - Data link and Physical: not examined here

#### Requirements
- Python 3
- Wireshark or tcpdump

Ports used:
- TCP: 9000
- UDP: 9001

---

### Step 1: Start the servers

Terminal 1:
- python3 tcp-server.py

Terminal 2:
- python3 udp-server.py

---

### Step 2: Start capturing

#### Variant A: tcpdump (Linux/macOS)
In another terminal:
- sudo tcpdump -i any -n '(tcp port 9000 or udp port 9001)'

#### Variant B: Wireshark (any OS)
Display filter:
- tcp.port == 9000 or udp.port == 9001

---

### Step 3: Generate traffic

Terminal 3:
- python3 tcp-client.py

Terminal 4:
- python3 udp-client.py

---

### What you should observe
TCP:
- connection setup (SYN, SYN-ACK, ACK)
- followed by data and ACKs

UDP:
- no handshake
- datagrams sent without a handshake

---

### Quick questions
1) For TCP, how many packets appear before the actual message is sent?
2) For UDP, what is missing compared with TCP?
3) In the capture, where do you see:
   - IP (the Network layer)?
   - TCP/UDP (the Transport layer)?
   - the application payload?

---

### Layer mapping (summary)
- Application: the string sent by the client
- Transport: TCP or UDP
- Network: IP (IP header in the capture)
- Network access: depends on the adaptor (Ethernet or Wi‑Fi); not examined here

## Files

| Name | Lines |
|------|-------|
| `tcp-client.py` | 15 |
| `tcp-server.py` | 21 |
| `udp-client.py` | 14 |
| `udp-server.py` | 16 |

## Cross-References

Parent lecture: [`C02/ — Architectural Models (OSI and TCP/IP)`](../../)
  
Lecture slides: [`c2-architectural-models.md`](../../c2-architectural-models.md)
  
Quiz: [`W02`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W02_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C02/assets/scenario-tcp-udp-layers
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C02/assets/scenario-tcp-udp-layers`
