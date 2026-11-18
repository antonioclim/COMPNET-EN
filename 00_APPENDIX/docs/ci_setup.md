# Continuous integration and local checks

Computer Networks — ASE, CSIE | ing. dr. Antonio Clim

## The workflow in this repository

The authoritative workflow is [ci.yml](../../.github/workflows/ci.yml).
It runs on pushes and pull requests, uses an Ubuntu runner and Python 3.11,
installs the [QA requirements](../../00_TOOLS/qa/requirements.txt), then runs:

```bash
python 00_TOOLS/qa/run_checks.py
```

The same command runs locally and inside the release helper. It performs:

1. Python source syntax parsing without executing lab entry points.
2. Executable permission checks before any repair.
3. Relative Markdown file-target checks; external URLs and heading fragments are outside that check.
4. Language and corrupted-token checks, with the historical root CHANGELOG explicitly excluded.
5. Lecture figure-source checks (`--puml-only`).
6. The pytest component regression suite with third-party plugin autoload disabled.

A failure stops the run. Missing pytest or PyYAML is an error, not a skipped pass.
pytest and PyYAML are pinned; the referenced lecture-test dependencies use bounded
version ranges. This dependency list is not a full transitive lockfile.
The workflow does not run Ruff, build/start containers, boot the OVA, start Mininet
or perform browser, Excel or LMS acceptance. Check the actual run's commit SHA and
log before attributing a CI result to a release candidate.

## Run locally

From the full repository root:

```bash
python3 -m venv .venv-qa
. .venv-qa/bin/activate
python -m pip install -r 00_TOOLS/qa/requirements.txt
python 00_TOOLS/qa/run_checks.py
```

A full Git checkout records executable bits. If an extraction tool discarded
permissions, `bash 00_TOOLS/qa/apply_permissions.sh` can repair that local copy;
record this repair separately from a clean Git checkout check. CI does not run it.

For appendix-only convenience targets, run `make -C 00_APPENDIX help`.
`make -C 00_APPENDIX ci` is an appendix check, not an alias for the repository-wide
workflow. Bash and GNU Make are used for these commands; a PowerShell session
should enter the documented VM/WSL shell first.

## Optional formatting

`node format-offline.js --check` checks only CRLF normalisation and a final newline.
It preserves Markdown hard breaks, code indentation and HTML preformatted content.
It is a conservative helper, not a substitute for a syntax-aware formatter.

## Release preparation

Use the [release helper](../../00_TOOLS/release/README.md) after committing the
reviewed source. Do not interpret passing source checks as native VM acceptance.

The shared gate also requires Node.js 24 for the Python-deck and setup-guide control-logic tests. CI installs it explicitly. Those tests execute actual inline JavaScript with limited DOM/timer/clipboard doubles; they do not establish native browser rendering or keyboard/accessibility acceptance.
