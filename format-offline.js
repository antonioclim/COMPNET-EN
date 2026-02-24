#!/usr/bin/env node
/**
 * format-offline.js
 *
 * Deterministic formatting pass for Markdown and HTML files.
 * Replicates the subset of Prettier behaviour configured in .prettierrc
 * (proseWrap: preserve, printWidth: 120, endOfLine: lf, tabWidth: 2).
 *
 * Usage:
 *   node format-offline.js --check   # exit 1 if any file would change
 *   node format-offline.js --write   # rewrite files in place
 *   node format-offline.js --list    # list files that would be touched
 */

"use strict";

const fs = require("fs");
const path = require("path");

// ── Exclusion patterns (mirrors .prettierignore) ──────────────────────
const EXCLUDE_PATTERNS = [
  /roCOMPNETclass_/,
  /00_APPENDIX\/c\)studentsQUIZes\(multichoice_only\)\//,
  /node_modules\//,
  /__pycache__\//,
  /\.git\//,
];

function isExcluded(relPath) {
  return EXCLUDE_PATTERNS.some((rx) => rx.test(relPath));
}

// ── Collect target files ──────────────────────────────────────────────
function collectFiles(root) {
  const results = [];

  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      const rel = path.relative(root, full);

      if (entry.isDirectory()) {
        if (entry.name === "node_modules" || entry.name === ".git") continue;
        if (isExcluded(rel + "/")) continue;
        walk(full);
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase();
        if (ext !== ".md" && ext !== ".html") continue;
        if (isExcluded(rel)) continue;
        results.push(full);
      }
    }
  }

  walk(root);
  return results.sort();
}

// ── Markdown formatter ────────────────────────────────────────────────
function formatMarkdown(src) {
  let out = src;

  // 1. Normalise line endings to LF
  out = out.replace(/\r\n/g, "\n").replace(/\r/g, "\n");

  // 2. Trim trailing whitespace on every line
  out = out.replace(/[ \t]+$/gm, "");

  // 3. Collapse runs of 3+ blank lines into exactly 2 newlines (one blank line)
  out = out.replace(/\n{3,}/g, "\n\n");

  // 4. Ensure single trailing newline
  out = out.trimEnd() + "\n";

  return out;
}

// ── HTML formatter ────────────────────────────────────────────────────
function formatHTML(src) {
  let out = src;

  // 1. Normalise line endings to LF
  out = out.replace(/\r\n/g, "\n").replace(/\r/g, "\n");

  // 2. Trim trailing whitespace per line
  out = out.replace(/[ \t]+$/gm, "");

  // 3. Collapse runs of 3+ blank lines into 2 newlines
  out = out.replace(/\n{3,}/g, "\n\n");

  // 4. Ensure single trailing newline
  out = out.trimEnd() + "\n";

  return out;
}

// ── Main ──────────────────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  const mode = args[0] || "--check";
  const root = path.resolve(__dirname);
  const files = collectFiles(root);

  let changed = 0;
  const changedPaths = [];

  for (const fp of files) {
    const raw = fs.readFileSync(fp, "utf8");
    const ext = path.extname(fp).toLowerCase();
    const formatted = ext === ".md" ? formatMarkdown(raw) : formatHTML(raw);

    if (formatted !== raw) {
      changed++;
      changedPaths.push(path.relative(root, fp));

      if (mode === "--write") {
        fs.writeFileSync(fp, formatted, "utf8");
      }
    }
  }

  if (mode === "--list" || mode === "--write") {
    for (const p of changedPaths) {
      console.log(p);
    }
  }

  console.log(
    `\n${files.length} files inspected, ${changed} file(s) ${mode === "--write" ? "reformatted" : "would change"}.`
  );

  if (mode === "--check" && changed > 0) {
    process.exit(1);
  }
}

main();
