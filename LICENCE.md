# Open Educational Licence — Multi-Category

**Version 14.00.00 — February 2026**

---

## Overview

This repository uses a **multi-licence model**, similar to those adopted by
open educational projects such as UCLouvain CNP3 and SEED Labs. Different
categories of content carry different licences so that educational materials
can be shared and adapted while examination resources remain controlled and
authorship is protected.

```
┌──────────────────────────────────────────────────────────────────────┐
│  Category A — Documentation and Educational Content                  │
│  Licence: CC BY-NC-SA 4.0                                            │
│  Scope:  lectures, seminars, README files, guides, diagrams (puml),  │
│          HTML presentations, instructor notes, project briefs,       │
│          cheatsheets, troubleshooting docs, the Python self-study    │
│          guide, Portainer guides                                     │
├──────────────────────────────────────────────────────────────────────┤
│  Category B — Source Code and Configuration                          │
│  Licence: GPL-3.0-or-later                                           │
│  Scope:  Python scripts (.py), shell scripts (.sh), Dockerfiles,     │
│          Docker Compose files (.yml/.yaml), nginx configs (.conf),   │
│          CI workflow files, QA scripts, Makefiles, PlantUML render   │
│          scripts, lab_runner, format-offline.js, package.json        │
├──────────────────────────────────────────────────────────────────────┤
│  Category C — Examination and Assessment Materials                   │
│  Licence: All Rights Reserved                                        │
│  Scope:  quiz banks (00_APPENDIX/c)studentsQUIZes*), formative       │
│          quizzes (quiz.json, quiz.yaml, parsons_problems.json),      │
│          assessment rubrics, verification index (.xlsx),              │
│          PCAP validation rules (tools/pcap_rules/*.json),            │
│          solution templates (*Solution*), instructor outlines         │
│          (d)instructor_NOTES4sem/*)                                   │
└──────────────────────────────────────────────────────────────────────┘
```

If a file does not clearly fall into one of the categories above, it
follows Category A by default.

---

## Copyright Notice

**© 2017–2027 ing. dr. Antonio Clim.**

The Materials are protected under Romanian law (Law No. 8/1996 on Copyright
and Related Rights, as amended), European Union Directive 2001/29/EC, and
applicable international treaties including the Berne Convention for the
Protection of Literary and Artistic Works.

---

## Category A — Documentation and Educational Content

### Licence

This content is licensed under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
licence.

### What This Permits

| Action | Permitted? | Condition |
|--------|:----------:|-----------|
| Read, download, study | ✓ | — |
| Share and redistribute | ✓ | Attribution required (see Section 5) |
| Adapt, translate, remix | ✓ | Same licence (ShareAlike), attribution, non-commercial |
| Use in teaching at any institution | ✓ | Non-commercial, with attribution (see Section 5) |
| Use in commercial training or paid courses | ✗ | Written permission required |
| Remove or obscure the original attribution | ✗ | — |

### ShareAlike Obligation

If you remix, transform, or build upon the Category A materials, you must
distribute your contributions under the **same or a compatible licence**
(CC BY-NC-SA 4.0 or later).

---

## Category B — Source Code and Configuration

### Licence

This content is licensed under the
[GNU General Public License v3.0 or later
(GPL-3.0-or-later)](https://www.gnu.org/licenses/gpl-3.0.html).

### What This Permits

| Action | Permitted? | Condition |
|--------|:----------:|-----------|
| Run, study, inspect | ✓ | — |
| Modify and distribute modifications | ✓ | Same licence (copyleft), attribution, source availability |
| Include in open-source projects | ✓ | GPL-3.0-compatible licence required |
| Include in proprietary/closed-source products | ✗ | GPL copyleft applies |
| Use code snippets for personal learning | ✓ | — |

### Copyleft Obligation

If you distribute modified versions of the Category B code, you must make
your source code available under the GPL-3.0-or-later licence.

### Linking and Aggregation

Mere aggregation of Category B code with independently developed software
in a distribution medium does not bring the other software under the scope
of the GPL-3.0. The full GPL-3.0 text governs boundary cases.

---

## Category C — Examination and Assessment Materials

### Licence

**All rights reserved.** No part of the Category C materials may be
reproduced, distributed, adapted, translated, publicly displayed, or used
for any purpose beyond personal study without the prior express written
consent of the Author.

### Rationale

Examination materials, quiz banks, solution templates, PCAP validation
rules, and instructor outlines derive their pedagogical value from
controlled access. Public redistribution would compromise assessment
integrity for current and future cohorts.

### How to Request Access

Instructors at other institutions who wish to use Category C materials
in their own courses may request access by:

1. Opening a formal request on the repository **Issue Tracker** or
   contacting the Author through official ASE-CSIE academic channels.
2. Specifying the institution, course, expected enrolment, and intended
   use.
3. Awaiting explicit written authorisation before any use.

Category C materials may be shared under a separate bilateral agreement
at the Author's discretion.

---

## 5. Attribution and Citation

### 5.1 Mandatory Attribution (all uses)

Any use of the Materials — whether under Category A, Category B, or an
authorised use of Category C — **must** include a clear and reasonably
prominent attribution in the following format:

```
Clim, A. (2025). Computer Networks — Course Kit (EN).
  Bucharest University of Economic Studies (ASE), Faculty of Economic
  Cybernetics, Statistics and Informatics (CSIE).
  https://github.com/antonioclim/COMPNET-EN
```

Where author names appear in full form, the Author must be referenced as
**ing. dr. Antonio Clim**.

For code files (Category B), attribution may alternatively take the form
of a comment header or a NOTICE file, consistent with GPL-3.0 practice.

### 5.2 Co-authorship Requirement (use exceeding 20%)

Any published work — including but not limited to journal articles,
conference papers, books, theses, technical reports, or course materials
intended for public distribution — in which materials from this repository
constitute **more than 20%** of the total content must include
**ing. dr. Antonio Clim** among the listed co-authors.

The 20% threshold applies to any combination of verbatim reproduction,
paraphrased content, adapted code, redrawn diagrams, restructured
exercises, or conceptual frameworks traceable to the Materials.

### 5.3 Determination of Proportion

In the event of a dispute regarding the proportion of Materials used, the
assessment shall be conducted by an independent academic expert mutually
agreed upon by the parties, or — failing agreement — appointed by the
competent court.

---

## 6. Teaching Permission — Detailed Terms

### 6.1 Non-Commercial Teaching

Any educational institution — university, school, or non-profit training
programme — may use Category A and Category B materials for classroom
instruction, seminar delivery, and laboratory exercises, **provided that**:

1. The use is **non-commercial** (no tuition surcharge, course fee, or
   other charge is levied specifically for access to these materials).
2. The attribution requirements of Section 5.1 are satisfied.
3. Any adapted or translated versions carry the CC BY-NC-SA 4.0 licence
   (for Category A content) or the GPL-3.0-or-later licence (for
   Category B content).

### 6.2 Commercial and Paid Use

Use of the Materials in any paid training programme, commercial bootcamp,
corporate workshop, or online platform that charges learners requires the
**prior express written consent** of the Author. Requests should be
submitted through the repository Issue Tracker or official ASE-CSIE
channels.

### 6.3 Examination Materials in External Teaching

Category C materials are **not included** in the general teaching
permission. Instructors at other institutions must request access
separately under Section 4 (Category C).

---

## 7. Contributions

### 7.1 Pull Requests and External Contributions

By submitting a pull request or other contribution to this repository,
you agree that your contribution will be licensed under the applicable
category licence:

- Documentation contributions: CC BY-NC-SA 4.0
- Code contributions: GPL-3.0-or-later

You retain copyright over your contribution but grant the Author a
perpetual, irrevocable, worldwide licence to use, modify, and distribute
it under the terms above.

### 7.2 Attribution of Contributors

Significant contributions will be acknowledged in the repository
CHANGELOG or README, at the Author's discretion.

---

## 8. Disclaimer of Warranty

THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE
MATERIALS.

---

## 9. Governing Law and Jurisdiction

This Licence shall be governed by and construed in accordance with the laws
of Romania. Any disputes arising under or in connection with this Licence
shall be subject to the exclusive jurisdiction of the courts of Bucharest,
Romania.

EU Directive 2001/29/EC and the Berne Convention apply where Romanian law
is silent or where cross-border enforcement requires harmonised
interpretation.

---

## 10. Severability

If any provision of this Licence is held to be invalid or unenforceable,
the remaining provisions shall continue in full force and effect. The
invalid provision shall be replaced by a valid provision that most closely
achieves the original intent.

---

## 11. Licence Compatibility Summary

| If you want to… | Use Category A (CC BY-NC-SA) | Use Category B (GPL-3.0) | Use Category C (Reserved) |
|------------------|:----------------------------:|:------------------------:|:-------------------------:|
| Study personally | ✓ | ✓ | ✓ |
| Teach non-commercially | ✓ with attribution | ✓ with attribution | Request required |
| Adapt and reshare | ✓ same licence, non-commercial | ✓ same licence, source available | ✗ |
| Include in commercial product | ✗ (request needed) | ✗ (GPL copyleft) | ✗ (request needed) |
| Publish a paper using < 20% | ✓ with citation | ✓ with citation | ✓ with citation |
| Publish a paper using > 20% | ✓ with co-authorship | ✓ with co-authorship | ✓ with co-authorship |
| Fork the repository | ✓ A+B only, with attribution | ✓ code under GPL-3.0 | ✗ (Category C excluded) |
| Translate into another language | ✓ same licence, attribution | ✓ same licence | ✗ (request needed) |

---

## Contact

**ing. dr. Antonio Clim**
Bucharest University of Economic Studies (ASE)
Faculty of Economic Cybernetics, Statistics and Informatics (CSIE)

For permissions, questions, or institutional access requests:
use the repository **Issue Tracker** or official ASE-CSIE channels.

---

*Last updated: February 2026*
