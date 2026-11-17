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
