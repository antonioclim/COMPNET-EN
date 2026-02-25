# release — Course Kit Packaging

Maintainer-only helper for producing a distributable ZIP archive of the repository. The script runs the repository QA checks first, then builds a ZIP using the inclusion and exclusion rules encoded in `create_release_zip.sh`.

## File and Folder Index

| Name | Type | Description | Metric |
|---|---|---|---|
| [`README.md`](README.md) | Markdown | Orientation for release packaging (this file) | — |
| [`create_release_zip.sh`](create_release_zip.sh) | Bash | Runs QA, then builds the release ZIP (path printed on success) | 60 lines |

## Usage

Run from the repository root:

```bash
bash 00_TOOLS/release/create_release_zip.sh
```

The script prints the output ZIP path and exits non-zero if a QA check fails.

## Design Rationale

Release creation is kept as a single script so that local packaging follows the same gates as CI. Packaging rules are kept next to the build logic to avoid divergence between documentation and what is actually shipped.

## Cross-References and Contextual Connections

### Prerequisites and Dependency Links

| Prerequisite | Path | Why |
|---|---|---|
| QA checks pass | [`../qa/`](../qa/) | The release builder aborts on failing checks |
| `zip` available | — | The script uses `zip` to produce the archive |

### Lecture, Seminar, Project and Quiz Mapping

| This folder | Lecture foundation | Seminar usage | Project usage | Quiz |
|---|---|---|---|---|
| Release packaging | — | — | — | — |

### Downstream Dependencies

No course content depends on this directory at runtime. It is referenced by tool documentation and by the executable permission manifest.

### Suggested Learning Sequence

**Suggested sequence:** run QA locally (`00_TOOLS/qa/`) → run this script → distribute the resulting ZIP through the course channel

## Selective Clone Instructions

**Method A — Git sparse-checkout (requires Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/release
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/release
```

## Version and Provenance

The release builder is updated when the packaging exclusions change or when the QA checks gain new gates.
