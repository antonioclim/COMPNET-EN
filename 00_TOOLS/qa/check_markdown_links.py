#!/usr/bin/env python3
"""check_markdown_links.py

Lightweight Markdown link checker for this repository.

It walks the repository, finds Markdown files, extracts relative link and image
targets, checks that the corresponding files or directories exist on disk, then
prints a clear report and exits non-zero on failures.

Scope and limitations
- Only relative links are checked. External URLs, mailto: links and intra-page
  anchors are ignored.
- Links inside fenced code blocks and inline code spans are ignored.
- The checker is intentionally conservative to avoid false positives.

Standard library only.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional, Sequence, Tuple
from urllib.parse import unquote


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
}

# Treat a leading scheme as an external link (http:, https:, mailto:, etc)
_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

# Match the start of an inline Markdown link or image: [text](...) or ![alt](...)
_INLINE_LINK_START_RE = re.compile(r"!?\[[^\]]*\]\(")

# Reference-style link definition: [id]: target
_REF_DEF_RE = re.compile(r"^\s*\[([^\]]+)\]:\s*(.+?)\s*$")

# Very small HTML attribute patterns, used to catch <a href="..."> and <img src="...">
_HTML_HREF_RE = re.compile(r"\bhref\s*=\s*([\"'])(.*?)\1", re.IGNORECASE)
_HTML_SRC_RE = re.compile(r"\bsrc\s*=\s*([\"'])(.*?)\1", re.IGNORECASE)


@dataclass(frozen=True)
class LinkIssue:
    markdown_file: Path
    line_no: int
    raw_target: str
    resolved_path: Path


def _repo_root() -> Path:
    """Return the repository root as a Path.

    Assumes this script lives at 00_TOOLS/qa/check_markdown_links.py.
    """

    return Path(__file__).resolve().parents[2]


def _iter_markdown_files(root: Path) -> Iterator[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune ignored directories in-place for performance
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]

        for filename in filenames:
            if filename.lower().endswith(".md"):
                yield Path(dirpath) / filename


def _strip_inline_code_spans(line: str) -> str:
    """Remove inline code spans from a line.

    This is a pragmatic implementation that supports backtick runs of arbitrary
    length (for example `code` and ``code with ` inside``).
    """

    out: list[str] = []
    i = 0
    n = len(line)

    while i < n:
        if line[i] != "`":
            out.append(line[i])
            i += 1
            continue

        # Count backticks
        tick_len = 1
        j = i + 1
        while j < n and line[j] == "`":
            tick_len += 1
            j += 1

        # Find matching closing run
        closing = "`" * tick_len
        k = line.find(closing, j)
        if k == -1:
            # No closing run, treat as literal
            out.append(line[i])
            i += 1
            continue

        # Skip content inside code span (including delimiters)
        i = k + tick_len

    return "".join(out)


def _parse_balanced_parentheses(line: str, open_paren_index: int) -> Tuple[Optional[str], Optional[int]]:
    """Parse the content of (...) starting at open_paren_index.

    Returns (raw_content, close_paren_index) where close_paren_index points to
    the closing ')'. If parsing fails, returns (None, None).
    """

    i = open_paren_index + 1
    depth = 0
    buf: list[str] = []

    while i < len(line):
        ch = line[i]

        if ch == "\\":
            # Keep escapes intact for later unescaping
            if i + 1 < len(line):
                buf.append(ch)
                buf.append(line[i + 1])
                i += 2
            else:
                buf.append(ch)
                i += 1
            continue

        if ch == "(":
            depth += 1
            buf.append(ch)
            i += 1
            continue

        if ch == ")":
            if depth == 0:
                return "".join(buf), i
            depth -= 1
            buf.append(ch)
            i += 1
            continue

        buf.append(ch)
        i += 1

    return None, None


def _extract_destination(raw: str) -> str:
    """Extract the destination part from the raw (...) content.

    Supports optional titles like (path "title") and angle-bracket destinations
    like (<path with spaces> "title").
    """

    s = raw.strip()
    if not s:
        return ""

    if s.startswith("<"):
        gt = s.find(">")
        if gt != -1:
            return s[1:gt].strip()

    # Otherwise, take the first whitespace-delimited token
    return s.split()[0].strip()


def _normalise_target(dest: str) -> str:
    """Normalise a Markdown destination into a filesystem path candidate."""

    s = dest.strip()

    # Remove surrounding angle brackets if present
    if s.startswith("<") and s.endswith(">"):
        s = s[1:-1].strip()

    # Unescape Markdown backslash escapes
    s = re.sub(r"\\(.)", r"\1", s)

    # Drop anchors and query strings
    s = s.split("#", 1)[0]
    s = s.split("?", 1)[0]

    # Decode URL-encoding
    s = unquote(s)

    # Treat backslashes as path separators for robustness
    s = s.replace("\\", "/")

    return s


def _is_relative_target(target: str) -> bool:
    t = target.strip()
    if not t:
        return False

    if t.startswith("#"):
        return False

    if t.startswith("/"):
        return False

    if t.startswith("//"):
        return False

    if _SCHEME_RE.match(t):
        return False

    return True


def _iter_line_targets(line: str) -> Iterator[str]:
    """Yield raw targets for inline links and images in a single line."""

    for match in _INLINE_LINK_START_RE.finditer(line):
        open_paren = match.end() - 1
        raw, close_paren = _parse_balanced_parentheses(line, open_paren)
        if raw is None or close_paren is None:
            continue

        dest = _extract_destination(raw)
        if dest:
            yield dest


def _iter_ref_definition_targets(line: str) -> Iterator[str]:
    m = _REF_DEF_RE.match(line)
    if not m:
        return

    raw_target = m.group(2).strip()
    if not raw_target:
        return

    # Support <...>
    if raw_target.startswith("<"):
        gt = raw_target.find(">")
        if gt != -1:
            yield raw_target[1:gt].strip()
            return

    yield raw_target.split()[0].strip()


def _iter_html_attribute_targets(line: str) -> Iterator[str]:
    for _, value in _HTML_HREF_RE.findall(line):
        if value:
            yield value

    for _, value in _HTML_SRC_RE.findall(line):
        if value:
            yield value


def _check_markdown_file(md_file: Path, repo_root: Path) -> Tuple[int, Sequence[LinkIssue]]:
    """Return (checked_count, issues) for a single Markdown file."""

    checked = 0
    issues: list[LinkIssue] = []

    try:
        text = md_file.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        issues.append(
            LinkIssue(
                markdown_file=md_file,
                line_no=0,
                raw_target=f"<unreadable file: {exc}>",
                resolved_path=md_file,
            )
        )
        return checked, issues

    in_fence = False
    fence_marker: Optional[str] = None

    in_comment = False

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line

        # HTML comments can span multiple lines
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue

        if "<!--" in line:
            if "-->" not in line:
                in_comment = True
            continue

        stripped = line.lstrip()

        # Fenced code blocks
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            else:
                # Close only if marker matches the opening one
                if fence_marker == marker:
                    in_fence = False
                    fence_marker = None
            continue

        if in_fence:
            continue

        # Remove inline code spans to reduce false positives
        line = _strip_inline_code_spans(line)

        raw_targets: Iterable[str] = (
            list(_iter_line_targets(line))
            + list(_iter_ref_definition_targets(line))
            + list(_iter_html_attribute_targets(line))
        )

        for raw_target in raw_targets:
            normalised = _normalise_target(raw_target)
            if not _is_relative_target(normalised):
                continue

            checked += 1

            resolved = (md_file.parent / normalised).resolve()

            # Ensure we do not accidentally treat the repository root as a target for "".
            if normalised in {"", "."}:
                continue

            if not resolved.exists():
                # Resolve again without following symlinks outside the repo when possible
                issues.append(
                    LinkIssue(
                        markdown_file=md_file,
                        line_no=line_no,
                        raw_target=raw_target,
                        resolved_path=resolved,
                    )
                )

    return checked, issues


def _format_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def main(argv: Sequence[str]) -> int:
    repo_root = _repo_root()

    md_files = list(_iter_markdown_files(repo_root))
    total_checked = 0
    all_issues: list[LinkIssue] = []

    for md_file in md_files:
        checked, issues = _check_markdown_file(md_file, repo_root)
        total_checked += checked
        all_issues.extend(issues)

    if not all_issues:
        print(f"Markdown link check passed: {len(md_files)} files scanned, {total_checked} targets checked.")
        return 0

    print("Markdown link check failed")
    print(f"Scanned {len(md_files)} Markdown files and checked {total_checked} relative targets.")
    print(f"Found {len(all_issues)} missing targets:\n")

    for issue in all_issues:
        file_display = _format_path(issue.markdown_file, repo_root)
        resolved_display = _format_path(issue.resolved_path, repo_root)
        line_part = f":{issue.line_no}" if issue.line_no else ""
        print(f"- {file_display}{line_part}: {issue.raw_target} -> {resolved_display}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
