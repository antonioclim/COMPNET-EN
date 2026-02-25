# Formative Assessment — Week 0 Environment Check

Self-assessment quiz and LMS export pipeline for the Week 0 prerequisite module. The 10-question quiz verifies that students can configure WSL2 + Docker, distinguish images from containers, apply port mapping and perform basic Python socket and byte operations.

| File / Folder | Description | Metric |
|---|---|---|
| [`quiz.yaml`](quiz.yaml) | Question source: 10 items across 3 Bloom levels | 269 lines |
| [`quiz.json`](quiz.json) | LMS-ready JSON export (Moodle / Canvas) | 264 lines |
| [`parsons_problems.json`](parsons_problems.json) | JSON export of code-ordering exercises | 130 lines |
| [`run_quiz.py`](run_quiz.py) | Interactive CLI runner with export, filter and review modes | 657 lines |
| [`tests/`](tests/) | Unit tests for export functions | 1 test file |

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  quiz.yaml   │────►│  run_quiz.py │────►│  quiz.json   │
│  (source)    │     │  (runner)    │     │  (LMS export)│
└──────────────┘     └──────────────┘     └──────────────┘
```

## Usage

```bash
# from 00_APPENDIX/
make quiz              # interactive mode
make quiz-review       # show answers
make quiz-random       # randomised order
make export-json       # export to JSON
make export-moodle     # export to Moodle GIFT format
```

Direct invocation:

```bash
python3 formative/run_quiz.py
python3 formative/run_quiz.py --show-answers
python3 formative/run_quiz.py --export json
python3 formative/run_quiz.py --validate
```

## Pedagogical Context

The quiz acts as a gate check before Week 1: students scoring below 70% are directed back to the prerequisite materials. Questions span recall (Docker terminology), application (port mapping, socket calls) and analysis (diagnosing byte-encoding errors), aligned to the learning objectives in [`../docs/learning_objectives.md`](../docs/learning_objectives.md).

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Learning objectives | [`../docs/learning_objectives.md`](../docs/learning_objectives.md) | Each question maps to a specific LO |
| Python guide quiz | [`../a)PYTHON_self_study_guide/formative/`](../a%29PYTHON_self_study_guide/formative/) | Separate, larger quiz (31 questions) focused on Python proficiency |
| Misconceptions | [`../docs/misconceptions.md`](../docs/misconceptions.md) | Quiz feedback references common errors documented here |
| Makefile | [`../Makefile`](../Makefile) | `make quiz`, `make export`, `make ci` targets |
| Prerequisites | [`../../00_TOOLS/Prerequisites/`](../../00_TOOLS/Prerequisites/) | Environment setup the quiz validates |

### Downstream Dependencies

The Makefile targets `quiz`, `export-json`, `export-moodle` and `ci` all invoke `run_quiz.py`. The `tests/test_quiz_exports.py` file imports from `run_quiz.py`.

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_APPENDIX/formative
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/formative
```
