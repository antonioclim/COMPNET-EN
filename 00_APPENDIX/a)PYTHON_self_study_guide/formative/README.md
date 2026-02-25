# formative — Python Bridge Quiz and Parsons Problems

Self-check material for the Python bridge pack: a YAML-authored quiz tagged by topic and source-language background, plus a small set of Parsons problems that focus on byte handling and socket sequencing. The quiz runner supports filtering and review mode and stores results locally.

## File and Folder Index

| Name | Description | Metric |
|---|---|---|
| [`README.md`](README.md) | Orientation for the Python bridge formative material | — |
| [`quiz.yaml`](quiz.yaml) | Quiz source in YAML (tagged by section and background) | 478 lines, 31 questions |
| [`run_quiz.py`](run_quiz.py) | Interactive quiz runner (filters, randomisation, review mode, result saving) | 700 lines |
| [`parsons/`](parsons/) | YAML Parsons problems (line-reordering exercises) | 3 files |
| [`parsons_runner.py`](parsons_runner.py) | Parsons runner (interactive, supports listing and file selection) | 191 lines |
| [`results/`](results/) | Local output directory for quiz result JSON files | 2 files |

## Visual Overview

```
quiz.yaml ──► run_quiz.py ──► results/quiz_results_<timestamp>.json

parsons/*.yaml ──► parsons_runner.py ──► (interactive only)
```

## Usage

```bash
cd "00_APPENDIX/a)PYTHON_self_study_guide/formative"

# interactive quiz
python3 run_quiz.py

# run only a subset (examples)
python3 run_quiz.py --background c
python3 run_quiz.py --section sockets
python3 run_quiz.py --random --limit 10

# review mode (shows correct answers and explanations)
python3 run_quiz.py --review

# Parsons problems
python3 parsons_runner.py --list
python3 parsons_runner.py --file parsons/parsons_socket.yaml
```

The quiz runner saves results to `results/` by default. Use `--no-save` to disable this.

## Design Notes

The quiz is tagged by section and background so instructors can direct targeted remediation without duplicating the same question bank for different cohorts. Parsons problems are included because they test sequencing and byte-handling correctness while reducing syntactic load.

## Cross-References and Context

### Prerequisites and Dependencies

| Prerequisite | Path | Why |
|---|---|---|
| Bridge pack root | [`../README.md`](../README.md) | Explains where this formative work fits in the wider bridge workflow |
| Python dependencies | [`../../requirements.txt`](../../requirements.txt) | Requires `PyYAML` for YAML parsing and `rich` for TUI output |

### Lecture ↔ Seminar ↔ Project ↔ Quiz Mapping

| This folder | Lecture | Seminar | Project | Quiz |
|---|---|---|---|---|
| Python readiness and byte-handling checks | [`../../../03_LECTURES/C03/c3-intro-network-programming.md`](../../../03_LECTURES/C03/c3-intro-network-programming.md) (socket concepts) | [`../../../04_SEMINARS/S02/`](../../../04_SEMINARS/S02/), [`../../../04_SEMINARS/S04/`](../../../04_SEMINARS/S04/) | [`../../../02_PROJECTS/01_network_applications/`](../../../02_PROJECTS/01_network_applications/) | Weeks 02–04 (revision bank) |

### Downstream Dependencies

- `../Makefile` calls `run_quiz.py` and `parsons_runner.py` as part of `make quiz-*` and `make parsons-*`.

### Suggested Learning Sequence

Read the relevant sections in `../PYTHON_NETWORKING_GUIDE.md` → run `python3 run_quiz.py --section <topic>` → proceed to the matching seminar

## Selective Clone

Method A — Git sparse-checkout (requires Git ≥ 2.25)

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/formative"
```

To run the quiz, also include the dependency list:

```bash
git sparse-checkout add 00_APPENDIX/requirements.txt
```

Method B — Direct download (no Git required)

```text
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/formative
```

## Version and Provenance

| Item | Value |
|---|---|
| YAML source of truth | `quiz.yaml` and `parsons/*.yaml` |
| Output location | `results/` (local JSON result files) |
