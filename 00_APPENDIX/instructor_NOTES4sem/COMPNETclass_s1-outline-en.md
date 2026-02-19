# Seminar 1 — Network Analysis

**Wireshark, netcat TCP/UDP, traffic debugging**

| | |
|---|---|
| **Course** | Computer Networks — ASE-CSIE |
| **Kit** | `v0compnet-2025-redo-main` |
| **Infra** | MININET-SDN (Ubuntu 24.04, VirtualBox) |
| **Useful time budget** | 35–50 minutes (remainder → semester overview, course syllabus, obligations, assessment) |

---

## Full Session Structure

| Block | What you do | Duration |
|:----:|---------|-------:|
| **A** | General presentation: semester, syllabus, rules, assessment, working environment | 30–40 min |
| **B** | Stage 1 — Basic commands: `ping`, `netstat`, `nslookup` | ~10 min |
| **C** | Stage 2 — Netcat TCP and UDP | ~15 min |
| **D** | Stage 3 — Wireshark on netcat traffic | ~15 min |
| **E** | Recap + individual assignment + wrap-up | ~5 min |

> *▸ Pacing note: Stages B–D are progressive: each builds on the previous one. If you run out of time, Stage D (Wireshark) can be postponed to the beginning of S2, since S2 in the backbone (Python socket programming) already assumes familiarity with Wireshark. Stages B and C are non-negotiable for the first seminar.*

---

## Block A — General Presentation

> *▸ This block is NOT part of the 35–50 min of technical content. It is the administrative/introductory block.*

**1. Who you are** — brief introduction, contact details, communication channel (Teams / email / Moodle).

**2. Course syllabus** — objectives, competences, bibliography, weighting of exam vs. seminar.

**3. Ground rules** — attendance, plagiarism, how seminar work is assessed, passing requirements.

**4. Semester calendar** — the 13–14 seminars with their respective topics (you can project `current-outline.md` from the backbone).

**5. Working environment: MININET-SDN** — explain *what it is* and *why*:

- Ubuntu 24.04 virtual machine, pre-configured, runs under Oracle VirtualBox.
- Contains everything they will need throughout the semester: Docker Engine + Compose v2, Mininet 2.3, Open vSwitch 3.3, Python 3.12 with venv `compnet`, tshark, Scapy, nmap, Paramiko, Flask etc.
- Downloaded as an `.ova` file (~2–3 GB) and imported into VirtualBox (File → Import Appliance).
- Credentials: `stud` / `stud`.
- Connection to the VM is done via SSH (PuTTY or `ssh -p 2222 stud@127.0.0.1`) — the VirtualBox console is only for emergencies.
- Show the architecture diagram from the setup guide (Windows host ↔ VirtualBox NAT ↔ VM with Docker, Mininet, Python).

**6. Point to the installation guide** (`SETUP-GHID-COMPNET_-RO.md`) — students must come with a working VM next time.

> *▸ Practical tip: If the lab has workstations with the VM pre-installed, boot one up and do a live `ssh -p 2222 stud@127.0.0.1` so they can see the prompt. If not — show it from your own laptop. Objective: students see `(compnet) stud@mininet-vm:~$` and understand that is where all work happens for the entire semester.*

---

## Block B — Stage 1: Basic Commands (~10 min)

**Backbone file:** `assets/tutorial/s1/1_basic-tools_scenario.md`
**Where you run it:** directly in the VM (via SSH/PuTTY) — or any Linux terminal
**What you demonstrate:** visibility into connectivity, connection state and DNS resolution

### Opening Narrative

> *▸ "Before any network programming, we need to know how to diagnose. Three commands will sort out 80% of your debugging problems: `ping` (does the path work?), `netstat` (who is listening on which port?) and `nslookup` (does DNS work?). We are going to try all three right now."*

### 1. `ping` — Connectivity Check

```bash
ping -c 4 google.com
```

Show: DNS resolution (the IP address), RTT (round-trip time) values, packet loss.

Explain: `ping` sends ICMP Echo Request packets and waits for an Echo Reply. If it works, the connection is functional end-to-end. If not, either DNS is broken or there is no route.

Optional: `ping -c 4 10.0.2.2` (the VirtualBox NAT gateway) — example of pinging by IP, without DNS.

### 2. `netstat` — Active Connections and Ports

```bash
netstat -tulnp
```

Explain each flag: `-t` TCP, `-u` UDP, `-l` listening, `-n` numeric (no reverse DNS), `-p` owning process.

Show the output: a port in LISTEN (e.g. sshd on :22), possibly ESTABLISHED (the current SSH session).

> *▸ Modern alternative: `ss -tulnp` — exactly the same flags, available on newer distributions.*

### 3. `nslookup` — DNS Query

```bash
nslookup google.com
```

Show: the DNS server used, the resolved IP address.

```bash
nslookup domeniu-inexistent-xyz123.com
```

Show the error "server can't find" — the difference between a resolvable domain and a nonexistent one.

### What you do NOT do here

Do not hand out the individual exercise now (`2_basic-tools_task.md`). It stays as homework or gets done if there is time left at the end. Do not go into detail about ICMP, the internal DNS protocol or ARP — those come in lectures 5–6.

> *▸ Target duration: 8–10 minutes (including any questions).*

---

## Block C — Stage 2: Netcat TCP and UDP (~15 min)

**Backbone file:** `assets/tutorial/s1/3_netcat-basics_scenario.md`
**What you demonstrate:** the fundamental difference TCP (connection-based, bidirectional, stateful) vs. UDP (datagrams, stateless)

### Opening Narrative

> *▸ "We move from diagnostics to real traffic. `netcat` (or `nc`) is the Swiss army knife of networking: it can act as server, client, and can send and receive over TCP or UDP. We use it to understand the difference between the two transport protocols — without a single line of code."*

### Preparation

Open **two SSH sessions** to the VM (two PuTTY windows or two terminal tabs). Place them **side-by-side on the projector**. Students must see simultaneously what happens in each.

---

### 🔷 STEP 1 — Start the TCP server

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `$ nc -l -p 9000` | *— does nothing yet, waits* |
| *(cursor blocked — waiting for connection)* | |

> *▸ Explain: `-l` = listen (server mode), `-p 9000` = the port. The command blocks — the server is waiting.*

---

### 🔷 STEP 2 — Connect the client

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| *(still blocked, but the connection is now established)* | `$ nc 127.0.0.1 9000` |
| | *(connected — you can type)* |

> *▸ Explain: the client connects to loopback (127.0.0.1) on port 9000. The TCP connection is established.*

---

### 🔷 STEP 3 — Bidirectional message exchange

**Client → Server:**

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `hello from client` | `> hello from client` ⏎ |
| ↑ *appears automatically* | ↑ *you type and press Enter* |

**Server → Client:**

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `> hello from server` ⏎ | `hello from server` |
| ↑ *you type and press Enter* | ↑ *appears automatically* |

> *▸ Emphasise: the connection is BIDIRECTIONAL and PERSISTENT — anything you type on one side appears on the other instantly.*

---

### 🔷 STEP 4 — Close the connection

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| **Ctrl+C** → server stops | *(disconnected automatically)* |
| | ↑ *the client detects the closure* |

> *▸ Explain: TCP has a termination procedure (FIN/ACK). When one side closes, the other finds out.*

---

### 🔷 STEP 5 — Start the UDP server

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `$ nc -u -l -p 9001` | *— does nothing yet* |
| *(waiting for datagrams)* | |

> *▸ Explain: `-u` = UDP. The server listens for datagrams, NOT connections. No handshake.*

---

### 🔷 STEP 6 — Send a UDP message

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `test UDP` | `$ echo "test UDP" \| nc -u 127.0.0.1 9001` |
| ↑ *the received message appears* | |

> *▸ Emphasise: there is no persistent connection. Each message is an independent datagram.*

---

### 🔷 STEP 7 — UDP loss (optional, but pedagogically powerful)

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| **Ctrl+C** → server STOPPED | *← server is no longer listening* |

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| *(nothing — nobody is listening)* | `$ echo "lost message" \| nc -u 127.0.0.1 9001` |
| | *(no error — but the message has vanished!)* |

**Punchline:** The client receives NO error. The message was silently lost. ***That is UDP — fire and forget.***

### Verbal Recap (30 seconds)

> *▸ "TCP = stable, bidirectional connection with delivery guarantees. UDP = independent datagrams, fast, no guarantees. Both are essential: TCP for web, email, SSH; UDP for DNS, streaming and online games."*

> *▸ Target duration: 12–15 minutes.*

---

## Block D — Stage 3: Wireshark on netcat traffic (~15 min)

**Backbone file:** `assets/tutorial/s1/5_wireshark-netcat_scenario.md`
**What you demonstrate:** how TCP vs. UDP looks at packet level; the difference between capture filter and display filter

### Logistical note — you now have 3 terminals

On top of the two SSH sessions from Block C (SERVER and CLIENT), open a **third SSH terminal** dedicated to capture. Alternatively, use Wireshark on Windows instead of the third terminal.

> *▸ Pragmatic tip: If the NAT configuration makes captures difficult in Wireshark on the host, do the entire demonstration with tshark from the VM. Pedagogically it is identical, only the interface is text instead of graphical.*

### Opening Narrative

> *▸ "So far we have sent and received data — but we have not seen what happens on the wire. Wireshark lets us capture every packet and break it down layer by layer. We see with our own eyes the TCP handshake and we understand why UDP looks different."*

---

### TCP Scenario

#### 🟠 STEP 1 — Start the capture — CAPTURE TERMINAL (SSH #3)

| 🟠 CAPTURE TERMINAL (SSH #3 or Wireshark on host) |
|:----|
| **tshark variant:** `$ sudo tshark -i lo -f "tcp port 9200"` |
| **Wireshark variant:** Capture Filter → `tcp port 9200` → Start |

---

#### 🟠 STEP 2 — Server + client netcat + messages

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `$ nc -l -p 9200` | `$ nc 127.0.0.1 9200` |
| *(waiting...)* | |

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `message1` | `> message1` ⏎ |
| `message2` | `> message2` ⏎ |
| `message3` | `> message3` ⏎ |

---

#### 🟠 STEP 3 — Stop the capture. What you see and what you explain:

**The TCP handshake (SYN → SYN-ACK → ACK):** the first 3 packets. The way TCP establishes a connection. Three-way handshake.

**Payload packets:** your data — message1, message2, message3 — encapsulated in TCP segments.

**The ACKs:** after each data packet, the other side confirms receipt.

**Display filter (after capture):** `tcp.stream eq 0` — isolates the conversation.

---

### UDP Scenario

#### 🟠 STEP 4 — New capture — CAPTURE TERMINAL

| 🟠 CAPTURE TERMINAL |
|:----|
| `$ sudo tshark -i lo -f "udp port 9201"` or Capture Filter: `udp port 9201` |

---

#### 🟠 STEP 5 — Server + UDP message

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `$ nc -u -l -p 9201` | *← waiting* |
| *(waiting for datagrams...)* | |

| 🔵 SERVER TERMINAL (SSH #1) | 🟢 CLIENT TERMINAL (SSH #2) |
|:----|:----|
| `test UDP` | `$ echo "test UDP" \| nc -u 127.0.0.1 9201` |

---

#### 🟠 STEP 6 — Stop the capture. What you see and what you explain:

**Zero handshake** — the first datagram already contains data. There is no SYN, there is no ACK. Each packet is independent.

**Display filter:** `udp.port == 9201`

---

### Comparative Table TCP vs. UDP (verbalised or projected)

| Aspect | TCP | UDP |
|--------|-----|-----|
| Connection | Yes (3-way handshake) | No |
| Acknowledgement | Yes (ACK) | No |
| Guaranteed ordering | Yes (seq/ack numbers) | No |
| Overhead | Higher | Lower |
| Visible in capture | Handshake + ACKs + data | Data only |

> *▸ Target duration: 12–15 minutes.*

---

## Block E — Recap and Assignment (~5 min)

### What you say

> *▸ "Today we laid the foundations: you know how to diagnose a network with `ping`/`netstat`/`nslookup`, you know how to generate traffic with `netcat` over TCP and UDP, and you have seen at packet level what the difference looks like. Next time we write code — TCP server and client in Python."*

### Homework / in-class assignment

Distribute (or point to on the repo/Moodle) the three exercise files from the backbone:

1. `2_basic-tools_task.md` → Producing the file `basic_tools_output.txt`
2. `4_netcat-basics_task.md` → Producing the file `netcat_activity_output.txt`
3. `6_wireshark-netcat_task.md` → Producing the file `wireshark_activity_output.zip`

Explain: each exercise requires proof of work — a text file containing the commands run, their outputs and the interpretation.

### Logistical Requirement for Seminar 2

> *▸ "Next time, everyone must have the MININET-SDN VM up and running. The most important test: open PuTTY, connect to `127.0.0.1:2222`, `stud/stud`, and see the prompt `(compnet) stud@mininet-vm:~$`. If that works, you are ready."*

---

## Cheat-sheet: what to have open before the session

| Element | Location / Action |
|---------|-------------------|
| MININET-SDN workstation | Booted in VirtualBox, connected via SSH on `127.0.0.1:2222` |
| Terminal 1 (SERVER) | SSH session open — labelled "SERVER" |
| Terminal 2 (CLIENT) | SSH session open — labelled "CLIENT" |
| Terminal 3 (capture) | SSH session — for `tshark` (or Wireshark on host) |
| Wireshark (on host) | Optional — open, ready for interface selection |
| Projector | Split-screen SERVER / CLIENT |
| Backbone files S1 | `assets/tutorial/s1/` |
| Setup guide | `SETUP-GHID-COMPNET_-RO.md` |

---

## Contingency Plan

| Problem | Quick fix |
|----------|---------------|
| VM will not start | Demonstrate everything from your personal laptop (any Linux / WSL) |
| `netcat` missing | `sudo apt install ncat` or `nmap` (ncat is included) |
| Wireshark cannot see loopback traffic | Switch to `tshark` from the VM: `sudo tshark -i lo -f "tcp port 9200"` |
| Students do not have the VM installed | Normal at S1 — that is why Block A explains the setup; they must have it by S2 |
| No internet in the VM | `ping 10.0.2.2` (VBox gateway) works; use IP addresses |
| Running over time | Sacrifice Stage D (Wireshark) — recover it at S2 |

---

*Outline generated from the backbone `v0compnet-2025-redo-main`, seminar S1 (`assets/tutorial/s1/`), the MININET-SDN workstation and the associated setup guide.*
