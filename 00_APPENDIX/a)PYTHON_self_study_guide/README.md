# 🐍 Python Self-Study Guide for Computer Networks
## Version 5.1 — Tailored for Multi-Language Backgrounds

> **Status:** Optional, Not Assessed
> **Course:** Computer Networks — ASE Bucharest, CSIE
> **Environment:** WSL2 + Ubuntu 22.04 + Docker + Python 3.10+
> **Version:** 5.1 — January 2026

---

## 🎯 What Is This?

This guide helps students who know **C, C++, JavaScript, Java or Kotlin** quickly understand Python code used in lab exercises. It is designed as a **translation guide**, not a Python course from scratch.

> "You do not need to learn Python from zero. You need to translate what you already know."

---

## 📑 Navigation Index

### Getting Started
- [Quick Start](#-quick-start) — Begin here
- [Learning Paths](#-choose-your-learning-path) — Based on your background
- [Environment Check](#1-check-your-environment) — Verify setup

### Core Resources
- [PYTHON_NETWORKING_GUIDE.md](PYTHON_NETWORKING_GUIDE.md) — Complete 9-step guide (2200+ lines)
- [Rosetta Stone](comparisons/ROSETTA_STONE.md) — Same code in 5 languages
- [Misconceptions Guide](comparisons/MISCONCEPTIONS_BY_BACKGROUND.md) — Common mistakes by background

### Practice & Assessment
- [Quiz System](formative/quiz.yaml) — 31 self-assessment questions
- [Parsons Problems](formative/parsons/) — Code ordering exercises
- [Examples](examples/) — Annotated working code

### Reference
- [Cheatsheet](cheatsheets/PYTHON_QUICK.md) — Quick reference for networking
- [Troubleshooting](docs/TROUBLESHOOTING.md) — 16 common issues and fixes
- [Presentations](PRESENTATIONS_EN/) — 10 HTML slide decks

---

## 📁 Contents

| Folder/File | Description | When to Use |
|-------------|-------------|-------------|
| `comparisons/` | 🆕 Side-by-side code in C, JS, Java, Kotlin, Python | First, to map your knowledge |
| `formative/` | 🆕 Quiz (31 questions) + Parsons problems | To self-assess readiness |
| `docs/` | 🆕 Troubleshooting guide (16 scenarios) | When you encounter errors |
| `Makefile` | Easy commands: `make quiz`, `make test` | To run everything |
| `cheatsheets/` | Quick reference for networking | During lab work |
| `examples/` | Annotated code examples with tests | To study patterns |
| `PRESENTATIONS_EN/` | 10 HTML slide presentations | For visual learners |
| `PYTHON_NETWORKING_GUIDE.md` | Complete guide (2200+ lines) | Deep study |

---

## 🚀 Quick Start

### 1. Check Your Environment
```bash
make check
```

Expected output:
```
Python version: Python 3.10.x or higher
Required modules:
  ✓ socket
  ✓ struct
  ✓ pyyaml
```

### 2. Take a Quick Assessment
```bash
make quiz-quick    # 10 questions, ~10 minutes
```

**Score interpretation:**
- **80%+** → Ready for labs, skim the guide
- **60-79%** → Review weak sections, then proceed
- **Below 60%** → Work through the full guide first

### 3. Choose Your Learning Path

| Your Background | Start Here | Quiz Command | Estimated Time |
|-----------------|------------|--------------|----------------|
| **C / C++** | [Rosetta Stone](comparisons/ROSETTA_STONE.md) | `make quiz-c` | 2-3 hours |
| **JavaScript** | [Misconceptions](comparisons/MISCONCEPTIONS_BY_BACKGROUND.md#for-javascript-programmers) | `make quiz-js` | 2-3 hours |
| **Java** | [Rosetta Stone](comparisons/ROSETTA_STONE.md) | `make quiz-java` | 1-2 hours |
| **Kotlin** | [Misconceptions](comparisons/MISCONCEPTIONS_BY_BACKGROUND.md#for-kotlin-programmers) | `make quiz-kotlin` | 1-2 hours |
| **Multiple** | Take quiz first | `make quiz-quick` | Varies |

---

## 📝 Available Commands

```bash
make help              # Show all commands

# === Quiz ===
make quiz              # Full quiz (31 questions)
make quiz-quick        # Quick check (10 questions)
make quiz-c            # For C/C++ programmers
make quiz-js           # For JavaScript programmers
make quiz-java         # For Java programmers
make quiz-kotlin       # For Kotlin programmers

# === Parsons Problems ===
make parsons           # Code ordering exercises
make parsons-socket    # Socket-specific problems
make parsons-bytes     # Bytes/encoding problems

# === View Documents ===
make view-rosetta      # Side-by-side code comparisons
make view-misconceptions  # Common mistakes by background
make view-cheatsheet   # Python quick reference
make view-troubleshooting # Error solutions

# === Testing ===
make test              # Run all tests
make check             # Verify Python environment
make lint              # Check code style
```

---

## 📖 Key Documents

### For Language Transition
| Document | Purpose | Best For |
|----------|---------|----------|
| [ROSETTA_STONE.md](comparisons/ROSETTA_STONE.md) | Same algorithms in 5 languages | Visual comparison |
| [MISCONCEPTIONS_BY_BACKGROUND.md](comparisons/MISCONCEPTIONS_BY_BACKGROUND.md) | What trips up C/JS/Java/Kotlin programmers | Avoiding common errors |

### For Reference
| Document | Purpose | Best For |
|----------|---------|----------|
| [PYTHON_QUICK.md](cheatsheets/PYTHON_QUICK.md) | Sockets, struct, argparse cheatsheet | Quick lookup |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | 16 error scenarios with fixes | Problem solving |
| [PYTHON_NETWORKING_GUIDE.md](PYTHON_NETWORKING_GUIDE.md) | Complete 9-step learning guide | Deep understanding |

### For Practice
| Resource | Purpose | Best For |
|----------|---------|----------|
| [formative/quiz.yaml](formative/quiz.yaml) | 31 self-assessment questions | Testing knowledge |
| [formative/parsons/](formative/parsons/) | Code ordering exercises | Active learning |
| [examples/](examples/) | Working code with tests | Studying patterns |

---

## 🗺️ Lab Week Correspondence

| Week | Lab Topic | Guide Section | Key Python Concepts |
|:----:|-----------|---------------|---------------------|
| 1-2 | Network fundamentals | Rosetta Stone: TCP/UDP | socket basics |
| 3-4 | Sockets, Binary protocols | struct parsing | bytes, struct.pack/unpack |
| 5 | CLI, IP addressing | argparse | command-line interfaces |
| 6-10 | Application protocols | HTTP, JSON | requests, json module |
| 11-14 | Advanced topics | Concurrency, debugging | threading, logging |

---

## 🔍 Self-Assessment Checkpoints

Before each lab, verify you can answer:

### Before Week 1-2
- [ ] How do I create a TCP socket in Python?
- [ ] What is the difference between `str` and `bytes`?
- [ ] How do I send data through a socket?

### Before Week 3-4
- [ ] How do I pack an integer into network byte order?
- [ ] What does `struct.pack('!H', 8080)` return?
- [ ] How do I receive exactly N bytes from a socket?

### Before Week 5+
- [ ] How do I parse command-line arguments?
- [ ] How do I handle socket timeouts?
- [ ] How do I read and write JSON data?

---

## ❓ FAQ

**Q: Is this mandatory?**
A: No. You can complete labs without it, but it will save you time.

**Q: I know multiple languages. Which quiz should I take?**
A: Take the quiz for your most recent language, or use `make quiz-quick` for a general assessment.

**Q: How do I know if I am ready for labs?**
A: If you score 70%+ on the quiz and can answer the checkpoint questions, you are ready.

**Q: I got an error. What do I do?**
A: Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for 16 common scenarios with solutions.

**Q: The quiz says I need to review "bytes_and_strings". Where is that?**
A: See [PYTHON_NETWORKING_GUIDE.md Step 2](PYTHON_NETWORKING_GUIDE.md#step-2-data-types-for-networking) and [examples/02_bytes_vs_str.py](examples/02_bytes_vs_str.py).

---

## 📚 Additional Resources

- **Official Python Tutorial:** [docs.python.org/3/tutorial](https://docs.python.org/3/tutorial/)
- **Socket Programming HOWTO:** [docs.python.org/3/howto/sockets.html](https://docs.python.org/3/howto/sockets.html)
- **Real Python Networking:** [realpython.com/python-sockets](https://realpython.com/python-sockets/)

---

## 🆘 Getting Help

1. **Check Troubleshooting:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
2. **Search the error message:** Copy the exact text into a search engine
3. **Review relevant section:** Use the Navigation Index above
4. **Ask during lab hours:** Bring your code and the full error message

---

*Python Self-Study Guide — Computer Networks Course*
*ASE Bucharest, CSIE — ing. dr. Antonio Clim*
*Version 5.1 — January 2026*
