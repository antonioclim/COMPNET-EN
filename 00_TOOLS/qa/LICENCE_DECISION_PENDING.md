# Licence policy decision — Option A approved and applied

Audit reference: **F3-R14**. Decision date: **17 November 2026**
(Europe/Bucharest). Antonio Clim explicitly approved the reconciled Option A
for base candidate `932b27a7962ad577892e0ee120f640fbc335e90c` and authorised its application and integration on
`audit/v1.5.0-remediation`.

This record forms part of the candidate commit applying the approved policy.
The external integration receipt identifies that resulting commit and its
verification. The retained filename preserves existing links; the earlier
pending-decision record is reproduced as historical material below.

## Author approval

The actual approval message is preserved in its original Romanian in the
[maintainer remediation register](ro_REMEDIATION_v1.5.0.json), under finding
`F3-R14`, field `licence_policy_application.author_approval_original_ro`.
That decoded value retains the exact message and its final newline; it is
distinct from the draft previously supplied for consideration. The message
approves the full reconciled dossier, its category mapping and exact reserved
list, the policy application, concordant record updates, verification and
integration on the named candidate branch. Its exclusions are retained below.
The calendar date is recorded above; no exact message timestamp was supplied.

Approval text SHA-256 (UTF-8, LF and one final newline):
`6db4bf349b4c55d30b3a385f89b0a17d31a11ff19355597621f7e7f966aada44`.

## Applied policy and scope

- Category A retains CC BY-NC-SA 4.0; Category B retains GPL-3.0-or-later.
- Category C is the exact unchanged list of 84 paths. Existing grants,
  component-specific third-party terms and applicable exceptions take precedence.
- The approved 1,343-path inventory is A939/B320/C84. The three added policy
  documents produce 1,346 paths, with administrative mapping A942/B320/C84.
  The GNU and Creative Commons licence texts retain their own notices and terms;
  the administrative A label does not relicense them.
- The mandatory Kotlin QA configuration is explicitly included in Category B.
  No general rule moves documentary JSON reports into that category.
- Additional commercial restrictions and mandatory research citation are not
  imposed on GPL-covered material. The automatic 20% co-authorship obligation is
  removed; academic citation is requested and authorship reflects contributions
  and agreement under the approved policy.
- README, this decision record and the F3-R14 remediation entries are updated
  concordantly. The original audit criteria and owner record remain historical.

Approved decision dossier SHA-256:
`3ad5acf5beabd8ec5c0cc3a43d51a996f2f6c4dcde0f77adabcfb79bdc599608`.

Approved 1,343-path classification manifest SHA-256:
`da06cacc1bad9a0cac66a52c89efc1716f0e4af2189a8d6b939cc886c50b08a8`.

Approved policy-only patch SHA-256:
`5620256534e23c851c1444a76b4c34aba2f63995703f089301ef83eb748e9b33`.

| Applied file | SHA-256 |
|---|---|
| `LICENCE.md` | `01d26ac36ec105e8396df18ede04fab4aae1462ad1eb1b027ad9193b036cd5d2` |
| `LICENCE_CATEGORY_C.txt` | `f9f2ec5eb1d276ebc1355b65418c980cd0aa1e7fc719d2d9cfecb5a512cb8daf` |
| `LICENSES/CC-BY-NC-SA-4.0.txt` | `e66c269d4819aaab34b49ef5220c4ddab6756f21bb5180761a4eb8561f2b7bbd` |
| `LICENSES/GPL-3.0-or-later.txt` | `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986` |

The [current policy](../../LICENCE.md), [exact reserved list](../../LICENCE_CATEGORY_C.txt)
and complete [CC](../../LICENSES/CC-BY-NC-SA-4.0.txt) and
[GPL](../../LICENSES/GPL-3.0-or-later.txt) texts are the applied files.
The full successor source/category manifests and actual commit identity belong
to the integration and acceptance-kit receipts, avoiding a self-referential
commit identifier in this record.

## Finding status and remaining gates

F3-R14 is **resolved for the approved licence policy and its application**.
This records the author's choice and the coherent policy text; it is not a
certification of ownership of third-party material. The other 202 audit finding
families and their evidence are unchanged by this update.

This approval does not authorise a merge into `main`, a tag or v1.5.0 release,
Zenodo changes or closure of unexecuted native acceptance. The
[remaining release gates](REMEDIATION_v1.5.0.md#remaining-release-gates) remain
separate. Earlier N08 and other runtime results retain their tested source
identities; no native rerun is implied by this policy commit.

## Historical pre-approval record

The following record is preserved verbatim as history. Its pending statuses and
prepared alternatives describe the earlier state, superseded by the actual
author approval and applied policy above.

```markdown
# Licence policy decision — pending author approval

Audit reference: F3-R14. Prepared for the v1.5.0 candidate on 17 November 2026.
This record is a proposal, not a licence grant or an amendment to `LICENCE.md`.
The existing licence text is retained pending Antonio Clim's explicit decision.

## Conflicts requiring a decision

| Location in the existing terms | Conflict to resolve |
|---|---|
| Category A and Category C | Instructor notes/outlines appear in both categories. A path-level precedence rule is missing. |
| Category B and sections 6.1–6.2 | GPL-3.0-or-later is declared for code, while additional clauses restrict commercial uses of all materials. |
| Section 5.2 | Mandatory co-authorship above a 20% threshold is added across all categories, including material declared under standard public licences. |
| README summary | Its blanket restriction on redistribution and teaching outside ASE-CSIE did not match the category grants. The inaccurate summary has been replaced by a pointer to the unresolved terms. |

The GNU GPL permits commercial use and distribution subject to its conditions.
Its FAQ also distinguishes preservation of notices from a mandatory citation in
research papers. CC BY-NC-SA has its own attribution, non-commercial and ShareAlike
conditions and prohibits downstream restrictions that conflict with the licence.
These observations identify inconsistencies; this audit does not determine their
legal effect for any particular recipient.

## Prepared option A — retain the declared standard licences

This is the recommended editorial resolution because it preserves the existing
A/B/C structure while making its intended boundaries explicit:

1. Keep CC BY-NC-SA 4.0 for Category A and GPL-3.0-or-later for Category B.
2. Define Category C by explicit paths and give those specific entries precedence
   over generic file-type rules. Confirm that `00_APPENDIX/d)instructor_NOTES4sem/`
   belongs to C, removing the overlapping A entry.
3. Apply additional permission requirements only to uses outside the applicable
   standard licence and to Category C. Do not apply the non-commercial restriction
   to GPL-covered code.
4. Replace mandatory co-authorship with a request for appropriate citation and
   discussion of collaboration. Authorship requires the applicable scholarly
   contribution criteria and is not an automatic percentage-based obligation.
5. Preserve copyright, attribution, provenance, contributor notices and existing
   recipient rights. Supply a path/category table and the standard licence texts.

**Proposed replacement principle, to apply only after approval:**

> The standard licence identified for a file governs that file. Additional
> permission requirements in this document apply only where the applicable
> licence does not already grant the requested use. No clause in this document
> adds a non-commercial restriction, mandatory research citation or automatic
> co-authorship obligation to GPL-covered code. Attribution required by each
> applicable licence and preservation of copyright notices remain in force.
> Academic citation is requested where the materials inform a publication;
> co-authorship must reflect substantive scholarly contributions and agreement
> among the authors.

## Prepared option B — specify a different future distribution policy

If the intended policy requires restrictions beyond the standard A/B licences,
the author must define that policy explicitly and identify which material and
future versions may use it. Merely adding restrictions while retaining the GPL
or CC label would not resolve the inconsistency. Existing grants and third-party
rights must be accounted for; this audit does not assume they can be revoked.

## Release gate

F3-R14 remains **open — author decision required**. The technical remediation can
be reviewed independently, but v1.5.0 should not be described as having a resolved
reuse policy until the approved text and category mapping have been applied and
checked. Saying “next” alone does not choose either policy.

## Primary sources

- GNU Project. [GNU GPL v3, especially sections 7 and 10](https://www.gnu.org/licenses/gpl-3.0.html).
- GNU Project. [GPL FAQ: requirements to cite research uses](https://www.gnu.org/licenses/gpl-faq.html#RequireCitation).
- GNU Project. [Selling free software](https://www.gnu.org/philosophy/selling.html).
- Creative Commons. [CC BY-NC-SA 4.0 legal code, especially section 2(a)(5)](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en).
```
