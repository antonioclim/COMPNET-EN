# Public networking teaching materials: dated descriptive comparison

**Observation date: 17 November 2026. Status: local review document for F3-R15.**

This comparison documents observable public materials for **18 units: the fixed
COMPNET-EN candidate and 17 external units**. Every C1–C10 cell has a bounded
claim, source identifiers and an explicit limitation. It supplies a new evidence
base for present descriptions. It does not reproduce the February 2026 study or
validate its numerical scores.

The anchor is COMPNET-EN v1.5.0 candidate commit
`8fb6afcd89eb3fa27b909941f96eff4276df8f29`, tree
`5884c293f2ec944a42a92c189ab6c178714c8e03`. Inventory statements refer to that
tree, before this documentary patch. The published v1.4.0 baseline is preserved.

## 1. Method and selection

The [protocol](PROTOCOL.md) was frozen before external collection, at
16:13:22.923724 UTC on 17 November 2026 (18:13:22 in Bucharest). Its SHA-256 is
`a036146226cc907d48d4e450e20acf6fa287bedbac541a2eaf717b02b0aa8c21`.
U01–U13 follow the historical report's final source table. U14–U17 are its four
additional visibility-table entries. This reconciles the new selection; it
does not establish the historical sample or a representative university ranking.

The unit of analysis is an explicitly identified course, course component or
framework. Public primary sources were inspected within a fixed search and
artefact budget. Repository metadata and trees route collection; they are not
automatically evidence that every listed file was read. Dates of access are
separate from course editions, document revisions and Git commit dates.

The canonical [CORPUS.json](CORPUS.json) contains all **180 cells**. The
[source register](SOURCES.md) and [machine-readable provenance](SOURCES.json)
resolve their identifiers to URLs, owners, actual access times, acquisition
methods and precisely labelled hashes. [COLLECTION_LOG.json](COLLECTION_LOG.json)
retains searches, failures and retrieval limits. A failed route never establishes
that the material or feature is absent.

The sample includes a purpose-built author kit with richer inherited verification
evidence than the external document sample. External code, grading systems and
workflows were not run. Comparability is therefore descriptive and dimension
specific; document visibility cannot be converted into a quality score.

## 2. Observed identities and editions

| ID | Unit and type | Observed edition/component |
|---|---|---|
| U00 | ASE-CSIE COMPNET-EN; integrated course kit | v1.5.0 candidate, commit 8fb6afcd89eb3fa27b909941f96eff4276df8f29 [CP001](SOURCES.md#cp001) |
| U01 | Stanford CS144; Dated course and its public starter-code component | Fall 2026; Imp source head dated 2026-09-29 [US014](SOURCES.md#us014) [US042](SOURCES.md#us042) |
| U02 | ETH Zurich Communication Networks / mini-Internet; Course-associated practical platform | Repository snapshot 006ec471cb90df12a6da179499b79cbb39a4c7ad (commit dated 2026-07-03); inspected assignment locator explicitly names 2024. [FW001](SOURCES.md#fw001) [FW002](SOURCES.md#fw002) |
| U03 | UC Berkeley CS168; Dated course with textbook and project documentation | Fall 2026 course; textbook source head dated 2026-10-01 retains a Fall 2024 maintenance notice [US011](SOURCES.md#us011) |
| U04 | CMU 15-441/641; Archived course landing and separately pinned public project template | Fall 2022 course landing; TCP template head dated 2026-09-24 does not state its course offering [US012](SOURCES.md#us012) |
| U05 | Princeton COS461; Historical public assignment repository with cross-course provenance evidence | Fall 2021 assignments, identified by COS461_F2021 hand-in URL; source head dated 2021-11-04 [US040](SOURCES.md#us040) |
| U06 | Michigan EECS489; Dated course repository and bundled project component | Winter 2025 (W25), default branch w25; source head dated 2025-05-11 [US033](SOURCES.md#us033) [US028](SOURCES.md#us028) |
| U07 | Georgia Tech CS 6250 Computer Networks; Online graduate course: public landing page and sample syllabus | Fall 2026 sample syllabus; landing page accessed 17 November 2026 [AO005](SOURCES.md#ao005) |
| U08 | KAIST CS341 / KENSv3; Course-associated C/C++ network simulation framework | master@7dfa45c6356a02b1ba330b6e900a759fdebd9809, committed 28 March 2026; CMake project version 3.3.8 [AO017](SOURCES.md#ao017) |
| U09 | UCLouvain CNP3 ebook and INGInious exercises; Textbook and exercise ecosystem | Third-edition ebook snapshot 5d270364790500fe58283be91329365835a69d66 (commit dated 2025-06-04), plus undated live CNP3 exercise catalogue. [FW012](SOURCES.md#fw012) [FW016](SOURCES.md#fw016) |
| U10 | NPS Labtainers; Laboratory framework and exercise collection | Repository snapshot fc1baca0aa2abe2809d92fbc9e93f5ce719b597e (commit dated 2026-11-06); README labels distribution v1.4.4n and 09/11/2026 11:33 without declaring the date format. [FW020](SOURCES.md#fw020) |
| U11 | Johns Hopkins EN.601.414/614; Historical course and linked assignment repositories | Fall 2020, identified by syllabus, Piazza link and final-exam schedule; source heads in November/December 2020 [US025](SOURCES.md#us025) |
| U12 | CUHK CSCI4430 / ESTR4120 Computer Networks; Course repository with lectures, tutorials and assignment starter materials | Fall 2025 term 1; 2025_fall@aac3e1e9a785c138da5d1ac8954470102571b522 [AO023](SOURCES.md#ao023) |
| U13 | University of Illinois Urbana-Champaign CS/ECE 438 Computer Networks; Cross-listed course: institution-indexed course site on Notion | Fall 2026 Notion course page; instructor homepage lists earlier Fall 2024/2025 editions [AO013](SOURCES.md#ao013) |
| U14 | MIT 6.5820 Computer Networks; Graduate networking course: official catalogue and numbering evidence | Fall 2026 catalogue; course renumbering introduced Fall 2022 [AO036](SOURCES.md#ao036) |
| U15 | Imperial networks course — unresolved legacy identity; Ambiguous legacy course label | Undated indexed institutional module descriptors accessed 2026-11-17; legacy course identity and edition remain unresolved. [FW024](SOURCES.md#fw024) [FW025](SOURCES.md#fw025) |
| U16 | TUM Advanced Computer Networking IN2097; University course | Advanced Computer Networking IN2097, winter semester 2026/27; project updated 2026-11-11. Tutorial captures at one live URL show document updates 2026-10-29 and 2026-11-16. [FW028](SOURCES.md#fw028) |
| U17 | National University of Singapore CS2105 Introduction to Computer Networks; Undergraduate course: current institutional outline plus explicitly archived assignment | AY 2026/27 institutional schedule; detailed Assignment 1 is Semester 2 AY 2013/14 [AO044](SOURCES.md#ao044) [AO042](SOURCES.md#ao042) |

Imperial remains an unresolved legacy identity: descriptors 50005 and 70041 are
candidates, not interchangeable substitutes. CMU's Fall 2022 course page and
its separately dated TCP template are not represented as one verified 2026
offering. NUS's current schedule is not evidence that its archived assignment is
still used. These limits are retained in the individual cells.

Auxiliaries are outside the 18-unit matrix. Containerlab and SEED were inspected
as project context ([AX002](SOURCES.md#ax002), [AX003](SOURCES.md#ax003)); INGInious
is part of the CNP3 row ([FW016](SOURCES.md#fw016)). Kathara was retained as a
legacy contextual name but was not substantively collected. None is counted as
an additional independent course.

## 3. Evidence map

C1 concerns scope; C2 code practices; C3 teaching and feedback; C4 environment;
C5 documentation; C6 practical work; C7 documented web interaction; C8
verification; C9 research and use; C10 declared reuse terms. Operational
definitions and exclusion rules are in the protocol.

**D = DOCUMENTED; M = MIXED; N = NOT_IDENTIFIED; A = ACCESS_LIMITED;
X = NOT_APPLICABLE.** These labels qualify the particular claim in the corpus.
They are not ordinal grades. A documented licence or test configuration is not
a certification of ownership or a successful test run.

| Unit | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|---|---|---|---|---|---|---|---|---|---|---|
| U00 | D | D | D | D | D | D | D | D | N | M |
| U01 | D | D | D | D | D | D | M | M | N | M |
| U02 | D | M | D | D | M | D | D | D | D | M |
| U03 | D | D | D | D | D | D | D | D | N | D |
| U04 | D | D | D | D | D | D | M | D | N | D |
| U05 | D | D | D | D | D | D | M | D | M | N |
| U06 | D | D | D | D | D | D | M | D | M | M |
| U07 | D | N | D | M | D | D | D | N | N | N |
| U08 | D | D | D | M | M | D | M | D | M | D |
| U09 | D | D | D | D | D | D | M | D | D | M |
| U10 | D | D | D | D | D | D | D | D | D | M |
| U11 | D | D | D | D | D | D | M | D | N | N |
| U12 | D | D | D | D | D | M | D | D | N | D |
| U13 | D | A | D | M | D | D | D | M | N | N |
| U14 | D | N | D | N | M | D | N | N | N | N |
| U15 | M | A | M | M | M | M | M | A | A | A |
| U16 | D | D | D | M | D | M | D | D | D | M |
| U17 | D | M | M | M | M | M | M | M | N | N |

Across the 180 cells: **111 DOCUMENTED**, **42 MIXED**, **22 NOT_IDENTIFIED**, **5 ACCESS_LIMITED**, **0 NOT_APPLICABLE**.

These totals describe coding coverage only. No score, weighting, aggregate
performance measure or institutional ranking was calculated. Reading an N cell
requires its listed inspected sources; reading an M or A cell requires its
limitation. The status table alone must not be reused as a feature checklist.

## 4. Consequential observations for current descriptions

| Unit | Supported current observation | Interpretation and evidence |
|---|---|---|
| Stanford | Fall 2026 uses Imp and C++23. The public README places most tests on the Stanford submission server. | Update the version and public-access scope; do not retrospectively falsify the older Minnow snapshot. [US042](SOURCES.md#us042), [US047](SOURCES.md#us047) |
| Berkeley | Project 2 has staged tests, prediction–observation prompts and browser-controlled network visualisation. Textbook notes carry a beta/not-proofread notice. | Current claims of no explicit scaffolding or a professionally edited textbook are unsupported. Course interaction and textbook features remain distinct. [US003](SOURCES.md#us003), [US002](SOURCES.md#us002) |
| ETH | Containers correspond to network components; the publication is a 2020 CCR article. | Do not describe one container per autonomous system or mislabel the article's venue. [FW001](SOURCES.md#fw001), [PB001](SOURCES.md#pb001) |
| Michigan, Princeton, JHU | Inspected editions are Winter 2025, Fall 2021 and Fall 2020, respectively. | These identify the current snapshots, not what was accessed in February 2026. [US033](SOURCES.md#us033), [US025](SOURCES.md#us025), [US027](SOURCES.md#us027) |
| Georgia Tech | A Fall 2026 sample syllabus is public; it lists five regular-semester projects. | The institution labels it a sample. Canvas delivery and grader implementation were not inspected. [AO001](SOURCES.md#ao001), [AO005](SOURCES.md#ao005) |
| KAIST | The pinned KENSv3 tree lists seven workflow files; one representative workflow was inspected. | File presence does not establish seven successful runs. The 2015 paper describes KENSv2. [AO011](SOURCES.md#ao011), [AO019](SOURCES.md#ao019), [AO022](SOURCES.md#ao022), [PB003](SOURCES.md#pb003) |
| CNP3 | The inspected source contains a GitHub Actions Pages workflow; README and book sources show different reuse notices. | Describe the actual configuration and notice scope. No workflow success or legal precedence is inferred. [FW010](SOURCES.md#fw010), [FW012](SOURCES.md#fw012), [FW013](SOURCES.md#fw013), [FW014](SOURCES.md#fw014) |
| Labtainers | Manuals distinguish instructor assessment, student checks and optional formative quizzes. | Framework classification does not imply absence of teaching support; an instructor interface is not a student slide feature. [FW020](SOURCES.md#fw020), [FW021](SOURCES.md#fw021), [FW022](SOURCES.md#fw022) |
| CUHK | README lists three assignments; the pinned public tree contains two assignment directories. | Public directory count is not total taught workload. The ESTR project remains separately identified. [AO023](SOURCES.md#ao023), [AO012](SOURCES.md#ao012) |
| UIUC | The resolved CS/ECE438 page is Fall 2026; two assignment-PDF retrieval routes failed with 404. | The course page is evidence of structure, while the failed routes limit implementation claims. [AO013](SOURCES.md#ao013), [AO034](SOURCES.md#ao034), [AO035](SOURCES.md#ao035) |
| MIT | The current catalogue identifies 6.5820 together with 6.5821. | Current identity is established; the 2002 OCW materials were not substituted for current handouts. [AO036](SOURCES.md#ao036) |
| TUM | WS 2026/27 has public course materials, including router-project and Jupyter instructions. | Public documentation and authenticated execution infrastructure are separate access layers. This does not reconstruct WS 2025/26. [FW028](SOURCES.md#fw028), [FW033](SOURCES.md#fw033), [FW034](SOURCES.md#fw034) |
| NUS | AY 2026/27 confirms the offering; the inspected detailed assignment is from 2013/14. | Archived code, grading and environment instructions are not attributed to the current edition. [AO044](SOURCES.md#ao044), [AO039](SOURCES.md#ao039) |

### Publication, reuse and outcomes

Four DOI records were verified against registration metadata and primary
institutional or author records; complete references and resolution notes are
in [PUBLICATIONS.json](PUBLICATIONS.json). This verifies publication identity,
not the quality of a full paper or the effectiveness of a current teaching kit.
The KENSv2/KENSv3 boundary is explicit. The NPS 2021 workshop is not promoted
to an additional research article. SEED is contextual to the study.

Cross-unit provenance matters. JHU acknowledges Princeton-origin exercises;
CUHK reports reuse of Michigan materials. This provides limited evidence about
downstream use of those source materials. It does not establish adoption of an
entire course, use of the exact Princeton 2021 or Michigan w25 snapshot, or
learning outcomes. For JHU and CUHK, crediting an upstream source is recorded
as provenance rather than proof of their own downstream adoption. CNP3's
reported Saylor use is likewise an author-reported reuse statement.
([US017](SOURCES.md#us017), [US019](SOURCES.md#us019),
[AO023](SOURCES.md#ao023), [FW013](SOURCES.md#fw013).)

No independent learning-outcome evaluation of COMPNET-EN was identified in the
selected project documents and exact-name query. That bounded result neither
proves universal absence nor turns self-report mirrors into independent
evaluation. [CP011](SOURCES.md#cp011) records the excluded mirror and scope.

## 5. What the COMPNET-EN anchor establishes

The fixed candidate has 1,318 files, including 413 Markdown files, 401 PlantUML
sources, 171 Python files and 101 HTML files. Its catalogue contains 30
alternative project briefs and its lab runner registers 18 lab definitions.
These are different inventory units, not equivalent workloads or successful
deployments. The new documentary patch is not included in those base counts.
([CP009](SOURCES.md#cp009).)

The source documents a fourteen-week structure, a model–observation–explanation–
transfer approach, formative bridge exercises and Python/Docker/Mininet
pathways. These are identifiable design choices. The comparison does not prove
their uniqueness or superior learning effects.
([CP001](SOURCES.md#cp001), [CP003](SOURCES.md#cp003), [CP004](SOURCES.md#cp004).)

CI invokes the shared source gate. Earlier F5 evidence records **188 pytest
passes and 14 current packaging checks**; this phase did not rerun them. The
28 historical packaging checks remain a separate historical set. Source
parsing and regressions do not constitute a repository-wide Python lint/type
gate, native browser acceptance or full network-lab execution.
([CP005](SOURCES.md#cp005), [CP006](SOURCES.md#cp006), [CP010](SOURCES.md#cp010).)

### Practical implications

The following are design inferences from the evidence, not measured benefits:

- Retain explicit links between each student's task, expected observation and
  evidence to submit. The Berkeley and Stanford examples provide concrete
  reference patterns for staged feedback; they do not justify claiming this
  approach is unique to COMPNET-EN.
- Describe verification by its executed scope. Strengthening a future code
  quality gate would require a separate implementation decision and meaningful
  regression checks; inspecting other frameworks' configuration is insufficient.
- Preserve the distinction between alternative project breadth and the depth of
  a progressive implementation. Selecting a suitable learning path requires
  stated prerequisites and objectives, not comparing raw assignment totals.
- Keep scholarly evaluation separate from engineering acceptance. Any future
  learning study needs its own design, participants, measures and actual data;
  public artefact counts cannot supply those results.

## 6. Reproducibility and limits

The record contains 146 provenance entries, including routing,
publication metadata and failed attempts. This is not a claim that
146 complete independent documents were read. Exact Git commit and
blob identifiers support immutable retrieval where available. SHA-256 values
for tool-returned JSON or text identify those saved responses; they are not
hashes of the original web pages or PDFs.

Raw external pages, papers and code were retained for working inspection and
are excluded from distribution. The distributed register supplies concise
claims and provenance, not a full-text archive. Consequently a live-page
fingerprint cannot guarantee future recovery of that page. The supplied
verification record distinguishes hashes checked against working artefacts
from structural checks that can be repeated using this distributed dossier.

One unplanned retrieval variation is preserved: the same TUM instructions URL
returned revisions dated 29 October and 16 November. Eight distinct artefact
URLs were inspected for TUM; this one URL yielded two revisions. The variation
was discovered during continuation of retrieval, not declared prospectively.
Both response fingerprints are retained; coding uses their common documented
features. No immutable PDF identity or retrospective pre-registration is
claimed. [FW034](SOURCES.md#fw034).

The sampling is purposive, the inspected artefacts per unit are bounded and the
unit types and editions are heterogeneous. Authenticated systems are outside
scope. Search results establish visibility only within the recorded queries.
The cross-checks are procedural reviews, not an independent human-rating study;
no inter-rater reliability statistic was calculated. No external software,
browser application, VM, container or workflow was executed for this comparison.

## 7. F3-R15 disposition and remaining gates

The present descriptive claims have a frozen protocol, an identified corpus,
dated sources and cell-level traceability. The local patch adds this report,
links it from the historical report and updates only the F3-R15 finding record.
**F3-R15 remains partially open for historical score provenance.**

The original historical report is preserved byte for byte after the new
introductory pointer. Its prior SHA-256 is
`33ecbecf179322234e8d3b09339b06d6da838d5f80e4ac335128d7ffa0b1d3db`.
Its scores, unfavourable findings and historical access account have not been
rewritten. The missing source captures, selection log and scoring derivation
cannot be supplied retrospectively from this new corpus. The unrecovered later
F4 chat response remains unrecovered; a recoverable F3 response is not labelled
as the latest chronological message.

| Gate | Status after this documentary work |
|---|---|
| Current comparison | Dated factual corpus supplied and checked; local review patch only |
| Historical numerical comparison | Original score derivation and historical source provenance remain unverified |
| F3-R14 licence decision | Open; prepared Option A remains unapproved and unapplied |
| F6/native acceptance | Outstanding in the required environments; this study does not begin or complete it |
| Remote integration/release | No push, pull request, merge, new Actions run or release performed in this phase |
| Appliance | Reference only: [stable Zenodo DOI](https://doi.org/10.5281/zenodo.24289763); no OVA retrieval |

The base candidate commit remains the published branch identity. A local patch
has its own hash and proposed tree in the phase record; it is not a published
v1.5.0 commit or release. See [VALIDATION.json](VALIDATION.json) for the exact
documentary checks and their limits, and [CORPUS_FREEZE.json](CORPUS_FREEZE.json)
for the frozen study-file hashes.

## References

Holterbach, T., Bühler, T., Rellstab, T., & Vanbever, L. (2020). An open platform to teach how the Internet practically works. ACM SIGCOMM Computer Communication Review, 50(2), 45–52. https://doi.org/10.1145/3402413.3402420

Thompson, M. F., & Irvine, C. E. (2018). Individualizing cybersecurity lab exercises with Labtainers. IEEE Security & Privacy, 16(2), 91–95. https://doi.org/10.1109/MSP.2018.1870862

Lee, K., Kim, J., & Moon, S. (2015). An educational networking framework for full layer implementation and testing. In Proceedings of the 46th ACM Technical Symposium on Computer Science Education (pp. 663–668). Association for Computing Machinery. https://doi.org/10.1145/2676723.2677304

Du, W., & Wang, R. (2008). SEED: A suite of instructional laboratories for computer security education. Journal on Educational Resources in Computing, 8(1), 1–24. https://doi.org/10.1145/1348713.1348716
