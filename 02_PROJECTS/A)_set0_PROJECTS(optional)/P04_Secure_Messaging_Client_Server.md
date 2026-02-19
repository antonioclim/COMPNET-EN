# Project 04: Secure Messaging Client-Server Application

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main

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

---

### 🐙 GitHub Publication

**Repository:** `https://github.com/[username]/retele-proiect-04`

---

## 📚 Project Description

This project implements a secure messaging application with client-server architecture. Messages are encrypted before transmission, ensuring confidentiality even if network traffic is intercepted. You will implement authentication, key exchange and encrypted message transport.

### 🎯 Learning Objectives

- **Implement** TLS/SSL encrypted connections in Python
- **Design** secure authentication mechanisms
- **Apply** symmetric and asymmetric encryption appropriately
- **Handle** multiple concurrent client connections
- **Test** security against common attack vectors

### 🛠️ Technologies and Tools

| Technology | Purpose |
|------------|---------|
| **Python ssl module** | TLS/SSL connections |
| **cryptography library** | Encryption primitives |
| **Sockets** | Network communication |
| **Threading** | Concurrent clients |

---

## 🎯 Concept Analogies

### TLS Handshake = Diplomatic Credentials Exchange

🏠 **Real-World Analogy:**  
When diplomats meet, they first verify each other's credentials (certificates), agree on a common language (cipher suite) and then exchange a secret code (session key) for private communications.

💻 **Technical Mapping:**
- Credentials = X.509 certificates
- Language negotiation = Cipher suite selection
- Secret code = Session key (symmetric)
- Private channel = Encrypted tunnel

### Symmetric vs Asymmetric = Shared Lock vs Mailbox

🏠 **Real-World Analogy:**  
**Symmetric:** Two people share the same key to a lockbox. Fast to use, but how do you safely share the key initially?

**Asymmetric:** A mailbox with a public slot (anyone can drop mail) and a private key to open (only owner can read). Slower but solves key distribution.

💻 **Technical Mapping:**
- Asymmetric (RSA) = Used for initial key exchange
- Symmetric (AES) = Used for bulk message encryption

---

## 🗳️ Peer Instruction Questions

### Question 1: Certificate Verification

> 💭 **PREDICTION:** What happens if the client doesn't verify the server's certificate?

**Options:**
- A) Connection fails
- B) Connection works but is vulnerable to man-in-the-middle ✓
- C) Messages are not encrypted
- D) Server rejects the client

**Correct answer:** B

**Explanation:** Without certificate verification, an attacker can present their own certificate and intercept all traffic. The encryption works, but to the wrong endpoint!

---

### Question 2: Key Exchange

**Question:** Why don't we encrypt messages directly with RSA?

**Options:**
- A) RSA is not secure enough
- B) RSA is too slow for large messages and has size limits ✓
- C) RSA keys are too small
- D) RSA doesn't work over networks

**Correct answer:** B

**Explanation:** RSA can only encrypt data smaller than the key size (minus padding). Also, RSA is ~1000x slower than AES. We use RSA to exchange an AES key, then AES for messages.

---

### Question 3: Perfect Forward Secrecy

**Scenario:** An attacker records all encrypted traffic today. Tomorrow, they steal the server's private key.

**Question:** With standard TLS, can they decrypt yesterday's traffic?

**Options:**
- A) No, each session has unique keys
- B) Yes, if RSA key exchange was used ✓
- C) Only if they also have the client's key
- D) Never, encryption is permanent

**Correct answer:** B

**Explanation:** With RSA key exchange, session keys are encrypted with the server's public key. Stealing the private key lets you decrypt all past session keys. This is why Diffie-Hellman (ECDHE) is preferred for forward secrecy.

---

## ❌ Common Misconceptions

### 🚫 Misconception 1: "HTTPS/TLS means the server is trustworthy"

**WRONG:** "The lock icon means this site is safe."

**CORRECT:** TLS only guarantees **encryption** and **authentication** of the server's identity. It doesn't mean the server itself is trustworthy or won't misuse your data.

---

### 🚫 Misconception 2: "Self-signed certificates are insecure"

**WRONG:** "We must buy certificates from a CA."

**CORRECT:** Self-signed certificates provide the same encryption strength. The difference is trust — browsers warn because they can't verify the server's identity. For internal applications, self-signed can be appropriate with proper distribution.

---

### 🚫 Misconception 3: "Password hashing is encryption"

**WRONG:** "I encrypt passwords with SHA256."

**CORRECT:** Hashing is one-way (can't decrypt), encryption is two-way. Passwords should be hashed (with salt) for storage, but encrypted for transmission.

---

## 📖 Project Glossary

| Term | Definition |
|------|------------|
| **TLS** | Transport Layer Security — encrypted connection protocol |
| **Certificate** | Digital document binding public key to identity |
| **CA** | Certificate Authority — trusted certificate issuer |
| **Symmetric encryption** | Same key for encrypt/decrypt (AES) |
| **Asymmetric encryption** | Public/private key pair (RSA, ECDSA) |
| **Key exchange** | Securely establishing shared secret |
| **Forward secrecy** | Past sessions secure even if key compromised |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""
Secure Messaging Server with TLS
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import ssl
import threading
from typing import Dict
import logging

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
HOST = '0.0.0.0'
PORT = 8443
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

# ═══════════════════════════════════════════════════════════════════════════════
# SSL_CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════
def create_ssl_context() -> ssl.SSLContext:
    """
    Create secure SSL context for server.
    
    Returns:
        Configured SSLContext
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT_FILE, KEY_FILE)
    
    # 💭 PREDICTION: What happens without these settings?
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.set_ciphers('ECDHE+AESGCM')  # Forward secrecy
    
    return context

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_HANDLER
# ═══════════════════════════════════════════════════════════════════════════════
def handle_client(conn: ssl.SSLSocket, addr: tuple, clients: Dict) -> None:
    """
    Handle authenticated client connection.
    
    Args:
        conn: SSL-wrapped socket
        addr: Client address tuple
        clients: Dictionary of connected clients
    """
    logging.info(f"Secure connection from {addr}")
    logging.info(f"Cipher: {conn.cipher()}")
    
    try:
        # Authentication phase
        conn.send(b"Username: ")
        username = conn.recv(1024).decode().strip()
        
        clients[username] = conn
        broadcast(f"{username} joined", clients, exclude=username)
        
        # Message loop
        while True:
            data = conn.recv(4096)
            if not data:
                break
            
            message = data.decode()
            broadcast(f"{username}: {message}", clients, exclude=username)
    
    finally:
        del clients[username]
        broadcast(f"{username} left", clients)
        conn.close()

def broadcast(message: str, clients: Dict, exclude: str = None) -> None:
    """Send message to all clients except excluded."""
    for name, conn in clients.items():
        if name != exclude:
            try:
                conn.send(message.encode())
            except:
                pass

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    logging.basicConfig(level=logging.INFO)
    
    context = create_ssl_context()
    clients = {}
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(5)
        
        with context.wrap_socket(sock, server_side=True) as ssock:
            logging.info(f"Secure server listening on {HOST}:{PORT}")
            
            while True:
                conn, addr = ssock.accept()
                thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr, clients)
                )
                thread.start()

if __name__ == "__main__":
    main()
```

---

## ❓ Frequently Asked Questions

**Q: How do I generate self-signed certificates?**

A:
```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
```

**Q: Client gets "certificate verify failed"**

A: Either disable verification (testing only!) or add your CA:
```python
context.load_verify_locations('server.crt')
# Or for testing:
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 2 | `02enWSL/` | Socket programming basics |
| 9 | `09enWSL/` | TLS/SSL, session security |
| 13 | `13enWSL/` | Network security concepts |

---

*Last update: January 2026*  
*Computer Networks — ASE Bucharest*
