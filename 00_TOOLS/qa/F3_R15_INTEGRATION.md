# Integration of the dated F3-R15 comparison

Prepared on 17 November 2026 for the existing `audit/v1.5.0-remediation` branch.
This record accompanies a documentary successor to candidate commit
`8fb6afcd89eb3fa27b909941f96eff4276df8f29`.

## Two separate records

The [dated comparison](../../00_APPENDIX/docs/comparison/2026-11-17/README.md)
records the earlier documentary phase. Its complete eleven-file directory is
preserved without alteration, including the frozen corpus, source register and
validation record. Statements there about a local-only patch, no remote write
and the branch identity describe that phase at its recorded time.

This later change carries the same corpus into the candidate source and adds
this integration record. The exact commit, Git tree, remote branch verification
and any automatic CI outcome belong to the separate integration receipt. The
commit containing this record identifies this version; no self-referential
commit SHA is embedded in the file.

The comparison anchor remains the earlier commit and its 1,318-file tree.
Adding documentary files does not change the object that was compared.

## Change scope and finding status

The source change is documentary. The historical text and scores in
`SPECIAL_REPORT.md` remain byte-identical after its introductory pointers.
Only F3-R15 is updated in the remediation register; the other 202 finding
records, licence, workflow definitions and runtime files remain unchanged.

F3-R15 supplies a dated 18-unit, 180-cell descriptive corpus. Its historical
numerical score derivation and historical source provenance remain unverified.
The register retains `local_documentary_update` as a prior-phase record and
adds `candidate_integration` for this subsequent change. The finding is not
declared fully closed.

## Verification and acceptance identities

The inherited F5 evidence belongs to the earlier commit: 188 pytest passes and
14 current packaging checks, with 28 historical packaging checks kept separate.
Those results are not relabelled as executions of this successor.

The existing CI configuration runs the shared source gate on pushes and pull
requests. An automatic result for the exact new commit is a separate event;
it does not establish VM, Docker/Mininet, browser, Windows, LMS or workbook
acceptance. This change does not activate, modify or manually dispatch a
workflow.

The earlier F5 acceptance kit deliberately requires the earlier commit, tree
and complete source manifest. A successor must use a separately identified kit
whose contract and full manifest match that successor. Do not weaken the old
identity checks or replace old execution records. Equality of selected runtime
sources establishes source continuity, not new native execution.

## Remaining release gates

F3-R14 remains subject to the author's explicit licence decision. Option A has
not been approved or applied. The native gates in the
[acceptance record](REMEDIATION_v1.5.0.md) remain outstanding.

This candidate-branch update does not merge into `main`, move either historical
tag or publish v1.5.0. The already published v1.4.0 remains the preserved
baseline. The appliance remains a
[reference through its stable DOI](https://doi.org/10.5281/zenodo.24289763);
it is not requested or downloaded for this integration.
