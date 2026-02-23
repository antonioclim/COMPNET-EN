# 🐍 Python for Computer Networks
## Complete Self-Study Guide

> **Supplementary material** for the Computer Networks course
> **Repository:** [github.com/antonioclim/netROwsl](https://github.com/antonioclim/netROwsl)
> **Status:** Optional, not assessed
> **Environment:** WSL2 + Ubuntu 22.04 + Docker + Portainer
> **Version:** 3.0 — January 2025 (with CPA, PI and CREATE pedagogical enhancements)

---

## 📋 Contents

1. [About This Guide](#about-this-guide)
2. [Repository Structure](#repository-structure)
3. [Learning Steps](#learning-steps)
   - [Step 1: Reading Python Code](#step-1-reading-python-code)
   - [Step 2: Data Types for Networking](#step-2-data-types-for-networking)
   - [Step 3: Socket Programming](#step-3-socket-programming)
   - [Step 4: Code Organisation](#step-4-code-organisation)
   - [Step 5: CLI Interfaces](#step-5-cli-interfaces)
   - [Step 6: Packet Analysis](#step-6-packet-analysis)
   - [Step 7: Concurrency](#step-7-concurrency)
   - [Step 8: HTTP and Application Protocols](#step-8-http-and-application-protocols)
   - [Step 9: Best Practices and Debugging](#step-9-best-practices-and-debugging)
4. [CREATE Exercises — Independent Design](#create-exercises--independent-design)
5. [Aderstanding Check (Peer Instruction)](#understanding-check-peer-instruction)
6. [Pair Programming Exercise](#pair-programming-exercise)
7. [Parsons Exercises (Code Rearrangement)](#parsons-exercises-code-rearrangement)
8. [Code Tracing Exercises](#code-tracing-exercises-execution-tracking)
9. [EVALUATE Exercise: Choose the Architecture](#evaluate-exercise-choose-the-architecture)
10. [Reference Diagrams](#reference-diagrams)
11. [Weekly Exploration Exercises](#weekly-exploration-exercises)
12. [Python-Networking Quick Reference](#python-networking-quick-reference)
13. [Extended FAQ](#extended-faq)
14. [Additional Resources](#additional-resources)
15. [Self-Assessment Checklist](#-self-assessment-checklist)

---

## About This Guide

The Computer Networks lab exercises use **Python** as the primary implementation tool. This guide **is not mandatory** — the labs can be completed without it.

### Who Is It For?

- Students who want to understand *why* code looks a certain way
- Those curious to modify or extend existing exercises
- Programmers with C/JavaScript/Java experience wanting a quick transition to Python

### How to Use the Guide

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  LAB WEEK                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Mandatory exercises (weekly kit from XXroWSL/)                      │   │
│  │ → Run the scripts, complete the TODOs                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ OPTIONAL: Corresponding step from this guide                        │   │
│  │ → Aderstand the Python concepts behind the code                    │   │
│  │ → Explore additional deepening exercises                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

The `netROwsl` repository has a consistent structure for each week:

```
netROwsl/
├── 01roWSL/                          # Week 1
│   ├── src/
│   │   ├── exercises/                # ← MAIN EXERCISES
│   │   │   ├── ex_1_01_latency_ping.py
│   │   │   ├── ex_1_02_tcp_server_client.py
│   │   │   └── ...
│   │   ├── apps/                     # Complete demo applications
│   │   └── utils/                    # Reusable helper functions
│   ├── scripts/                      # Orchelayerion scripts
│   ├── docker/                       # Docker configurations
│   ├── docs/                         # Documentation
│   ├── tests/                        # Automated tests
│   └── README.md
├── 02roWSL/ ... 14roWSL/
```

### Week Correspondence Table

| Folder | Week | Networking Theme | Correlated Python Step |
|--------|------|------------------|------------------------|
| `01roWSL` | W1-2 | Network fundamentals | Step 1: Reading code |
| `02roWSL` | W2-3 | TCP/UDP socket programming | Step 2 + Step 3 |
| `03roWSL` | W3 | Broadcast, Multicast, Tunnel | Step 3: Advanced sockets |
| `04roWSL` | W4 | Physical/Data Link Layer | Step 4: Code organisation |
| `05roWSL` | W5 | Network Layer, IP, Subnetting | Step 5: CLI argparse |
| `06roWSL` | W6 | NAT/PAT, SDN | Step 6: Packet analysis |
| `07roWSL` | W7 | Packet filtering, Firewall | Step 6: Analysis (continued) |
| `08roWSL` | W8 | Transport Layer, HTTP | Step 7 + Step 8 |
| `09roWSL` | W9 | Session/Presentation Layer | Step 8: HTTP |
| `10roWSL` | W10 | Application Layer protocols | Step 8: Application protocols |
| `11roWSL` | W11 | Load balancing, DNS | Step 8: REST, DNS |
| `12roWSL` | W12 | Email, RPC | Step 8: Application protocols |
| `13roWSL` | W13 | IoT, Security | Step 7 + Step 9 |
| `14roWSL` | W14 | Recap, Projects | Step 9: Best practices |

---

## Learning Steps

### Step 1: Reading Python Code

**📅 Correlated with:** Weeks 1-2 (`01roWSL`, `02roWSL`)

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: Python Code as a Cooking Recipe

Reading Python code is like reading a recipe before cooking:

| Code Element | Recipe Equivaslow |
|--------------|-------------------|
| **Imports** (`import socket`) | Ingredient list — what you need before starting |
| **Functions** (`def server():`) | Recipe steps — instructions to follow in order |
| **Variables** (`port = 8080`) | Bowls and containers — where you keep ingredients temporarily |
| **Return** (`return result`) | Plated dish — the final result |
| **Comments** (`# explanation`) | Chef's notes — tips for next time |

**Why it matters:** Nobody cooks by reading the recipe word by word whilst working. First you read through to understand the flow, then you execute.

#### ═══════════════════════════════════════════════════════════════
#### 🎯 OBJECTIVES_AND_REFERENCES
#### ═══════════════════════════════════════════════════════════════

#### Why It Matters

Before modifying the lab scripts, you need to be able to read and understand them. Exercises start with working code that you will adapt.

#### Reference Files

Open and study the structure of these files:
- `01roWSL/src/exercises/ex_1_01_latency_ping.py`
- `01roWSL/src/exercises/ex_1_02_tcp_server_client.py`

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### Key Concepts from Code

**1. Shebang and Docstring**
```python
#!/usr/bin/env python3
"""
Exercise 1.01: Measuring Latency with Ping
COMPUTER NETWORKS Course - ASE, Informatics | by Revolvix

This exercise demonlayeres measuring network latency...
"""
```
- The first line tells the shell which interpreter to use
- The docstring (between `"""`) documents the module

**2. Dataclasses — Data Structures**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class PingResult:
    """Stores the result of a single ping."""
    sequence: int
    rtt_ms: Optional[float]
    success: bool
    message: str = ""
```

Compare with `struct` in C:
```c
// C equivaslow
typedef struct {
    int sequence;
    float rtt_ms;  // can be NULL?
    bool success;
    char message[256];
} PingResult;
```

**3. Type Hints (Optional but Useful)**
```python
def measure_latency(host: str, count: int = 3) -> float:
    """Measures average latency to a host."""
    # implementation
    return average_ms
```
- `host: str` — parameter is a string
- `count: int = 3` — optional parameter with default value
- `-> float` — function returns a float

**4. Quick Syntax Comparison**

| Concept | C/Java | JavaScript | Python |
|---------|--------|------------|--------|
| Variable declaration | `int x = 5;` | `let x = 5;` | `x = 5` |
| Function | `int f(int x) {...}` | `function f(x) {...}` | `def f(x):` |
| Condition | `if (x > 0) {...}` | `if (x > 0) {...}` | `if x > 0:` |
| Loop | `for (int i=0; i<n; i++)` | `for (let i=0; i<n; i++)` | `for i in range(n):` |
| Array | `int arr[] = {1,2,3}` | `let arr = [1,2,3]` | `arr = [1, 2, 3]` |
| Dictionary | `HashMap<>` | `{key: value}` | `{key: value}` |

#### ═══════════════════════════════════════════════════════════════
#### 🔍 DETAILED_EXPLANATIONS
#### ═══════════════════════════════════════════════════════════════

#### 🔍 Why Does It Work This Way?

**Question:** Why doesn't Python have `{` and `}` like C or Java?

**Explanation:** Python uses **indentation** (spaces or tabs) to define code blocks. This forces code to be readable — you cannot write everything on one line. It's a language design decision.

**Practical consequence:** If you mix tabs with spaces, you'll get `IndentationError`. Configure your editor to use 4 spaces.

#### ═══════════════════════════════════════════════════════════════
#### 🔮 PREDICTION_AND_PRACTICE
#### ═══════════════════════════════════════════════════════════════

#### 🔮 PREDICTION: Practical Exploration

Before running the command below, answer:
1. What output do you expect to see?
2. What happens if the host doesn't exist?

```bash
cd /mnt/d/NETWORKING/netROwsl/01roWSL
python3 src/exercises/ex_1_01_latency_ping.py --host 127.0.0.1 --count 5
```

<details>
<summary>✅ Check your prediction</summary>

**Expected output:** 5 ping results with RTT in milliseconds to localhost.

**If the host doesn't exist:** Pings will fail with timeout or "Host unreachable".

</details>

**Identify** in the code:
- What does the `@dataclass` decorator do?
- What does `Optional[float]` mean?
- How does `subprocess.run()` work?

---

### Step 2: Data Types for Networking

**📅 Correlated with:** Weeks 2-3 (`02roWSL`, `03roWSL`)

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: Bytes and Strings as Letters and Telegrams

| Concept | Real Life Equivaslow |
|---------|----------------------|
| **String** (`str`) | Letter in your language that you read directly |
| **Bytes** (`bytes`) | Telegram encoded in Morse — needs decoding |
| **encode()** | Translating the letter to Morse for transmission |
| **decode()** | Translating Morse back to readable text |

**Why it matters:** The network "speaks" only in Morse (bytes). Your computer "thinks" in text (strings). You always need to translate.

#### Why It Matters

Networks transport **bytes**, not text. Python makes an explicit distinction between `str` (text) and `bytes` (raw data) — a critical distinction for networking.

#### Reference Files

- `02roWSL/src/exercises/ex_2_01_tcp.py`
- `02roWSL/src/exercises/ex_2_02_udp.py`

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### Key Concepts

**1. Bytes vs. Strings**
```python
# String (text for humans)
message_text = "GET /index.html HTTP/1.1"

# Bytes (what's actually sent on the network)
message_bytes = b"GET /index.html HTTP/1.1"

# Conversion
message_bytes = message_text.encode('utf-8')
message_text = message_bytes.decode('utf-8')
```

#### 🔍 Why Does It Work This Way?

**Question:** Why did Python 3 strictly separate `bytes` from `str`?

**Explanation:** In Python 2, strings were bytes implicitly, which caused subtle bugs with non-ASCII characters (Romanian, Chinese, emoji). Python 3 forces the programmer to be explicit about encoding, preventing data corruption.

**Practical consequence:** If you send `str` on a socket instead of `bytes`, you get `TypeError`. It's a reminder that the network doesn't understand text directly.

**2. Dataclasses for Protocol Structures**
```python
from dataclasses import dataclass

@dataclass
class PacketInfo:
    src_ip: str
    dst_ip: str
    protocol: int
    length: int

# Creating an instance
pkt = PacketInfo("192.168.1.1", "8.8.8.8", 6, 1500)
print(pkt.src_ip)  # 192.168.1.1
```

**3. List Comprehensions — Compact Processing**
```python
# Classic way (as in C/Java)
ports = []
for i in range(1, 101):
    if i % 2 == 0:
        ports.append(i)

# Pythonic way — one line
ports = [i for i in range(1, 101) if i % 2 == 0]
```

**4. Dict Comprehensions for Parsing**
```python
# Parse HTTP headers in a single expression
raw = "Host: localhost\r\nContent-Type: text/html"
headers = {
    key: value
    for line in raw.split('\r\n')
    for key, value in [line.split(': ')]
}
# Result: {'Host': 'localhost', 'Content-Type': 'text/html'}
```

#### ═══════════════════════════════════════════════════════════════
#### 🔮 PREDICTION_AND_PRACTICE
#### ═══════════════════════════════════════════════════════════════

#### 🔮 PREDICTION: Practical Exploration

In `02roWSL/src/exercises/ex_2_01_tcp.py`:

**Before looking at the code, predict:**
1. Where is the `encode()` conversion done?
2. What error appears if you send `str` instead of `bytes`?

<details>
<summary>✅ Check</summary>

1. At `send()` or `sendall()` — data must be bytes
2. `TypeError: a bytes-like object is required, not 'str'`

</details>

---

### Step 3: Socket Programming

**📅 Correlated with:** Weeks 2-4 (`02roWSL`, `03roWSL`, `04roWSL`)

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: Socket as a Landline Telephone

| Socket Operation | Telephone Equivaslow |
|------------------|---------------------|
| `socket()` | You buy a new telephone |
| `bind()` | You get assigned a phone number (port) |
| `listen()` | You plug in the phone, wait for calls |
| `accept()` | You pick up the receiver when it rings |
| `connect()` | You dial someone's number |
| `send()/recv()` | You speak / You listen |
| `close()` | You hang up the phone |

**TCP vs UDP:**
- **TCP** = phone conversation (you confirm the other person is on the line, you take turns speaking)
- **UDP** = voicemail message (you send and hope it arrives, no confirmation)

#### Why It Matters

Sockets are the foundation of network communication. The exercises implement TCP/UDP servers and clients.

#### Reference Files

- `02roWSL/src/exercises/ex_2_01_tcp.py` — TCP Server/Client
- `02roWSL/src/exercises/ex_2_02_udp.py` — UDP Server/Client
- `03roWSL/src/exercises/ex_3_01_udp_broadcast.py` — UDP Broadcast

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### C vs. Python Comparison

**TCP Client in C:**
```c
int sock = socket(AF_INET, SOCK_STREAM, 0);
struct sockaddr_in serv_addr;
serv_addr.sin_family = AF_INET;
serv_addr.sin_port = htons(8080);
inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);
connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
send(sock, "Hello", 5, 0);
char buffer[1024];
recv(sock, buffer, 1024, 0);
close(sock);
```

**TCP Client in Python:**
```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("127.0.0.1", 8080))
    sock.sendall(b"Hello")
    response = sock.recv(1024)
# Socket closes automatically on exiting 'with'
```

#### 🔍 Why Does It Work This Way?

**Question:** Why do we need `SO_REUSEADDR`?

**Explanation:** When a server stops, the operating system keeps the port "reserved" for ~60 seconds (TIME_WAIT). Without `SO_REUSEADDR`, you cannot restart the server immediately — you get "Address already in use".

**Practical consequence:** Always add this line before `bind()`:
```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

#### Context Managers (`with`)

`with` guarantees the resource closes even if an exception occurs:
```python
# Without with (risk of resource leak)
sock = socket.socket(...)
sock.connect(...)
data = sock.recv(1024)  # If an error occurs here?
sock.close()  # Never executes!

# With with (safe)
with socket.socket(...) as sock:
    sock.connect(...)
    data = sock.recv(1024)
# close() called automatically, regardless of errors
```

#### Minimal TCP Server

```python
def run_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"Server started on {host}:{port}")

        while True:
            conn, addr = server.accept()
            with conn:
                data = conn.recv(1024)
                conn.sendall(b"OK: " + data.upper())
```

#### TCP vs. UDP Differences

| Aspect | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
|--------|---------------------|---------------------|
| Connection | `connect()` required | No connection needed |
| Sending | `send()`, `sendall()` | `sendto(data, addr)` |
| Receiving | `recv()` | `recvfrom()` → (data, addr) |
| Guarantees | Ordered, no loss | No guarantees |
| Overhead | Higher | Lower |

#### ═══════════════════════════════════════════════════════════════
#### 🔮 PREDICTION_AND_PRACTICE
#### ═══════════════════════════════════════════════════════════════

#### 🔮 PREDICTION: Practical Exploration

```bash
cd /mnt/d/NETWORKING/netROwsl/02roWSL
python3 src/exercises/ex_2_01_tcp.py --mode server --port 9090
```

**Predict:**
1. What message will appear?
2. What happens if port 9090 is already in use?
3. What happens if you run the command again in another terminal?

<details>
<summary>✅ Check</summary>

1. "Server started on 0.0.0.0:9090" or similar
2. `OSError: Address already in use`
3. Same thing — only one process can listen on a port

</details>

---

### Step 4: Code Organisation

**📅 Correlated with:** Week 4 (`04roWSL`)

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: Python Modules as Drawers in a Cabinet

| Code Element | Cabinet Equivaslow |
|--------------|-------------------|
| **`.py` file** | A drawer with a specific purpose |
| **`import`** | You open the drawer and take what you need |
| **`from X import Y`** | You open drawer X and take only object Y |
| **`utils/`** | Drawer with general tools (screwdrivers, tape) |
| **`exercises/`** | Drawer with work in progress |
| **`__init__.py`** | Label on the drawer saying what it contains |

**Why it matters:** A well-organised cabinet = an easy-to-navigate project. You find what you're looking for quickly.

#### Why It Matters

The kits have a consistent structure: `src/`, `scripts/`, `utils/`. Aderstanding the organisation helps you navigate and reuse code.

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### Modular Structure

```
04roWSL/src/
├── __init__.py          # Makes src/ a Python "package"
├── exercises/
│   ├── __init__.py
│   ├── ex1_text_client.py
│   └── ...
├── apps/                # Complete demo applications
│   └── ...
└── utils/               # Reusable helper functions
    ├── __init__.py
    └── protocol_utils.py
```

#### What Does `__init__.py` Do?

Converts a folder into an importable Python package:
```python
# src/utils/__init__.py
from .protocol_utils import calculate_crc, validata_frame
from .net_utils import format_mac, parse_ip

__all__ = ['calculate_crc', 'validata_frame', 'format_mac', 'parse_ip']
```

Then you can import:
```python
from src.utils import calculate_crc
```

#### 🔍 Why Does It Work This Way?

**Question:** Why do we need an empty `__init__.py` in each folder?

**Explanation:** Without it, Python doesn't recognise the folder as a package and you cannot `import` from it. In Python 3.3+ you can use "namespace packages" without `__init__.py`, but explicit is clearer.

**Practical consequence:** When creating a new folder for modules, always add an `__init__.py` (it can be empty).

---

### Step 5: CLI Interfaces

**📅 Correlated with:** Week 5 (`05roWSL`)

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: argparse as a Restaurant Menu

| CLI Element | Restaurant Equivaslow |
|-------------|----------------------|
| **Command** (`python script.py`) | You enter the restaurant |
| **Positional arguments** (`192.168.1.0`) | Main order (mandatory) |
| **Options** (`--verbose`) | Preferences (with/without peppers) |
| **Default values** (`port=8080`) | Standard portion if you don't specify |
| **`--help`** | Menu with explanations |

**Why it matters:** Like at a restaurant — clear orders avoid confusion. `--help` is always available.

#### Why It Matters

All exercises accept command line parameters (`--host`, `--port`, etc.). The `argparse` module handles this.

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### Simple CLI

```python
import argparse

parser = argparse.ArgumentParser(description="Subnet Calculator")
parser.add_argument("network", help="Network in CIDR format (e.g.: 192.168.1.0/24)")
parser.add_argument("--subnets", "-s", type=int, default=4, help="Number of subnets")
parser.add_argument("--verbose", "-v", action="store_true", help="Detailed output")

args = parser.parse_args()

print(f"Dividing {args.network} into {args.subnets} subnets")
if args.verbose:
    print("Detailed mode activeated")
```

Usage:
```bash
python calculator.py 192.168.1.0/24 --subnets 8 -v
```

#### 🔮 PREDICTION

**Before running:**
```bash
python3 ex_5_01_cidr_flsm.py --help
```

**Predict:** What sections will the output have?

<details>
<summary>✅ Check</summary>

- usage: the usage line
- description: programme description
- positional arguments: mandatory arguments
- options: optional arguments with explanations

</details>

---

### Step 6: Packet Analysis

**📅 Correlated with:** Weeks 6-7 (`06roWSL`, `07roWSL`)

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: Network Packets as Postal Letters

| Packet Element | Letter Element |
|----------------|----------------|
| **IP Header** | Envelope with addresses (sender, recipient) |
| **TCP Header** | Stamp and regilayerion number |
| **Payload** | Letter contents inside the envelope |
| **Checksum** | Wax seal (verifies integrity) |
| **TTL** | "Return after 30 days if undelivered" |

**Wireshark** = CCTV camera at the post office — you see everything passing through.

**struct.unpack()** = you open the envelope and read addresses in standard format.

#### Why It Matters

Traffic capture and packet analysis labs use `struct` for binary parsing.

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### The `struct` Module — Binary Parsing

Network protocols have strict binary formats. `struct` converts between bytes and Python types.

```python
import struct

# Format: ! = network byte order (big-endian)
#         H = unsigned short (2 bytes)
#         I = unsigned int (4 bytes)
#         B = unsigned char (1 byte)

# Simplified TCP header parsing
data = b'\x00\x50\x1f\x90...'  # bytes from network
src_port, dst_port = struct.unpack('!HH', data[:4])
print(f"Source port: {src_port}, Dest port: {dst_port}")

# Header construction
header = struct.pack('!HH', 8080, 443)
```

#### 🔍 Why Does It Work This Way?

**Question:** Why do we use `!` (network byte order) and not native format?

**Explanation:** Different processors store numbers differently (little-endian vs big-endian). Networks always use big-endian (standardised in RFCs). `!` guarantees your data will be read correctly by any machine.

**Practical consequence:** Without `!`, a packet created on Windows (little-endian) would be read incorrectly on a big-endian machine.

#### struct Format Table

| Format | C Type | Bytes | Python |
|--------|--------|-------|--------|
| `B` | unsigned char | 1 | int |
| `H` | unsigned short | 2 | int |
| `I` | unsigned int | 4 | int |
| `Q` | unsigned long long | 8 | int |
| `!` | network order | - | big-endian |
| `s` | char[] | n | bytes |

---

### Step 7: Concurrency

**📅 Correlated with:** Weeks 7-9 and 13

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: Threading as Chefs in a Kitchen

| Concurrency Element | Kitchen Equivaslow |
|--------------------|-------------------|
| **Thread** | An individual chef |
| **ThreadPool** | Team of chefs |
| **Task/Future** | An order from a table |
| **Lock** | A single large knife — only one can use it |
| **as_completed()** | Plates ready, in the order they're finished |

**Why threading for networking:** When one chef waits for water to boil, another can chop vegetables. Similarly, when one thread waits for a server response, others can work.

#### Why It Matters

Port scanning, multi-client servers and load tests use threading for parallelism.

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

def check_port(host: str, port: int) -> tuple[int, bool]:
    """Check if a port is open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        result = sock.connect_ex((host, port))
        return (port, result == 0)
    finally:
        sock.close()

def scan_ports(host: str, ports: list[int], workers: int = 100) -> list[int]:
    """Scan ports in parallel."""
    open_ports = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(check_port, host, p): p for p in ports}

        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"Port {port} OPEN")

    return sorted(open_ports)
```

#### 🔍 Why Does It Work This Way?

**Question:** Why `max_workers=100` and not 1000?

**Explanation:** Each thread consumes memory (~8MB stack). 1000 threads = 8GB RAM just for stacks. 100 is a good compromise between speed and resources. For I/O-bound tasks (networking), threading is efficient; for CPU-bound, use `ProcessPoolExecutor`.

---

### Step 8: HTTP and Application Protocols

**📅 Correlated with:** Weeks 8-12

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: HTTP as a Bank Conversation

| HTTP Element | Bank Equivaslow |
|--------------|-----------------|
| **Request** | You fill in a request form |
| **GET** | "I want to see my balance" (read only) |
| **POST** | "I want to deposit money" (send data) |
| **PUT** | "I want to update my address" (replace completely) |
| **DELETE** | "I want to close the account" |
| **Headers** | Form header (name, data, signature) |
| **Body** | Request content (amount, details) |
| **Response 200** | "Request approved" |
| **Response 404** | "We cannot find this account" |
| **Response 500** | "Our system has problems" |

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### HTTP from Scratch

```python
import socket

def http_get(host: str, path: str, port: int = 80) -> str:
    """Execute a manual HTTP GET."""
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    return response.decode('utf-8', errors='replace')
```

---

### Step 9: Best Practices and Debugging

**📅 Correlated with:** Week 14 (`14roWSL`)

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_AND_ANALOGY
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogy: Debugging as Detective Work

| Debug Technique | Detective Equivaslow |
|-----------------|---------------------|
| **print()** | You leave notes in key places |
| **logging** | CCTV camera recording everything |
| **breakpoint()** | You stop time and examine the scene |
| **Stack trace** | Timeline of events |
| **Ait tests** | You verify each suspect's alibi |

#### ═══════════════════════════════════════════════════════════════
#### 📖 KEY_CONCEPTS
#### ═══════════════════════════════════════════════════════════════

#### Logging vs Print

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Instead of print(), use:
logger.debug("Debugging details")
logger.info("General information")
logger.warning("Something suspicious")
logger.error("Problem!")
```

#### Integrated Debugger

```python
def complex_function(data):
    result = process(data)
    breakpoint()  # Stops here — you can inspect 'result'
    return result
```

---

## CREATE Exercises — Independent Design

These exercises require you to **design** and **build** solutions from scratch, not just complete existing code.

### 🛠️ CREATE #1: Design a Chat Protocol

**Bloom Level:** CREATE
**Estimated time:** 45-60 minutes
**Mode:** Individual or pairs

#### Task

Design and implement a simple binary protocol for a messaging system.

#### Protocol Specification

| Field | Size | Description |
|-------|:----:|-------------|
| Version | 1 byte | Protocol version (0x01) |
| Message type | 1 byte | 0x01=text, 0x02=image, 0x03=status |
| Length | 2 bytes | Payload length (big-endian) |
| Timestamp | 4 bytes | Aix timestamp (seconds) |
| Payload | variable | Message content |

#### Protocol Diagram

```
┌─────────┬──────────┬──────────┬────────────┬─────────────────┐
│ Version │ Msg Type │  Length  │ Timestamp  │    Payload      │
│ (1B)    │  (1B)    │  (2B)    │   (4B)     │  (0-65535 B)    │
└─────────┴──────────┴──────────┴────────────┴─────────────────┘
```

#### Deliverables

**1. Python Code — complete the functions:**

```python
import struct
import time

def pack_message(msg_type: int, payload: bytes) -> bytes:
    """Pack a message according to the protocol.

    Args:
        msg_type: Message type (1=text, 2=image, 3=status)
        payload: Message content as bytes

    Returns:
        Complete packed message (header + payload)
    """
    # TODO: Implement with struct.pack
    # Hint: format is '!BBHI' + payload
    pass

def unpack_message(data: bytes) -> tuple[int, int, int, bytes]:
    """Apack a message and extract fields.

    Args:
        data: Complete message (header + payload)

    Returns:
        Tuple: (version, msg_type, timestamp, payload)

    Raises:
        ValueError: If header is invalid or insufficient data
    """
    # TODO: Implement with struct.unpack
    pass
```

**2. Tests — minimum 3:**

```python
def test_roundtrip():
    """Verify pack → unpack returns original data."""
    original = b"Hello!"
    packed = pack_message(0x01, original)
    version, msg_type, timestamp, payload = unpack_message(packed)
    assert payload == original
    assert msg_type == 0x01

def test_empty_payload():
    """Verify it works with empty payload."""
    # TODO

def test_max_payload():
    """Verify maximum payload size (65535 bytes)."""
    # TODO
```

#### Assessment Criteria

- [ ] Header is exactly 8 bytes
- [ ] Fields are in network byte order (big-endian)
- [ ] Works for empty payload
- [ ] Works for maximum payload (65535 bytes)
- [ ] Timestamp is valid (not 0)
- [ ] Code has complete docstrings
- [ ] Minimum 3 unit tests

---

### 🛠️ CREATE #2: Design a Port Scanner

**Bloom Level:** CREATE
**Estimated time:** 30-45 minutes

#### Task

Design a port scanner with the following requirements:

**Mandatory features:**
1. Scan a range of ports (e.g.: 1-1000)
2. Detect open ports (TCP connect)
3. Configurable timeout per port
4. Output in JSON format

**Bonus:**
- Parallelisation with ThreadPoolExecutor
- Service detection (HTTP, SSH, FTP)

#### Starter Skeleton

```python
#!/usr/bin/env python3
"""
Port Scanner - CREATE Exercise
Design and implement a TCP port scanner.
"""
import socket
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict

@dataclass
class ScanResult:
    """Result of scanning a port."""
    port: int
    status: str  # "open", "closed", "filtered"
    service: str = ""  # optional: "http", "ssh", etc.

def scan_port(host: str, port: int, timeout: float = 1.0) -> ScanResult:
    """Scan a single port.

    TODO: Implement TCP connect scan logic.
    """
    pass

def scan_range(host: str, start: int, end: int,
               workers: int = 10, timeout: float = 1.0) -> list[ScanResult]:
    """Scan a range of ports in parallel.

    TODO: Use ThreadPoolExecutor for parallelisation.
    """
    pass

def main():
    # TODO: Implement CLI with argparse
    # Example: python scanner.py 192.168.1.1 --ports 1-100 --timeout 0.5
    pass

if __name__ == "__main__":
    main()
```

---

### 🛠️ CREATE #3: Design a Simple Load Balancer

**Bloom Level:** CREATE
**Estimated time:** 60-90 minutes

#### Task

Design a TCP load balancer that distributes connections to multiple backends.

**Algorithms to implement (choose one):**
1. **Round Robin** — cycle through backends
2. **Random** — choose randomly
3. **Least Connections** — choose backend with fewest connections

#### Architecture

```
                    ┌─────────────────┐
                    │  LOAD BALANCER  │
   Client ─────────►│   (port 8080)   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   ┌──────────┐        ┌──────────┐        ┌──────────┐
   │ Backend1 │        │ Backend2 │        │ Backend3 │
   │ :8081    │        │ :8082    │        │ :8083    │
   └──────────┘        └──────────┘        └──────────┘
```

#### Deliverables

Functional `load_balancer.py` file with:
- Backend configuration from command line
- Logging of connection distribution
- Periodic health check (optional)

---

## Aderstanding Check (Peer Instruction)

### 🗳️ PI #1: Bytes vs Strings

**Scenario:**
```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8080))
s.send("Hello")
```

**Question:** What happens when you run this code?

**Options:**
- A) The message "Hello" is sent successfully
- B) `TypeError: a bytes-like object is required, not 'str'`
- C) The message is sent but corrupted
- D) The socket blocks waiting

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: B**

Python 3 sockets accept ONLY bytes, not strings.

**Why not A:** Python 3 strictly separated bytes from str
**Why not C:** Nothing is sent, the error occurs first
**Why not D:** The error is immediate, not blocking

**Correct code:** `s.send(b"Hello")` or `s.send("Hello".encode())`

</details>

---

### 🗳️ PI #2: Port Binding

**Scenario:**
- Terminal 1: `python server.py` (listens on 8080)
- Terminal 2: `python server.py` (same script)

**Question:** What happens in Terminal 2?

**Options:**
- A) The second server starts and both work
- B) `OSError: Address already in use`
- C) The second server replaces the first
- D) The system automatically chooses another port (8081)

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: B**

A port can have ONE listener at a time.

**Why not A:** Two processes cannot listen on the same port
**Why not C:** The OS protects occupied ports
**Why not D:** There is no auto-allocation (except for port 0)

**Solution:** `SO_REUSEADDR` for quick restart, or different port.

</details>

---

### 🗳️ PI #3: struct.unpack

**Scenario:**
```python
import struct
data = b'\x00\x50'
port, = struct.unpack('!H', data)
print(port)
```

**Question:** What does it display?

**Options:**
- A) 80
- B) 20480
- C) `b'\x00\x50'`
- D) `(80,)`

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: A**

`!H` = network byte order (big-endian), unsigned short (2 bytes)
`0x0050` in big-endian = 80 in decimal

**Why not B:** Would be 20480 if little-endian (`<H`)
**Why not C:** `unpack` returns numbers, not bytes
**Why not D:** The comma after `port` extracts the value from the tuple

</details>

---

### 🗳️ PI #4: Docker Port Mapping

**Scenario:**
```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

**Question:** What URL do you use from Windows to access nginx?

**Options:**
- A) `http://localhost:80`
- B) `http://localhost:8080`
- C) `http://172.17.0.2:80`
- D) `http://nginx:80`

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: B**

`8080:80` = host port 8080 maps to container port 80.

**Why not A:** 80 is the container port, not the host
**Why not C:** Internal Docker IP is not directly accessible from Windows
**Why not D:** Service name resolves only within Docker network

</details>

---

### 🗳️ PI #5: Context Managers

**Scenario:**
```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('google.com', 80))
sock.send(b'GET / HTTP/1.0\r\n\r\n')
raise Exception("Error!")
sock.close()
```

**Question:** What happens to the socket?

**Options:**
- A) It closes normally before the exception
- B) It remains open (resource leak)
- C) Python closes it automatically
- D) The OS closes it immediately

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: B**

`sock.close()` never executes because of the exception.

**Why not A:** Exception occurs before close()
**Why not C:** Python has no garbage collection for sockets
**Why not D:** OS closes it eventually, but not immediately

**Solution:** Use `with socket.socket(...) as sock:`

</details>

---

### 🗳️ PI #6: WSL File Paths

**Scenario:**
```bash
# You create a file in Ubuntu WSL:
echo "test" > /home/stud/data.txt

# Then you want to open it from Windows.
```

**Question:** What is the correct path in Windows Explorer?

**Options:**
- A) `C:\home\stud\data.txt`
- B) `\\wsl$\Ubuntu\home\stud\data.txt`
- C) `D:\WSL\Ubuntu\home\stud\data.txt`
- D) You cannot access WSL files from Windows

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: B**

The WSL file system is accessible from Windows via the network path `\\wsl$\<distro>\`.

**Why not A:** WSL doesn't mount `/home` on C:\
**Why not C:** There is no D:\WSL\ folder by default
**Why not D:** Windows 10/11 can access WSL files natively

**Caution:** Editing WSL files with Windows applications can cause permission issues. Use VS Code with the Remote - WSL extension.

</details>

---

### 🗳️ PI #7: recv() Buffering

**Scenario:**
```python
# Server sends:
conn.sendall(b"HELLO WORLD FROM SERVER!")  # 24 bytes

# Client receives:
data = sock.recv(10)
print(data)
```

**Question:** What does the client display?

**Options:**
- A) `b'HELLO WORLD FROM SERVER!'`
- B) `b'HELLO WORL'`
- C) Error — buffer too small
- D) Nothing — recv() waits for 24 bytes

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: B**

`recv(10)` returns **at most** 10 bytes, not exactly 10 and not the entire message.

**Why not A:** recv() doesn't wait for the whole message
**Why not C:** Buffer is only the upper limit, not requirement
**Why not D:** recv() returns what's available, doesn't wait for more

**Implication:** For longer messages, you need to call recv() in a loop or use a protocol with length prefix.

</details>

---

### 🗳️ PI #8: bind() Address

**Scenario:**
```python
server.bind(('0.0.0.0', 8080))
# vs
server.bind(('127.0.0.1', 8080))
```

**Question:** What is the practical difference?

**Options:**
- A) No difference, both work the same
- B) 0.0.0.0 accepts only local connections, 127.0.0.1 from anywhere
- C) 0.0.0.0 accepts connections from anywhere, 127.0.0.1 only local
- D) 127.0.0.1 is faster for local connections

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: C**

- `0.0.0.0` = listens on **all** interfaces (localhost, LAN, WAN)
- `127.0.0.1` = listens **only** on loopback (local)

**Why not A:** The difference is significant for security
**Why not B:** It's the opposite
**Why not D:** Performance is identical for local connections

**Security rule:** In production, bind to the specific interface IP. 0.0.0.0 exposes the server to the entire network!

</details>

---

### 🗳️ PI #9: Docker Network Default

**Scenario:**
```yaml
# docker-compose.yml
services:
  web:
    image: nginx
  api:
    image: python:3.11
```

**Question:** Can the `web` container reach `api` by name?

**Options:**
- A) No, you must use IP addresses
- B) Yes, Docker Compose creates a shared network automatically
- C) Only if you add `links: [api]`
- D) Only if both use `network_mode: host`

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: B**

Docker Compose automatically creates a network for all services in the same file. Services can reach each other by name.

**Why not A:** DNS resolution works between services
**Why not C:** `links` is deprecated, network is automatic
**Why not D:** `host` mode removes container isolation

**Example:** From `web`, you can do `curl http://api:8000`

</details>

---

### 🗳️ PI #10: Threading vs Multiprocessing

**Scenario:** You want to scan 10,000 ports as fast as possible.

**Question:** Which approach is more appropriate?

**Options:**
- A) `threading.Thread` — one thread per port
- B) `ThreadPoolExecutor` with 100 workers
- C) `ProcessPoolExecutor` with 100 workers
- D) Sequential `for` loop with timeout

<details>
<summary>🔑 Answer and Explanation</summary>

**Correct: B**

Port scanning is **I/O-bound** (waiting for network responses), not CPU-bound. `ThreadPoolExecutor` is ideal because:
- Threads share memory (low overhead)
- GIL doesn't block I/O operations
- 100 workers = good parallelism without exhausting resources

**Why not A:** 10,000 threads = ~80GB RAM for stacks alone
**Why not C:** Processes have higher overhead, unnecessary for I/O
**Why not D:** Would take hours (10,000 × timeout)

</details>

---

## Parsons Exercises (Code Rearrangement)

### 🧩 PARSONS #1: TCP Server

**Task:** Rearrange the lines to create a functional TCP server.

**Shuffled lines:**
```python
# A
server.listen(5)
# B
conn.sendall(b"Hello from server!")
# C
server.bind(('0.0.0.0', 8080))
# D
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
# E
    conn, addr = server.accept()
# F
    data = conn.recv(1024)
# G
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

<details>
<summary>🔑 Correct Order</summary>

```python
# D - Create socket with context manager
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # G - Set socket option (before bind!)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # C - Bind to address
    server.bind(('0.0.0.0', 8080))
    # A - Start listening
    server.listen(5)
    # E - Accept connection
    conn, addr = server.accept()
    # F - Receive data
    data = conn.recv(1024)
    # B - Send response
    conn.sendall(b"Hello from server!")
```

**Order: D → G → C → A → E → F → B**

**Key points:**
- `setsockopt` MUST be before `bind`
- `listen` MUST be after `bind`
- `accept` MUST be after `listen`

</details>

---

### 🧩 PARSONS #2: Binary Header Parsing

**Task:** Rearrange to parse an 8-byte header (version, type, length, timestamp).

**Shuffled lines:**
```python
# A
print(f"Version: {version}, Type: {msg_type}")
# B
version, msg_type, length, timestamp = struct.unpack('!BBHI', header)
# C
header = data[:8]
# D
import struct
# E
data = sock.recv(1024)
# F
payload = data[8:8+length]
```

<details>
<summary>🔑 Correct Order</summary>

```python
# D - Import first
import struct
# E - Receive raw data
data = sock.recv(1024)
# C - Extract header (first 8 bytes)
header = data[:8]
# B - Apack header fields
version, msg_type, length, timestamp = struct.unpack('!BBHI', header)
# A - Display parsed values
print(f"Version: {version}, Type: {msg_type}")
# F - Extract payload using length from header
payload = data[8:8+length]
```

**Order: D → E → C → B → A → F**

</details>

---

### 🧩 PARSONS #3: Parallel Port Scan

**Task:** Rearrange for a parallel port scanner.

**Shuffled lines:**
```python
# A
    for future in as_completed(futures):
# B
from concurrent.futures import ThreadPoolExecutor, as_completed
# C
        port, is_open = future.result()
# D
with ThreadPoolExecutor(max_workers=50) as executor:
# E
    futures = {executor.submit(check_port, host, p): p for p in ports}
# F
        if is_open:
            print(f"Port {port} OPEN")
```

<details>
<summary>🔑 Correct Order</summary>

```python
# B - Import
from concurrent.futures import ThreadPoolExecutor, as_completed
# D - Create executor context
with ThreadPoolExecutor(max_workers=50) as executor:
    # E - Submit all tasks
    futures = {executor.submit(check_port, host, p): p for p in ports}
    # A - Process results as they complete
    for future in as_completed(futures):
        # C - Get result
        port, is_open = future.result()
        # F - Handle open ports
        if is_open:
            print(f"Port {port} OPEN")
```

**Order: B → D → E → A → C → F**

</details>

---

## Code Tracing Exercises (Execution Tracking)

### 🔍 TRACE #1: Bytes Transformation

```python
data = b"HELLO"
result = []
for i, byte in enumerate(data):
    if i % 2 == 0:
        result.append(chr(byte).lower())
    else:
        result.append(chr(byte))
output = ''.join(result)
print(output)
```

**🔮 PREDICTION:** What will it display? Complete the table step by step:

| i | byte (decimal) | chr(byte) | i % 2 == 0? | result (after this step) |
|---|----------------|-----------|-------------|--------------------------|
| 0 | 72 | 'H' | Yes | ['h'] |
| 1 | ? | ? | ? | ? |
| 2 | ? | ? | ? | ? |
| 3 | ? | ? | ? | ? |
| 4 | ? | ? | ? | ? |

<details>
<summary>🔑 Complete Solution</summary>

| i | byte | chr(byte) | i % 2 == 0? | result |
|---|------|-----------|-------------|--------|
| 0 | 72 | 'H' | Yes | ['h'] |
| 1 | 69 | 'E' | No | ['h', 'E'] |
| 2 | 76 | 'L' | Yes | ['h', 'E', 'l'] |
| 3 | 76 | 'L' | No | ['h', 'E', 'l', 'L'] |
| 4 | 79 | 'O' | Yes | ['h', 'E', 'l', 'L', 'o'] |

**Output:** `hElLo`

**Remember:** `b"HELLO"` contains ASCII codes: H=72, E=69, L=76, L=76, O=79

</details>

---

### 🔍 TRACE #2: Network Byte Order

```python
import struct
value = 0x1234
packed = struct.pack('!H', value)  # Network order (big-endian)
print(f"Bytes: {packed.hex()}")
print(f"Byte 0: {packed[0]:02x}")
print(f"Byte 1: {packed[1]:02x}")
```

**🔮 PREDICTION (write BEFORE running):**
- `packed.hex()` = ____________
- `packed[0]` (hex) = ____________
- `packed[1]` (hex) = ____________

<details>
<summary>🔑 Answer</summary>

- `packed.hex()` = `"1234"`
- `packed[0]` = `0x12` (18 in decimal) — **MSB first** (big-endian)
- `packed[1]` = `0x34` (52 in decimal)

**Key concept:** Network byte order = Big-endian = Most Significant Byte FIRST

If you had used little-endian (`'<H'`), the order would be reversed: `0x34`, `0x12`.

</details>

---

### 🔍 TRACE #3: Socket Accept Loop

```python
connections = 0
while connections < 3:
    conn, addr = server.accept()  # Assume 3 clients connect
    print(f"Client #{connections}: {addr[1]}")
    connections += 1
    conn.close()
print(f"Total: {connections}")
```

**🔮 PREDICTION:** If 3 clients connect from ports 50001, 50002, 50003, what does it display?

<details>
<summary>🔑 Answer</summary>

```
Client #0: 50001
Client #1: 50002
Client #2: 50003
Total: 3
```

**Watch for off-by-one:** First client is `#0`, not `#1`. If you want numbering from 1, use `connections + 1` in print.

</details>

---

## EVALUATE Exercise: Choose the Architecture

### 🎯 EVALUATE: Centralised Logging System

**Scenario:** You're building a logging system for 50 Docker containers in a cluster.

**Architectural options:**

| Option | Description | Pro | Con |
|--------|-------------|-----|-----|
| **A** | Each container writes to local file | Simple, no dependencies | Fragmented, hard to aggregate |
| **B** | All send UDP to central server | Fast, non-blocking | Possible message loss |
| **C** | All send TCP to central server | Guaranteed delivery | Can block if server is slow |
| **D** | Message broker (Redis/Kafka) | Decoupled, scalable, persistent | Added complexity |

**Tasks:**

1. **Development context** (5 containers, 1 developer): Which option do you choose and why?

2. **Production context** (50 containers, 1000 req/s): Which option and why?

3. **IoT context** (100 devices on unstable network): Which option and why?

<details>
<summary>🔑 Analysis</summary>

**Development:** Option **A** or **B** — simplicity takes priority, losing some logs isn't critical.

**Production:** Option **D** — decoupling and persistence are essential at scale. TCP (C) would create a bottleneck.

**IoT:** Option **B** (UDP) with local retry logic — unstable network makes TCP the problemtic (constant reconnections).

**Key lesson:** There is no "universally correct" solution — it depends on context, scale and loss tolerance.

</details>

---

## Reference Diagrams

### Diagram: TCP Three-Way Handshake

```
     CLIENT                                 SERVER
        │                                      │
        │ ────────── SYN (seq=100) ─────────► │
        │        "I want to connect"           │
        │                                      │
        │ ◄──── SYN-ACK (seq=300,ack=101) ─── │
        │     "OK, I heard you, are you there?"│
        │                                      │
        │ ────────── ACK (ack=301) ──────────► │
        │            "Yes, I'm here"           │
        │                                      │
        │         ═══ CONNECTION ═══           │
        │         ═══ ESTABLISHED ═══          │
        ▼                                      ▼
```

---

### Diagram: Docker Port Mapping

```
┌─────────────────────────────────────────────────────────────────────┐
│ WINDOWS HOST                                                        │
│                                                                     │
│   Browser ──► http://localhost:8080                                 │
│                        │                                            │
│   ┌────────────────────┼────────────────────────────────────────┐   │
│   │ WSL2 (Ubuntu)      │                                        │   │
│   │                    │                                        │   │
│   │   ┌────────────────▼────────────────────────────────────┐   │   │
│   │   │ Docker Engine                                       │   │   │
│   │   │                                                     │   │   │
│   │   │   ports: "8080:80"                                  │   │   │
│   │   │      ▲         │                                    │   │   │
│   │   │      │         ▼                                    │   │   │
│   │   │   ┌──┴──────────────────────────────┐               │   │   │
│   │   │   │ Container: nginx                │               │   │   │
│   │   │   │                                 │               │   │   │
│   │   │   │   nginx listens on port 80 ◄───┘               │   │   │
│   │   │   │   (internal, not directly exposed)             │   │   │
│   │   │   └─────────────────────────────────┘               │   │   │
│   │   └─────────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘

LEGEND: 8080 = HOST port (Windows sees this)
        80   = CONTAINER port (nginx sees this)
```

---

### Diagram: Socket Lifecycle (TCP Server)

```
          socket()
             │
             ▼
    ┌─────────────────┐
    │  SOCKET CREATED │
    │  (file descriptor)
    └────────┬────────┘
             │
         bind(addr, port)
             │
             ▼
    ┌─────────────────┐
    │  SOCKET BOUND   │
    │  to address:port│
    └────────┬────────┘
             │
         listen(backlog)
             │
             ▼
    ┌─────────────────┐
    │  LISTENING      │◄──────────────┐
    │  (waiting)      │               │
    └────────┬────────┘               │
             │                        │
         accept() ◄─── client connects│
             │                        │
             ▼                        │
    ┌─────────────────┐               │
    │  CONNECTION     │               │
    │  conn, addr     │               │
    └────────┬────────┘               │
             │                        │
       recv() / send()                │
             │                        │
         close(conn) ─────────────────┘
             │
    (server continues listening)
```

---

### Diagram: bytes ↔ str Conversion

```
    ┌─────────────────┐                    ┌─────────────────┐
    │      str        │                    │     bytes       │
    │  "Hello! 👋"    │                    │  b'Hello! \xf0' │
    │                 │                    │   \x9f\x91\x8b' │
    │  (human text)   │                    │  (binary data)  │
    └────────┬────────┘                    └────────┬────────┘
             │                                      │
             │                                      │
             │ ───── .encode('utf-8') ────────────► │
             │                                      │
             │ ◄──── .decode('utf-8') ───────────── │
             │                                      │
             ▼                                      ▼

    PYTHON                                    NETWORK
    (text processing)                    (data transmission)

    ⚠️  RULE: socket.send() accepts ONLY bytes, NOT str!

    Wrong:   sock.send("Hello")        → TypeError!
    Correct: sock.send(b"Hello")       → OK
    Correct: sock.send("Hello".encode()) → OK
```

---

### Diagram: struct.pack / struct.unpack

```
                    struct.pack('!HH', 8080, 443)
                                │
    ┌───────────────────────────┴───────────────────────────┐
    │                                                       │
    │  8080 (decimal) ──► 0x1F90 ──► bytes: \x1f\x90       │
    │   443 (decimal) ──► 0x01BB ──► bytes: \x01\xbb       │
    │                                                       │
    │  Result: b'\x1f\x90\x01\xbb' (4 bytes)               │
    │                                                       │
    └───────────────────────────────────────────────────────┘

                    struct.unpack('!HH', data)
                                │
    ┌───────────────────────────┴───────────────────────────┐
    │                                                       │
    │  data = b'\x1f\x90\x01\xbb'                           │
    │                                                       │
    │  \x1f\x90 ──► 0x1F90 ──► 8080 (decimal)              │
    │  \x01\xbb ──► 0x01BB ──►  443 (decimal)              │
    │                                                       │
    │  Result: (8080, 443) ← Python tuple                  │
    │                                                       │
    └───────────────────────────────────────────────────────┘

    FORMAT CODES:
    ┌────┬───────────────────┬───────────┐
    │ !  │ network byte order│ big-endian│
    │ H  │ unsigned short    │ 2 bytes   │
    │ I  │ unsigned int      │ 4 bytes   │
    │ B  │ unsigned char     │ 1 byte    │
    │ 4s │ char array        │ 4 bytes   │
    └────┴───────────────────┴───────────┘
```

---

### Diagram: OSI vs TCP/IP

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OSI MODEL vs TCP/IP MODEL                        │
├─────────────────────────────────┬───────────────────────────────────┤
│          OSI (7 layers)         │        TCP/IP (4 layers)          │
├─────────────────────────────────┼───────────────────────────────────┤
│  7. Application    ─┐           │                                   │
│  6. Presentation   ─┼──────────►│  4. Application (HTTP, DNS, SSH)  │
│  5. Session        ─┘           │                                   │
├─────────────────────────────────┼───────────────────────────────────┤
│  4. Transport      ────────────►│  3. Transport (TCP, UDP)          │
├─────────────────────────────────┼───────────────────────────────────┤
│  3. Network        ────────────►│  2. Internet (IP, ICMP)           │
├─────────────────────────────────┼───────────────────────────────────┤
│  2. Data Link      ─┐           │                                   │
│  1. Physical       ─┴──────────►│  1. Network Access (Ethernet)     │
└─────────────────────────────────┴───────────────────────────────────┘
```

---

### Diagram: Client-Server Exchange

```
    ┌────────────────┐                    ┌────────────────┐
    │     CLIENT     │                    │     SERVER     │
    │   (initiates)  │                    │   (listens)    │
    └───────┬────────┘                    └───────┬────────┘
            │                                     │
            │                              bind(port=8080)
            │                              listen()
            │                                     │
            │ ──────── connect() ───────────────► │ accept()
            │                                     │
            │ ──────── send("GET /") ───────────► │
            │                                     │
            │                              recv() → process
            │                                     │
            │ ◄─────── send("<html>...") ──────── │
            │                                     │
         recv()                                   │
            │                                     │
            │ ──────── close() ─────────────────► │ close(conn)
            │                                     │
            ▼                                     │
       [finished]                          [waits for next]
```

---

## Weekly Exploration Exercises

### Weeks 1-2: Fundamentals

| File | What to explore | Python concept |
|------|-----------------|----------------|
| `ex_1_01_latency_ping.py` | `@dataclass`, `subprocess.run()` | Dataclasses, subprocesses |
| `ex_1_02_tcp_server_client.py` | `socket`, `threading` | Basic sockets |
| `ex_1_03_csv_parsing.py` | `csv` module, comprehensions | Data processing |

### Weeks 2-3: Sockets

| File | What to explore | Python concept |
|------|-----------------|----------------|
| `ex_2_01_tcp.py` | `SOCK_STREAM`, `accept()` | TCP sockets |
| `ex_2_02_udp.py` | `SOCK_DGRAM`, `sendto()` | UDP sockets |
| `ex_3_01_udp_broadcast.py` | `SO_BROADCAST` | Socket options |

### Weeks 4-14: Advanced

Consult the complete table in the [Repository Structure](#repository-structure) section.

---

## Python-Networking Quick Reference

### Essential Libraries

```python
# Basic networking
import socket                    # TCP/UDP sockets
import ssl                       # TLS/SSL wrapper
import struct                    # Binary packing/unpacking

# IP and addresses
import ipaddress                 # IP address manipulation

# CLI
import argparse                  # Command line arguments

# Concurrency
import threading                 # Thread-based parallelism
from concurrent.futures import ThreadPoolExecutor

# HTTP (client)
import requests                  # pip install requests

# Logging
import logging

# JSON
import json

# Processes
import subprocess
```

### Socket Cheatsheet

```python
# TCP Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)
conn, addr = server.accept()
data = conn.recv(1024)
conn.sendall(b"response")
conn.close()

# TCP Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
client.sendall(b"request")
response = client.recv(1024)
client.close()

# UDP Server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 8080))
data, addr = server.recvfrom(1024)
server.sendto(b"response", addr)

# UDP Client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"request", ('127.0.0.1', 8080))
response, _ = client.recvfrom(1024)
```

### struct Format Codes

```python
# Network byte order (big-endian): prefix with '!'
struct.pack('!H', 8080)         # unsigned short (2 bytes)
struct.pack('!I', 0xC0A80101)   # unsigned int (4 bytes)
struct.pack('!4s', b'\xC0\xA8\x01\x01')  # 4 bytes string

# Extraction
port, = struct.unpack('!H', data[:2])
ip_int, = struct.unpack('!I', data[2:6])
```

---

## Extended FAQ

**Q: Do I need to go through all steps in order?**
A: No. You can jump to the step relevant to the current lab. Use the correspondence table.

**Q: What do I do if I don't understand something?**
A: Run the code, modify values, observe what changes. Experimentation is the best teacher.

**Q: Do I need to memorise syntax?**
A: No. Use the documentation and cheatsheet. Professional programmers constantly look things up in docs.

**Q: How do I test if I've understood?**
A: Try modifying an existing exercise or adding new functionality without looking at the solution.

**Q: Docker Desktop or native Docker Engine in WSL?**
A: For this course, native Docker Engine in WSL2 is sufficient and uses fewer resources. Docker Desktop is optional.

**Q: Why do I get "Permission denied" on docker commands?**
A: Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```
Then logout and login again (or `newgrp docker`).

**Q: How do I check I have WSL2, not WSL1?**
A: Run in PowerShell:
```powershell
wsl --list --verbose
```
The VERSION column should show `2`.

**Q: What do I do if Portainer won't start?**
A: Check status:
```bash
docker ps -a | grep portainer
```
If stopped: `docker start portainer`. If doesn't exist, recreate it.

**Q: How do I reset the Portainer password if I forgot it?**
A: Delete the data volume and recreate:
```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data
# Then recreate the container
```

**Q: Why does my socket "block" at recv()?**
A: `recv()` is blocking by default — it waits for data. Solutions:
```python
sock.settimeout(5.0)  # 5 second timeout
# or
sock.setblocking(False)  # non-blocking (with select/poll)
```

**Q: Can I run GUI applications from WSL?**
A: Yes, WSL2 on Windows 11 supports WSLg natively. On Windows 10 you need an X server (VcXsrv). But for this course, Wireshark runs natively on Windows, not in WSL.

**Q: Why do I get "Address already in use" when restarting the server?**
A: The port is still in TIME_WAIT. Solutions:
1. Wait ~60 seconds
2. Add before bind():
```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```
3. Use a different port temporarily

**Q: How do I see which ports are occupied?**
A:
```bash
# In WSL:
ss -tlnp | grep 8080

# In Windows PowerShell:
netstat -ano | findstr :8080
```

---

## Additional Resources

### Official Documentation
- [Python Socket HOWTO](https://docs.python.org/3/howto/sockets.html)
- [struct Module](https://docs.python.org/3/library/struct.html)
- [ipaddress Module](https://docs.python.org/3/library/ipaddress.html)
- [argparse Tutorial](https://docs.python.org/3/howto/argparse.html)

### Practice
- [Exercism Python Track](https://exercism.org/tracks/python)
- [Build Your Own X - Network Stack](https://github.com/codecrafters-io/build-your-own-x)

### Books (Optional)
- "Black Hat Python" — Network security with Python
- "Foundations of Python Network Programming"

---

## ✅ Self-Assessment Checklist

Before considering this guide complete, check your progress:

### REMEMBER Level (Recall)
- [ ] I can list the 5 server socket operations in order (socket → bind → listen → accept → close)
- [ ] I know the main difference between TCP and UDP
- [ ] I recognise `struct.pack('!H', port)` syntax and know what it does

### UNDERSTAND Level (Comprehension)
- [ ] I can explain why `bytes ≠ str` in Python 3
- [ ] I understand what `SO_REUSEADDR` does and why it's useful
- [ ] I can describe the TCP three-way handshake flow

### APPLY Level (Application)
- [ ] I have successfully run at least 3 examples from this guide
- [ ] I have correctly completed at least 1 Parsons exercise
- [ ] I have correctly answered >70% of the Peer Instruction questions

### ANALYSE Level (Analysis)
- [ ] I have debugged at least 1 network problem (port in use, connection refused, etc.)
- [ ] I have analysed `docker logs` output for debugging
- [ ] I have correctly completed at least 1 Code Tracing exercise

### EVALUATE Level (Evaluation)
- [ ] I can argue for choosing between TCP and UDP for a given scenario
- [ ] I have completed the EVALUATE exercise on logging architecture

### CREATE Level (Creation)
- [ ] I have implemented at least 1 CREATE exercise (chat protocol, port scanner, or load balancer)
- [ ] I have modified an existing example to add new functionality

---

### 📊 Score Interpretation

| Checks | Level | Recommendation |
|:------:|-------|----------------|
| 0-5 | Beginner | Review basic sections, run more examples |
| 6-10 | Satisfactory | You're ready for standard labs |
| 11-14 | Good | You can tackle advanced exercises |
| 15-17 | Very Good | Ready for independent projects |

---

*Material created as optional support for the Computer Networks course.*
*Repository: [github.com/antonioclim/netROwsl](https://github.com/antonioclim/netROwsl)*
*Version: 3.1 — January 2025 (with Parsons Problems, Code Tracing and self-assessment Checklist)*
