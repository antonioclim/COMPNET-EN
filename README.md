# Computer Networks — Course Kit (EN)

A full course kit for an undergraduate computer networks module. It covers 13 lectures, 13 practical seminars, team projects and PlantUML diagrams.

---

## Table of Contents

| Folder | Description |
|--------|-------------|
| [`00_APPENDIX/`](00_APPENDIX/) | Supplementary materials: Python guide, student quizzes, optional HTML lectures, instructor notes |
| [`00_TOOLS/`](00_TOOLS/) | Tooling: PlantUML diagrams, generation scripts, prerequisite checklist |
| [`01_GHID_MININET-SDN/`](01_GHID_MININET-SDN/) | Installation and configuration guide for the Mininet-SDN virtual machine |
| [`02_PROJECTS/`](02_PROJECTS/) | 15 network-application projects and 10 administration/security projects with specifications, diagrams and a CI pipeline |
| [`03_LECTURES/`](03_LECTURES/) | 13 lectures with slide-by-slide markdown, PlantUML diagrams and executable demo scenarios (Python/Docker) |
| [`04_SEMINARS/`](04_SEMINARS/) | 13 practical seminars with explanation/task/scenario files, Python code, Docker configurations and HTML support pages |

---

## Prerequisites

See [`00_TOOLS/Prerequisites/Prerequisites.md`](00_TOOLS/Prerequisites/Prerequisites.md) for the full list.

Java 8 or later is required for PlantUML rendering.

---

## Quick start

1. Clone the repository.
2. Install Java if absent.
3. Download `plantuml.jar`:
   ```bash
   wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar -P 00_TOOLS/
   ```
4. Generate diagrams:
   ```bash
   cd 03_LECTURES/C01/assets && bash render.sh
   ```

---

## Formatting

The repository uses [Prettier](https://prettier.io/) for deterministic
Markdown and HTML formatting. See
[`00_TOOLS/README.md`](00_TOOLS/README.md#prettier-formatting-phase-5) for
full details.

```bash
npm install && npm run format:check   # CI gate
node format-offline.js --write        # offline alternative
```

Romanian instructor notes (`roCOMPNETclass_*`) and bilingual quizzes are
intentionally excluded.

---

## Quality checks

Run the Markdown link checker locally from the repository root:

```bash
python 00_TOOLS/qa/check_markdown_links.py
```

Continuous integration (GitHub Actions) runs on each push and pull request. It
executes the Markdown link checker and, if pytest-style tests are detected,
runs `pytest`.

---

## Structure

```
.
├── 00_APPENDIX
├── 00_TOOLS
├── 01_GHID_MININET-SDN
├── 02_PROJECTS
├── 03_LECTURES
├── 04_SEMINARS
├── CHANGELOG.md
├── current-outline.md
└── requirements-optional.txt
```

---

## Notes

- Quizzes in `00_APPENDIX/c)studentsQUIZes(multichoice_only)/` carry bilingual EN + RO headers. This is intentional — the quizzes are intended for students studying in Romanian.
- Instructor files in `00_APPENDIX/d)instructor_NOTES4sem/` are in Romanian.

---

## Licence

Academic use.
