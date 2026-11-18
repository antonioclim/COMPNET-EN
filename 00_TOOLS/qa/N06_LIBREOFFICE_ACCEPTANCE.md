# N06 — native workbook pagination and remaining acceptance

## Current record — 18 November 2026

**The default native Calc PDF passes the exercised print-layout checks on all
125 pages. Complete workbook acceptance remains open. X03 is PARTIAL:** GUI
Print Preview and Microsoft Excel have not been executed.

The [pagination attestation](evidence/libreoffice/2026-11-18/N06_PAGINATION_ATTESTATION.json)
records the exact inputs, authoring controls, native command and evidence hashes.
The base is `7753beb88a9f8589b34b92070d9737ecd4583dbd`, tree `098e63f085b78be4f1ab97e159e963243f3a4e35`. The tested workbook
`02_PROJECTS/RC2026_VERIFICATION_INDEX.xlsx` changes from SHA-256 `08128be05a3860c0e60661f271b6b1790a0ecfeb3237e38f894cf4c544970e67` to `5d6685976a6022890ee45de9ed5bd9733e3711ed51f234b6e90350a987b4982c`.
The native run preceded integration; the identity claim is the exact tested
workbook bytes, not an execution of every file in the later commit.

### Persistent print correction

The user explicitly confirmed the proposed narrow openpyxl route. Public print
APIs generated a settings-only skeleton; only its approved print nodes were
transplanted into the original OOXML. The original workbook was not roundtripped,
reserialised through a spreadsheet editor or recalculated.

RULES uses A4 portrait. INDEX and the 30 project sheets use A3 landscape. All
sheets fit one page wide with unrestricted vertical pagination and 10 mm outer
margins; the existing 0.3-inch header/footer offsets are preserved. Print areas
end at each sheet's last populated row. INDEX repeats row 1; projects repeat
rows 1–3. RULES has no repeated heading.

Independent read-only comparison confirms all 42 ZIP parts, 33 print-only changed
XML parts and nine byte-identical other parts. Removing only the approved print
insertions from every changed part recovers its exact prior bytes. All 8,669 cell
records, 7,290 non-empty values, 1,102 criterion IDs and status validations, five
formulas with their cached `Open` values, 25 relationship hyperlinks and 270 merged
ranges are preserved, together with styles, dimensions, panes and provenance.

### Native execution and complete PDF review

One default `pdf:calc_pdf_Export` ran in an isolated native Linux profile using
LibreOfficeDev 26.8.0.0.alpha0, build
`2c87e51eeaa2b413ff4ae097b2705eea1995d8e5`. It exited 0 with empty stderr;
the input and disposable copy remained unchanged and owned processes were reaped.
No `SinglePageSheets` override or native XLSX roundtrip was used in this phase.

The unmodified native PDF is 2,653,269 bytes, SHA-256
`ffbefa4d3121f27cc2ec107e69ca69e24d82e69f99c57a20d77b344aa49a3c6e`. It has 125 pages and 32 sheet bookmarks:
RULES one page, INDEX two, S01 and S02 five each, and every other project four.
The previous default exports of 231 and 419 pages remain historical evidence.

All 7,290 source values were reconciled with the PDF; all 1,102 criterion IDs
occur in column B and in source order. All 4,398 non-empty C–F criterion cells
were checked within their own row and column regions: 4,393 literal-normalised
matches and five font-run/glyph-order cases resolved with symbols retained.
Repeated headings, every Status cell boundary and A4/A3 dimensions pass.

Every one of the 125 full-page 96 dpi images was actually opened and visually
inspected. No material text clipping, overlap, missing column or split criterion
row was observed. Some section bands fall at a page bottom, with their first
criterion on the following page under repeated table headings; these presentation
limitations are recorded individually and were not hidden or treated as lost
content. Strict PDF reading covered 18,861 objects with no errors or warnings.

### Exported links and acceptance limits

The native PDF retains 30 unsuitable INDEX annotations: 25 worksheet-fragment
URIs have misplaced hotspots, and five formula-derived links have empty URIs.
The PDF is delivered byte-exact for printing, with its 32 native sheet bookmarks;
its link navigation is not accepted. No link was activated, and no PDF repair is
presented as native output. Workbook hyperlinks retain their original bytes.

| Criterion | Current status | Actual boundary |
|---|---|---|
| X01: opening | PARTIAL | Native import/export executed; GUI repair dialogues and Excel opening untested |
| X02: normal view | NOT_RUN | No native GUI sheet inspection |
| X03: print/export layout | PARTIAL | All 125 default-export pages checked; GUI Print Preview and Excel remain untested |
| X04: status and persistence | NOT_RUN | No dropdown selection, edited-status save/reopen or interactive validation |
| X05: student evidence | NOT_RUN | No student submission assessed |
| X06: navigation and instructions | NOT_RUN | No native link activation or complete instructional acceptance |

The 101 browser and 32 workbook forms remain blank `NOT_RUN` future acceptance
forms. This source correction does not establish VM, Windows/WSL, Docker,
Mininet/OVS, packet capture, LMS or browser acceptance. The development-build
result does not establish equivalence with other LibreOffice versions or Excel.

### Decision and source continuity

The patch changes the workbook and three concordant QA records, and adds this
dated attestation. The current administrative inventory is A945/B320/C84.
The approved A939/B320/C84 snapshot, intervening inventories, exact C84 list,
licence texts and complete F3-R14 decision are preserved. Only the workbook's
print bytes change among Category C; the other 83 paths remain byte-identical.
All 203 finding statuses and owner records remain unchanged. The eight current
workbook hashes are refreshed; the complete 17 November native receipt is kept
in `native_workbook_acceptance_history`, and the current receipt records the new
document identities. F3-R14's historical document hash is not rewritten.

N08 was not rerun. No merge to `main`, v1.5.0 tag/release, Zenodo modification or
closure of an unexecuted native gate is established by this record.

## Preserved historical record — 17 November 2026

The following earlier record retains its dated failures and limitations. Its
then-current X03 FAIL is superseded only by the scoped 18 November evidence
above; it is not rewritten into a historical PASS.

Recorded on 17 November 2026 for the v1.5.0 candidate. **Native Calc import,
PDF export and XLSX export were executed. Full workbook acceptance remains
open, and X03 print-layout acceptance still fails.**

The machine-readable [attestation](evidence/libreoffice/2026-11-17/N06_ATTESTATION.json)
records the actual inputs, outputs, command receipts and evidence hashes.
The F6 continuation dossier retains the failed original export, corrected
export, raw logs, structural comparisons and selected visual-review images.

### Source and runtime identity

| Item | Identity |
|---|---|
| Repository | `antonioclim/COMPNET-EN` |
| Baseline candidate | `efe829c5bec7e80078e5b88e81151dcc4d94f1d5` |
| Baseline tree | `e67b8b63eab2234f2cd7bd31379ab17a2c19c1e1` |
| Workbook | `02_PROJECTS/RC2026_VERIFICATION_INDEX.xlsx` |
| Original workbook SHA-256 | `0832263c17ded112cf8bb9479b074ab4bfcbb5647db4a4b52f720e7c27707ef9` |
| Repaired workbook SHA-256 | `08128be05a3860c0e60661f271b6b1790a0ecfeb3237e38f894cf4c544970e67` |
| Actual engine | LibreOfficeDev 26.8.0.0.alpha0, build `2c87e51eeaa2b413ff4ae097b2705eea1995d8e5` |
| Execution route | Native Linux headless CLI, separate disposable input copies and explicit isolated profiles |

The retest ran on the repaired workbook bytes before their integration commit
existed. Integration must preserve that exact hash. This proves the identity of
the tested workbook, not a native run of every file in the later commit. The
engine is a development build; Microsoft Excel and other LibreOffice versions
were not tested.

### What actually ran

Both the original workbook and the repaired copy were passed separately through
the installed `soffice` executable with these native conversion filters:

- `--headless --nologo --norestore --convert-to pdf:calc_pdf_Export`
- `--headless --nologo --norestore --convert-to "xlsx:Calc MS Excel 2007 XML"`

Each invocation used an explicit `-env:UserInstallation=file:///...` profile,
a separate output directory and a 90-second timeout. All four conversions
returned exit code 0 with empty stderr, and their owned processes were reaped.
Version/help probes and exact argument arrays are recorded separately. No
package installation, macro execution, UNO automation or link activation was
performed. The original and selected input bytes remained unchanged by testing.

| Native PDF | Pages | Visual sample | Result |
|---|---:|---:|---|
| Original workbook | 231 | 9 pages | Vertical clipping, RULES right-edge clipping and fragmented print context observed |
| Repaired workbook | 419 | 17 pages | Previously clipped text is readable in the reviewed samples; horizontal fragmentation and missing repeated headers remain |

The original pages reviewed were 1, 2, 3, 4, 6, 7, 8, 9 and 231. The retest
pages reviewed were 1, 2, 3, 4, 6, 7, 10, 11, 14, 15, 156, 160, 315, 319, 405,
409 and 419. These samples include RULES, INDEX, A01, S03, S14 and S20. The
images were rendered from actual Calc PDF output and visually inspected;
extractable PDF text alone was not treated as proof of legibility. Neither PDF
received an all-page visual acceptance review.

### The source correction and its limits

The integrated workbook is the second layout correction, authored from the
original candidate through the documented artifact-tool API. It changes
**1,330 row heights and the RULES column A width from 130 to 92**. There are
no `wrapText` changes. The complete `xl/styles.xml` and document-provenance
parts remain byte-identical to the original. Generated relationship identifiers
were reserialised, with their targets, types and modes preserved. The changed
RULES column explicitly serialises `hidden=0`; its visibility is unchanged.

Two separate structural comparisons preserve all 32 sheets and their order,
7,290 populated values, 1,102 criterion IDs, 1,102 validation cells, five
formula records and 25 internal relationship hyperlinks. Merged cells, panes
and defined names are also preserved. These comparisons establish structural
preservation; they do not establish interactive behaviour.

The larger row heights expose text that was previously hidden. They also
increase the PDF from 231 to 419 pages. Horizontal print pagination still
separates IDs and criteria from evidence, commands and status. Some merged
titles and section bands remain clipped across those boundaries, and
continuation pages have no repeated headers. **X03 remains FAIL.** The
available authoring API did not expose documented paper, fit-to-page or
repeated-print-heading controls; those settings were not invented or changed
through undocumented interfaces.

### Native roundtrip observation

Both native XLSX outputs preserve the inspected cell values, formula text,
criterion IDs and validation memberships. LibreOffice adds `aca=false` to the
five formulas and `formula2=0` to the list validations. It also rewrites the
25 existing INDEX relationship hyperlinks to the disposable input-copy path
plus a worksheet location. This link-context change is retained as an
unfavourable compatibility observation; link activation was not executed.

**The LibreOffice roundtrip XLSX is evidence only.** It was not used as the
source correction or committed to the repository. The integrated workbook
retains the original 25 hyperlink targets and the five formula hyperlinks.

### Acceptance status

| Criterion | Status | Boundary |
|---|---|---|
| X01: opening | PARTIAL | Native import/export executed; GUI opening, repair dialogues and Excel opening untested |
| X02: normal-view inspection | NOT_RUN | No native GUI sheet, symbol or readability inspection |
| X03: print/export layout | FAIL | Reviewed vertical-clipping examples repaired; horizontal pagination and headers unresolved |
| X04: status input and persistence | NOT_RUN | No native dropdown selection, edited-status save/reopen or validation interaction |
| X05: student-evidence acceptance | NOT_RUN | No actual student submission was assessed |
| X06: navigation and instructions | NOT_RUN | No native hyperlink activation or full S/A Flex instruction acceptance |

The blank successor acceptance forms retain their 101 browser rows and 32
workbook rows as `NOT_RUN`. This dated partial native record is separate from
those unexecuted complete acceptance forms. Browser preparation and synthetic
navigation assertions are also separate; no candidate page was accepted in a
native browser during F6.

### Preserved decisions and remaining work

The workbook remains one of the exact 84 Category C paths. Its layout bytes
change in this phase; the other 83 Category C files remain byte-identical to
`efe829c5`. The licence policy, exact C84 list, standard licence texts, author
approval and F3-R14 decision remain unchanged. The two added QA documents are
administrative Category A paths under the existing rules; they do not alter
the approved A939/B320/C84 snapshot or the workbook's rights boundary.

All 203 finding statuses and historical owner records are preserved. Only the
eight current workbook hashes in the maintainer register are refreshed, and a
separate `native_workbook_acceptance` receipt is appended. In particular,
F3-R14's recorded remediation-document hash remains evidence of its original
application at `efe829c5`; the new receipt records the current document hash.

The [remaining release gates](REMEDIATION_v1.5.0.md#remaining-release-gates)
still apply. No appliance download, VM acceptance, Docker/Mininet/OVS or tshark
acceptance, Windows/WSL acceptance, LMS import, merge to `main`, v1.5.0 tag or
release, or Zenodo modification is established by this record. N08 retains its
separate Kotlin/JVM source identity and was not rerun.
