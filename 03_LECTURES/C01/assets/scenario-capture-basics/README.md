### Scenario: mini traffic analysis (ping + DNS + local HTTP)

#### Objective
- See real packets: ICMP (ping), DNS query and a simple HTTP request.
- The OSI and TCP/IP layers are not analysed yet; this is an observation-only exercise.

#### Requirements
Select one of the following:
- Wireshark (GUI)
- tcpdump (CLI, Linux or macOS)
- On Windows, Wireshark is recommended.

---

### Variant A: tcpdump (Linux/macOS)

#### 1) Start a local HTTP server
From within the scenario folder, run:
- python3 start-http-server.py

The server starts at http://127.0.0.1:8000

#### 2) Capture DNS + ICMP + HTTP
In a second terminal, run:
- sudo tcpdump -i any -n '(icmp or udp port 53 or tcp port 8000)'

#### 3) Generate traffic
- ping -c 4 1.1.1.1
- python3 dns-query.py
- Open the URL in a web browser: http://127.0.0.1:8000

Expected observations:
- ICMP echo request/reply
- UDP 53 (DNS)
- TCP traffic to port 8000 (local HTTP)

---

### Variant B: Wireshark (any OS)

#### 1) Start capture on the active interface (Wi-Fi/Ethernet)
Use either a capture filter or a display filter:
- icmp or dns or tcp.port == 8000

#### 2) Generate traffic
- ping 1.1.1.1
- python3 dns-query.py
- Open http://127.0.0.1:8000

#### Quick questions
- How many packets do you see for DNS?
- How many request/reply pairs does ping generate?
- Why do more packets appear for HTTP than "a single message"?

## Files

| Name | Lines |
|------|-------|
| `dns-query.py` | 12 |
| `start-http-server.py` | 9 |

## Cross-References

Parent lecture: [`C01/ — Network Fundamentals`](../../)
  
Lecture slides: [`c1-network-fundamentals.md`](../../c1-network-fundamentals.md)
  
Quiz: [`W01`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W01_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C01/assets/scenario-capture-basics
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C01/assets/scenario-capture-basics`
