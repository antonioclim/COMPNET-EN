# Open Educational Licence — Multi-Category

**Policy revision prepared for v1.5.0 — 17 November 2026**

## 1. Scope and order of precedence

This policy distinguishes educational documentation, software and reserved
assessment material in the COMPNET-EN course kit. It applies only to rights that
the relevant rightsholder is entitled to license. Copyright, authorship and
component-specific notices must be preserved.

Apply the following rules in order:

1. A component-specific third-party licence or an existing licence grant remains
   effective. This document does not relicense third-party material or withdraw
   permissions already received under an earlier valid grant.
2. The exact repository-relative paths in `LICENCE_CATEGORY_C.txt` identify
   Category C for this policy. This list takes precedence over the general
   documentation and file-type descriptions below, subject to rule 1.
3. Source code and configuration outside that list belong to Category B. This
   includes `.py`, `.sh`, `.ps1`, `.js`, `.cjs`, `.mjs`, `.c`, `.h`, `.cc`, `.cpp`,
   `.hpp`, `.java`, `.kt`, `.kts`, `.php`, `.conf`, `.env`, `.zone`, `.proto`,
   `.yml`, `.yaml` and `.toml` files; Docker build recipes with a `Dockerfile`
   token in the filename, including prefixed names; Makefiles; package and
   requirements manifests, including `requirements-optional.txt`; Git, editor
   and Prettier configuration (`.gitattributes`, `.gitignore`, `.editorconfig`,
   `.prettierignore` and `.prettierrc`). It also includes the operational
   configurations `00_TOOLS/lab_runner/labs.json`,
   `00_TOOLS/qa/executable_manifest.txt`,
   `03_LECTURES/C11/assets/scenario-ssh-provision/controller/plan.json` and
   `00_TOOLS/qa/evidence/kotlin/2026-11-17/PROTOCOL_FREEZE.json`.
4. Other repository materials belong to Category A. HTML teaching presentations,
   PlantUML diagram sources and project briefs remain educational content under
   this default. A separately identified third-party component keeps its terms.

The reserved-path list includes the weekly question-bank directory, the named
formative datasets, the assessment workbook, PCAP assessment-rule JSON files,
identified solution templates and the S14 assessment rubric. Instructor outlines
under `00_APPENDIX/d)instructor_NOTES4sem/` are included in that explicit list;
other instructor-facing documentation follows the rules above.

An embedded assessment example does not automatically change an entire
Category A presentation or project brief into Category C. New reserved files must
be identified explicitly when released; a filename resemblance alone does not
expand the reserved list. The policy and reserved-path list are documentation.

## 2. Copyright and provenance

**© 2017–2027 ing. dr. Antonio Clim.**

Retain the original copyright, contributor credits, academic provenance and
third-party notices. This policy does not assert that every component has a
single author or that the named author owns third-party material.

## 3. Category A — Documentation and Educational Content

Category A material is offered under [Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International
(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en).
A complete, unmodified copy is included in `LICENSES/CC-BY-NC-SA-4.0.txt`.
The standard licence governs the permissions, attribution, non-commercial scope,
ShareAlike conditions, exceptions and limitations. This summary adds no further
restriction to that grant.

Non-commercial sharing, adaptation and teaching are permitted under that licence.
Whether a particular use is non-commercial is determined by the licence, not by a
blanket assumption about an institution or the existence of tuition fees. Uses
outside its grant may be discussed with the relevant rightsholder.

## 4. Category B — Source Code and Configuration

Category B material is offered under the [GNU General Public License, version 3
or any later version (GPL-3.0-or-later)](https://www.gnu.org/licenses/gpl-3.0.html).
The GPL version 3 text is included in `LICENSES/GPL-3.0-or-later.txt`; the
permission to use any later version is expressed by this policy and applicable
component notices. The applicable GPL text governs copying, modification, distribution and source
availability. Existing notices and applicable component-specific terms remain.

Commercial use and distribution are permitted when the GPL conditions are met.
This policy imposes no non-commercial condition, automatic co-authorship
obligation or additional research-citation condition on GPL-covered material.
Private use is not treated as a duty to publish modifications. Distribution and
combination with other works must be assessed under the applicable GPL terms.

## 5. Category C — Examination and Assessment Materials

For the exact paths in `LICENCE_CATEGORY_C.txt`, rights not already granted are
reserved. Personal study is permitted. Other uses requiring the rightsholder's
permission require prior written authorisation, unless an existing grant,
applicable exception or limitation already permits the use.

This category covers the named controlled assessment resources. It does not
remove earlier permissions, override a third-party licence or limit uses that do
not require permission. Public visibility of a repository is distinct from this
category's reuse permissions; applicable platform terms also remain unaffected.

Instructors may request permission through the repository issue tracker or
official ASE-CSIE academic channels, describing the materials, institution,
course and intended use. A separate agreement may define the authorised scope.

## 6. Attribution, academic citation and authorship

Comply with the attribution and notice requirements of each applicable licence.
For Category A, use a reasonable attribution suited to the medium and context.
For Category B, preserve the copyright, licence and other notices required by the
GPL. Category C permissions may specify attribution in the relevant agreement.

The following citation is a suggested academic format, preserving the existing
project citation. It is not an additional condition on a standard public licence:

> Clim, A. (2025). *Computer Networks — Course Kit (EN).* Bucharest University of
> Economic Studies (ASE), Faculty of Economic Cybernetics, Statistics and
> Informatics (CSIE). https://github.com/antonioclim/COMPNET-EN

Where the author is identified in full, the preferred form is
**ing. dr. Antonio Clim**. Academic citation is requested when the materials
inform a publication. Collaboration and co-authorship should reflect substantive
scholarly contributions, the applicable publication criteria and the agreement
of the authors. Reuse above a numerical percentage does not automatically create
a co-authorship obligation. No licence permission depends on such an obligation.

## 7. Teaching and commercial permission requests

Teaching with Category A follows CC BY-NC-SA 4.0. Teaching with Category B follows
the GPL and is not restricted to non-commercial courses. Category C follows the
specific permission or existing grant applicable to the identified material.
Requests for uses beyond those permissions may be submitted through the channels
listed below. This section does not narrow any standard licence grant.

## 8. Contributions

Contributors retain their copyright. Contributions intended for Category A or B
should identify and use the corresponding category licence, subject to retained
third-party terms and the contributor's authority to grant rights. Contributions
to reserved assessment material require a separately agreed scope. Submission
alone does not transfer copyright or permit relicensing of third-party content.
Contributor notices and acknowledgements must be retained as applicable.

## 9. Warranty, other terms and interpretation

The warranty exclusions, limitations of liability and other conditions of the
applicable standard licence govern Category A and B. No supplementary jurisdiction,
severability, permission or attribution term in this policy adds a restriction
to those standard licences.

For reserved material, it is supplied as available without a separate warranty,
to the extent permitted by applicable law; any express written agreement governs
its own terms. Mandatory law and statutory exceptions remain unaffected.

This clarification preserves existing grants and original provenance. It is not
a representation that an earlier ambiguity removed the recipient's rights.

## 10. Contact

**ing. dr. Antonio Clim**

Bucharest University of Economic Studies (ASE)

Faculty of Economic Cybernetics, Statistics and Informatics (CSIE)

For permissions, questions or institutional access requests, use the repository
issue tracker or official ASE-CSIE academic channels.
