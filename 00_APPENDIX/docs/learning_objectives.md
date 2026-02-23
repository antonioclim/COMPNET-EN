# 🎯 Learning Objectives — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Explicit mapping of Learning Objectives to Bloom Taxonomy levels and course artefacts.

---

## Overview

Week 0 serves as the **foundation layer** for the entire course. Students must master these prerequisites before proceeding to Week 1 network concepts.

**Time allocation:** 4-6 hours self-study
**Assessment:** Formative quiz (≥70% to proceed)

---

## Bloom Taxonomy Reference

| Level | Cognitive Process | Typical Verbs | Assessment Type |
|-------|-------------------|---------------|-----------------|
| 1. Remember | Recall facts | List, Define, Name | Quiz (MC) |
| 2. Understand | Explain concepts | Explain, Describe, Compare | Short answer |
| 3. Apply | Use in new situations | Execute, Implement, Configure | Hands-on lab |
| 4. Analyse | Break down, examine | Differentiate, Debug, Trace | Code tracing, PCAP |
| 5. Evaluate | Judge, critique | Assess, Justify, Recommend | Troubleshooting |
| 6. Create | Produce new work | Design, Construct, Develop | Projects |

---

## Learning Objectives Summary

| LO ID | Description | Bloom Level | Primary Assessment |
|-------|-------------|-------------|-------------------|
| LO0.1 | Configure complete WSL2 + Docker environment | Apply (3) | Quiz Q1-Q2, verify script |
| LO0.2 | Distinguish Docker images from containers | Understand (2) | Quiz Q3, Q10 |
| LO0.3 | Apply port mapping between host and containers | Apply (3) | Quiz Q4-Q5 |
| LO0.4 | Convert between bytes and strings in Python | Apply (3) | Quiz Q6-Q7, Code Tracing |
| LO0.5 | Create and configure basic TCP sockets | Apply (3) | Quiz Q8-Q9, Parsons P1-P3 |

---

## Traceability Matrix

### Complete LO → Artefact Mapping

| LO ID | Theory Source | Practice Artefact | Assessment | Parsons | Misconceptions |
|-------|---------------|-------------------|------------|---------|----------------|
| LO0.1 | Prerequisites.md §4-7 | verify_lab_environment.sh | Quiz Q1, Q2; Peer Q1-Q2 | — | #1, #2, #7 |
| LO0.2 | Prerequisites.md §2.1 | docker commands demo | Quiz Q3, Q10; Peer Q3 | — | #3, #4 |
| LO0.3 | Prerequisites.md §2.3 | Portainer setup | Quiz Q4, Q5; Peer Q4-Q5 | — | #5, #6 |
| LO0.4 | PYTHON_GUIDE §3 | 02_bytes_vs_str.py | Quiz Q6, Q7; Tracing T2 | P2 | #9, #10 |
| LO0.5 | PYTHON_GUIDE §4 | 01_socket_tcp.py | Quiz Q8, Q9; Tracing T1, T3 | P1, P3, P4, P5 | #11, #12 |

### Assessment Coverage Matrix

| Assessment Item | LO0.1 | LO0.2 | LO0.3 | LO0.4 | LO0.5 |
|-----------------|-------|-------|-------|-------|-------|
| Quiz Q1 | ✓ | | | | |
| Quiz Q2 | ✓ | | | | |
| Quiz Q3 | | ✓ | | | |
| Quiz Q4 | | | ✓ | | |
| Quiz Q5 | | | ✓ | | |
| Quiz Q6 | | | | ✓ | |
| Quiz Q7 | | | | ✓ | |
| Quiz Q8 | | | | | ✓ |
| Quiz Q9 | | | | | ✓ |
| Quiz Q10 | | ✓ | | | |
| Parsons P1 | | | | | ✓ |
| Parsons P2 | | | | ✓ | ✓ |
| Parsons P3 | | | | | ✓ |
| Parsons P4 | | | | | ✓ |
| Parsons P5 | | | | | ✓ |
| Code Tracing T1 | | | | | ✓ |
| Code Tracing T2 | | | | ✓ | |
| Code Tracing T3 | | | | | ✓ |
| Peer Instruction Q1-Q2 | ✓ | | | | |
| Peer Instruction Q3 | | ✓ | | | |
| Peer Instruction Q4-Q5 | | | ✓ | | |

---

## Detailed LO Specifications

### LO0.1: Configure WSL2 + Docker Environment

**Description:** Students can independently set up a complete lab environment consisting of WSL2, Ubuntu 22.04, Docker Engine and Portainer on a Windows machine.

**Bloom Level:** Apply (Level 3)

**Success Criteria:**
- [ ] WSL2 installed and running (`wsl --status` shows version 2)
- [ ] Ubuntu 22.04 installed with user `stud`
- [ ] Docker Engine running (`docker ps` works without sudo)
- [ ] Portainer accessible at `http://localhost:9000`

**Linked Artefacts:**
- 📚 Theory: `../00_TOOLS/Prerequisites/Prerequisites.md` sections 4-7
- 🔬 Practice: `../00_TOOLS/Prerequisites/verify_lab_environment.sh`
- ✅ Assessment: `formative/quiz.yaml` Q1, Q2; `docs/peer_instruction.md` Q1-Q2
- ❌ Misconceptions: #1 (WSL emulation), #2 (Docker Desktop required), #7 (auto-start)

**Verification Command:**
```bash
./verify_lab_environment.sh
# All checks should pass (green ✓)
```

---

### LO0.2: Distinguish Images from Containers

**Description:** Students can correctly differentiate between Docker images (read-only templates) and containers (running instances) and understand their lifecycle relationship.

**Bloom Level:** Understand (Level 2)

**Success Criteria:**
- [ ] Can explain image vs container using an analogy
- [ ] Correctly predicts output of `docker images` vs `docker ps`
- [ ] Understands that multiple containers can share one image

**Linked Artefacts:**
- 📚 Theory: `../00_TOOLS/Prerequisites/Prerequisites.md` section 2.1
- 🔬 Practice: Docker commands (`docker images`, `docker ps -a`)
- ✅ Assessment: `formative/quiz.yaml` Q3, Q10; `docs/peer_instruction.md` Q3
- ❌ Misconceptions: #3 (container = image), #4 (stop deletes data)

**Verification Command:**
```bash
docker images
docker ps -a
# Student should explain the difference in output
```

---

### LO0.3: Apply Port Mapping

**Description:** Students can correctly configure and use Docker port mapping (`-p HOST:CONTAINER`) to access containerised services from the host machine.

**Bloom Level:** Apply (Level 3)

**Success Criteria:**
- [ ] Can predict which URL accesses a mapped service
- [ ] Understands HOST:CONTAINER format
- [ ] Knows about localhost isolation in containers

**Linked Artefacts:**
- 📚 Theory: `../00_TOOLS/Prerequisites/Prerequisites.md` section 2.3
- 🔬 Practice: Portainer setup with `-p 9000:9000`
- ✅ Assessment: `formative/quiz.yaml` Q4, Q5; `docs/peer_instruction.md` Q4-Q5
- ❌ Misconceptions: #5 (ports auto-exposed), #6 (localhost is global)

**Verification Command:**
```bash
docker run -d -p 8080:80 nginx
curl http://localhost:8080
# Should return nginx welcome page
```

---

### LO0.4: Convert Bytes ↔ Strings

**Description:** Students can correctly encode strings to bytes and decode bytes to strings in Python, including proper error handling for invalid sequences.

**Bloom Level:** Apply (Level 3)

**Success Criteria:**
- [ ] Knows `encode()` direction: str → bytes
- [ ] Knows `decode()` direction: bytes → str
- [ ] Can use `errors='replace'` for safe decoding

**Linked Artefacts:**
- 📚 Theory: `PYTHON_self_study_guide/PYTHON_NETWORKING_GUIDE.md` section 3
- 🔬 Practice: `PYTHON_self_study_guide/examples/02_bytes_vs_str.py`
- ✅ Assessment: `formative/quiz.yaml` Q6, Q7; `docs/code_tracing.md` T2; `docs/parsons_problems.md` P2
- ❌ Misconceptions: #9 (encode/decode direction), #10 (UTF-8 safety)

**Verification Code:**
```python
text = "Hello"
wire = text.encode('utf-8')
back = wire.decode('utf-8')
assert text == back
```

---

### LO0.5: Create Basic TCP Sockets

**Description:** Students can create, configure and use TCP sockets for basic client-server communication, including proper use of SO_REUSEADDR and struct packing.

**Bloom Level:** Apply (Level 3)

**Success Criteria:**
- [ ] Can create socket with correct AF_INET, SOCK_STREAM
- [ ] Knows server sequence: socket → setsockopt → bind → listen → accept
- [ ] Knows client sequence: socket → connect → send → recv → close
- [ ] Can use struct.pack with network byte order (`!`)

**Linked Artefacts:**
- 📚 Theory: `PYTHON_self_study_guide/PYTHON_NETWORKING_GUIDE.md` section 4
- 🔬 Practice: `PYTHON_self_study_guide/examples/01_socket_tcp.py`
- ✅ Assessment: `formative/quiz.yaml` Q8, Q9; `docs/parsons_problems.md` P1, P3, P4, P5; `docs/code_tracing.md` T1, T3
- ❌ Misconceptions: #11 (client/server sequence), #12 (recv() partial data)

**Verification Code:**
```python
import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Socket created successfully
```

---

## Cross-Reference Quick Lookup

### By Assessment Type

| Assessment | LO Coverage |
|------------|-------------|
| Quiz Q1-Q2 | LO0.1 |
| Quiz Q3, Q10 | LO0.2 |
| Quiz Q4-Q5 | LO0.3 |
| Quiz Q6-Q7 | LO0.4 |
| Quiz Q8-Q9 | LO0.5 |
| Parsons P1, P3, P4, P5 | LO0.5 |
| Parsons P2 | LO0.4, LO0.5 |
| Code Tracing T1, T3 | LO0.5 |
| Code Tracing T2 | LO0.4 |
| Peer Instruction Q1-Q2 | LO0.1 |
| Peer Instruction Q3 | LO0.2 |
| Peer Instruction Q4-Q5 | LO0.3 |

### By Bloom Level

| Bloom Level | Learning Objectives |
|-------------|---------------------|
| Understand (2) | LO0.2 |
| Apply (3) | LO0.1, LO0.3, LO0.4, LO0.5 |

### By Misconception

| Misconception | Related LO |
|---------------|------------|
| #1, #2, #7 | LO0.1 |
| #3, #4 | LO0.2 |
| #5, #6 | LO0.3 |
| #9, #10 | LO0.4 |
| #11, #12 | LO0.5 |

---

## Self-Assessment Checklist

Before proceeding to Week 1, verify you can:

- [ ] Start WSL2 and Docker without errors
- [ ] Access Portainer at localhost:9000
- [ ] Run `verify_lab_environment.sh` with all checks passing
- [ ] Score ≥70% on `formative/quiz.yaml`
- [ ] Explain the container/image relationship to a peer
- [ ] Write a simple TCP client that connects and sends a message
- [ ] Convert between bytes and strings without errors
- [ ] Identify the correct socket sequence for server vs client

---

## Formative Assessment Path

```
┌─────────────────────────────────────────────────────────────────┐
│  1. SELF-STUDY                                                   │
│     └── Read Prerequisites.md + PYTHON_NETWORKING_GUIDE.md      │
│                              ↓                                   │
│  2. PRACTICE                                                     │
│     └── Run examples/*.py, complete Parsons problems            │
│                              ↓                                   │
│  3. SELF-CHECK                                                   │
│     └── Review misconceptions.md, complete code_tracing.md      │
│                              ↓                                   │
│  4. ASSESSMENT                                                   │
│     └── Run: python formative/run_quiz.py                       │
│                              ↓                                   │
│  5. REMEDIATION (if score < 70%)                                │
│     └── Review linked artefacts for failed questions            │
│                              ↓                                   │
│  6. READY FOR WEEK 1 ✓                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

*Learning Objectives Document — Week 0 | Computer Networks | ASE-CSIE*
*Version: 1.5.0 | Date: 2026-01-24*
