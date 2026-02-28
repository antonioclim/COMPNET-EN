# Computer Networks Teaching Materials at Top Universities
## A Comparative Analysis — Second Edition

---

<div align="center">

**Comparative Study: Computer Networks Curricula**  
*Top 50 QS/THE/ARWU Faculties vs. the COMPNET-EN / ASE-CSIE Course Kit*

---

*"If you want to truly learn something, try teaching it."*  
— Richard Feynman (probably over coffee, much like us)

</div>

---

## Disclaimer and Conflict of Interest

This report was written by one of the authors of the COMPNET-EN materials. The conflict of interest is therefore structural, not incidental, and no amount of careful phrasing eliminates it. What can be done — and what this second edition attempts more rigorously than the first — is to ground every claim in publicly verifiable artefacts: URLs, file counts, commit histories, and published papers. Where a claim cannot be independently verified, it is marked as such.

The reader who wants to check the data should start at `https://github.com/antonioclim/COMPNET-EN` (the kit under evaluation), then visit the repositories and course pages listed in Section 2. Every factual assertion in this document is intended to be falsifiable against those sources.

In other words: the bias is disclosed, the evidence is public, and the invitation to disagree is genuine.

---

## 1. Introduction and Methodology

### 1.1. Research Context and Motivation for a Second Edition

The first edition of this report (January 2025, v1.0) compared an earlier version of the CLIM&TOMA/ASE-CSIE laboratory kit against publicly available networking curricula from approximately 20 institutions. Since that comparison, the kit has undergone substantial refactoring: it was forked from a joint backbone repository (`compnet-2025-redo-main`), expanded from 501 files to 1 249 files, reorganised into a modular structure with CI/CD quality assurance, and published as `COMPNET-EN` at `github.com/antonioclim/COMPNET-EN` (version v13.05.00, February 2026).

The changes are not cosmetic. The first edition evaluated a kit that lacked, among other things, a unified lab execution framework, automated integrity checks, Docker Compose coherence validation, a structured project catalogue with assessment gates, instructor notes with environment-specific variants, or a CI pipeline. The current kit has all of these. A fresh comparison is therefore warranted — not because the previous conclusions were wrong, but because the object of comparison has changed materially.

This second edition also attempts to correct a methodological weakness of the first: it now distinguishes more carefully between *what a course publicly exposes* and *what a course actually contains*. Many elite programmes keep their best materials behind institutional authentication. The absence of a feature from a public repository does not prove the feature does not exist — it proves only that we cannot verify it.

### 1.2. Scope and Methodology

We examined **17 networking courses** from institutions ranked in the QS World University Rankings, Times Higher Education, and ARWU top 50 for Computer Science. The analysis is restricted to materials that are **publicly accessible** as of February 2026 — GitHub repositories, course websites, open educational platforms, and published papers. No materials behind login walls (Canvas, Moodle, Courseworks) were included.

**Reproducibility note:** Every URL cited in this report was accessed between 25 and 28 February 2026. The reader can verify all claims by visiting the cited sources. Where a repository has a commit history, the relevant commit date is noted. Where a course website may have changed since our access, the limitation is acknowledged.

**Evaluation criteria (unchanged from v1.0, extended with C8–C10):**

| Code | Dimension | Description |
|:---:|:-----------|:----------|
| **C1** | Comprehensiveness | Number of weeks, topic coverage breadth |
| **C2** | Code Quality | Linting, type hints, coding standards, sanitisers |
| **C3** | Pedagogical Sophistication | Evidence-based methods, formative assessment, documented scaffolding |
| **C4** | Infrastructure | Docker, virtualisation, execution frameworks, environment verification |
| **C5** | Documentation | README depth, guides, cheatsheets, glossaries, instructor notes |
| **C6** | Projects | Variety, depth, scale, assessment structure |
| **C7** | Interactive Elements | HTML presentations, embedded quizzes, self-paced materials |
| **C8** | Quality Assurance | CI/CD pipelines, automated checks, integrity validation |
| **C9** | Academic Validation | Peer-reviewed publications, documented adoption, conference presentations |
| **C10** | Licensing and Reuse | Licence type, community contribution potential, ecosystem maturity |

The addition of C8–C10 reflects a hard lesson learnt from the first edition: a good kit that nobody can verify, cite, or adapt has limited impact beyond its home institution.

### 1.3. A Note on Fairness

It would be dishonest to pretend that a course kit developed at ASE-CSIE Bucharest competes on equal footing with programmes backed by Stanford's endowment, ETH Zürich's research infrastructure, or CMU's decades of systems-programming tradition. The comparison is not "who is better" — it is "what does each approach offer, what are the trade-offs, and what can be learnt from the differences." Where the reference project is weaker, this report says so.

---

## 2. The Academic Landscape: What Is Publicly Available

### 2.1. Institutions and Courses Analysed

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GEOGRAPHY OF ANALYSED COURSES                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   🇺🇸 USA                           🇪🇺 Europe                              │
│   ├── Stanford CS144               ├── ETH Zürich (227-0120-00L)           │
│   ├── UC Berkeley CS168            ├── UCLouvain CNP3                      │
│   ├── CMU 15-441/641               ├── TU München (ACN)                    │
│   ├── MIT 6.5820                   ├── Imperial College London             │
│   ├── Princeton COS 461            └── Roma Tre / Kathará                  │
│   ├── U. Michigan EECS 489                                                 │
│   ├── UIUC ECE 438                 🇦🇸 Asia-Pacific                        │
│   ├── Georgia Tech CS 6250         ├── KAIST CS341                         │
│   ├── Johns Hopkins EN.601.414     ├── NUS CS2105                          │
│   └── NPS Labtainers               └── CUHK CSCI 4430                     │
│                                                                             │
│   🇷🇴 Romania                                                               │
│   └── ASE-CSIE (COMPNET-EN)                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2. The Visibility Problem

A fundamental constraint of any analysis based on publicly available materials is that *absence of evidence is not evidence of absence*. Several institutions keep their most valuable teaching artefacts behind authentication barriers. This matters because any comparison that ignores this asymmetry will systematically overrate courses that happen to be transparent and underrate those that are not.

The following table documents what we could and could not access:

| University | Course | Public Repository | Materials Inspectable | Last Verified Update |
|:-----------|:-------|:------------------|:---------------------:|:-------------------:|
| 🇺🇸 Stanford | CS144 | `cs144.github.io`, GitHub org | ✅ Full | Dec 2025 |
| 🇺🇸 CMU | 15-441/641 | `computer-networks` GitHub org (23 repos) | ✅ Mostly | Sep 2025 |
| 🇺🇸 MIT | 6.5820 | OCW only | ❌ Stale (2002 on OCW) | N/A |
| 🇺🇸 Berkeley | CS168 | `textbook.cs168.io`, `berkeley-cs168` org | ✅ Full | Feb 2026 |
| 🇺🇸 Princeton | COS 461 | `PrincetonUniversity/COS461-Public` | ⚠️ Partial (Feamster era, ~2020) | ~2020 |
| 🇺🇸 Georgia Tech | CS 6250 | Student repos only; Canvas | ⚠️ Syllabus only (2023 PDF) | 2023 |
| 🇺🇸 UIUC | ECE 438 | GitHub Pages site | ⚠️ Limited | Feb 2026 |
| 🇺🇸 Michigan | EECS 489 | `mosharaf/eecs489` (267 ⭐) | ✅ Full | Fall 2025 |
| 🇺🇸 Johns Hopkins | EN.601.414 | `xinjin/course-net` (63 ⭐) | ✅ Full (but stale) | Spring 2019 |
| 🇺🇸 NPS | Labtainers | `mfthomps/Labtainers`, NPS website | ✅ Full | Jan 2026 |
| 🇨🇭 ETH Zürich | 227-0120-00L | `nsg-ethz/mini_internet_project` | ✅ Mostly | Dec 2025 |
| 🇧🇪 UCLouvain | CNP3 | `cnp3` GitHub org (ebook, IPMininet, INGInious) | ✅ Full | Active 2026 |
| 🇬🇧 Imperial College | Networks | None found | ❌ Not public | N/A |
| 🇩🇪 TU München | ACN | SSH-auth Git, Moodle | ❌ Behind auth | WS 25/26 |
| 🇰🇷 KAIST | CS341 | `ANLAB-KAIST/KENSv3` (151 ⭐) | ✅ Full | Mar 2025 |
| 🇸🇬 NUS | CS2105 | Archival blog post (2014) | ⚠️ Archival | 2014 |
| 🇭🇰 CUHK | CSCI 4430 | `henryhxu/CSCI4430` (54 ⭐, 863 commits) | ✅ Full | Fall 2025 |
| 🇷🇴 ASE-CSIE | COMPNET-EN | `antonioclim/COMPNET-EN` | ✅ Full | Feb 2026 |

**Observation.** Of the 17 external courses examined, only roughly half (9–10) offer substantial publicly inspectable materials. MIT 6.5820 — often cited as a benchmark — has no current public materials beyond OCW archives from over two decades ago. Imperial College London has no publicly accessible networking course materials whatsoever. TU München distributes via SSH-authenticated Git and Moodle. These are not lesser courses; they are simply courses whose quality we cannot independently evaluate.

This means the comparison that follows is inherently biased towards courses that *choose transparency*. The reader should weight conclusions accordingly.

### 2.3. Main Feature Comparison

> **Legend:** ✅ Present and verifiable | ⚠️ Partial or community-maintained | ❌ Absent or not publicly verifiable

| University | Course | Weeks | Docker (official) | Interactive Slides | Explicit Pedagogy | Projects | Auto-test | CI/CD | Peer-Reviewed |
|:-----------|:-------|:-----:|:------------------:|:------------------:|:-----------------:|:--------:|:---------:|:-----:|:-------------:|
| 🇷🇴 **ASE-CSIE** | **COMPNET-EN** | **14** | **✅ 18 Compose labs** | **✅ 101 HTML** | **✅ documented** | **25 briefs** | **✅** | **✅** | ❌ |
| 🇺🇸 Stanford | CS144 | 10 | ❌ (VM image) | ❌ PDF | ⚠️ Lab hints | 8 checkpoints | ✅ CMake | ❌ | ⚠️ |
| 🇨🇭 ETH Zürich | Comm. Net. | 15 | ✅ (mini-Internet) | ❌ | ❌ | 1 large group | ✅ connectivity | ❌ | ✅ SIGCOMM'20 |
| 🇺🇸 CMU | 15-441/641 | ~14 | ✅ (partial) | ❌ | ❌ | 3 multi-week | ✅ Gradescope | ❌ | ⚠️ |
| 🇺🇸 Berkeley | CS168 | 17 | ❌ | ⚠️ Google Slides | ❌ | 3 projects | ✅ | ❌ | ❌ |
| 🇺🇸 Michigan | EECS 489 | 14–15 | ⚠️ | ❌ PDF slides | ⚠️ Quizzes | 4 assignments | ✅ | ❌ | ❌ |
| 🇺🇸 Princeton | COS 461 | 12 | ⚠️ (VM) | ❌ Flipped video | ❌ | 5 labs | ✅ | ❌ | ❌ |
| 🇰🇷 KAIST | CS341 | 16 | ✅ Dockerfile | ❌ | ✅ PCAP/Wireshark | 4 TCP impl. | ✅ gtest | ✅ 4 workflows | ✅ SIGCSE'15 |
| 🇧🇪 UCLouvain | CNP3 | Var. | ✅ (ebook build) | ✅ Sphinx ebook | ✅ INGInious | Multiple | ✅ INGInious | ✅ Travis CI | ✅ multiple |
| 🇺🇸 NPS | Labtainers | Modular | ✅ (core tech) | ❌ PDF manuals | ✅ individualised | 50+ labs | ✅ gradelab | regression | ✅ IEEE S&P'18 |
| 🇺🇸 Georgia Tech | CS 6250 | ~16 | ❌ (VM) | ❌ | ⚠️ 12 quizzes | 7 assignments | ✅ Gradescope | ❌ | ❌ |
| 🇭🇰 CUHK | CSCI 4430 | 13 | ⚠️ | ❌ | ❌ | 2 projects | ✅ | ❌ | ❌ |

---

## 3. Detailed Analysis by Dimension

### 3.1. Dimension C1: Comprehensiveness and Topic Coverage

```
Number of Course Weeks

Berkeley CS168     ████████████████████████████████░░  17 weeks
KAIST CS341        ███████████████████████████████░░░  16 weeks
Georgia Tech 6250  ███████████████████████████████░░░  ~16 weeks
ETH Zürich         █████████████████████████████░░░░░  15 weeks
Michigan EECS 489  ████████████████████████████░░░░░░  14–15 weeks
COMPNET-EN         ███████████████████████████░░░░░░░  14 weeks  ◄── Reference
CMU 15-441         ███████████████████████████░░░░░░░  ~14 weeks
CUHK CSCI 4430     ██████████████████████████░░░░░░░░  13 weeks
Princeton COS 461  ███████████████████████░░░░░░░░░░░  12 weeks
Stanford CS144     ████████████████████░░░░░░░░░░░░░░  10 weeks (quarter)
```

Topic coverage reveals a more interesting picture than raw week counts. The following table marks topics based on verifiable presence in publicly accessible materials (syllabi, assignments, code):

| Topic | Stanford | ETH | CMU | Berkeley | Michigan | UCLouvain | KAIST | COMPNET-EN |
|:------|:--------:|:---:|:---:|:--------:|:--------:|:---------:|:-----:|:----------:|
| TCP/IP Fundamentals | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Socket Programming | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| HTTP/REST | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| DNS Deep Dive | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Routing (OSPF, BGP) | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ❌ | ✅ |
| SDN/OpenFlow | ❌ | ⚠️ | ❌ | ✅ | ✅ | ⚠️ | ❌ | ✅ |
| Load Balancing | ❌ | ⚠️ | ✅ | ✅ | ⚠️ | ❌ | ❌ | ✅ |
| IoT/MQTT | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| gRPC/Modern RPC | ❌ | ❌ | ❌ | ⚠️ | ⚠️ | ❌ | ❌ | ✅ |
| Security (TLS, VPN) | ⚠️ | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ❌ | ✅ |
| Email Protocols | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| FTP | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |

**Observation.** COMPNET-EN covers the broadest range of application-layer protocols among the courses examined. IoT/MQTT and gRPC appear in none of the other 17 courses. Email protocols (SMTP/POP3/IMAP) appear only in UCLouvain's textbook. This breadth comes at a cost: where Stanford allocates 3–4 weeks to incrementally building a TCP implementation, COMPNET-EN necessarily treats each topic at lesser depth. The trade-off is real, and whether breadth or depth is preferable depends on the programme's objectives.

### 3.2. Dimension C2: Code Quality

Stanford CS144 remains the benchmark. The Minnow codebase enforces `.clang-format` and `.clang-tidy`, references the C++ Core Guidelines, uses AddressSanitiser and UndefinedBehaviorSanitiser via CMake, and includes explicit coding-style documentation. Students write modern C++20 against a well-defined API.

CMU 15-441 provides a custom Wireshark dissector plugin (`tcp.lua`) for decoding student protocol headers — an investment in tooling that directly serves the pedagogical objective of protocol-level reasoning.

KAIST KENSv3 uses `clang-format` and compiles with Google Test, supporting reproducible C++ builds across Linux, WSL, and macOS via 4 GitHub Actions workflows.

COMPNET-EN uses Python throughout, with type hints (partial coverage), docstrings, and a modular structure. The kit includes a `ruff.toml` configuration in the Python self-study guide. However, no strict linting gate exists in the CI pipeline for Python code — the CI checks Markdown links, lexical integrity, figure targets, and executable permissions, but not code style enforcement.

> *Self-criticism:* Stanford and KAIST taught us — again — that automated code quality gates belong in CI, not in aspirational documentation. This remains an open item.

### 3.3. Dimension C3: Pedagogical Sophistication

This dimension is where the differences between courses are most pronounced and also hardest to evaluate fairly, because pedagogical design is precisely the kind of thing that often lives behind LMS walls rather than on GitHub.

**What COMPNET-EN makes publicly visible:**

The kit documents a teaching loop — model → observation → explanation → transfer — and provides artefacts that embody it: 39 runnable micro-scenarios embedded in lecture directories (so students observe before they theorise), documented misconception lists organised by programming background (C/C++, JavaScript, Java/Kotlin), Parsons problems for socket programming and byte handling, and a 2 222-line Python self-study guide with Rosetta Stone cross-language comparisons. The guide includes 13 annotated examples, 31 formative quiz questions, and language-specific cheatsheets. There are 14 weekly multiple-choice quiz banks and a subnetting quiz generator.

None of these elements are revolutionary individually. What is unusual is their *co-presence in a single, publicly inspectable repository*. Most courses that employ these techniques do so in internal LMS modules that cannot be verified externally.

**What elite courses do differently (and sometimes better):**

UCLouvain's **INGInious platform** represents the most sophisticated publicly accessible auto-graded formative assessment in networking education. Students analyse real PCAP files converted to PDML, fill in hidden TCP header fields (sequence numbers, ACK flags, window sizes), and receive per-field automated feedback. The platform also supports C socket programming exercises with automated testing. It has been running since approximately 2014, is backed by published research, and is used at multiple European institutions.

NPS **Labtainers** implements per-student parameterisation: exercise parameters are generated from keyed hashes tied to student email addresses, so each student gets unique network configurations, discouraging solution-sharing. This was published at IEEE Security & Privacy 2018 and demonstrated at SIGCSE 2021.

Georgia Tech **CS 6250** administers 12 weekly quizzes (10% of grade) via Honorlock, making it one of the most aggressively quiz-oriented courses in the sample — though none of the quiz content is publicly accessible.

TU München reportedly uses a two-pass exercise correction model (submit → discuss → self-correct → resubmit) and gamified hacking challenges with automated token verification. We cannot verify this from public sources, but it was described in course documentation fragments accessible via search engines.

```
┌──────────────────────────────────────────────────────────────────────────┐
│              EVIDENCE-BASED PEDAGOGICAL ELEMENTS                         │
│              (publicly verifiable instances only)                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Element                        Present in public course materials?      │
│  ───────────────────────────────────────────────────────────────────     │
│                                                                          │
│  Documented Misconceptions      COMPNET-EN ✅ | Rest ❌                  │
│  (per topic, by background)                                              │
│                                                                          │
│  Parsons Problems               COMPNET-EN ✅ | Rest ❌                  │
│  (code arrangement exercises)                                            │
│                                                                          │
│  Cross-Language Rosetta Stone   COMPNET-EN ✅ | Rest ❌                  │
│                                                                          │
│  PCAP-Based Auto-Grading        UCLouvain ✅ | COMPNET-EN ⚠️ | Rest ❌  │
│  (automated field validation)                                            │
│                                                                          │
│  Per-Student Parameterisation   NPS Labtainers ✅ | Rest ❌              │
│  (keyed hash individualisation)                                          │
│                                                                          │
│  Code Tracing Exercises         COMPNET-EN ✅ | KAIST ⚠️ | Rest ❌      │
│  (step-by-step execution)                                                │
│                                                                          │
│  Instructor Notes per Session   COMPNET-EN ✅ | NPS ✅ | Rest ❌         │
│  (with environment variants)                                             │
│                                                                          │
│  Weekly Formative Quiz Banks    COMPNET-EN ✅ | GA Tech ✅* | Rest ❌    │
│  (* behind Canvas)                                                       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Important caveat.** The near-total absence of explicit pedagogical elements from elite public repositories should not be interpreted as evidence that those courses lack pedagogy. It is far more likely that such elements exist within institutional LMS platforms. What can be said is that COMPNET-EN is unusual in making its pedagogical scaffolding *externally verifiable*.

### 3.4. Dimension C4: Docker Infrastructure and Execution Frameworks

This is the dimension where the reference project has changed most dramatically since the first edition.

**COMPNET-EN now provides:**
- 20 Dockerfiles and 28 YAML configuration files across the repository
- 18 registered Docker Compose labs in a unified `lab_runner` framework (`00_TOOLS/lab_runner/labs.json`), each with named variants (e.g. `c13-iot-basic` has `cli`, `default`, `tls`, `tls+cli` variants)
- Portainer CE integration guides per seminar (weeks 8–13), with both shell and PowerShell init scripts
- Docker Compose coherence validation in the QA audit: `depends_on: service_healthy` sanity checks, Python-image dependency risk scanning, YAML parse validation
- An environment verification script (`00_TOOLS/Prerequisites/verify_lab_environment.sh`)

```
                        INFRASTRUCTURE MATURITY (Feb 2026)

          Nothing   Basic VM    Mininet    Docker    Full Stack
            │         │          │          │           │
Stanford ───┼─────────┼──────────┼────⚫─────┼───────────┤  (VM image, no Docker)
            │         │          │          │           │
ETH Zürich ─┼─────────┼──────────┼──────────┼─────────⚫─┤  (mini-Internet in Docker)
            │         │          │          │           │
CMU ────────┼─────────┼──────────┼──────────┼────⚫──────┤  (Docker for some projects)
            │         │          │          │           │
COMPNET-EN ─┼─────────┼──────────┼──────────┼────────⚫──┤  (18 Compose + lab_runner)
            │         │          │          │           │
NPS ────────┼─────────┼──────────┼──────────┼─────────⚫─┤  (50+ containerised labs)
            │         │          │          │           │
KAIST ──────┼─────────┼──────────┼──────────┼───⚫───────┤  (Dockerfile, CI builds)
            │         │          │          │           │
UCLouvain ──┼─────────┼──────────┼────⚫─────┼───────────┤  (Kathará/IPMininet focus)
            │         │          │          │           │
GA Tech ────┼─────────┼────⚫─────┼──────────┼───────────┤  (VirtualBox VMs)
            │         │          │          │           │
```

**ETH Zürich's mini-Internet project** remains the most ambitious containerised networking infrastructure in academia. Published at SIGCOMM Education Workshop 2020 and presented at NANOG 78, it runs each autonomous system in its own Docker container with real FRRouting for BGP/OSPF, supports MPLS and RPKI, and requires the entire class to cooperate for end-to-end connectivity. However, it is a *single multi-week project*, not a semester-spanning lab framework.

**NPS Labtainers** is the closest structural parallel to COMPNET-EN's Docker philosophy: every lab is containerised, distributed via Docker Hub, and operated through a unified CLI. It offers over 50 labs covering networking and security. However, Labtainers is a *lab framework*, not a complete course kit with integrated lectures, quizzes, projects, and instructor notes.

**COMPNET-EN's 18 Docker Compose labs spanning the full 14-week semester, with a unified `lab_runner` and Portainer integration, is — to the best of our knowledge and based on publicly verifiable evidence — unmatched among semester-long undergraduate networking courses.** The external frameworks that come closest — Kathará (Roma Tre / Télécom Paris, used at KTH, UCLouvain) and Containerlab — are standalone tools, not integrated course kits.

### 3.5. Dimension C5: Documentation

The quantitative inventory of COMPNET-EN is straightforward to verify:

| Artefact Type | Count | Verification |
|:--------------|------:|:-------------|
| Markdown files | 391 | `find . -name "*.md" \| wc -l` |
| PlantUML diagram sources | 386 | `find . -name "*.puml" \| wc -l` |
| Python scripts | 154 | `find . -name "*.py" \| wc -l` |
| HTML support files | 101 | `find . -name "*.html" \| wc -l` |
| Shell scripts | 55 | `find . -name "*.sh" \| wc -l` |
| Docker YAML configs | 28 | `find . -name "*.yml" -o -name "*.yaml" \| wc -l` |
| Dockerfiles | 20 | `find . -name "*Dockerfile*" \| wc -l` |
| **Total files** | **1 249** | QA audit report |

Comparative documentation features:

| Element | Stanford | Berkeley | CMU | UCLouvain | NPS | COMPNET-EN |
|:--------|:--------:|:--------:|:---:|:---------:|:---:|:----------:|
| Comprehensive README | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Troubleshooting Guide | ⚠️ (FAQ) | ⚠️ | ❌ | ✅ | ✅ | ✅ |
| Instructor Guide/Notes | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ (per seminar, ±Mininet) |
| Glossary | ❌ | ✅* | ❌ | ✅* | ❌ | ✅ |
| PlantUML Diagram-as-Code | ❌ | ❌ | ❌ | ⚠️ (Tikz/mscgen) | ❌ | ✅ (386 sources) |
| Environment Verification | ⚠️ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Sparse Checkout Guidance | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| QA Audit Report | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Python Self-Study Bridge | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (2 222 lines) |

*\* Within the textbook*

The **PlantUML toolchain** with 386 source diagrams is unique among all courses examined. No other course publicly maintains a diagram-as-code infrastructure of comparable scope. The pedagogical value is reproducibility: any diagram can be regenerated, diffed, and version-controlled. The practical cost is the Java dependency for rendering.

**Berkeley CS168's open textbook** (`textbook.cs168.io`) remains, in our judgement, the single most valuable open-access networking reference for self-learners. It is professionally edited, free under CC BY-SA 4.0, and covers 17 weeks of material. COMPNET-EN does not have an equivalent companion textbook, and this is a genuine gap.

### 3.6. Dimension C6: Projects

This is the dimension where elite programmes most clearly surpass COMPNET-EN in *depth per project*, while COMPNET-EN leads in *breadth of project catalogue*.

**Stanford CS144** asks students to build a complete TCP/IP stack across 8 incremental checkpoints in modern C++: ByteStream → Reassembler → TCPReceiver → TCPSender → NetworkInterface → Router. The code quality bar is enforced by clang-format, clang-tidy, and sanitisers. The narrative coherence — each checkpoint building on the previous one, culminating in real end-to-end connectivity — is pedagogically exemplary.

**CMU 15-441** assigns three multi-week paired projects: (1) a privacy-preserving mix network with STP and routing (Mixnet), (2) a full TCP implementation over UDP with Reno congestion control tested on AWS EC2, and (3) an HTTP/1.1 server with adaptive bitrate video streaming. CMU provides a custom Wireshark dissector (`tcp.lua`) for decoding student protocol headers.

**ETH Zürich's mini-Internet** requires class-wide cooperation: each group operates an AS, collectively building Internet-wide BGP connectivity. Published at SIGCOMM'20.

**KAIST KENSv3** is a custom network simulation framework (comparable to ns-2) where students implement TCP from system calls through handshaking, flow control, and congestion control. Google Test integration and automatic PCAP recording of all packets for Wireshark analysis.

**COMPNET-EN** offers **25 project briefs** organised in two groups:
- Group 1 (S01–S15): Network applications — TCP chat, FTP, HTTP server, HTTP proxy, load balancer, pub-sub broker, DNS resolver, email system, TCP tunnel, file sync, REST microservices, TLS messaging, gRPC service, distance-vector routing in Mininet, IoT gateway.
- Group 2 (A01–A10): Administration and security — SDN firewall, IDS, PCAP report generator, ARP spoofing detection, port scanning, NAT/DHCP lab, SDN learning switch, VXLAN tunnelling, SDN IPS, network hardening.

Each brief includes E1/E2/E3 assessment gates, PCAP validation rules (`tools/pcap_rules/*.json`), and a mandatory multi-language "Flex component" (interoperability proof in a language other than Python). Project-seminar mappings are documented in `COURSE_SEMINAR_MAPPING.md`.

```
Project Catalogue Scale (number of distinct briefs/labs)

NPS Labtainers      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  50+ labs
                    (modular, security focus)

COMPNET-EN          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  25 briefs
                    (application + security, E1/E2/E3 gates)

Stanford CS144      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                  8 checkpoints
                    (deep TCP/IP stack build)

GA Tech CS 6250     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓                    7 assignments
                    (BGP, SDN, Mininet focus)

KAIST KENSv3        ▓▓▓▓▓▓▓▓                          4 TCP implementations
                    (deep systems work)

CMU 15-441          ▓▓▓▓▓▓                            3 large multi-week
                    (Mixnet, TCP, HTTP+video)
```

**Fair assessment.** COMPNET-EN offers the largest project catalogue after NPS Labtainers. However, the individual projects do not reach the implementation depth of building a complete TCP stack (Stanford, KAIST) or operating a class-wide BGP network (ETH Zürich). The Flex component requirement — demanding interoperability in a second programming language — is distinctive and pedagogically motivated, but it does not compensate for the depth difference. This is the breadth-versus-depth trade-off, and it is inherent to the design philosophy, not a deficiency that can be patched.

### 3.7. Dimension C7: Interactive Elements

The first edition identified interactive HTML presentations as a differentiator. This remains true in the second edition: COMPNET-EN provides 101 HTML files across `04_SEMINARS/_HTMLsupport/` and `00_APPENDIX/b)optional_LECTURES/`, plus 10 HTML slide decks in the Python self-study guide.

Among the 17 external courses examined, **UCLouvain's Sphinx-based ebook** is the closest parallel — it renders as an interactive web document with embedded exercises. Berkeley CS168's textbook (`textbook.cs168.io`) is web-based but read-only, without embedded quizzes or interactive elements. All other courses distribute materials as PDFs, PPTs, Google Slides, or pre-recorded video.

The claim from the first edition — that interactive HTML presentations with embedded quizzes and keyboard navigation remain a largely unexploited niche — still holds.

### 3.8. Dimension C8: Quality Assurance and CI/CD

This dimension is new to the second edition and reflects what is arguably COMPNET-EN's most distinctive infrastructure investment.

**COMPNET-EN's CI/CD pipeline** (`.github/workflows/ci.yml`) runs on every push and pull request:

1. Executable permissions normalisation from manifest (`apply_permissions.sh`)
2. Executable permissions verification (`check_executability.sh`)
3. Markdown relative link checking across 391 files, 2 231 targets (`check_markdown_links.py`)
4. Language and lexical integrity check — UTF-8 token validation, Romanian leakage control (`check_integrity.py`)
5. PlantUML figure target validation (`check_fig_targets.py --puml-only`)

The **QA Audit Report** (`QA_AUDIT_REPORT.md`) additionally documents:
- Docker Compose YAML parse validation for all 28 config files
- `depends_on: service_healthy` sanity checks for all registered labs
- Python-image dependency risk scanning (detecting runtime failures from missing packages)
- Archive hygiene: no `__pycache__` or `.pyc` artefacts shipped

Among all courses examined, the closest parallel is **KAIST CS341**, which has 4 GitHub Actions workflows testing builds on Linux, WSL, and macOS. **UCLouvain's ebook** uses Travis CI for automated builds. **No other networking course** in the sample shows evidence of CI/CD in its public repository. Stanford, CMU, Princeton, Georgia Tech, Michigan, Johns Hopkins, Berkeley, and CUHK have no visible CI/CD.

| QA Feature | COMPNET-EN | KAIST | UCLouvain | NPS | All Others |
|:-----------|:----------:|:-----:|:---------:|:---:|:----------:|
| CI pipeline on push/PR | ✅ | ✅ | ✅ | regression | ❌ |
| Markdown link validation | ✅ (2 231 targets) | ❌ | ❌ | ❌ | ❌ |
| Docker Compose coherence | ✅ | ❌ | ❌ | ❌ | ❌ |
| Executable permission control | ✅ (96 manifest entries) | ❌ | ❌ | ❌ | ❌ |
| Lexical integrity / leakage | ✅ | ❌ | ❌ | ❌ | ❌ |
| Figure target validation | ✅ | ❌ | ❌ | ❌ | ❌ |

This level of QA automation for *teaching materials* (as distinct from code) is, to our knowledge, without precedent in the courses examined.

### 3.9. Dimension C9: Academic Validation (Where COMPNET-EN Loses)

This is the dimension that the first edition ignored and that the second edition cannot afford to. The most significant gap between COMPNET-EN and the elite programmes it seeks to benchmark against is not technical but scholarly.

**Courses with peer-reviewed publications on their teaching approach:**

| Course | Publication | Venue | Year |
|:-------|:-----------|:------|:----:|
| ETH Zürich mini-Internet | "An Open Platform to Teach How the Internet Practically Works" | ACM SIGCOMM Education Workshop | 2020 |
| KAIST KENSv3 | "Teaching Networking by Building Protocol Stacks" | ACM SIGCSE (predecessor work) | 2015 |
| NPS Labtainers | "Individualizing Cybersecurity Lab Exercises with Labtainers" | IEEE Security & Privacy | 2018 |
| NPS Labtainers | Conference demonstration | ACM SIGCSE | 2021 |
| UCLouvain IPMininet | Multiple publications on INGInious and IPMininet | Various | 2014–2024 |
| SEED Labs (Du, Syracuse) | "SEED: A Suite of Instructional Laboratories" | ACM Journal on Educational Resources | 2011+ |

**COMPNET-EN has zero peer-reviewed publications, zero documented adoption beyond ASE-CSIE Bucharest, and limited external community engagement.** No GitHub stars/forks data suggests significant external usage. No conference presentation has described its approach. No measurable learning outcomes have been published.

This matters because, without external validation, the pedagogical claims made in this report — and in the kit's own documentation — rest entirely on the authors' assertions. The recently adopted multi-licence model (CC BY-NC-SA 4.0 for documentation, GPL-3.0 for code — see Section 3.10) removes the licensing barrier to external replication that existed in the first edition, but replication itself has not yet occurred.

> *Self-criticism:* This is the single largest weakness of the COMPNET-EN project. Infrastructure without validation is engineering; validated infrastructure is scholarship. The transition from the first to the second requires work that has not yet been done.

### 3.10. Dimension C10: Licensing, Ecosystem, and Adoption

The value of a course kit is a function not only of its contents but of who can use it, adapt it, and build upon it. As of February 2026, COMPNET-EN has adopted a **multi-licence model** structurally aligned with UCLouvain CNP3:

- **Category A (documentation, lectures, seminars, guides, diagrams, HTML presentations):** CC BY-NC-SA 4.0 — any institution may use, adapt, and translate for non-commercial teaching, provided attribution and ShareAlike conditions are met.
- **Category B (Python scripts, shell scripts, Dockerfiles, Compose configs, CI workflows, QA tools, lab_runner):** GPL-3.0-or-later — standard open-source copyleft; modifications must be published under the same licence.
- **Category C (quiz banks, formative quizzes, solution templates, PCAP validation rules, instructor outlines):** All Rights Reserved — access by bilateral agreement, protecting assessment integrity.

An additional clause requires co-authorship when materials constitute more than 20% of a derived published work.

| Course/Framework | Licence Model | Non-Commercial Teaching | Adaptation Permitted | Institutional Adoption (documented) |
|:-----------------|:-------------|:-----------------------:|:--------------------:|:-----------------------------------:|
| NPS Labtainers | Public domain | ✅ | ✅ | Military + civilian; NSF-funded |
| SEED Labs (Syracuse) | Open | ✅ | ✅ | 1 180+ institutions worldwide |
| UCLouvain CNP3 ecosystem | CC BY-SA (ebook), GPL (exercises) | ✅ | ✅ | Multiple European universities |
| Kathará | GPL-3.0 | ✅ | ✅ | Roma Tre, Télécom Paris, KTH, UCLouvain |
| ETH mini-Internet | Apache-2.0 | ✅ | ✅ | Workshops, NANOG presentations |
| Stanford CS144 | — (no explicit licence) | ⚠️ | ⚠️ | Global self-study community (PKUFlyingPig fork) |
| KAIST KENSv3 | MIT | ✅ | ✅ | 151 GitHub stars |
| **COMPNET-EN** | **CC BY-NC-SA / GPL-3.0 / Reserved** | **✅** | **✅ (A+B)** | **ASE-CSIE Bucharest (elsewhere not yet documented)** |

**What changed and why.** The first edition of this report identified the then-restrictive CC BY-NC-ND 4.0 licence as a structural impediment to community growth. That licence has since been replaced. COMPNET-EN now uses a tri-category model comparable in openness to UCLouvain, Kathará, and SEED Labs — the three projects with the strongest documented adoption trajectories. The non-commercial clause (NC in CC BY-NC-SA) is more restrictive than UCLouvain's CC BY-SA or NPS's public domain, but it is the same constraint applied by many OER projects and does not prevent academic adoption.

**What has not changed.** The licence is a structural prerequisite for community growth, not a guarantee of it. No documented adoption outside ASE-CSIE Bucharest exists yet. No GitHub fork or star data suggests significant external usage. The licence change removes a barrier; whether the materials prove useful enough for others to invest in adapting them is a question that only time and the quality of the kit itself can answer.

---

## 4. Case Studies: What Others Do Well (and What We Learnt)

### 4.1. Stanford CS144: The Implementation Benchmark

**What they do brilliantly:** The 8-checkpoint TCP/IP stack build is the gold standard for networking project pedagogy. The narrative coherence — each lab extending the previous one — creates a sense of architectural accumulation that discrete weekly projects cannot replicate. Code quality enforcement (clang-format, clang-tidy, sanitisers) is exemplary.

**What they lack publicly:** No Docker infrastructure (VM image only). No explicit pedagogical methodology documentation. No formative assessment tools. No instructor guides.

**Lesson for COMPNET-EN:** A single deep, narratively coherent project can teach more about TCP than fifteen separate briefs. The roadmap should consider a "capstone track" option alongside the existing catalogue.

### 4.2. ETH Zürich: The Infrastructure and Validation Model

**What they do brilliantly:** The mini-Internet project is unique in requiring class-wide cooperation at Internet scale. Each group operates a real AS. And critically, they *published the approach* at SIGCOMM'20, providing academic validation that others can cite and replicate.

**What they lack publicly:** No explicit pedagogical scaffolding. No interactive presentations. No formative quizzes. Limited documentation beyond the project itself.

**Lesson for COMPNET-EN:** Publication matters. The mini-Internet project is influential not only because it is good but because it is *documented in a peer-reviewed venue*.

### 4.3. UCLouvain CNP3: The Ecosystem Standard

**What they do brilliantly:** The complete ecosystem — open textbook (3rd edition, 4th in progress), INGInious auto-graded exercises with PCAP field validation, IPMininet for topology creation, C socket exercises, network trace problems, over 40 GitHub repositories in the `cnp3` organisation — demonstrates what long-term sustained investment in open educational resources can achieve.

**What they lack:** Docker-native weekly labs. Interactive HTML presentations. Weekly quiz banks. The ebook is comprehensive but static (Sphinx rendering, no embedded interactivity).

**Lesson for COMPNET-EN:** Building an ecosystem takes years of consistent effort across textbook, tooling, and grading infrastructure. COMPNET-EN has the *breadth* but not yet the *longevity* or *external validation*.

### 4.4. NPS Labtainers: The Assessment Framework

**What they do brilliantly:** Per-student parameterisation via keyed hashes is genuinely innovative for academic integrity. The `gradelab` automated assessment tool, Docker Hub distribution model, and instructor guides represent a mature operational framework. Published at IEEE S&P 2018 and demonstrated at SIGCSE 2021.

**What they lack:** Not a complete course kit — no lectures, no progressive curriculum, no quiz banks. Security-focused rather than general networking.

**Lesson for COMPNET-EN:** The per-student parameterisation model is worth studying. COMPNET-EN's subnetting quiz generator is a small step in this direction; extending the approach to all labs would significantly strengthen assessment integrity.

### 4.5. CMU 15-441: The Systems Ambition

**What they do brilliantly:** The three multi-week projects (Mixnet, TCP, HTTP+video) are technically ambitious and industry-relevant. The custom Wireshark dissector and AWS EC2 testing infrastructure demonstrate serious investment. Recent offerings (Fall 2024) added a privacy-preserving mix network project — a contemporary topic that no other course in the sample addresses.

**What they lack publicly:** No CI/CD. No Docker for most work (custom VMs). No formative assessment tools visible. No instructor guides.

**Lesson for COMPNET-EN:** The Wireshark dissector idea is excellent — building custom protocol decoders forces students to think at the wire level. COMPNET-EN's PCAP tools (`pcap_stats.py`, `pcap_tshark_summary.py`) could evolve in this direction.

---

## 5. Summary of Findings

### 5.1. Evaluation Matrix

Scoring 1–10 per dimension, evaluated by the author with acknowledged bias. Scores reflect only what is publicly verifiable. "N/V" = not verifiable from public sources.

| Course | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | TOTAL |
|:-------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:-----:|
| **COMPNET-EN** | **8** | **6** | **8** | **9** | **9** | **8** | **9** | **10** | **2** | **7** | **76/100** |
| Stanford CS144 | 7 | 10 | 4 | 5 | 7 | 10 | 2 | 2 | 5 | 6 | 58/100 |
| ETH Zürich | 9 | 7 | 3 | 10 | 6 | 7 | 2 | 2 | 9 | 8 | 63/100 |
| Berkeley CS168 | 10 | 5 | 3 | 3 | 9 | 5 | 3 | 2 | 3 | 8 | 51/100 |
| CMU 15-441 | 8 | 9 | 2 | 7 | 6 | 9 | 2 | 2 | 5 | 5 | 55/100 |
| Michigan EECS 489 | 8 | 8 | 4 | 5 | 7 | 6 | 2 | 2 | 3 | 5 | 50/100 |
| KAIST KENSv3 | 6 | 8 | 5 | 7 | 5 | 7 | 2 | 8 | 7 | 7 | 62/100 |
| UCLouvain CNP3 | 9 | 5 | 8 | 6 | 9 | 6 | 5 | 5 | 9 | 9 | 71/100 |
| NPS Labtainers | 6 | 4 | 7 | 10 | 8 | 10 | 2 | 5 | 8 | 10 | 70/100 |
| GA Tech CS 6250 | 8 | N/V | 5 | 4 | N/V | 7 | 2 | 2 | 4 | 3 | ~35+/100 |

**Reading guide.** The total scores should not be interpreted as rankings. They aggregate dimensions that different stakeholders weight differently. An instructor choosing a Docker-native lab framework cares about C4 and C8. A student seeking deep systems experience cares about C2 and C6. A department evaluating scholarly impact cares about C9 and C10.

### 5.2. Findings that Changed from the First Edition

1. **C1 (Comprehensiveness) raised from 7 to 8.** The first edition evaluated a kit that covered standard networking topics across 14 weeks but lacked IoT/MQTT, gRPC/modern RPC, and the 39 runnable micro-scenarios now embedded in lecture directories. The current kit is the broadest in the sample — no other course covers both IoT/MQTT and gRPC. The score does not reach 9 or 10 because Berkeley CS168 (17 weeks) and ETH Zürich (15 weeks, deeper per-topic) remain ahead in either duration or depth.

2. **C2 (Code Quality) lowered from 7 to 6.** The first edition was generous. Without strict Python linting in CI, the score cannot match Stanford (10) or CMU (9). The `ruff.toml` exists but is not enforced.

3. **C3 (Pedagogy) maintained at 8 but with caveats.** The new kit has significantly more pedagogical artefacts (misconception lists, Parsons problems, Python self-study guide with cross-language comparisons), but UCLouvain's INGInious remains ahead in auto-graded formative assessment. Score 8 reflects artefact richness, not validated effectiveness.

4. **C4 (Infrastructure) raised from 8 to 9.** The lab_runner framework, Docker Compose coherence validation, Portainer integration, and 18 registered labs represent a genuine advance.

5. **C5 (Documentation) raised from 8 to 9.** The first edition already scored well on documentation, but the current kit adds 386 PlantUML diagram sources with a render toolchain (unique in the sample), a 2 222-line Python self-study guide with Rosetta Stone cross-language comparisons, per-seminar instructor notes with Mininet-SDN variants, sparse checkout guidance, and a full QA audit report. Only Berkeley CS168's open textbook prevents a score of 10.

6. **C6 (Projects) adjusted from 9 to 8.** The 25 project briefs with E1/E2/E3 gates and PCAP validation rules are substantial, but honest comparison with Stanford's TCP stack build and CMU's multi-week systems projects requires acknowledging the depth gap.

7. **C8 (Quality Assurance) is a new dimension — scored 10.** No other course in the sample maintains a CI/CD pipeline that validates Markdown links (2 231 targets), Docker Compose coherence, executable permissions from a manifest, lexical integrity, and PlantUML figure targets on every push. KAIST CS341 is the closest with 4 GitHub Actions workflows, but their scope is build verification, not content quality assurance.

8. **C9 (Academic Validation) is a new dimension — scored 2.** COMPNET-EN has zero peer-reviewed publications, zero documented adoption beyond ASE-CSIE Bucharest, and no conference presentations describing its approach. Compare this to ETH Zürich (SIGCOMM'20), KAIST (SIGCSE'15), NPS Labtainers (IEEE S&P'18, SIGCSE'21), and UCLouvain (multiple venues, 2014–2024). The asymmetry between C8 (10) and C9 (2) is itself a finding: engineering excellence and scholarly validation are independent dimensions.

9. **C10 (Licensing) raised from 3 to 7.** The adoption of a multi-licence model (CC BY-NC-SA / GPL-3.0 / Reserved) replaces the CC BY-NC-ND 4.0 licence that the first edition flagged as a growth constraint. The new structure is comparable to UCLouvain and Kathará. The score remains below NPS (public domain, 10) and UCLouvain (CC BY-SA, 9) because the NC clause and the co-authorship requirement introduce frictions that fully permissive licences do not, and because no external adoption has yet been documented under the new terms.

### 5.3. Main Conclusions

1. **COMPNET-EN occupies a distinctive niche.** It is arguably the most infrastructure-complete, pedagogically explicit, and operationally detailed single-repository networking course kit that is publicly accessible. This is a verifiable claim: the reader can check the file counts, the CI pipeline, the QA report, and the documentation against any other course in the sample.

2. **No single course excels across all dimensions.** Stanford dominates project depth and code quality. ETH Zürich dominates infrastructure ambition and academic validation. UCLouvain dominates ecosystem breadth and formative assessment. NPS dominates lab variety and assessment integrity. Berkeley dominates textbook quality. COMPNET-EN dominates operational completeness, QA automation, and pedagogical documentation. The landscape is fragmented.

3. **The validation gap is the critical weakness.** Without peer-reviewed publication, documented learning outcomes, and multi-institutional adoption, COMPNET-EN's claims rest on self-assessment. This report is itself an instance of the problem: a self-evaluation cannot substitute for external review.

4. **The licence model is now structurally aligned with the field.** The adoption of a multi-licence model (CC BY-NC-SA for documentation, GPL-3.0 for code, all-rights-reserved for examination materials) removes the licensing barrier identified in the first edition. COMPNET-EN now uses a structure comparable to UCLouvain CNP3, Kathará, and SEED Labs — the three projects with the strongest documented adoption trajectories. Whether the materials attract external adoption remains an open question, but the licence is no longer the obstacle.

5. **The breadth-versus-depth trade-off is real.** COMPNET-EN covers IoT/MQTT, gRPC, email protocols, SDN, load balancing, and security across 14 weeks. No other course in the sample matches this breadth. But no other course in the sample sacrifices as much depth per topic, either. The design philosophy prioritises survey completeness over implementation mastery.

### 5.4. Limitations of This Analysis

- **Author bias.** Structural and irreducible. Mitigated by grounding claims in verifiable artefacts, but not eliminated.
- **Private materials.** Approximately half the courses examined keep their best materials behind authentication. The comparison systematically favours transparent courses.
- **Temporal snapshot.** Curricula evolve. This analysis reflects the state as of February 2026.
- **Subjectivity in scoring.** The C1–C10 scores reflect the author's priorities. Different weights produce different rankings. The matrix is offered as a structured opinion, not as an objective measurement.
- **No student outcome data.** This report compares *inputs* (materials, infrastructure, documentation) rather than *outputs* (student learning, skill acquisition, employability). The correlation between the two is assumed but not demonstrated.

---

## 6. Recommendations and Future Directions

### 6.1. What COMPNET-EN Should Learn from Others

| From | Lesson | Priority |
|:-----|:-------|:--------:|
| Stanford CS144 | Add a "capstone track" — a single deep, narratively coherent TCP/IP stack build as an alternative to the 25-brief catalogue | High |
| Stanford CS144 | Enforce Python linting in CI (ruff or similar) | High |
| ETH Zürich | Publish the teaching approach at a peer-reviewed venue (SIGCSE, ITiCSE, ACM TOCE) | Critical |
| UCLouvain CNP3 | Develop auto-graded PCAP exercises with per-field validation (extend existing PCAP tools) | Medium |
| NPS Labtainers | Implement per-student parameterisation for lab exercises | Medium |
| CMU 15-441 | Build custom Wireshark dissectors for student protocols | Low |
| Berkeley CS168 | Develop a companion open textbook or integrate with existing open textbooks | Long-term |

### 6.2. Proposed Roadmap

```
2026 Q1–Q2  ─────► Enforce Python linting in CI (ruff strict, mypy)
                  │ Prepare a short paper on the teaching approach for ITiCSE or SIGCSE
                  │
2026 Q3     ─────► Auto-graded PCAP exercises with field validation
                  │ Capstone track: design a 6-checkpoint TCP implementation project
                  │
2026 Q4     ─────► Per-student parameterisation for selected labs
                  │ First external pilot (partner institution)
                  │
2027+       ─────► Publication of learning outcome data
                  │ Track and document external adoption under the new licence
                  │ Companion open textbook (Berkeley-inspired)
```

---

## 7. Acknowledgements

This project continues to benefit from the foundational work of **conf. dr. Andrei TOMA**, whose initial ideas, base scripts, and sustained discussions at The Dose coffee shop in Bucharest shaped the core architecture. The Dose deserves credit for the amount of caffeine that has been converted into Docker Compose files.

Thanks are also owed to the open-source communities behind Docker, Wireshark, PlantUML, Mininet, and Python — tools that make this kind of project possible. And to the students at ASE-CSIE, who continue to serve as both the primary beneficiaries and the most honest critics of each iteration.

---

## References and Resources

### Courses Analysed

| # | University | Course | Primary Public URL | Last Verified |
|:-:|:-----------|:-------|:-------------------|:-------------:|
| 1 | Stanford | CS144 | `cs144.github.io` / `github.com/CS144` | Dec 2025 |
| 2 | ETH Zürich | 227-0120-00L | `github.com/nsg-ethz/mini_internet_project` | Dec 2025 |
| 3 | UC Berkeley | CS168 | `textbook.cs168.io` / `github.com/berkeley-cs168` | Feb 2026 |
| 4 | CMU | 15-441/641 | `computer-networks.github.io` / `github.com/computer-networks` | Sep 2025 |
| 5 | Princeton | COS 461 | `github.com/PrincetonUniversity/COS461-Public` | ~2020 |
| 6 | U. Michigan | EECS 489 | `github.com/mosharaf/eecs489` | Fall 2025 |
| 7 | Georgia Tech | CS 6250 | `omscs.gatech.edu/cs-6250-computer-networks` | 2023 (syllabus) |
| 8 | KAIST | CS341 / KENSv3 | `github.com/ANLAB-KAIST/KENSv3` | Mar 2025 |
| 9 | UCLouvain | CNP3 | `github.com/cnp3` / `inginious.org/course/cnp3` | Active 2026 |
| 10 | NPS | Labtainers | `github.com/mfthomps/Labtainers` / `nps.edu/web/c3o/labtainers` | Jan 2026 |
| 11 | Johns Hopkins | EN.601.414 | `github.com/xinjin/course-net` | 2019 |
| 12 | CUHK | CSCI 4430 | `github.com/henryhxu/CSCI4430` | Fall 2025 |
| 13 | UIUC | ECE 438 | GitHub Pages site | Feb 2026 |

### Peer-Reviewed Publications Referenced

- Holterbach, T. et al. (2020). "An Open Platform to Teach How the Internet Practically Works." *ACM SIGCOMM Education Workshop*.
- Thompson, M. F. et al. (2018). "Individualizing Cybersecurity Lab Exercises with Labtainers." *IEEE Security & Privacy*, 16(2).
- Du, W. (2011+). "SEED: A Suite of Instructional Laboratories for Computer Security Education." *ACM Journal on Educational Resources in Computing*.
- Brown, N. C. C. & Wilson, G. (2018). "Ten Quick Tips for Teaching Programming." *PLOS Computational Biology*.
- Mazur, E. (1997). *Peer Instruction: A User's Manual*. Prentice Hall.
- Parsons, D. & Haden, P. (2006). "Parson's Programming Puzzles: A Fun and Effective Learning Tool for First Programming Courses." *Australasian Computing Education Conference*.

### Frameworks and Tools Referenced

| Tool/Framework | URL | Licence |
|:---------------|:----|:--------|
| Kathará | `github.com/KatharaFramework/Kathara` | GPL-3.0 |
| Containerlab | `containerlab.dev` | BSD-3-Clause |
| SEED Labs | `seedsecuritylabs.org` | Open |
| INGInious | `inginious.org` | AGPL-3.0 |

---

<div align="center">

**COMPNET-EN — Computer Networks Course Kit**  
*Bucharest University of Economic Studies*  
*Faculty of Economic Cybernetics, Statistics and Informatics*

---

*Last updated: 28 February 2026*  
*Document version: 2.0*  
*Kit version: v13.05.00*  
*Repository: `github.com/antonioclim/COMPNET-EN`*

</div>
