# CHANGELOG: v0 (RO) → v11 (EN) CompNet 2025 Kit

**Migration scope:** Romanian-language networking course kit → Bilingual (EN primary, RO preserved) kit  
**Generated:** 2026-02-18  
**Method:** Automated file-by-file hash comparison + code-fingerprint matching + manual diff review

---

## Directory Structure Overhaul

```
v0 (RO)                              v11 (EN)
─────────────────────────            ─────────────────────────
assets/                              ├── 00_APPENDIX/
├── course/c1..c13/                  │   └── optional_LECTURES/ (14 HTMLs)
├── tutorial/s1..s13/                ├── 00_TOOLS/
├── tutorial-solve/                  │   ├── plantuml.jar
├── tools/plantuml.jar               │   └── PlantUML(optional)/ (NEW)
└── current-outline.md               ├── 01_GHID_MININET-SDN/ (NEW)
                                     ├── 02_PROJECTS/ (NEW — 15 projects)
                                     ├── 03_LECTURES/C01..C13/
                                     ├── 04_SEMINARS/S01..S13/
                                     │   ├── _HTMLsupport/ (NEW — 60 HTMLs)
                                     │   └── _tutorial-solve/
                                     ├── current-outline.md (rewritten)
                                     ├── requirements-optional.txt (NEW)
                                     └── CHANGELOG.md (NEW)
```

**Naming convention change:** All seminar files renamed from short names (e.g., `1_tcp-server_example.py`) to structured names (e.g., `S02_Part01_Example_TCP_Server.py`).

---

## LECTURES (03_LECTURES)

### C01 — Network Fundamentals

| Change | Detail |
|--------|--------|
| **ADDED** | `c1-network-fundamentals.md` — English translation of lecture |
| **KEPT** | `c1-fundamente-retele.md` — original RO version preserved alongside |
| **TRANSLATED** | All 8 PUML files — labels translated (e.g., `"Magistrala (bus)"` → `"Bus"`) |
| **ADDED** | 8 EN-translated PUML files as separate files (e.g., `fig-topologies.puml`, `fig-devices.puml`, `fig-encapsulation.puml`, `fig-network-vs-system.puml`, `fig-media.puml`, `fig-transmission-media.puml`, `fig-circuit-vs-packet.puml`) |
| **ADDED** | 8 EN-rendered PNG images corresponding to translated PUMLs |
| **PRESERVED** | All 8 original RO PUMLs + 8 original RO PNG images (byte-identical) |
| **PRESERVED** | `scenario-capture-basics/` — `dns-query.py` (minor comment translation), `start-http-server.py` (identical) |
| **PRESERVED** | `scenario-ping-traceroute/README.md` |
| **REMOVED** | `render-presentation.py` (103 lines) — PPTX generation utility |
| **REMOVED** | `c1-fundamente-retele.pptx` — PowerPoint file |

**Snippet verification (C01):**
- `dns-query.py`: 12 lines. Socket logic, `socket.getaddrinfo()` call, port definitions — all preserved. Only comment language changed.
- `start-http-server.py`: identical byte-for-byte.

### C02 — Architectural Models

| Change | Detail |
|--------|--------|
| **ADDED** | `c2-architectural-models.md` — EN translation |
| **KEPT** | `c2-modele-arhitecturale.md` — RO preserved |
| **TRANSLATED** | 6 PUML files — labels translated. Added EN copies. |
| **PRESERVED** | `scenario-tcp-udp-layers/` — all 4 Python files + README |

**Snippet verification (C02):**
- `tcp-server.py` (16 lines): identical.
- `tcp-client.py` (15 lines): minor comment translation (`# Mesaj de test` → EN equivalent). Socket logic preserved.
- `udp-server.py` (16 lines): identical.
- `udp-client.py` (14 lines): minor comment translation. `sendto()` / `recvfrom()` logic preserved.

### C03 — Introduction to Network Programming

| Change | Detail |
|--------|--------|
| **ADDED** | `c3-intro-network-programming.md` (151 lines) — EN translation |
| **MODIFIED** | `c3-introducere-programare-retea.md` — RO version expanded (36% similarity to original) |
| **ADDED** | `assets/` folder with 5 new images, 5 new PUMLs, render.sh — diagrams for tcp-server-flow, udp-server-flow, tcp-concurrency, raw-layering, app-over-http |
| **PRESERVED** | `scenario-scapy-icmp/icmp-ping.py` — identical |
| **PRESERVED** | `scenario-tcp-framing/server.py` — identical |
| **PRESERVED** | `scenario-tcp-framing/client.py` — 95% match (comment translation) |
| **PRESERVED** | `scenario-tcp-multiclient/server.py` — identical |
| **PRESERVED** | `scenario-tcp-multiclient/client.py` — 97% match |
| **PRESERVED** | `scenario-udp-session-ack/server.py` — identical |
| **PRESERVED** | `scenario-udp-session-ack/client.py` — 99% match |

**Snippet verification (C03):**
- `icmp-ping.py`: Scapy `IP()/ICMP()` construction, `sr1()` call — byte-identical.
- `scenario-tcp-framing/server.py`: `struct.pack`/`unpack` framing, length-prefix protocol — identical.
- `scenario-tcp-framing/client.py`: frame construction logic preserved. Comment translation only.

### C04 — Physical and Data Link Layer

| Change | Detail |
|--------|--------|
| **ADDED** | `c4-physical-and-data-link.md` — EN translation |
| **KEPT** | `c4-fizic-si-legatura-de-date.md` — RO preserved |
| **TRANSLATED** | 13 PUML files — labels translated |
| **ADDED** | `scenario-line-coding/` — NEW (line_coding_demo.py + README) |
| **ADDED** | `scenario-mac-arp-ethernet/` — NEW (README) |

### C05 — Network Layer Addressing

| Change | Detail |
|--------|--------|
| **ADDED** | `c5-network-layer-addressing.md` — EN translation |
| **PRESERVED** | All 5 scenarios with Python scripts |

**Snippet verification (C05):**
- `cidr-calc.py` (24 lines): `ipaddress.ip_network()` logic — preserved (minor comment changes).
- `flsm-split.py` (36 lines): FLSM subdivision algorithm — preserved.
- `vlsm-alloc.py` (51 lines): VLSM allocation with sorted requirements — preserved.
- `ipv6-norm.py` (14 lines): IPv6 normalization — preserved.

### C06 — NAT, ARP, DHCP, NDP, ICMP

| Change | Detail |
|--------|--------|
| **TRANSLATED** | 11 PUML files — labels translated |
| **PRESERVED** | All 5 scenario READMEs |
| **PRESERVED** | `nat-demo.sh` — identical |

### C07 — Routing Protocols

| Change | Detail |
|--------|--------|
| **ADDED** | `c7-routing-protocols.md` — EN translation |
| **TRANSLATED** | 7 PUML files |
| **PRESERVED** | `bellman_ford.py` — identical |
| **PRESERVED** | `djikstra.py` — present in original location |
| **ADDED** | `scenario-dijkstra/` — corrected spelling, contains both `dijkstra.py` (new correct name) and `djikstra.py` (backward compat) |
| **PRESERVED** | `tringle-net.py` (139 lines) — minor changes |

### C08 — Transport Layer (TCP/UDP/TLS/QUIC)

| Change | Detail |
|--------|--------|
| **PRESERVED** | All 3 scenarios (tcp-handshake-tcpdump, tls-openssl, udp-vs-tcp-loss) |
| **PRESERVED** | All 15 files — identical or near-identical |

**Snippet verification (C08):**
- `scenario-tcp-handshake-tcpdump/run.sh`: `tcpdump` capture command — identical.
- `scenario-tls-openssl/gen_certs.sh`: OpenSSL certificate generation chain — identical.
- `topo.py`: Mininet topology with `TCLink(loss=...)` — identical.

### C09 — Session and Presentation Layer

| Change | Detail |
|--------|--------|
| **ADDED** | New PUML `fig-mime-examples.puml` + PNG |
| **PRESERVED** | `scenario-encoding-utf8/` — server.py, run.sh |
| **PRESERVED** | `scenario-mime-encoding-gzip/` — all 4 files |

### C10 — HTTP and WebSocket

| Change | Detail |
|--------|--------|
| **PRESERVED** | All 4 scenarios (custom-http-semantics, http-compose, rest-maturity, websocket-protocol) |
| **PRESERVED** | All Python, Dockerfile, docker-compose, nginx.conf, HTML files — identical |

**Snippet verification (C10):**
- `scenario-rest-maturity/server-level0.py` through `server-level3.py`: all 4 REST maturity levels — identical.
- `scenario-websocket-protocol/server.py`: WebSocket handshake + framing — identical.
- `scenario-http-compose/docker-compose.yml`: nginx + Flask API + web — identical.

### C11 — DNS, FTP, SSH

| Change | Detail |
|--------|--------|
| **PRESERVED** | All 4 scenarios (dns-ttl-caching, ftp-baseline, ftp-nat-firewall, ssh-provision) |
| **ADDED** | `scenario-ftp-nat-firewall/data/README.txt` and `ftp/README.txt` — new helper files |
| **MODIFIED** | `scenario-ftp-nat-firewall/client/ftp_client.py`: expanded from 21→34 lines (added error handling) |

### C12 — Email (SMTP/POP3/IMAP)

All files identical. No changes.

### C13 — Security and IoT

All files identical. No changes.

---

## SEMINARS (04_SEMINARS)

### S01 — Basic Tools, Netcat, Wireshark

| RO File | EN File | Snippet Status |
|---------|---------|----------------|
| `1_basic-tools_scenario.md` | `S01_Part01_Scenario_Basic_Tools.md` | ✅ Fully translated. `ping`, `netstat`, `nslookup` commands preserved. |
| `2_basic-tools_task.md` | `S01_Part02_Tasks_Basic_Tools.md` | ✅ Translated |
| `3_netcat-basics_scenario.md` | `S01_Part03_Scenario_Netcat_Basics.md` | ✅ Translated. `nc -l`, `nc -u` commands preserved. |
| `4_netcat-basics_task.md` | `S01_Part04_Tasks_Netcat_Basics.md` | ✅ Translated |
| `5_wireshark-netcat_scenario.md` | `S01_Part05_Scenario_Wireshark_Netcat.md` | ✅ Translated. Capture filters preserved. |
| `6_wireshark-netcat_task.md` | `S01_Part06_Tasks_Wireshark_Netcat.md` | ✅ Translated |

### S02 — TCP/UDP Server-Client

| RO File | EN File | Code Status |
|---------|---------|-------------|
| `1_tcp-server_example.py` (71 lines) | `S02_Part01_Example_TCP_Server.py` | ✅ 87% — refactored to `main()`, socket logic preserved |
| `2_tcp-server_template.py` (61 lines) | `S02_Part02_Template_TCP_Server.py` | ✅ 95% — `TODO` placeholders preserved |
| `3_tcp-server-netcat-wireshark_scenario.md` | `S02_Part03_Scenario...md` | ✅ Translated |
| `4_tcp-client_example.py` (33 lines) | `S02_Part04_Example_TCP_Client.py` (28 lines) | ⚠️ 67% — rewritten to OOP. `socket.connect()`, `sendall()`, `recv()` preserved. Inline RO comments replaced with EN docstring. |
| `5_tcp-client_template.py` (48 lines) | `S02_Part05_Template_TCP_Client.py` (55 lines) | ✅ CODE_MATCH — identical functional code |
| `6_tcp-client_scenario.py` (146 lines) | `S02_Part06_Scenario_TCP_Client.py` (147 lines) | ✅ 45% text — this is scenario documentation embedded in `.py`. Fully translated. Line count preserved. |
| `7_udp-server_example.py` (57 lines) | `S02_Part07_Example_UDP_Server.py` | ✅ 95% |
| `8_udp-server_template.py` (57 lines) | `S02_Part08_Template_UDP_Server.py` | ✅ 95% |
| `9_udp-client_example.py` (38 lines) | `S02_Part09_Example_UDP_Client.py` | ✅ 73% — `sendto()`/`recvfrom()` logic preserved |
| `10_udp-client_template.py` (65 lines) | `S02_Part10_Template_UDP_Client.py` | ✅ 92% |
| `11_udp-server-client-wireshark_scenario.md` | `S02_Part11_Scenario...md` | ✅ Translated |
| **ADDED** | 11 `.html` rendered versions for each part | 🆕 |

### S03 — Multi-client TCP, Broadcast, Multicast, Anycast

All 12 Python files matched. Key snippets:
- **Threading model** (`threading.Thread(target=handle_client)`) in tcp-multiclient-server: ✅ preserved.
- **Broadcast** (`SO_BROADCAST` setsockopt, `'<broadcast>'` address): ✅ preserved.
- **Multicast** (`IP_ADD_MEMBERSHIP`, `struct.pack('4sl', ...)`) : ✅ preserved.
- **Anycast** (SO_REUSEADDR, client hash-based selection): ✅ preserved.

### S04 — Text Protocol, Binary Protocol, UDP Protocol

All 13 Python files matched. Key snippets:
- **Text protocol** (CRLF delimiters, `readline()` framing): ✅ CODE_MATCH.
- **Binary protocol** (`struct.pack('!BHI', ...)`, header parsing): ✅ CODE_MATCH.
- **UDP protocol** with `serialization.py`, `state.py`, `transfer_units.py`: ✅ all present.

⚠️ `transfer_units.py` (74% match): structural changes in class definitions. Functional constants and serialization methods need manual verification.

### S05 — IPv4/IPv6 Subnetting, Mininet

All files matched (MD translated, Python 96%). Key snippets:
- **Mininet topology** (`Topo`, `addHost`, `addSwitch`, `addLink`): ✅ preserved.
- **Subnetting exercises** with CIDR/FLSM/VLSM calculations: ✅ translated.

### S06 — Routing, SDN, OpenFlow

All 7 Python files matched (94-100%). Key snippets:
- **Routing triangle topology**: ✅ `ip route add` commands, Mininet setup.
- **OS-Ken SDN controller** (217 lines, 98%): `OFPActionOutput`, `OFPFlowMod`, `OFPPacketIn` handlers — ✅ all preserved.
- **TCP/UDP traffic generation scripts**: ✅ CODE_MATCH.

### S07 — Packet Sniffing, Filtering, Port Scanning, IDS

All 5 Python files matched (86-94%). Key snippets:
- **Scapy sniffer** (`sniff(filter=..., prn=...)`, packet dissection): ✅ preserved.
- **Packet filter** (BPF expressions, IP/TCP layer extraction): ✅ preserved.
- **Port scanner** (`connect_ex()`, threading, banner grabbing): ✅ preserved.
- **Scan detector** (connection rate tracking, threshold alerting): ✅ preserved.
- **Mini-IDS** (300 lines, 92%): signature matching, anomaly detection rules — ✅ preserved.

### S08 — HTTP Server (Builtin, Socket, Nginx)

All Python files matched (93-94%). Key snippets:
- **http.server** subclass with custom handler: ✅ preserved.
- **Raw socket HTTP server** (148 lines): header parsing, static file serving, content-type detection — ✅ preserved.

⚠️ **Config files divergence:**
- `docker-compose.yml`: 58% match. Services renamed or restructured.
- `nginx.conf`: 46% match. Proxy directives may have changed.

### S09 — FTP (pyftpd, Custom Pseudo-FTP, Multi-client Containers)

All 6 Python files matched. Key snippets:
- **pyftpd server** (`pyftpdlib.handlers.FTPHandler`, `DTPHandler`): ✅ preserved.
- **Pseudo-FTP server** (299 lines): custom command protocol (`LIST`, `GET`, `PUT`, `QUIT`), threading — ✅ CODE_MATCH.
- **Pseudo-FTP client** (269 lines): command loop, file transfer logic — ✅ 100%.
- **Multi-client** (102 lines): ⚠️ 73% — review concurrent FTP operations.

### S10 — DNS Containers, SSH, Port Forwarding

All Python files matched. Key snippets:
- **DNS server** (`socketserver.BaseRequestHandler`, query parsing): ✅ CODE_MATCH.
- **Paramiko SSH client** (76 lines): `paramiko.SSHClient()`, key-based auth, command execution — ✅ 96%.

### S11 — Nginx Compose, Custom Load Balancer

All files matched. Key snippets:
- **Load balancer** (120 lines): round-robin, socket forwarding, health checks — ✅ 100%.
- **Nginx config**: ✅ identical.

### S12 — JSON-RPC, Protobuf, gRPC

All files matched. Key snippets:
- **JSON-RPC client**: `jsonrpcclient` library usage — ✅ CODE_MATCH.
- **gRPC server** (110 lines): `grpc.server()`, service registration — ✅ 96%.
- **gRPC client** (108 lines): stub creation, unary/streaming calls — ✅ 92%.
- **calculator.proto**: message/service definitions — 83% (comment translation).

### S13 — Penetration Testing

All files matched. Key snippets:
- **Simple scanner** (55 lines): `socket.connect_ex()`, port sweep — ✅ 97%.
- **FTP backdoor exploit** (82 lines): vsftpd 2.3.4 exploit logic — ✅ CODE_MATCH.
- **docker-compose.pentest.yml**: ✅ 96%.

---

## New Content in EN Kit (Not in RO)

### 00_APPENDIX/optional_LECTURES/
14 standalone HTML lecture presentations (S1Theory–S14Theory) covering all 14 weeks. Each 76–190KB. Self-contained with embedded styling.

### 00_TOOLS/PlantUML(optional)/
- `generate_a4.py`, `generate_all.sh`, `generate_diagrams.py`, `generate_png_simple.py` — batch PUML rendering tools
- `week_01-14.zip` — archived PUML sources by week

### 01_GHID_MININET-SDN/
- `SETUP-GUIDE-COMPNET-EN.md` + `.html` — Mininet/SDN environment setup guide (EN)

### 02_PROJECTS/
- 15 optional project descriptions (`P01_SDN_Firewall_Mininet.md` through `P15_MQTT_IoT_Client_Server.md`)
- `common/` — shared resources (bibliography, glossary, code standards, troubleshooting, git workflow, etc.)
- `templates/` — project template + starter kit (Makefile, config.yaml, requirements.txt, main.py, test_smoke.py)

### 04_SEMINARS/_HTMLsupport/
60 HTML files mirroring seminar content for web delivery.

### Inline HTML Pages
59 additional `.html` files within seminar folders rendering Python code with syntax highlighting.

### Other
- `requirements-optional.txt` — optional Python package list
- `CHANGELOG.md` — change documentation
- New `.gitkeep` files in S09 for empty directory preservation

---

## Files Removed from EN Kit

| File | Lines | Reason |
|------|-------|--------|
| `assets/course/c1/render-presentation.py` | 103 | PPTX generation utility — not needed if PowerPoint pipeline is not used |
| `assets/course/c1/c1-fundamente-retele.pptx` | binary | PowerPoint file — no EN equivalent created |
| `.gitignore` | moved to root level |

---

## Summary Statistics

| Category | RO → EN | Status |
|----------|---------|--------|
| PNG images | 85 → 85+ | ✅ All preserved + EN translations added |
| PUML diagrams | ~90 → ~90+ | ✅ All preserved + EN translations added |
| Python scripts (lectures) | ~50 → ~50 | ✅ All preserved (0 lost) |
| Python scripts (seminars) | 63 → 63 | ✅ All matched (CODE_MATCH or ≥73%) |
| MD documents | 135 → 135+ | ✅ All preserved + EN translations |
| Config files (yml/conf/proto) | ~15 → ~15 | ⚠️ 5 need functional review |
| HTML pages | 0 → 119 | 🆕 Added for web delivery |
| Optional lectures | 0 → 14 | 🆕 |
| Projects | 0 → 15 | 🆕 |
| Files removed | 2 | `render-presentation.py`, `.pptx` |
