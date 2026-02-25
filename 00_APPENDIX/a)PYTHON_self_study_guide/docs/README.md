# Supporting Documentation — Python Self-Study Guide

Reference documents that support the self-study workflow: readiness checklists aligned to weekly labs and a troubleshooting compendium covering the most common Python-in-networking errors.

| File | Lines | Purpose |
|---|---|---|
| [`SELF_CHECK_CHECKPOINTS.md`](SELF_CHECK_CHECKPOINTS.md) | 280 | Per-week readiness criteria — what a student must be able to do before each lab |
| [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) | 535 | 16 error scenarios with symptoms, causes and fixes |

## When to Use

Consult the checkpoints *before* each week's seminar to confirm you have the required Python fluency. Consult the troubleshooting guide when an error message appears during example execution or lab work.

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Root-level troubleshooting | [`../../docs/troubleshooting.md`](../../docs/troubleshooting.md) | Broader environment and Docker troubleshooting (not Python-specific) |
| Quiz system | [`../formative/quiz.yaml`](../formative/quiz.yaml) | Checkpoint readiness can be validated via quiz |
| Networking guide | [`../PYTHON_NETWORKING_GUIDE.md`](../PYTHON_NETWORKING_GUIDE.md) | Explanations for concepts tested in the checkpoints |

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/docs"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/docs
```
