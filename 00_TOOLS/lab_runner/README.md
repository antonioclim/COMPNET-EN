# 00_TOOLS/lab_runner — Minimal Lab Runner (Docker Compose)

This folder contains a small **lab runner framework** intended to minimise classroom disruption when starting and stopping Docker Compose scenarios.

It is deliberately conservative:

- **No repository-wide refactor** (pilot integration only).
- **Standard library only** (no Python dependencies).
- Works with either **`docker compose`** (preferred) or legacy **`docker-compose`**.

## Why this exists

In teaching environments, the common failure mode is not “networking is broken”, but:

- a client container starts too early (race conditions),
- a student runs the wrong Compose file from the wrong folder,
- multiple labs collide via the same Compose project name,
- containers remain running from a previous attempt.

`lab_runner.py` provides a predictable interface:

- list labs
- start a lab
- stop a lab
- show status/logs

## Quickstart

Run from the repository root:

```bash
# list registered labs (pilot set)
python 00_TOOLS/lab_runner/lab_runner.py list

# start a lab (default variant)
python 00_TOOLS/lab_runner/lab_runner.py up c10-http-compose --build

# stop a lab
python 00_TOOLS/lab_runner/lab_runner.py down c10-http-compose

# start an optional variant (if defined)
python 00_TOOLS/lab_runner/lab_runner.py up c13-iot-basic --variant tls --build
```

## Design rules (important)

1. **The runner never edits files**. It only calls Compose.
2. **The runner always runs Compose inside the lab folder** so relative paths in Compose files behave as intended.
3. By default, the runner assigns a **project name** derived from the lab id, to avoid collisions.

## How labs are registered

See [`labs.json`](labs.json). Each lab declares:

- `id`
- `path` (relative to repository root)
- `variants` (a mapping: variant name → list of compose files)

Only a small set of labs are registered as a pilot (Phase C). The repository is **not** restructured around the runner.

