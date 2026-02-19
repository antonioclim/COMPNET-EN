# Project 16: HTTP Traffic Analysis with Wireshark

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Reserve (Individual)

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Analysis Plan | 20% |
| **E2** - Prototype | Week 9 | Partial captures and analysis | 25% |
| **E3** - Final | Week 13 | Complete analysis report | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-16`

---

## 📚 Project Description

Capture and analyse HTTP/HTTPS traffic using Wireshark. Document the complete request-response cycle, analyse headers, identify performance issues and compare HTTP versions.

### 🎯 Learning Objectives
- **Capture** HTTP traffic with Wireshark
- **Analyse** request/response structure
- **Compare** HTTP/1.1 vs HTTP/2
- **Identify** security implications of unencrypted traffic

---

## 🎯 Concept Analogies

### HTTP Request = Restaurant Order
🏠 **Analogy:** You tell the waiter (request) what you want, including special instructions (headers). The kitchen prepares it and the waiter brings your food (response) with the bill (status code).

💻 **Technical:** GET/POST = order type, Headers = preferences, Body = content.

---

## 🗳️ Peer Instruction Questions

### Question 1: HTTP Headers
**Question:** Which header tells the server what content types the client accepts?
- A) Content-Type
- B) Accept ✓
- C) User-Agent
- D) Host

### Question 2: Status Codes
**Question:** What does HTTP 304 mean?
- A) Error occurred
- B) Resource not found
- C) Resource not modified (use cache) ✓
- D) Redirect

---

## ❌ Common Misconceptions

### 🚫 "HTTPS means I can't analyse traffic"
**CORRECT:** You can't see content, but metadata (IPs, ports, timing, sizes) is visible. With your own certificate, you can decrypt your own traffic.

### 🚫 "HTTP/2 is just faster HTTP/1.1"
**CORRECT:** HTTP/2 uses binary framing, multiplexing, header compression — fundamentally different protocol, just backward compatible.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **HTTP Method** | GET, POST, PUT, DELETE, etc. |
| **Status Code** | 200 OK, 404 Not Found, 500 Error |
| **Header** | Metadata about request/response |
| **TLS** | Encryption layer for HTTPS |
| **Wireshark Filter** | Display filter syntax |

---

## 🔨 Analysis Tasks

```
# ═══════════════════════════════════════════════════════════════════════════════
# WIRESHARK_FILTERS
# ═══════════════════════════════════════════════════════════════════════════════

# Capture only HTTP traffic
http

# Filter by method
http.request.method == "GET"
http.request.method == "POST"

# Filter by status code
http.response.code == 200
http.response.code >= 400

# 💭 PREDICTION: What will "http.host contains 'google'" show?
# Answer: All HTTP requests to domains containing "google"

# Filter by content type
http.content_type contains "json"

# Follow HTTP stream
Right-click packet → Follow → HTTP Stream
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 7 | `07enWSL/` | Wireshark capture and filtering |
| 8 | `08enWSL/` | HTTP server implementation |
| 10 | `10enWSL/` | Application protocols (HTTP/HTTPS) |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
