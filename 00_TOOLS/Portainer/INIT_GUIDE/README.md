# Portainer — Installation and Configuration Guide

Pre-semester setup for Portainer Community Edition on port 9050. Students (or instructors) run this once; the container persists across all Docker-heavy seminars from week 8 onwards.

## File Index

| File | Description | Lines |
|---|---|---|
| [`PORTAINER_SETUP.md`](PORTAINER_SETUP.md) | Step-by-step installation guide covering Windows (PowerShell) and Linux/WSL (Bash) paths | 218 |
| [`docker-compose-portainer.yml`](docker-compose-portainer.yml) | Declarative Compose file — the recommended deployment method | 23 |
| [`portainer-init.ps1`](portainer-init.ps1) | PowerShell automation script for Windows hosts | 153 |
| [`portainer-init.sh`](portainer-init.sh) | Bash automation script for Linux/WSL hosts | 121 |

## Usage

The fastest path is the Compose file:

```bash
docker compose -f docker-compose-portainer.yml up -d
```

Then open `http://localhost:9050` and log in with `stud` / `studstudstud`.

For automated setup with health checks and credential pre-configuration, use the platform-appropriate script:

```bash
# Linux / WSL
bash portainer-init.sh

# Windows PowerShell
.\portainer-init.ps1
```

## Design Rationale

Port 9050 was chosen because port 9000 is reserved for the S10 SSH tunnel exercise and port 9090 is occupied by C08 TCP handshake scenarios. The Compose file pins the image to `portainer/portainer-ce:2.21-alpine` for reproducibility.

## Cross-References

| Aspect | Link |
|---|---|
| Parent guide | [`../README.md`](../README.md) |
| Docker prerequisites | [`../../Prerequisites/Prerequisites.md`](../../Prerequisites/Prerequisites.md) |
| First use in class | [`../SEMINAR08/S08_PORTAINER_TEASER.md`](../SEMINAR08/S08_PORTAINER_TEASER.md) |
| First full introduction | [`../SEMINAR09/S09_PORTAINER_GUIDE.md`](../SEMINAR09/S09_PORTAINER_GUIDE.md) |

No other repository components reference this directory directly. The setup is a one-time operation with no downstream CI or build dependencies.

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Portainer/INIT_GUIDE
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/Portainer/INIT_GUIDE
```
