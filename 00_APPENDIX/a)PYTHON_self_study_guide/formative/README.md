# Formative Assessment — Python Self-Study Guide

Self-assessment toolkit for students transitioning to Python from C, C++, JavaScript, Java or Kotlin. Contains a question bank, Parsons problems and the CLI runner that drives both.

| File / Folder | Description | Metric |
|---|---|---|
| [`quiz.yaml`](quiz.yaml) | Question bank with metadata, Bloom levels and per-language filtering | 31 questions |
| [`run_quiz.py`](run_quiz.py) | Interactive CLI quiz runner with export capabilities | Python 3.10+ |
| [`parsons_runner.py`](parsons_runner.py) | Parsons problem executor — shuffles lines for reordering exercises | Python 3.10+ |
| [`parsons/`](parsons/) | YAML definitions for Parsons problems (sockets, bytes) | 2 files |
| [`results/`](results/) | Output directory for quiz session results (git-ignored content) | — |

## Usage

From the guide root (`a)PYTHON_self_study_guide/`):

```bash
make quiz              # full 31-question interactive quiz
make quiz-quick        # 10 random questions (~10 min)
make quiz-c            # questions weighted for C/C++ background
make quiz-js           # questions weighted for JavaScript background
make quiz-java         # questions weighted for Java background
make quiz-kotlin       # questions weighted for Kotlin background
make parsons           # all Parsons problems
make parsons-socket    # socket-specific ordering exercises
make parsons-bytes     # encoding-specific ordering exercises
```

Direct invocation:

```bash
python3 formative/run_quiz.py                    # interactive mode
python3 formative/run_quiz.py --show-answers     # review mode
python3 formative/run_quiz.py --export json      # JSON export
python3 formative/run_quiz.py --export moodle    # Moodle GIFT export
```

## Pedagogical Context

The quiz covers three cognitive levels: recall of Python syntax differences, application of socket and struct patterns and analysis of common cross-language misconceptions. Parsons problems complement the quiz by targeting procedural knowledge without requiring syntax production.

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Networking guide | [`../PYTHON_NETWORKING_GUIDE.md`](../PYTHON_NETWORKING_GUIDE.md) | Theory behind quiz questions |
| Rosetta Stone | [`../comparisons/ROSETTA_STONE.md`](../comparisons/ROSETTA_STONE.md) | Multi-language comparisons tested in quiz |
| Misconceptions | [`../comparisons/MISCONCEPTIONS_BY_BACKGROUND.md`](../comparisons/MISCONCEPTIONS_BY_BACKGROUND.md) | Error patterns the quiz probes |
| Self-check checkpoints | [`../docs/SELF_CHECK_CHECKPOINTS.md`](../docs/SELF_CHECK_CHECKPOINTS.md) | Weekly readiness criteria |
| Root-level formative | [`../../formative/`](../../formative/) | Separate Week 0 quiz (environment-focused, 10 questions) |

**Suggested sequence:** read the guide → attempt the quiz → review weak areas → retake.

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/formative"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/formative
```
