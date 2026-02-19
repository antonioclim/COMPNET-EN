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
