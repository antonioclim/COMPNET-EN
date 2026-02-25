# S14 — Revision and Team Project Assessment

Week 14 is a consolidation session. It provides the assessment model, evidence expectations and viva format for the team projects, together with a preparation checklist and a rubric template that can be used by assessors and by teams for self-audit. No new technical content is introduced; the session serves as the bridge between seminar work and project delivery.

## File/Folder Index

| Name | Type | Description |
|---|---|---|
| [`S14_Part01_Explanation_Revision_and_Assessment.md`](S14_Part01_Explanation_Revision_and_Assessment.md) | Explanation | Assessment model, evidence expectations and viva format |
| [`S14_Part02_Tasks_Preparation.md`](S14_Part02_Tasks_Preparation.md) | Tasks | Preparation checklist and self-checks |
| [`S14_Part03_Template_Assessment_Rubric.md`](S14_Part03_Template_Assessment_Rubric.md) | Template | Rubric, evidence checklist and viva prompts |
| [`assets/puml/fig-assessment-workflow.puml`](assets/puml/fig-assessment-workflow.puml) | Diagram | PlantUML source: assessment workflow |
| [`assets/render.sh`](assets/render.sh) | Script | PlantUML batch renderer |

## Pedagogical Context

The rubric and preparation tasks are designed so that teams can self-audit their deliverables before the viva. The assessment model values verifiable evidence (running containers, reproducible test output, Wireshark captures) over declarative documentation. This principle aligns with the evidence-first methodology practised throughout S01–S13.

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Project specifications (Group 1) | [`../../02_PROJECTS/01_network_applications/`](../../02_PROJECTS/01_network_applications/) | Projects assessed in this session |
| Project specifications (Group 2) | [`../../02_PROJECTS/02_administration_security/`](../../02_PROJECTS/02_administration_security/) | Projects assessed in this session |
| Common deliverable standards | [`../../02_PROJECTS/00_common/`](../../02_PROJECTS/00_common/) | `README_STANDARD_RC2026.md` and verification tools |
| Lecture C14 — Revision | [`../../03_LECTURES/C14/`](../../03_LECTURES/C14/) | Revision lecture accompanying this seminar |
| Quiz Week 14 | [`../../00_APPENDIX/c)studentsQUIZes(multichoice_only)/COMPnet_W14_Questions.md`](../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W14_Questions.md) | Final revision quiz |
| All seminars S01–S13 | [`../`](../) | Skills and evidence accumulated across the semester |
| Previous: S13 (security, pentest) | [`../S13/`](../S13/) | Final technical seminar |

No specific prerequisites beyond having completed or substantially progressed through seminars S01–S13 and a team project.

**Suggested sequence:** S01–S13 → project work → this folder

## Selective Clone

**Method A — Git sparse-checkout (requires Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 04_SEMINARS/S14
```

To include the project standards:

```bash
git sparse-checkout add 02_PROJECTS/00_common
```

**Method B — Direct download**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/04_SEMINARS/S14
```

---

*Course: COMPNET-EN — ASE Bucharest, CSIE*
