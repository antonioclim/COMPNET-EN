# Dated public-material comparison protocol

Version 1.0, frozen before external collection on 17 November 2026.

## Question and scope

Which observable public teaching artefacts are documented for the legacy seed
units, and how do their declared designs differ from the fixed COMPNET-EN
candidate? This is a bounded descriptive document study, not a university ranking,
systematic literature review, pedagogical effectiveness study or recovery of the
February 2026 dataset. Counts of artefacts of different kinds are not commensurate.

COMPNET-EN anchor: commit `8fb6afcd89eb3fa27b909941f96eff4276df8f29`, tree
`5884c293f2ec944a42a92c189ab6c178714c8e03`. The historical SPECIAL_REPORT.md SHA-256
is `33ecbecf179322234e8d3b09339b06d6da838d5f80e4ac335128d7ffa0b1d3db`.
Its scores, adverse findings and provenance remain unchanged. A separately dated
report will contain new observations. Existing F5 test results retain their scope.

## Selection fixed before collection

U00 is COMPNET-EN. U01–U13 follow the thirteen entries in the historical final
source table. U14–U17 are the additional names in its visibility table, included
explicitly to reconcile the scope. The selection is purposive and inherited; it
does not claim representativeness, a Top 50 sampling frame or complete coverage.

| ID | Legacy unit | Initial locator |
|---|---|---|
| U00 | ASE-CSIE COMPNET-EN | fixed candidate above |
| U01 | Stanford CS144 | cs144.github.io; github.com/CS144 |
| U02 | ETH Zurich communication networks / mini-Internet | github.com/nsg-ethz/mini_internet_project |
| U03 | UC Berkeley CS168 | textbook.cs168.io; github.com/berkeley-cs168 |
| U04 | CMU 15-441/641 | computer-networks.github.io; github.com/computer-networks |
| U05 | Princeton COS 461 | github.com/PrincetonUniversity/COS461-Public |
| U06 | Michigan EECS 489 | github.com/mosharaf/eecs489 |
| U07 | Georgia Tech CS 6250 | omscs.gatech.edu/cs-6250-computer-networks |
| U08 | KAIST CS341 / KENSv3 | github.com/ANLAB-KAIST/KENSv3 |
| U09 | UCLouvain CNP3 ecosystem | github.com/cnp3; inginious.org/course/cnp3 |
| U10 | NPS Labtainers | github.com/mfthomps/Labtainers; nps.edu/web/c3o/labtainers |
| U11 | Johns Hopkins EN.601.414 | github.com/xinjin/course-net |
| U12 | CUHK CSCI4430 | github.com/henryhxu/CSCI4430 |
| U13 | UIUC ECE438 | course identity to resolve from an institutional source |
| U14 | MIT networking course named 6.5820 | course identity to resolve; do not substitute 2002 OCW silently |
| U15 | Imperial networks course | course identity unspecified; resolve or retain ambiguity |
| U16 | TU Munich Advanced Computer Networks | edition and public scope to resolve |
| U17 | NUS CS2105 | resolve institutional course page |

Auxiliary resources X01 Kathara, X02 Containerlab, X03 SEED Labs and X04 INGInious
are context, not additional course observations or independent counts when part
of an ecosystem row. Paper metadata describing a predecessor framework must not
be treated as evaluation of its current version or of COMPNET-EN.

## Retrieval rule

Use primary sources: institutional/course sites, owner-maintained repositories,
official project documentation and publisher/author/institutional publication
records. Start from the legacy locator. Use at most two broad queries per unit
and one targeted clarification query if identity or access remains unresolved.
Inspect up to eight substantive artefacts per unit (repository metadata/tree
responses are routing records, not separate substantive evidence). Log justified
deviations before additional retrieval; do not expand the sample opportunistically.

A course landing page, schedule/syllabus, assignment or manual, environment
instructions, representative configuration/tests and licence are suitable
artefacts. Record the exact course edition stated, not an assumed latest offering.
Where a live URL and an immutable source exist, retain the exact commit/blob and
permalink. Repository head inspection is read-only and does not execute that code.
Authenticated content is outside the corpus. Do not log in, trigger workflows,
contact staff, request/download OVA or execute external software.

For each retrieval record: actual UTC access time, requested/final URL if known,
publisher/owner, title/path, edition/publication date if stated, retrieval method,
source reference ID, success/failure and a SHA-256 of the acquired local artefact.
Identify the hash layer: original response bytes, decoded Git blob bytes or
tool-returned text/JSON. A wrapper hash is not the hash of the original webpage.
Keep failed attempts. Date of access is distinct from date of content.

Full tool responses may be retained in the working evidence directory for
inspection. Distribution uses provenance records and concise factual notes;
unlicensed full pages or papers are not republished. Optional excerpts must total
no more than 20 words per source across all distributed records. Prefer paraphrase.
Immutable public links and Git blob identities allow exact retrieval where
available; a live-page fingerprint alone does not guarantee future recovery.

## Operational coding C1–C10

Record a claim and its supporting source identifiers for every cell. No numeric
score, weighting, aggregate or ranking is computed.

| Dimension | Observable question | Limit |
|---|---|---|
| C1 Scope and structure | Is there a dated schedule, topic outline or organised module list? | Presence and declared scope, not mastery or equivalent credit/load |
| C2 Code practices | Which explicit format/lint/type/sanitiser/build conventions are visible? | Configuration or instructions, not executed correctness or overall quality |
| C3 Teaching and feedback | Which instructions, checkpoints, exercises, assessment or feedback mechanisms are documented? | Designed scaffolding, not measured learning effectiveness |
| C4 Environment | Which setup, VM/container/network or execution instructions are documented? | Source evidence, not native deployment acceptance |
| C5 Documentation | Which guides, textbook/manual, troubleshooting or instructor materials are inspectable? | Named artefacts, not a subjective depth score |
| C6 Practical work | What assignment, checkpoint, project or laboratory structure is stated? | Different units are not counted as equivalent projects |
| C7 Web interaction | What web teaching, quizzes, simulations or interactive assessment is documented? | Documented feature/source only; no browser interaction certified |
| C8 Verification | Are tests, graders or CI configurations visible, and what do they claim to run? | Configured tests are distinct from an observed successful run |
| C9 Research and use | Which linked publications/adoption statements/outcome evidence are identifiable? | Separate publication, adoption and learning outcomes; no inference from stars or prestige |
| C10 Reuse | What explicit component licence or reuse notice is accessible? | Declared terms only, not legal ownership certification or approval of COMPNET policy |

Allowed cell statuses:
- DOCUMENTED: direct primary-source support for the precise stated feature.
- NOT_IDENTIFIED: not identified within the listed inspected sources and queries.
- ACCESS_LIMITED: relevant material could not be inspected (with exact limitation).
- NOT_APPLICABLE: dimension does not apply to this explicitly identified unit.
- MIXED: subclaims have different visibility, each explained and sourced.

Every NOT_IDENTIFIED cell must list what was inspected. Failure to retrieve a
page is not evidence that a feature is absent. An ambiguous course identity is
not replaced by an attractive unrelated course. Give each unit a declared type
and observed edition; an ecosystem row must name its constituent artefacts.

## Verification and reporting

Check all 18 by 10 cells for source references and scope. Verify every included
claim against its source, preferably with a second reviewer on consequential
corrections and weak cells. Automated or assistant cross-checks are not human
independent ratings or inter-rater reliability measurements. Preserve negative
and inconclusive results. Freeze the resulting corpus manifest and coding data.

Publish a separate English report and a Romanian phase report. Prepare a local,
reviewable repository patch linking the new comparison and accurately updating
the F3-R15 record. Preserve the historical scores/text, F3-R14 and native gates.
No remote write, merge, release, licence application or new CI run is included.

F3-R15 may advance only for the new dated current claims after traceability
verification. Historical score reproduction remains explicitly unverified;
neither a plan nor a URL list is sufficient for full closure.
