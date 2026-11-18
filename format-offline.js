#!/usr/bin/env node
/**
 * format-offline.js
 *
 * Deterministic formatting pass for Markdown and HTML files.
 * Preserves significant whitespace; only converts CRLF line endings and adds
 * a missing final newline. Syntax-aware formatting remains a separate task.
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
// This conservative pass deliberately preserves whitespace inside Markdown code,
// hard line breaks and HTML pre/script/style content. It is not a Prettier clone.
function normaliseText(src) {
  const out = src.replace(/\r\n/g, "\n");
  return out.endsWith("\n") || out.length === 0 ? out : out + "\n";
}
function formatMarkdown(src) { return normaliseText(src); }
function formatHTML(src) { return normaliseText(src); }

// ── Main ──────────────────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  const mode = args[0] || "--check";
  if (!["--check", "--write", "--list"].includes(mode)) {
    console.error("Usage: node format-offline.js --check|--write|--list");
    process.exitCode = 2;
    return;
  }
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

module.exports = { formatMarkdown, formatHTML };
if (require.main === module) main();
