# Project 09: Multi-Client FTP Server

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

> 📍 **Navigation:** [00PROJ](../README.md) → [PROJECTS](./README.md) → P09

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Project assessment takes place EXCLUSIVELY at the faculty, with mandatory physical attendance.**

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md) | [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-09`

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | FTP commands, modes, authentication |
| Architecture diagrams | 20 | Control/data channels, state machine |
| Implementation plan | 15 | Realistic timeline |
| Repository initialised | 15 | GitHub configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Basic FTP commands work | 35 | LIST, RETR, STOR |
| Code quality | 25 | Clean, typed, documented |
| Multi-client support | 15 | Threading/async handling |
| Progress report | 10 | Documents progress |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete FTP implementation | 40 | All required commands |
| Final code quality | 20 | Production-ready |
| Tests | 15 | Unit and integration |
| Documentation | 10 | Complete docs |
| Performance analysis | 5 | Concurrent connections metrics |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus: FTPS support** | +10 | TLS encryption (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | File transfer works |
| Technical presentation | 25 | Explains FTP protocol |
| Answers to questions | 20 | Demonstrates understanding |
| Team contribution | 15 | All members know code |
| Time management | 5 | 10-15 minutes |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Basic commands (LIST, RETR, STOR, USER, PASS) |
| **2 persons** | + Passive/Active modes + directory navigation |
| **3 persons** | + FTPS + resume support + bandwidth limiting |

---

## 📚 Project Description

Implement a simplified FTP server that supports multiple concurrent clients. The server will handle standard FTP commands for file listing, upload, download and directory navigation. This project provides deep understanding of the FTP protocol with its unique dual-channel architecture (control + data).

### 🎯 Learning Objectives

- **LO1:** Implement FTP command/response protocol over control connection
- **LO2:** Manage separate data connections for file transfers
- **LO3:** Support both active and passive transfer modes
- **LO4:** Handle multiple clients concurrently using threading
- **LO5:** Implement user authentication
- **LO6:** Parse and generate FTP protocol messages

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Python sockets** | Network programming | [docs.python.org](https://docs.python.org/3/library/socket.html) |
| **threading** | Concurrent clients | [docs.python.org](https://docs.python.org/3/library/threading.html) |
| **FTP RFC 959** | Protocol specification | [RFC 959](https://tools.ietf.org/html/rfc959) |
| **FileZilla** | FTP client testing | [filezilla-project.org](https://filezilla-project.org) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **Control Connection** | Port 21, sends commands/responses |
| **Data Connection** | Transfers files and directory listings |
| **Active Mode** | Server connects to client's data port |
| **Passive Mode** | Client connects to server's data port |
| **Response Codes** | 3-digit codes (220, 331, 230, 550) |
| **ASCII/Binary Mode** | Text vs binary transfer |
| **PWD/CWD** | Print/Change working directory |
| **RETR/STOR** | Retrieve (download) / Store (upload) |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST implement USER, PASS, LIST, RETR, STOR, QUIT commands
- [ ] MUST support passive mode (PASV)
- [ ] MUST handle multiple concurrent clients
- [ ] MUST return correct FTP response codes
- [ ] MUST log all commands and transfers
- [ ] MUST pass all smoke tests

### MUST NOT (Forbidden)
- [ ] MUST NOT use ftplib for server (only for testing)
- [ ] MUST NOT allow directory traversal attacks (../)
- [ ] MUST NOT crash on malformed commands
- [ ] MUST NOT leave data connections open

### SHOULD (Recommended)
- [ ] SHOULD implement active mode (PORT)
- [ ] SHOULD support binary and ASCII modes
- [ ] SHOULD implement CWD, PWD, MKD, RMD

---

## 🎯 Concept Analogies

### FTP = Phone Call with Fax

🏠 **Real-World Analogy:**  
You call someone (control connection) to discuss what documents to send. When ready to transfer, you use a fax machine (data connection) to send the actual documents. The phone call stays open to coordinate, but the fax is a separate channel for the data.

💻 **Technical Mapping:**
- Phone call = Control connection (port 21)
- Fax machine = Data connection (port 20 or random)
- "Please send invoice" = RETR invoice.pdf
- "Document received" = 226 Transfer complete

⚠️ **Where the analogy breaks:** Modern fax doesn't require a separate phone call. FTP's dual-channel design is a historical artefact from when this made sense for network architecture.

---

### Active vs Passive = Who Calls Whom

🏠 **Real-World Analogy:**  
Active mode: "I'll call you back at this number" — server calls client. Passive mode: "Here's my direct line, call me" — client calls server.

💻 **Technical Mapping:**
- Active: Client sends PORT command with its IP:port, server connects
- Passive: Client sends PASV, server replies with IP:port, client connects

---

## 🗳️ Peer Instruction Questions

### Question 1: Why Two Connections?

> 💭 **PREDICTION:** Why does FTP use separate control and data connections?

**Options:**
- A) Security reasons
- B) Allow commands while transferring ✓
- C) Faster transfers
- D) Protocol limitation

**Correct answer:** B

**Explanation:** With separate channels, you can send commands (like ABOR to cancel) while a file transfer is in progress. The control connection remains responsive.

---

### Question 2: Passive Mode Purpose

> 💭 **PREDICTION:** When is passive mode necessary?

**Options:**
- A) When server is behind firewall
- B) When client is behind NAT/firewall ✓
- C) For faster transfers
- D) For secure transfers

**Correct answer:** B

**Explanation:** In active mode, the server connects TO the client — but if the client is behind NAT, the server can't reach it. Passive mode reverses this: client connects to server, which works through NAT.

---

### Question 3: Response Code Meaning

> 💭 **PREDICTION:** What does response code 550 mean?

**Options:**
- A) Success
- B) Need password
- C) File not found/permission denied ✓
- D) Transfer complete

**Correct answer:** C

**Explanation:** 5xx codes indicate permanent failures. 550 specifically means "Requested action not taken" — usually file not found or permission denied.

---

### Question 4: PORT Command

> 💭 **PREDICTION:** What does PORT 192,168,1,5,4,1 mean?

**Options:**
- A) Server port 4.1
- B) IP 192.168.1.5, port 1025 ✓
- C) IP 192.168.1.54, port 1
- D) Error format

**Correct answer:** B

**Explanation:** PORT format is h1,h2,h3,h4,p1,p2. Port = p1*256 + p2 = 4*256 + 1 = 1025. IP = 192.168.1.5.

---

## ❌ Common Misconceptions

### 🚫 "FTP is secure"

**WRONG:** Standard FTP sends passwords in plain text.

**CORRECT:** FTP has no encryption. Use FTPS (FTP over TLS) or SFTP (SSH File Transfer) for security. Your project can note this limitation.

---

### 🚫 "Port 21 transfers files"

**WRONG:** All FTP traffic goes through port 21.

**CORRECT:** Port 21 is only for commands. Files transfer on separate connections (port 20 for active, random high port for passive).

---

### 🚫 "Active mode is better"

**WRONG:** Active mode is the original, so it's better.

**CORRECT:** Passive mode works better with modern networks (NAT, firewalls). Most clients default to passive.

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **Control Connection** | TCP connection on port 21 for commands |
| **Data Connection** | Separate TCP connection for file data |
| **Active Mode** | Server initiates data connection to client |
| **Passive Mode** | Client initiates data connection to server |
| **ASCII Mode** | Text transfer with line ending conversion |
| **Binary Mode** | Raw byte transfer without conversion |
| **RETR** | Retrieve (download) a file |
| **STOR** | Store (upload) a file |
| **PASV** | Request passive mode |
| **Response Code** | 3-digit status (2xx success, 5xx error) |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""FTP Server - Command Handler"""

# ═══════════════════════════════════════════════════════════════════════════════
# FTP_COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════
class FTPHandler:
    """Handle FTP commands for a single client."""
    
    def __init__(self, control_socket, root_dir: str):
        self.control = control_socket
        self.root_dir = Path(root_dir)
        self.cwd = self.root_dir
        self.authenticated = False
        self.data_socket = None
        self.transfer_mode = "passive"
    
    def handle_USER(self, username: str) -> str:
        """Handle USER command."""
        self.username = username
        return "331 Username OK, need password"
    
    def handle_PASS(self, password: str) -> str:
        """Handle PASS command."""
        # 💭 PREDICTION: What if wrong password?
        # Answer: Return 530 Login incorrect
        if self._check_credentials(self.username, password):
            self.authenticated = True
            return "230 Login successful"
        return "530 Login incorrect"
    
    def handle_PASV(self, args: str) -> str:
        """Handle PASV command - enter passive mode."""
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.bind(('0.0.0.0', 0))
        self.data_socket.listen(1)
        
        ip = self.control.getsockname()[0]
        port = self.data_socket.getsockname()[1]
        
        # Format: h1,h2,h3,h4,p1,p2
        ip_parts = ip.split('.')
        p1, p2 = port // 256, port % 256
        
        return f"227 Entering Passive Mode ({','.join(ip_parts)},{p1},{p2})"
    
    def handle_LIST(self, path: str = "") -> str:
        """Handle LIST command - directory listing."""
        if not self.authenticated:
            return "530 Not logged in"
        
        target = self.cwd / path if path else self.cwd
        
        # Accept data connection
        data_conn, _ = self.data_socket.accept()
        
        try:
            listing = self._format_listing(target)
            data_conn.sendall(listing.encode())
            return "226 Directory listing sent"
        finally:
            data_conn.close()
    
    def handle_RETR(self, filename: str) -> str:
        """Handle RETR command - download file."""
        if not self.authenticated:
            return "530 Not logged in"
        
        file_path = self.cwd / filename
        if not file_path.exists():
            return "550 File not found"
        
        data_conn, _ = self.data_socket.accept()
        
        try:
            with open(file_path, 'rb') as f:
                data_conn.sendall(f.read())
            return "226 Transfer complete"
        finally:
            data_conn.close()
```

---

## 📋 Expected Outputs

### Scenario 1: Successful Login

```
USER student
331 Username OK, need password
PASS secret
230 Login successful
```

### Scenario 2: Directory Listing

```
PASV
227 Entering Passive Mode (192,168,1,1,4,1)
LIST
150 Opening data connection
226 Directory listing sent
```

---

## ❓ Frequently Asked Questions

**Q: How do I test with FileZilla?**

A: Connect to localhost:21 with your test credentials. Enable passive mode in settings if behind NAT.

**Q: Why does active mode fail?**

A: Your client is probably behind NAT. Server can't connect back. Use passive mode.

---

## 📚 Laboratory References

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 11 | `11enWSL/` | FTP protocol, file transfer |
| 2 | `02enWSL/` | Socket programming |
| 9 | `09enWSL/` | Session layer protocols |

---

## 📚 Bibliography

1. **[OFFICIAL]** FTP RFC 959  
   URL: https://tools.ietf.org/html/rfc959  
   Verified: 2026-01-24 ✓

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
