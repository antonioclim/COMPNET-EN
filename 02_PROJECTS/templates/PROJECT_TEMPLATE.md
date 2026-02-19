# Project XX: [PROJECT_TITLE]

> **Course:** Computer Networks  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Project type:** Main/Reserve

---

## 📋 Assessment and Delivery Guide

### ⚠️ IMPORTANT: Assessment with Physical Attendance

**Project assessment takes place EXCLUSIVELY at the faculty, with mandatory physical attendance.**

- The final presentation (Stage 4) takes place before the instructor/committee
- You must demonstrate understanding of the code and project architecture
- Questions about implementation and theoretical concepts may be asked
- Absence from presentation = project failure

**Common guides (read before starting):**
- [Pair Programming Guide](../docs/common/pair_programming_guide.md)
- [Code Quality Standards](../docs/common/code_quality_standards.md)
- [Git Workflow](../docs/common/git_workflow_detailed.md)
- [Troubleshooting](../docs/common/troubleshooting_common.md)

---

### 📅 Stage Calendar

| Stage | Week | Deadline | Deliverables | Score |
|-------|------|----------|--------------|-------|
| **E1** - Design | Week 5 | Week 5 (2026) | Specifications + Diagrams + Plan | 20% |
| **E2** - Prototype | Week 9 | Week 9 (2026) | Partial functional implementation | 25% |
| **E3** - Final | Week 13 | Week 13 (2026) | Complete version + Documentation | 35% |
| **E4** - Presentation | Week 14 | Week 14 (2026) | Live demo + Oral defence | 20% |

**Intermediate checks (optional, for feedback):** Weeks 3, 6, 8, 11

---

### 🐙 GitHub Publication

**MANDATORY:** The project must be published on GitHub before each stage.

#### Your Repository

```
https://github.com/[username]/retele-proiect-XX
```

#### Required Repository Structure

```
retele-proiect-XX/
├── README.md                    # Project description, run instructions
├── docs/
│   ├── specificatii.md          # [E1] Technical specifications
│   ├── diagrame/                # [E1] Architecture diagrams
│   ├── raport_progres.md        # [E2] Progress report
│   └── documentatie_finala.md   # [E3] Complete documentation
├── src/
│   ├── main.py                  # Entry point
│   ├── [module]/                # Core modules
│   └── utils/                   # Utilities
├── tests/
│   ├── test_smoke.py            # Smoke tests (MUST PASS)
│   ├── test_[module].py         # Unit tests
│   └── expected_outputs/        # Reference outputs
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── artifacts/
│   └── screenshots/
├── Makefile                     # Build automation
├── requirements.txt             # Python dependencies
├── MANIFEST.txt
├── CHANGELOG.md
└── .gitignore
```

#### What to Publish at Each Stage

| Stage | Mandatory Files/Folders on GitHub |
|-------|-----------------------------------|
| **E1** | `README.md`, `docs/specificatii.md`, `docs/diagrame/`, `.gitignore` |
| **E2** | + `src/` (partial functional code), `docker/`, `docs/raport_progres.md` |
| **E3** | + `tests/`, `artifacts/`, `docs/documentatie_finala.md`, `CHANGELOG.md` |
| **E4** | Complete repository + tag `v1.0-final` |

#### Git Commands for Each Stage

```bash
# Stage 1 - After preparing specifications
git add docs/ README.md .gitignore
git commit -m "E1: Initial specifications and design"
git push origin main

# Stage 2 - After implementing prototype
git add src/ docker/ docs/raport_progres.md
git commit -m "E2: Functional prototype"
git push origin main

# Stage 3 - Final version
git add tests/ artifacts/ docs/documentatie_finala.md CHANGELOG.md
git commit -m "E3: Complete final version"
git tag -a v1.0-final -m "Final project version"
git push origin main --tags

# Stage 4 - Final adjustments before presentation
git add .
git commit -m "E4: Presentation preparation"
git push origin main
```

---

### 📦 Archive Naming Convention

**Format:** `SURNAME_Firstname_GGGG_PXX_TT.zip`

| Field | Description | Example |
|-------|-------------|---------|
| SURNAME | Family name (UPPERCASE, no diacritics) | POPESCU |
| Firstname | First name (capitalised) | Ion |
| GGGG | Group number (4 digits) | 1098 |
| PXX | Project number | P01 |
| TT | Deliverable type (E1-E4 or SXX) | E1 |

**Examples:**
- `POPESCU_Ion_1098_PXX_E1.zip` — Stage 1
- `POPESCU_Ion_1098_PXX_E2.zip` — Stage 2

---

### 📊 Assessment Rubric

#### Stage 1 — Design (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete specifications | 30 | All requirements identified and documented |
| Architecture diagrams | 20 | Network topology, data flow, components |
| Implementation plan | 15 | Realistic timeline with milestones |
| Repository initialised | 15 | GitHub correctly configured |
| MANIFEST.txt correct | 10 | Valid signature |
| Archive naming | 10 | Follows convention |

#### Stage 2 — Prototype (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Partial functionality | 35 | Minimum 50% of functional requirements |
| Code quality | 25 | Clean, commented, structured |
| Environment configured | 15 | Docker/setup works, dependencies met |
| Progress report | 10 | Documents what is done and what remains |
| MANIFEST.txt | 10 | Valid signature |
| On-time delivery | 5 | Meets deadline |

#### Stage 3 — Final Version (100 points + 10 bonus)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Complete functionality | 40 | All requirements implemented |
| Final code quality | 20 | Production-ready code |
| Tests | 15 | Unit and integration tests |
| Documentation | 10 | Complete README, code comments |
| Comparative analysis | 5 | Comparison with alternatives |
| MANIFEST.txt | 10 | Valid signature |
| **Bonus extensions** | +10 | Additional features (teams of 3) |

#### Stage 4 — Presentation (100 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Live demo functional | 35 | Application runs and demonstrates requirements |
| Technical presentation | 25 | Explains architecture and decisions |
| Answers to questions | 20 | Demonstrates deep understanding |
| Team contribution | 15 | Each member knows all the code |
| Time management | 5 | 10-15 minutes per team |

---

### 👥 Team Size

| Team | Requirements |
|------|--------------|
| **1 person** | Basic complete functionality |
| **2 persons** | + Extended testing + Detailed documentation |
| **3 persons** | + Advanced extensions + Performance analysis |

---

## 📚 Project Description

[DETAILED_DESCRIPTION - minimum 150 words describing the project context, real-world relevance and technical scope]

### 🎯 Learning Objectives

By completing this project, you will be able to:

- **LO1:** [Bloom verb] [specific objective] [context]
- **LO2:** [Bloom verb] [specific objective] [context]
- **LO3:** [Bloom verb] [specific objective] [context]
- **LO4:** [Bloom verb] [specific objective] [context]
- **LO5:** [Bloom verb] [specific objective] [context]

### 🛠️ Technologies and Tools

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **[Tech1]** | [Purpose] | [URL] |
| **[Tech2]** | [Purpose] | [URL] |
| **Python 3** | Programming language | [python.org](https://python.org) |
| **Docker** | Container runtime | [docs.docker.com](https://docs.docker.com) |

### 📖 Key Concepts

| Concept | Description |
|---------|-------------|
| **[Concept1]** | [Brief definition] |
| **[Concept2]** | [Brief definition] |
| **[Concept3]** | [Brief definition] |

---

## ⛔ Constraints (MUST/MUST NOT)

### MUST (Mandatory)
- [ ] MUST use Python 3.10+ syntax
- [ ] MUST include type hints on ALL public functions
- [ ] MUST use subgoal labels for code sections
- [ ] MUST handle exceptions with specific types (not bare `except`)
- [ ] MUST log to both console AND file using `logging` module
- [ ] MUST pass all smoke tests before submission (`make smoke`)
- [ ] MUST follow code quality standards document

### MUST NOT (Forbidden)
- [ ] MUST NOT use `except Exception` or bare `except:` (too broad)
- [ ] MUST NOT hardcode IP addresses or ports (use config file)
- [ ] MUST NOT use `print()` for logging (use `logging` module)
- [ ] MUST NOT submit without running `make lint`
- [ ] MUST NOT leave debug code or commented-out code
- [ ] MUST NOT use deprecated APIs

### SHOULD (Recommended)
- [ ] SHOULD include unit tests for core functions
- [ ] SHOULD document edge cases in docstrings
- [ ] SHOULD use context managers for resources
- [ ] SHOULD use type aliases for complex types

---

## 🎯 Concept Analogies

### [Main Concept] = [Real-World Analogy]

🏠 **Real-World Analogy:**  
[Detailed description of real-world scenario that maps to the technical concept]

🖼️ **Visual Representation:**
```
[ASCII art or diagram showing the concept]
```

💻 **Technical Mapping:**
- [Real-world element 1] = [Technical element 1]
- [Real-world element 2] = [Technical element 2]
- [Real-world element 3] = [Technical element 3]

⚠️ **Where the analogy breaks:**  
[Limitations of the analogy - what doesn't map correctly]

---

### [Secondary Concept] = [Real-World Analogy 2]

🏠 **Real-World Analogy:**  
[Description]

💻 **Technical Mapping:**
- [Mapping points]

---

## 🗳️ Peer Instruction Questions

Use these questions for collaborative learning. Follow the protocol:
1. Read individually (1 min)
2. Vote your answer (30 sec)
3. Discuss with neighbour (2 min)
4. Re-vote (30 sec)
5. Instructor explains (2 min)

### Question 1: [Title]

> 💭 **PREDICTION:** Before reading the options, think: [prediction question]

**Scenario:** [Specific technical scenario]

**Question:** [Clear question]

**Options:**
- A) [Option A]
- B) [Option B] ✓
- C) [Option C]
- D) [Option D]

**Correct answer:** B

**Explanation:** [Detailed explanation of why B is correct and others are wrong]

**Misconception targeted:** [What common mistake this question addresses]

---

### Question 2: [Title]

> 💭 **PREDICTION:** [Prediction prompt]

**Scenario:** [Context]

**Question:** [Question]

**Options:**
- A) [Option]
- B) [Option]
- C) [Option] ✓
- D) [Option]

**Correct answer:** C

**Explanation:** [Explanation]

**Misconception targeted:** [Misconception]

---

### Question 3: [Title]

[Same structure as above]

---

### Question 4: [Title]

[Same structure as above]

---

## ❌ Common Misconceptions

### 🚫 "[Common false belief 1]"

**WRONG:** [Why this belief is incorrect]

**CORRECT:** [The accurate understanding]

**Evidence:** [How to verify/demonstrate the correct answer]

---

### 🚫 "[Common false belief 2]"

**WRONG:** [Explanation]

**CORRECT:** [Truth]

**Evidence:** [Proof]

---

### 🚫 "[Common false belief 3]"

**WRONG:** [Explanation]

**CORRECT:** [Truth]

**Evidence:** [Proof]

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **[Term 1]** | [Clear, concise definition] |
| **[Term 2]** | [Definition] |
| **[Term 3]** | [Definition] |
| **[Term 4]** | [Definition] |
| **[Term 5]** | [Definition] |
| **[Term 6]** | [Definition] |
| **[Term 7]** | [Definition] |
| **[Term 8]** | [Definition] |

---

## 🔨 Implementation Stages

### Stage 1 (Week 5) — Design

**Tasks:**
1. Define system architecture and components
2. Create network topology diagram
3. Document all requirements and constraints
4. Plan implementation timeline

**Deliverables:**
- `docs/specificatii.md` — Technical specifications
- `docs/diagrame/` — Architecture diagrams
- `README.md` — Project overview

---

### Stage 2 (Week 9) — Prototype

**Tasks:**
1. Implement core functionality (minimum 50%)
2. Set up Docker environment
3. Create basic tests
4. Document progress

**Code Example:**

```python
#!/usr/bin/env python3
"""
[Module description]
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import logging
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_PORT = 8080
BUFFER_SIZE = 4096

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def process_request(data: bytes) -> Optional[bytes]:
    """
    Process incoming request data.
    
    Args:
        data: Raw bytes from client
        
    Returns:
        Response bytes or None if invalid
        
    # 💭 PREDICTION: What happens if data is empty?
    # Answer: Returns None (invalid request)
    """
    if not data:
        return None
    # TODO: Implement processing logic
    return data
```

**Deliverables:**
- `src/` — Partial functional code
- `docker/` — Docker configuration
- `docs/raport_progres.md` — Progress report

---

### Stage 3 (Week 13) — Final Version

**Tasks:**
1. Complete all functionality
2. Add complete error handling
3. Create full test suite
4. Write final documentation
5. Performance analysis

**Deliverables:**
- Complete source code
- Test suite with >80% coverage
- Final documentation
- Comparative analysis

---

### Stage 4 (Week 14) — Presentation

**Demo checklist:**
```
□ Environment starts correctly
□ Core functionality demonstrated
□ Error handling shown
□ Logs visible and meaningful
□ Tests pass live
```

**Presentation structure:**
1. Introduction (2 min)
2. Architecture explanation (3 min)
3. Live demo (5 min)
4. Challenges and solutions (2 min)
5. Q&A (3 min)

---

## 📋 Expected Outputs

### Scenario 1: Normal Operation

**Input:**
```bash
python src/main.py --config config.yaml
```

**Expected stdout:**
```
[INFO] Loading configuration from config.yaml
[INFO] Starting service on 0.0.0.0:8080
[INFO] Service ready. Press Ctrl+C to stop.
```

**Expected exit code:** 0

---

### Scenario 2: Missing Configuration

**Input:**
```bash
python src/main.py --config nonexistent.yaml
```

**Expected stderr:**
```
[ERROR] Configuration file not found: nonexistent.yaml
[ERROR] Usage: python src/main.py --config <path>
```

**Expected exit code:** 1

---

### Scenario 3: Port Already in Use

**Input:**
```bash
python src/main.py  # when port is busy
```

**Expected stderr:**
```
[ERROR] Port 8080 is already in use
[ERROR] Try: lsof -i :8080 to find the process
```

**Expected exit code:** 2

---

## ❓ Frequently Asked Questions

**Q: How do I start the development environment?**

A: Use the provided Makefile:
```bash
make install    # Install dependencies
make run        # Start application
```

**Q: How do I run the tests?**

A: Run smoke tests first, then full suite:
```bash
make smoke      # Quick validation
make test       # Full test suite
```

**Q: What if Docker containers won't start?**

A: Check the troubleshooting guide and verify:
```bash
docker-compose logs -f [service]
docker ps -a
```

**Q: How do I verify my code quality before submission?**

A: Run the linter and tests:
```bash
make lint       # Check code style
make smoke      # Verify basic functionality
```

**Q: Where can I find help?**

A: Check these resources in order:
1. [Troubleshooting Guide](../docs/common/troubleshooting_common.md)
2. Laboratory materials from netENwsl
3. Course forum
4. Instructor office hours

---

## 🔗 JavaScript → Python Bridge

For students with Web Technologies background:

| JavaScript (TW) | Python (Networks) | Notes |
|-----------------|-------------------|-------|
| `const fn = (x) => x * 2` | `fn = lambda x: x * 2` | Arrow functions → lambda |
| `arr.map(x => x * 2)` | `[x * 2 for x in arr]` | List comprehension |
| `arr.filter(x => x > 0)` | `[x for x in arr if x > 0]` | Filter in comprehension |
| `JSON.parse(str)` | `json.loads(str)` | Parse JSON |
| `async/await` | `async/await` with `asyncio` | Similar syntax |
| `try { } catch (e) { }` | `try: ... except Exception as e:` | Exception handling |

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| [N] | `[NN]enWSL/` | [Topic] |
| [N] | `[NN]enWSL/` | [Topic] |
| [N] | `[NN]enWSL/` | [Topic] |

---

## 📚 Bibliography

> ⚠️ **IMPORTANT:** Use ONLY verified sources. Do NOT invent references!

### Primary Sources (Mandatory)
1. **[OFFICIAL]** [Technology] Documentation  
   URL: [verified URL]  
   Verified: 2026-01-24 ✓

2. **[OFFICIAL]** [Framework] Guide  
   URL: [verified URL]  
   Verified: 2026-01-24 ✓

3. **[ACADEMIC]** [Author] ([Year]). [Title].  
   DOI: [DOI if available]  
   Verified in Google Scholar ✓

### Secondary Sources (Optional)
4. **[TUTORIAL]** [Tutorial name]  
   URL: [URL]

### ❌ Sources to AVOID
- Wikipedia (may be inaccurate)
- Random blog posts without verification
- AI-generated content without validation

---

## 📝 Final Notes

- **Always verify** that the GitHub repository is updated before deadlines
- **Test** the application on a clean machine before presentation
- **Prepare** answers for questions about architecture and code
- **Communicate** with team members to coordinate contributions
- **Review** the [Presentation Guide](../docs/common/presentation_guide.md) before E4

---

*Last update: January 2026*  
*Computer Networks — ASE Bucharest*
