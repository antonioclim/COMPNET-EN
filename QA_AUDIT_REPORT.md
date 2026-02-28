# QA_AUDIT_REPORT — Phase C+ (functional coherence hardening)

**Repository snapshot:** COMPNET-EN-main (Phase C + extended lab_runner registry + QA fixes)
**Audit date:** 2026-02-27 (Europe/Bucharest)

This report documents a *paranoid* static audit of the distributed kit archive, aiming for functional coherence across:
- Docker Compose labs (including those registered in `00_TOOLS/lab_runner/labs.json`)
- Python and shell scripts (syntax-level validity)
- Internal QA gate scripts
- Archive hygiene (no accidental bytecode artefacts; executable bits enforced)

## 1. Inventory (what the kit contains)

- Total files (excluding directories): **1248**
- File types (top 12 by count):
  - `.md`: 390
  - `.puml`: 386
  - `.py`: 154
  - `.html`: 101
  - `(no extension)`: 67
  - `.sh`: 55
  - `.json`: 31
  - `.yml`: 24
  - `.conf`: 13
  - `.txt`: 12
  - `.yaml`: 4
  - `.zone`: 2

## 2. QA gates executed (repository-native)

All QA scripts are located under `00_TOOLS/qa/` and were executed from the repository root (as documented by the kit).

- Executability (manifest-driven): **PASS**
  - Checked 96 manifest entries. All entries OK.
- Markdown relative links: **PASS**
  - Markdown link check passed: 390 files scanned, 2231 targets checked.
- Integrity (UTF-8 tokens + Romanian leakage control): **PASS**
  - check_integrity PASSED (no corrupted tokens or Romanian leakage).
- Figure targets (`[FIG]` → `.puml` sources): **PASS**
  - check_fig_targets PASSED (puml-only).

## 3. Docker Compose coherence checks

### 3.1 YAML parse validation
- All `*.yml` and `*.yaml` files were parsed successfully with a strict YAML loader (syntax-level validation).

### 3.2 `depends_on: condition: service_healthy` sanity
- For every registered lab variant, all `depends_on: {service: {condition: service_healthy}}` edges were checked against the merged Compose model.
- Result: **no missing healthchecks** in the merged configurations.

### 3.3 Python-image dependency risk scan (runtime failure detector)
A targeted scan looked for a specific class of common lab breakage:

> Service runs a Python script inside a plain `python:*` image, but the script imports non-stdlib packages and no install/build step exists.

**Findings (fixed in this release):**

| Scenario | Service | Missing dependency class | Fix applied |
|---|---|---|---|
| `C11 scenario-dns-ttl-caching` | `client` | `dnspython` (`import dns.resolver`) | Added `client/Dockerfile` + switched to `build: ./client` |
| `C11 scenario-ftp-baseline` | `ftp` | `pyftpdlib` | Added `server/Dockerfile` + switched to `build: ./server` |
| `C11 scenario-ftp-nat-firewall` | `ftp` | `pyftpdlib` | Added `ftp/Dockerfile` + switched to `build: ./ftp` |
| `C11 scenario-ssh-provision` | `controller` | `paramiko` | Added `controller/Dockerfile` + switched to `build: ./controller` |

These repairs are deliberately minimal-disruption: bind-mounts remain, so students can edit scripts on the host and see changes immediately.

## 4. lab_runner registry audit

- `00_TOOLS/lab_runner/labs.json` loaded successfully (**18 labs registered**).
- Each registered variant was validated for:
  - path existence
  - compose file existence
  - YAML parse validity

Registered labs (ID → variants):
- `c10-http-compose` → advanced-proxy, default
- `c11-dns-ttl-caching` → default
- `c11-ftp-baseline` → default
- `c11-ftp-nat-firewall` → default
- `c11-ssh-provision` → default
- `c12-local-mailbox` → default
- `c13-iot-basic` → cli, default, tls, tls+cli
- `c13-vulnerability-lab` → default
- `c14-week14-integration` → default, tls
- `s08-nginx-compose` → default
- `s09-multi-client-containers` → default
- `s10-dns-containers` → default
- `s10-ssh` → default
- `s10-ssh-port-forwarding` → default
- `s11-custom-load-balancer` → default
- `s11-nginx-compose` → default
- `s13-pentest-compose` → default
- `tool-portainer` → default

## 5. Archive hygiene and distribution correctness

### 5.1 Bytecode artefacts
- **Enforced:** no `__pycache__/` directories and no `*.pyc` files are shipped in the archive.

### 5.2 Executable permissions in zip distribution
- **Enforced before packaging:** `bash 00_TOOLS/qa/apply_permissions.sh`
- **Verified:** `bash 00_TOOLS/qa/check_executability.sh`

## 6. Remaining runtime-only uncertainties (cannot be proven without Docker execution)

The following cannot be fully verified in a static audit environment (no Docker engine available here), but are noted explicitly:

- Healthcheck *semantics* depend on tool availability inside the image (e.g., `grep` in minimal images). The healthchecks were chosen to be conservative and based on common utilities, but runtime confirmation should be done on a real Docker host.
- Scenarios that use `:latest` tags (e.g., `mailserver/docker-mailserver:latest`) are inherently time-variant; pinning is recommended for exam-period reproducibility.
- Privileged networking labs (e.g., NAT/FW) depend on host kernel features and Docker runtime permissions.

## 7. What changed compared to the previous PHASEC+ archive

Only the following functional repairs and hygiene steps were introduced:
- Added four small Dockerfiles for C11 lecture scenarios (DNS, FTP, FTP+NAT, SSH).
- Updated the associated C11 `docker-compose.yml` files to use those builds.
- Updated the four scenario READMEs to keep their file-count tables correct.
- Removed accidental Python bytecode artefacts from the distributed archive.
- Ensured executable bits match the manifest and are preserved in the packaged archive.
