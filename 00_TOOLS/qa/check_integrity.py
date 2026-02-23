#!/usr/bin/env python3
"""check_integrity.py  --  Phase 7 language & lexical integrity guard.

Prevents two classes of regression from entering the repository:

1. **Corrupted-token detection** -- UTF-8 mojibake sequences that arise when
   Romanian diacritics are double-encoded or decoded under the wrong codepage.
   Their presence anywhere in a tracked file is unconditionally a violation
   (unless the line carries an inline suppression marker).

2. **Romanian-leakage detection** -- Romanian-language sentences that appear
   outside the two permitted zones:
       - files whose *basename* starts with ``ro`` (case-insensitive)
       - anything under ``00_APPENDIX/c)studentsQUIZes(multichoice_only)/``
   The check uses a two-pronged heuristic: Romanian-specific diacritics
   (a-breve, s/t-comma-below and their uppercase forms) *or* a density
   threshold of high-frequency Romanian function words that have no plausible
   English homograph.

Design goals
   * Standard-library only -- no pip dependencies.
   * Fast -- single-pass line scan; compiled regex; early directory pruning.
   * Extensible -- all token lists and word lists are plain Python sets at the
     top of the file; add entries and re-run.

Inline suppression
   Append ``qa:allow-ro`` or ``qa:allow-corrupt`` to any line (typically inside
   a comment) to suppress the corresponding check on that line only.

Exit codes
   * 0 -- repository clean.
   * 1 -- one or more violations found (details on stdout).
   * 2 -- unexpected runtime error.

Standard library only.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import List, NamedTuple, Set

# ======================================================================== #
#  CONFIGURATION -- edit these collections to extend coverage              #
# ======================================================================== #

# -- 1. Corrupted tokens (mojibake) -------------------------------------- #
# Each string is a byte-level artefact from double-encoding or CP1252
# mis-decoding of Romanian diacritics.  To extend: reproduce the encoding
# round-trip for the new character and append the garbled result.
#
# NOTE: this script is self-exempted (see SELF_EXEMPT_BASENAMES below) so
# that these literal definitions do not trigger violations.
CORRUPTED_TOKENS: Set[str] = {
    # lowercase diacritics
    "Ä\u0083",       # a-breve
    "Ã¢",            # a-circumflex
    "Ã®",            # i-circumflex
    "È™",            # s-comma-below
    "È›",            # t-comma-below
    "Å\u0163",       # t via legacy cedilla (U+0163)
    "Å\u015F",       # s via legacy cedilla (U+015F)
    # uppercase diacritics
    "Ä\u0082",       # A-breve
    "Ã\u0082",       # A-circumflex
    "ÃŽ",            # I-circumflex
    "È˜",            # S-comma-below
    "Èš",            # T-comma-below
    "Å¢",            # T via legacy cedilla (U+0162)
    "Åž",            # S via legacy cedilla (U+015E)
    # triple-encoding artefacts
    "Ãƒ",            # generic triple-encode marker
    "Â\u00A0",       # non-breaking space double-encoded
}

_corrupted_re = re.compile(
    "|".join(re.escape(t) for t in sorted(CORRUPTED_TOKENS, key=len, reverse=True))
)

# -- 2. Romanian leakage ------------------------------------------------- #
# 2a. Romanian-specific diacritics (not shared with French / German / etc.
#     in a networking-English context).
_RO_DIACRITICS_RE = re.compile(r"[\u0103\u0102\u0219\u0218\u021B\u021A]")
#   ă=U+0103  Ă=U+0102  ș=U+0219  Ș=U+0218  ț=U+021B  Ț=U+021A

# 2b. High-confidence Romanian function words (>= 3 chars to avoid English
#     homograph collisions like "sa"="SA", "mai"="May", "cel"="cel(l)").
#     A line must contain >= RO_WORD_THRESHOLD of these (case-insensitive,
#     word-boundary-delimited) to be flagged when it lacks diacritics.
RO_FUNCTION_WORDS: Set[str] = {
    # conjunctions, prepositions, adverbs
    "pentru", "care", "acest", "despre", "prin",
    "fiecare", "astfel", "deoarece", "dintre", "oricare",
    "niciunul", "niciun", "nicio", "altfel", "doar",
    "deja", "atunci", "acolo",
    # verbs / modals (unambiguous forms)
    "este", "sunt", "poate", "trebuie",
    # pronouns / articles (unambiguous >= 3 chars)
    "acest", "unui", "unei", "unor",
    # networking domain terms (Romanian-only)
    "nivelul", "stratul", "conexiune", "protocoale",
    "adresare", "rutare", "comutare", "calculatoare",
    "utilizator", "securitate", "comunicare",
    "transmisie",
}

_ro_word_re = re.compile(
    r"\b("
    + "|".join(re.escape(w) for w in sorted(RO_FUNCTION_WORDS, key=len, reverse=True))
    + r")\b",
    re.IGNORECASE,
)

RO_WORD_THRESHOLD = 2

# 2c. Allowlisted proper nouns / phrases.  If a flagged line matches any of
#     these patterns the Romanian-leakage violation is suppressed.  This
#     covers institutional names, city names, and encoding-pedagogy examples
#     that legitimately appear inside otherwise-English files.
RO_PROPER_NOUN_PATTERNS: list[str] = [
    r"Bucure[s\u0219]ti",                   # city name
    r"Academia de Studii Economice",         # ASE full name
    r"Universitatea Politehnica",            # UPB full name
    r"Departamentul pentru Preg[a\u0103]tirea",  # DPPD full name
    r"DPPD\s*\(",                            # DPPD abbreviation
    # encoding / charset pedagogy -- diacritics used as data examples
    r'["`\'][^\s]*[\u0218\u0219\u021A\u021B\u0102\u0103][^\s]*["`\']',  # quoted diacritical token
    r"Unicode characters?\s*\(",             # "For Unicode characters (..."
    r"bytes?\s+in\s+UTF-8",                  # encoding length discussion
    r"\\u0[0-9A-Fa-f]{3}",                   # Unicode escape sequences
]

_proper_noun_re = re.compile("|".join(RO_PROPER_NOUN_PATTERNS))

# -- 3. Scan scope -------------------------------------------------------- #
SCAN_EXTENSIONS: Set[str] = {
    ".md", ".html", ".htm", ".txt", ".py", ".sh", ".bash",
    ".yml", ".yaml", ".js", ".json", ".css", ".puml", ".csv",
    ".rst", ".toml", ".cfg", ".ini", ".xml",
}

IGNORED_DIRS: Set[str] = {
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".venv", "venv", "node_modules", "dist", ".tox",
}

# -- 4. Exempt zones ------------------------------------------------------ #
EXEMPT_SUBTREE = "00_APPENDIX/c)studentsQUIZes(multichoice_only)"
RO_FILE_PREFIX = "ro"

# Basenames unconditionally exempt from *all* checks (the checker itself
# must be exempt or it would flag its own token/word definitions).
SELF_EXEMPT_BASENAMES: Set[str] = {
    "check_integrity.py",
}

# -- 5. Inline suppression markers ---------------------------------------- #
SUPPRESS_CORRUPT = "qa:allow-corrupt"
SUPPRESS_RO      = "qa:allow-ro"


# ======================================================================== #
#  DATA TYPES                                                              #
# ======================================================================== #

class Violation(NamedTuple):
    path: str
    line_no: int
    kind: str          # "CORRUPTED_TOKEN" | "ROMANIAN_LEAKAGE"
    excerpt: str       # trimmed line content (max 120 chars)


# ======================================================================== #
#  CORE LOGIC                                                              #
# ======================================================================== #

def _is_fully_exempt(relpath: str) -> bool:
    """Return True when *relpath* should be skipped entirely."""
    basename = os.path.basename(relpath)
    return basename in SELF_EXEMPT_BASENAMES


def _is_exempt_from_romanian_check(relpath: str) -> bool:
    """Return True when *relpath* is allowed to contain Romanian text."""
    posix = relpath.replace(os.sep, "/")
    if EXEMPT_SUBTREE in posix:
        return True
    basename = os.path.basename(posix)
    if basename.lower().startswith(RO_FILE_PREFIX):
        return True
    return False


def _is_pedagogical_mojibake(line: str) -> bool:
    """True when corrupted tokens appear only inside code spans.

    Recognises both Markdown backtick spans and HTML ``<code>`` elements.
    """
    if "`" not in line and "<code>" not in line:
        return False
    stripped = re.sub(r"`[^`]+`", "", line)
    stripped = re.sub(r"<code>[^<]+</code>", "", stripped)
    return not _corrupted_re.search(stripped)


def scan_file(filepath: str, relpath: str) -> List[Violation]:
    """Scan a single file and return a list of violations."""
    if _is_fully_exempt(relpath):
        return []

    violations: List[Violation] = []
    exempt_ro = _is_exempt_from_romanian_check(relpath)

    try:
        with open(filepath, encoding="utf-8", errors="replace") as fh:
            for line_no, raw_line in enumerate(fh, start=1):
                line = raw_line.rstrip("\n\r")

                # ---- Check 1: corrupted tokens (never zone-exempt) ------
                if SUPPRESS_CORRUPT not in line and _corrupted_re.search(line):
                    if not _is_pedagogical_mojibake(line):
                        violations.append(Violation(
                            relpath, line_no, "CORRUPTED_TOKEN",
                            line.strip()[:120],
                        ))

                # ---- Check 2: Romanian leakage (respects exemptions) ----
                if exempt_ro or SUPPRESS_RO in line:
                    continue

                # Heuristic A: Romanian-specific diacritics
                if _RO_DIACRITICS_RE.search(line):
                    if not _proper_noun_re.search(line):
                        violations.append(Violation(
                            relpath, line_no, "ROMANIAN_LEAKAGE",
                            line.strip()[:120],
                        ))
                    continue

                # Heuristic B: function-word density (diacritic-free lines)
                hits = _ro_word_re.findall(line)
                if len(hits) >= RO_WORD_THRESHOLD:
                    if not _proper_noun_re.search(line):
                        violations.append(Violation(
                            relpath, line_no, "ROMANIAN_LEAKAGE",
                            line.strip()[:120],
                        ))

    except (OSError, UnicodeDecodeError) as exc:
        print(f"WARNING: could not read {relpath}: {exc}", file=sys.stderr)

    return violations


def walk_repo(root: str) -> List[Violation]:
    """Walk the repository tree and collect all violations."""
    all_violations: List[Violation] = []
    root_path = Path(root).resolve()

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        dirnames.sort()

        for fname in sorted(filenames):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SCAN_EXTENSIONS:
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, root_path)
            all_violations.extend(scan_file(full, rel))

    return all_violations


# ======================================================================== #
#  REPORTING                                                               #
# ======================================================================== #

_KIND_LABELS = {
    "CORRUPTED_TOKEN":  "CORRUPTED",
    "ROMANIAN_LEAKAGE": "RO-LEAK  ",
}


def report(violations: List[Violation]) -> None:
    """Print a human-readable report to stdout."""
    if not violations:
        print("check_integrity  PASSED  (no corrupted tokens or Romanian leakage)")
        return

    corrupted = sum(1 for v in violations if v.kind == "CORRUPTED_TOKEN")
    leakage   = sum(1 for v in violations if v.kind == "ROMANIAN_LEAKAGE")

    print("=" * 78)
    print(f"  INTEGRITY CHECK FAILED  --  {len(violations)} violation(s)")
    print(f"    corrupted tokens : {corrupted}")
    print(f"    Romanian leakage : {leakage}")
    print("=" * 78)

    for v in violations:
        label = _KIND_LABELS.get(v.kind, v.kind)
        print(f"\n  [{label}] {v.path}:{v.line_no}")
        print(f"           {v.excerpt}")

    print()


# ======================================================================== #
#  ENTRY POINT                                                             #
# ======================================================================== #

def main(argv: list[str] | None = None) -> int:
    """Return 0 on success, 1 on violations, 2 on error."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Phase 7 -- language & lexical integrity guard.",
    )
    parser.add_argument(
        "root", nargs="?", default=".",
        help="Repository root directory (default: cwd).",
    )
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"ERROR: {root} is not a directory.", file=sys.stderr)
        return 2

    try:
        violations = walk_repo(root)
    except Exception as exc:
        print(f"ERROR: unexpected failure -- {exc}", file=sys.stderr)
        return 2

    report(violations)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
