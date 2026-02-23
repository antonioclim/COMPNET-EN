# Tools

Utility scripts and reference materials for the course.

## Contents

### Prettier formatting (Phase 5)

The repository ships a Prettier configuration (`.prettierrc`, `.prettierignore`)
and a `package.json` at the root so that Markdown and HTML files can be
formatted deterministically.

**Running locally (with npm)**

```bash
npm install          # one-time — fetches prettier
npm run format:check # dry-run: exits non-zero if any file would change
npm run format:write # rewrite files in place
```

**Running without network access**

A zero-dependency Node.js script (`format-offline.js`) replicates the same
formatting rules. No `npm install` required.

```bash
node format-offline.js --check
node format-offline.js --write
```

**What is formatted**

Prettier (and the offline script) targets every `*.md` and `*.html` file in the
repository except for the items listed in `.prettierignore`:

- `roCOMPNETclass_*` — Romanian-only instructor notes (untouched).
- `00_APPENDIX/c)studentsQUIZes(multichoice_only)/` — bilingual student quizzes
  (untouched).
- Binary, Python, PlantUML and shell files — not applicable.

The formatting pass normalises LF line endings, strips trailing whitespace,
collapses excessive blank lines and ensures a single trailing newline. Prose
wrapping is set to `preserve` so paragraph reflows do not occur.

### `PlantUML(optional)/`

118 PlantUML diagram sources organised by week, with generation scripts
for PNG output (via HTTP server or local JAR). See
[PlantUML(optional)/README.md](<PlantUML(optional)/README.md>) for details.

### `Prerequisites/`

Student-facing checklist covering the tools needed before the first seminar:
Python 3.10+, Wireshark, Docker, Java (for PlantUML) and the Mininet-SDN VM.
See [Prerequisites/Prerequisites.md](Prerequisites/Prerequisites.md).
