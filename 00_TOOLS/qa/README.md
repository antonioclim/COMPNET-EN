# QA tools

Automated quality-assurance scripts that run in CI and can be invoked locally.

## Quick reference

| Script | Phase | What it guards |
|---|---|---|
| `check_executability.sh` | 4 | File permission bits match `executable_manifest.txt` |
| `check_markdown_links.py` | 5 | Relative links in `*.md` resolve to existing files |
| `check_integrity.py` | 7 | No corrupted tokens (mojibake) or Romanian-language leakage |

## `check_integrity.py` — language & lexical integrity guard

### Running locally

```bash
# from the repository root
python 00_TOOLS/qa/check_integrity.py          # default: scans "."
python 00_TOOLS/qa/check_integrity.py /path/to/repo   # explicit root
```

The script is **standard-library only** (Python 3.10+); no `pip install`
required.  Exit code `0` = clean, `1` = violations found, `2` = runtime error.

### What it checks

1. **Corrupted tokens** — UTF-8 mojibake byte sequences produced when Romanian
   diacritics (a-breve, s/t-comma-below, i/a-circumflex and uppercase forms)
   undergo double-encoding or
   CP1252 mis-decoding.  These are invalid in *every* file regardless of
   language zone.

2. **Romanian leakage** — Romanian prose that appears outside the two
   permitted zones:
   - files whose basename starts with `ro` (case-insensitive)
   - files under `00_APPENDIX/c)studentsQUIZes(multichoice_only)/`

   Detection uses two heuristics: (a) Romanian-specific diacritics  <!-- qa:allow-ro -->
   (U+0103, U+0218, U+021A and uppercase), and (b) a density threshold of Romanian function words
   that have no English homograph.

### Extending the token / word lists

All configuration lives as plain Python sets at the top of
`check_integrity.py`:

| Collection | Purpose | How to extend |
|---|---|---|
| `CORRUPTED_TOKENS` | Mojibake byte strings | Reproduce the encoding round-trip and add the garbled result |
| `RO_FUNCTION_WORDS` | Romanian function words (≥ 3 chars) | Add unambiguous words that have no English homograph |
| `RO_PROPER_NOUN_PATTERNS` | Allowlisted proper nouns (regex) | Add patterns for institutional names, city names, or encoding examples |
| `SELF_EXEMPT_BASENAMES` | Files entirely skipped | Add filenames that contain token definitions by necessity |

### Inline suppression

Append one of the following markers anywhere on a line (typically inside a code
comment) to suppress the corresponding check **on that line only**:

- `qa:allow-corrupt` — suppress the corrupted-token check
- `qa:allow-ro` — suppress the Romanian-leakage check

Example:

```markdown
This line mentions București as a proper noun  <!-- qa:allow-ro -->
```

### Pedagogical exemption

Lines where corrupted tokens appear exclusively inside inline code spans
(Markdown `` ` `` or HTML `<code>`) are recognised as encoding-pedagogy
examples and are automatically exempted from the corrupted-token check.
