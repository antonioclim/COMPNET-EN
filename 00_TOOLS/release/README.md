# release — Distributable ZIP Builder

Single-script utility for producing a clean, distributable ZIP archive of the course kit. The script runs the QA checks, applies executable permission bits from the manifest and packages the repository while excluding development artefacts.

## File Index

| File | Description | Lines |
|---|---|---|
| [`create_release_zip.sh`](create_release_zip.sh) | Bash script: runs QA, applies permissions, builds ZIP | 60 |

## Usage

From the repository root:

```bash
bash 00_TOOLS/release/create_release_zip.sh
```

To specify an explicit output name:

```bash
bash 00_TOOLS/release/create_release_zip.sh compnet-course-kit.zip
```

The script performs three steps in order: runs the repository QA checks, applies `chmod +x` based on `qa/executable_manifest.txt` and packages a ZIP excluding `.git/`, `node_modules/` and other development-only files.

## Cross-References

| Aspect | Link |
|---|---|
| QA checks (invoked internally) | [`../qa/`](../qa/README.md) |
| Executable manifest | [`../qa/executable_manifest.txt`](../qa/executable_manifest.txt) |
| Permission repair script | [`../qa/apply_permissions.sh`](../qa/apply_permissions.sh) |

No other repository components depend on this directory. It is a leaf node in the build graph.

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/release
```

The release script requires the `qa/` folder to run. Add it:

```bash
git sparse-checkout add 00_TOOLS/qa
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/release
```
