# Project 18: TCP Chat Client-Server Application

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Reserve (Individual)

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Protocol specification | 20% |
| **E2** - Prototype | Week 9 | Basic client-server | 25% |
| **E3** - Final | Week 13 | Multi-client support | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-18`

---

## 📚 Project Description

Build a chat application using TCP sockets supporting multiple concurrent clients. Implement message broadcasting, private messages and user management.

### 🎯 Learning Objectives
- **Implement** TCP client-server communication
- **Handle** multiple concurrent connections
- **Design** application-level protocol
- **Manage** user sessions and broadcasts

---

## 🎯 Concept Analogies

### TCP = Phone Call
🏠 **Analogy:** You dial (connect), wait for answer (handshake), talk (exchange data) and hang up (close). The connection stays open during conversation.

💻 **Technical:** Connection-oriented, reliable, ordered delivery.

### Multi-threading = Multiple Phone Lines
🏠 **Analogy:** A business has multiple phone lines. Each call gets its own line (thread) so conversations don't interfere.

---

## 🗳️ Peer Instruction Questions

### Question 1: TCP Handshake
**Question:** How many packets in TCP three-way handshake?
- A) 2
- B) 3 ✓
- C) 4
- D) 1

### Question 2: Message Framing
**Question:** How does the receiver know where one message ends?
- A) TCP handles it automatically
- B) Application must define framing (length prefix, delimiter) ✓
- C) Messages are fixed size
- D) Each packet = one message

---

## ❌ Common Misconceptions

### 🚫 "TCP send() = one message"
**CORRECT:** TCP is a stream. Multiple sends may arrive as one recv() or one send may arrive as multiple recv(). You must handle framing.

### 🚫 "Threads share nothing"
**CORRECT:** Threads share memory. Must use locks for shared data (like client list).

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **Socket** | Endpoint for communication |
| **Thread** | Parallel execution unit |
| **Broadcast** | Send to all connected clients |
| **Framing** | Delimiting message boundaries |
| **Buffer** | Temporary data storage |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""Multi-Client Chat Server"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import threading
from typing import Dict

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
HOST = '0.0.0.0'
PORT = 9999
BUFFER_SIZE = 4096

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
clients: Dict[str, socket.socket] = {}
clients_lock = threading.Lock()

def broadcast(message: str, exclude: str = None) -> None:
    """Send message to all clients except excluded."""
    with clients_lock:
        for name, sock in clients.items():
            if name != exclude:
                try:
                    # 💭 PREDICTION: What if send fails?
                    sock.send(f"{message}\n".encode())
                except:
                    pass

def handle_client(conn: socket.socket, addr: tuple) -> None:
    """Handle single client connection."""
    conn.send(b"Enter your name: ")
    name = conn.recv(BUFFER_SIZE).decode().strip()
    
    with clients_lock:
        clients[name] = conn
    
    broadcast(f"[{name} joined the chat]", exclude=name)
    
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            
            message = data.decode().strip()
            broadcast(f"{name}: {message}", exclude=name)
    
    finally:
        with clients_lock:
            del clients[name]
        broadcast(f"[{name} left the chat]")
        conn.close()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print(f"Chat server running on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 2 | `02enWSL/` | Socket programming basics |
| 3 | `03enWSL/` | Network programming, threading |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
