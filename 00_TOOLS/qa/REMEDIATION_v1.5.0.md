# v1.5.0 candidate — remediation and acceptance record

Prepared on 17 November 2026. This is a source candidate, not a published release
or a declaration that every supported environment has passed acceptance.

## Version identity

| Item | Identity and status |
|---|---|
| Preserved release | [v1.4.0](https://github.com/antonioclim/COMPNET-EN/releases/tag/v1.4.0) |
| Audited baseline commit | `8b10df86bdd9dae33a7aa82beb580fa449c530ea` |
| Baseline Git tree | `4b58433c4e2c5e2d779f7d064af9a561acf184c2` |
| Proposed source release | v1.5.0; review and environment acceptance pending |
| Appliance | MININET-SDN 1.0.0, distributed independently through [Zenodo](https://doi.org/10.5281/zenodo.24289763) |

The appliance bytes, DOI and checksum have not been changed by this source audit.
Historical package version strings are retained where they identify historical
material; they are not all aliases for the proposed GitHub release version.

## What changed

- Reconcile the Python bridge, optional lectures, weekly quizzes, seminar
  protocols and project briefs with executable paths in this repository.
- Correct TCP framing, partial I/O, connection ownership, interrupted quiz
  sessions, scoring and LMS export structure. Add regressions against the actual
  implementations, including failure cases that previously produced false passes.
- Correct lecture and seminar service configurations, cleanup and error
  propagation, protocol assumptions, TLS identity handling and HTTP state logic.
  Corrected source is not evidence that the complete Compose/Mininet stack ran.
- Repair slide navigation, answer controls and asynchronous copy feedback.
  Label prewritten demonstrations as simulations and link them to canonical labs.
- Reconcile project acceptance criteria, evidence capture, PCAP rules and the
  verification workbook while preserving the author's assessment structure.
- Align local checks, GitHub CI and release packaging, preserve recorded
  executable permissions and prevent packaging an uncommitted source state.
- Correct verified bibliography errors and qualify unsupported comparative
  claims. Preserve the original report in the v1.4.0 snapshot.

## Evidence levels

The cumulative audit contains **203 finding families**, not 203 independent
runtime tests. Some families span several areas and have more than one owner.
The [maintainer remediation register](ro_REMEDIATION_v1.5.0.json) records the source changes and evidence
for each family. Counts of checks from different reports must not be added when
the same test also appears in the integrated pytest run.
It retains the original Romanian finding titles and acceptance criteria so that
the author can trace each correction to the agreed audit record.

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| Source inventory, hashes, syntax and reference checks | File identity, parseability, recorded modes and checked targets | Successful deployment or pedagogical completeness |
| Native Python/C/Java/Node probes and the separately dated Kotlin/JVM probe | The exercised implementation behaviour in each recorded Linux environment | Equivalent behaviour in every guest, OS or complete lab |
| Test doubles and DOM models | The explicitly modelled protocol/control contracts | Real SSH/MQTT service acceptance or native browser accessibility |
| PlantUML generation and visual inspection | Renderability and reviewed diagram content | The network behaviour depicted in a diagram |
| OOXML checks and workbook preview | Workbook structure, tables, values and inspected rendering | Excel/LibreOffice interaction, recalculation or dropdown acceptance |
| Dated native LibreOffice import/export and PDF review | Actual Calc conversion and the observed layout repair on exact workbook bytes | Complete print-layout acceptance, GUI interaction or Microsoft Excel equivalence |

Run the same source gate as CI from a full checkout:

```bash
python3 -m venv .venv-qa
. .venv-qa/bin/activate
python -m pip install -r 00_TOOLS/qa/requirements.txt
python 00_TOOLS/qa/run_checks.py
```

Bash and Node.js 24 must also be available. The gate does not install or start
Docker, Mininet, VirtualBox or a browser. See [CI details](../../00_APPENDIX/docs/ci_setup.md)
and [release packaging](../release/README.md).

## Licence policy decision applied

On 17 November 2026 Antonio Clim explicitly approved the reconciled Option A
and authorised its application on the candidate branch. **F3-R14 is resolved
for the approved licence policy.** The [decision and application record](LICENCE_DECISION_PENDING.md)
preserves the actual approval, exact policy hashes and earlier pending history.
CC BY-NC-SA 4.0 applies to Category A and GPL-3.0-or-later to Category B;
Category C remains the exact 84-path list, subject to existing grants and
third-party terms. The three added policy documents have their applicable
notices; their administrative inventory labels do not override those terms.
The approved 1,343-path classification is A939/B320/C84; this application adds
three administrative paths. It does not establish new native environment
acceptance or close the environment, comparative-history or publication gates
below. Earlier component results retain their recorded source identities.

## Partial native workbook acceptance

The [N06 LibreOffice record](N06_LIBREOFFICE_ACCEPTANCE.md) documents actual
native import, PDF export and XLSX export of both the `efe829c5` workbook and
its layout correction. The first PDF exposed clipped text. The correction
changes 1,330 row heights and the RULES column A width while preserving values,
formulas, IDs, validations, link targets, styles and document provenance.
Seventeen pages of the corrected native PDF were visually inspected.

Previously clipped text is readable in those reviewed samples, but horizontal
pagination and unrepeated headers remain: **X03 is still FAIL**, X01 is partial,
and the other interactive workbook criteria remain unexecuted. The correction
increases the native PDF from 231 to 419 pages. The native XLSX roundtrip also
rewrites 25 hyperlinks to the disposable input-copy context; that output is
retained as evidence and is not the integrated workbook.

The workbook remains Category C. Only that one Category C file changes in this
phase; the other 83 retain their bytes. The exact C84 membership, licence texts
and F3-R14 decision remain unchanged. The two new QA documents bring the
current administrative inventory to A944/B320/C84 without changing the approved
A939/B320/C84 snapshot or the intervening A942/B320/C84 application record.

## Remaining release gates

1. **Appliance and host routes.** Import/boot, host-to-guest SSH, the VM Python
   environments, native Windows PowerShell and the supported WSL/Desktop routes
   require acceptance in their actual environments. The institutional provisioning
   script was not present in this repository and is outside the inspected source.
2. **Complete network labs.** Docker builds/start-up, DNS/FTP/mail/MQTT stacks,
   packet capture with tshark, Mininet/OVS/OpenFlow and the integration lab require
   their native end-to-end probes. Use the corrected scenario READMEs and preserve
   their evidence; do not treat a parser or mock result as a substitute.
3. **Student interfaces and exports.** Native browser keyboard/clipboard/layout
   checks, Moodle/QTI import and Excel/LibreOffice workbook interaction remain.
   N06 records partial native Calc conversion and an observed layout repair;
   the failed full print-layout gate and unexecuted interaction checks remain
   open, as detailed above.
   The separate [N08 Kotlin/JVM record](N08_KOTLIN_ACCEPTANCE.md) now verifies
   compilation and the bounded Rosetta echo/EOF scenarios on its pinned
   Linux/JVM input. This result does not close the interface/export gates.
4. **Comparative study.** A separately dated [public-material comparison](../../00_APPENDIX/docs/comparison/2026-11-17/README.md)
   now supplies a frozen protocol, 18 identified units, 180 factual cells and
   dated source provenance. This dated documentary update supports its new
   bounded claims. F3-R15 remains partially open because the historical score
   derivation and February source captures are still unverified. The old text
   and unfavourable results are preserved; no new numerical ranking is supplied.
   The [integration note](F3_R15_INTEGRATION.md) distinguishes this candidate
   update from the frozen comparison phase and preserves acceptance identities.
5. **Publication.** Review the exact candidate commit and its CI results before
   approving integration and creating v1.5.0. The v1.4.0 tag is the preserved
   baseline and must not be moved to the candidate.

Passing the available checks supports review of the candidate. It does not close
the gates listed above or justify a claim of universal correctness.
