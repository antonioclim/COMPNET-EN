# Acknowledgments

## Week 8: Transport Layer — HTTP Server Implementation and Reverse Proxies

---

## Contributors

### Primary Author
**ing. dr. Antonio Clim**
Assistant Lecturer, Computer Science and Economic Informatics
Academia de Studii Economice din București (ASE)

### Pedagogical Collaboration
**Andrei T.**
ASE colleague and invaluable collaborator

At least 50% of the pedagogical design in this laboratory kit emerged from our
brainstorming sessions. Andrei's contributions include:

- The misconception-first approach to exercise design
- Question formulation for the formative quiz
- The "predict before you code" checkpoints throughout exercises
- Refinement of Parsons problems to include realistic distractors
- The troubleshooting guide's "Before You Debug: Predict" section

Our discussions — often extending well past reasonable hours — shaped the core
philosophy: students learn best when they confront their misconceptions directly,
rather than memorising correct procedures.

---

## Pedagogical Framework

The teaching methodology in this kit draws heavily from my experience in the
**DPPD (Departamentul pentru Pregătirea Personalului Didactic) module** at
**Universitatea Politehnica din București**.

*A brief aside: I would have preferred to complete the psychopedagogy
qualification at ASE, but their programme doesn't accept engineers. I understand
the rationale — economists teaching economists makes sense. But UPB's approach
proved valuable: engineers learn to teach technical subjects differently, with
emphasis on mental models and practical verification.*

Key principles from DPPD that influenced this kit:

1. **Constructive Alignment** (Biggs, 1996)
   Every Learning Objective has at least three supporting artefacts (theory,
   practice, assessment). See `docs/learning_objectives.md` for the full matrix.

2. **Deliberate Practice** (Ericsson, 2008)
   Exercises include prediction checkpoints and immediate feedback, not just
   "do this, then that" instructions.

3. **Peer Instruction** (Mazur, 1997)
   The ConcepTest questions in `docs/peer_instruction.md` follow the validated
   5-step protocol for conceptual change.

4. **Threshold Concepts** (Meyer & Land, 2003)
   The misconceptions document targets known "troublesome knowledge" that blocks
   student progress until resolved.

---

## Technical Acknowledgments

### Infrastructure Design

The Docker architecture mirrors patterns I observed while consulting on cloud
deployments. The nginx → backend topology is simplified but pedagogically
complete.

### Code Style

The exercise scaffolds use a consistent structure:
- Clear section headers with visual separators
- Prediction checkpoints (💭) before implementation sections
- Pair programming notes with explicit swap points
- Type hints and docstrings suitable for IDEs

This structure emerged from observing where students get lost and designing
waypoints to prevent that.

---

## Tools and Resources

This kit was built using:

- **Python 3.11** — For exercise implementations
- **Docker** with **Docker Compose** — Container orchestration
- **nginx:alpine** — Reference reverse proxy
- **Wireshark** — Packet analysis (Windows native)
- **WSL2 + Ubuntu 22.04** — Development environment

---

## Academic References

The theoretical content draws from:

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley.
- Rhodes, B. & Goerzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
- RFC 793 (TCP), RFC 768 (UDP), RFC 9110 (HTTP Semantics), RFC 9112 (HTTP/1.1)

---

## A Note on Kit Development

Creating educational materials is iterative. This kit represents version 1.0
after three years of teaching Computer Networks at ASE-CSIE. Each year, student
feedback shapes improvements:

- **Year 1:** Basic exercises, students struggled with setup
- **Year 2:** Added troubleshooting guide, setup scripts
- **Year 3:** Added formative assessment, misconceptions documentation

If you find issues or have suggestions, feedback helps improve future versions.

---

## Licence

This educational material is provided for students of ASE-CSIE.
See `LICENSE` for terms.

---

*"Teaching is not about transferring knowledge. It's about creating the conditions*
*for someone else to construct their own understanding."*

— A paraphrase of something I read during the DPPD module that stuck with me

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*București, January 2026*
