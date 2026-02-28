# PHASE A — Implementation status (COMPNET-EN)

**Status:** Completed (low-risk additions, no intentional breaking changes)  
**Date:** 27 February 2026

This section records what was actually *ported/adapted* from `netEN` into `COMPNET-EN`
and what was verified in this integration step.

## A.1 Implemented carry-overs (netEN → COMPNET-EN)

### R2 — Mininet/OVS deep reset helper
- **Added:** `00_TOOLS/mininet/ovs_reset.sh`
- **Why it is worth porting:** netEN includes a pragmatic “clean the mess” utility which removes stale OVS bridges and leftover controller processes; this reduces lab disruption when Mininet fails to reconnect.
- **Verification performed:** `bash -n` syntax check; executable bit set; added to `00_TOOLS/qa/executable_manifest.txt`.

### R8 — PCAP statistics helper (lightweight)
- **Added:** `00_TOOLS/pcap/pcap_stats.py`
- **Notes:** implemented with *auto backend selection* (Scapy → dpkt → pure classic-PCAP parser) to stay functional even when third‑party libraries are absent.
- **Verification performed:**
  - `python3 -m py_compile` (syntax sanity),
  - generated a minimal classic PCAP and confirmed correct protocol counts with `--backend pure --json`.

### R16 — Demo PCAP capture helper
- **Added:** `00_TOOLS/pcap/capture_demo.sh` (+ `00_TOOLS/pcap/artifacts/.gitkeep`)
- **Verification performed:** `bash -n` syntax check; executable bit set; added to manifest.

### R7 — MQTT TLS optional assets + CLI client (IoT scenario)
- **Updated (non-breaking):**
  - `03_LECTURES/C13/assets/scenario-iot-basic/docker-compose.yml` (environment normalised to mappings; Mosquitto config mount changed to a directory)
  - `03_LECTURES/C13/assets/scenario-iot-basic/mosquitto/mosquitto.conf` (adds `include_dir` for optional snippets)
  - `03_LECTURES/C13/assets/scenario-iot-basic/sensor/sensor.py` (TLS optional via env)
  - `03_LECTURES/C13/assets/scenario-iot-basic/actuator/actuator.py` (TLS optional via env)
  - `03_LECTURES/C13/assets/scenario-iot-basic/README.md` (updated run instructions)
- **Added (optional TLS):**
  - `03_LECTURES/C13/assets/scenario-iot-basic/docker-compose.tls.yml`
  - `03_LECTURES/C13/assets/scenario-iot-basic/tls/` (CA/server/private layout + `generate_demo_certs.sh` + `mosquitto_tls.conf` + README)
- **Added (optional CLI client):**
  - `03_LECTURES/C13/assets/scenario-iot-basic/docker-compose.cli.yml`
  - `03_LECTURES/C13/assets/scenario-iot-basic/client/` (Dockerised `mqtt_cli.py`)
- **Verification performed:**
  - YAML parsing of all Compose files,
  - `python3 -m py_compile` for modified Python files,
  - `bash -n` for `generate_demo_certs.sh`,
  - executed certificate generator and verified:
    - CA chain: `openssl verify -CAfile ca/ca.crt server/server.crt`
    - SAN presence: includes `DNS:broker`, `DNS:localhost`, `IP:127.0.0.1`
  - (Generated cert artefacts were removed afterwards; only generator + directories are shipped.)

### R6 — Defensive vulnerability checker for S13
- **Added:** `04_SEMINARS/S13/S13_Part05_Script_Defensive_Vuln_Checker.py`
- **Design constraints:** defensive-only (banner grabbing + conservative HTTP GET); no exploit attempts; standard-library only.
- **Outputs:** JSON is written to `04_SEMINARS/S13/artifacts/` by default.

### R15 — Markdown report generator helper for S13
- **Added:** `04_SEMINARS/S13/report_generator.py`
- **Added:** `04_SEMINARS/S13/artifacts/.gitkeep`
- **Outputs:** aggregates `vulncheck_*.json` + optional notes file into `artifacts/report.md`.

### R17 — Advanced Os‑Ken policy controller (extra SDN part)
- **Added:** `04_SEMINARS/S06/2_sdn/S06_Part02C_Script_SDNOS_Ken_Controller_AdvancedPolicy.py`
- **Also corrected (doc bugfix):** `04_SEMINARS/S06/2_sdn/S06_Part02D_Tasks_SDN.md` now references the correct script names and includes the optional advanced controller.

### R9 — Dynamic subnet quiz generator (optional)
- **Added:** `00_TOOLS/subnetting/subnet_quiz_generator.py` (+ README)
- **Modes:** IPv4 CIDR questions + small VLSM scenario generator.
- **Verification performed:** `python3 -m py_compile`; `--markdown` output generation.

## A.2 Repository integration hygiene

- `00_TOOLS/qa/executable_manifest.txt` updated to include:
  - `00_TOOLS/mininet/ovs_reset.sh`
  - `00_TOOLS/pcap/*`
  - `00_TOOLS/subnetting/subnet_quiz_generator.py`
  - `03_LECTURES/C13/assets/scenario-iot-basic/tls/generate_demo_certs.sh`

---

# REVISELOG — netEN → COMPNET-EN (curated carry‑overs)

**Date:** 27 February 2026  
**Backbone:** `COMPNET-EN-main` (kept as canonical)  
**Input analysed:** `netEN-main.zip` (legacy kit) with cross-checks against `COMPNET-EN-main.zip` (current kit)  
**Focus:** Docker Compose (`*.yml`/`*.yaml`), Python (`*.py`), Bash (`*.sh`) — reviewed for functionality, robustness, and pedagogical value.

---

## 0. Why this file exists (and what it is *not*)

You asked for a “blood-level” review of the **legacy** kit (`netEN-main`) and then a **curated** list of things worth revising and migrating into **COMPNET** *only if* they add genuine value and are not mere repetition.

This document is **not** a migration script and it is **not** a diff dump. It is a **reasoned, educationally oriented code review** with concrete integration proposals.

---

## 1. Methodology and evidence that the review is exhaustive

### 1.1 File inventory (scripts and compose only)
I extracted both archives and enumerated only the requested file types:

- `netEN-main`: **307** files (`.yml/.yaml/.py/.sh`)
- `COMPNET-EN-main`: **212** files (`.yml/.yaml/.py/.sh`)

### 1.2 Content identity check (to avoid recommending duplicates)
I computed SHA‑256 hashes for every relevant file in both kits and matched identical contents.

- **9** distinct content hashes are shared between kits, corresponding to **21** `netEN` files with byte-identical twins in COMPNET.
- These are mostly `__init__.py` placeholders and a few Docker demo files already present in COMPNET, so they are **not** recommended for migration.

**Exactly identical `netEN` files (already in COMPNET):**
- `WEEK1/python/__init__.py`
- `WEEK1/python/utils/__init__.py`
- `WEEK11/docker/dns_demo/client/query.py`
- `WEEK11/docker/dns_demo/docker-compose.yml`
- `WEEK11/docker/ftp_demo/client/ftp_client.py`
- `WEEK11/docker/ftp_demo/docker-compose.yml`
- `WEEK11/docker/ftp_demo/nat_variant/docker-compose.yml`
- `WEEK11/docker/ftp_demo/nat_variant/natfw/setup.sh`
- `WEEK11/docker/ssh_demo/controller/provision.py`
- `WEEK11/docker/ssh_demo/docker-compose.yml`
- `WEEK2/python/__init__.py`
- `WEEK2/python/apps/__init__.py`
- `WEEK2/python/utils/__init__.py`
- `WEEK4/python/__init__.py`
- `WEEK4/python/apps/__init__.py`
- `WEEK4/python/solutions/__init__.py`
- `WEEK4/python/templates/__init__.py`
- `WEEK4/python/utils/__init__.py`
- `WEEK7/python/__init__.py`
- `WEEK7/python/apps/__init__.py`
- `WEEK7/python/utils/__init__.py`

### 1.3 What “adds value” means in this ReviseLog
I only recommend carry‑overs that improve at least one of:

1. **Reliability** (less “works on my machine”; fewer race conditions; fewer port collisions).
2. **Reproducibility** (deterministic endpoints/ports; predictable artefact handling; repeatable scripts).
3. **Pedagogical leverage** (new perspective, new comparison axis, or a better teaching scaffold).
4. **Safety & ethics for security labs** (safe-by-design demos over real exploit primitives).
5. **Maintainability** (less duplicated boilerplate; shared helpers; coherent structure).

If a legacy item is **already present** (or better replaced) in COMPNET, I explicitly say “**do not port**”.

---

## 2. High-value carry‑overs (recommended)

> **Reading guide:**  
> Each recommendation has: **(a)** netEN sources; **(b)** why it matters; **(c)** COMPNET target(s); **(d)** “line-range” review (“what each block actually does”); **(e)** a minimal integration recipe.

---

### R1 — Add a *standard* `verify / run_all / cleanup / smoke_test` runner pattern (student‑friendly and CI‑friendly)

**netEN sources (examples):**
- `WEEK1/scripts/verify.sh`
- `WEEK1/scripts/run_all.sh`
- `WEEK1/scripts/cleanup.sh`
- `WEEK1/tests/smoke_test.sh`
- (richer example) `WEEK13/scripts/run_all.sh`

**Why it is worth porting**
COMPNET already has a strong repo-wide QA layer (`00_TOOLS/qa/*`), but it does **not** provide a **per-scenario** or **per-lecture** “press one button to validate and/or demo” runner that:

- creates **artefacts/logs** in a deterministic location,
- checks **syntax sanity** across Python and Bash,
- validates `docker compose config`,
- can be used both by **students** (self-check) and **TAs** (fast grading sanity),
- and can be wired into CI without requiring deep scenario knowledge.

In short: netEN’s runner pattern is an *operational scaffold* that reduces friction and support load.

**COMPNET nearest equivalent**
- `00_TOOLS/qa/check_integrity.py` etc. (repo-level consistency checks)
- `00_TOOLS/Prerequisites/verify_lab_environment.sh` (environment checks)

These are important, but they do not replace a **module-level** runner.

**Proposed COMPNET targets**
- Add a new folder: `00_TOOLS/lab_runner/`
  - `verify_code_sanity.sh` (bash -n, python -m py_compile, docker compose config)
  - `run_all_template.sh` (pattern for artefacts, logging, safe continuation)
  - `cleanup_template.sh`
  - `smoke_test_template.sh`
- For selected lectures/seminars with Docker/Mininet, add a tiny wrapper:
  - `03_LECTURES/C11/assets/scenario-ftp-nat-firewall/run_all.sh`
  - `04_SEMINARS/S13/run_all.sh`
  - etc., **only where it really helps**.

#### R1.1 Line-range review: `WEEK1/scripts/verify.sh`
- **Lines 1–2:** shebang + `set -euo pipefail` → strict Bash (good; prevents silent errors).
- **Lines ~10–17:** locate repo root and artefacts folder → makes script location-independent.
- **Lines ~19–34:** check toolchain presence (`python3`, `docker`, `docker compose`, `mn`) → avoids cryptic failures.
- **Lines ~36–60:** static checks:
  - `bash -n` on scripts,
  - `python -m py_compile` on exercises,
  - `docker compose config` if compose exists.
- **Net effect:** *fast*, non-destructive verification.

**What to improve before porting**
- Turn repeated “check command exists” blocks into a small shared helper function (`require_cmd`).
- Consider a `--strict` flag:
  - default: best-effort checks (do not fail on missing Docker if not required for that module),
  - strict: fail fast (useful in CI).

#### R1.2 Line-range review: `WEEK1/scripts/run_all.sh`
Key design choices worth keeping:

- **Strict mode** at the top, then selectively using `|| true` where continuing makes sense.
- **Artefacts directory** (`artifacts/`) created early and used consistently for logs, pcap, and validation.
- **Timestamped run header** in logs → makes TA debugging easier.
- Optional **tcpdump capture** (when available) → produces a pcap “proof” of traffic.

**What to improve before porting**
- Add a `--no-sudo` mode (some environments forbid sudo).
- Make capture interface explicit (`IFACE=...`) rather than relying on `-i any` always.

#### R1.3 Line-range review: `WEEK13/scripts/run_all.sh` (why it matters)
This is the “mature” runner:

- Reads `.env` (ports) **with sane defaults**.
- Uses a venv **if present**, but doesn’t require it.
- Runs multiple tools and records outcomes without stopping at the first failure (good for labs).

**Port idea**
COMPNET can adopt the *pattern*, not necessarily every action, especially for:
- vulnerability lab (defensive checks, artefacts)
- docker stacks with multiple ports (port collisions are common in student laptops)

**Minimal integration recipe**
1. Create `00_TOOLS/lab_runner/verify_code_sanity.sh`.
2. Add one pilot wrapper in a Docker-heavy scenario, e.g. `C11 scenario-ftp-nat-firewall`.
3. Provide a single README snippet:  
   “Run `./run_all.sh` to produce `artifacts/demo.log` and `artifacts/validation.txt`.”
4. (Optional) hook into CI with `bash 00_TOOLS/lab_runner/verify_code_sanity.sh`.

---

### R2 — Add an “OVS/Mininet hard reset” tool (`ovs_reset.sh`) to reduce lab downtime

**netEN source:**
- `WEEK5/scripts/ovs_reset.sh`

**Why it is worth porting**
Mininet + OVS labs sometimes end up in broken states (dangling bridges, stale namespaces, half-dead controllers). Students then waste 30–60 minutes on “it’s not working” without learning networking.

This script provides a **surgical reset**. COMPNET currently lacks an equivalent single-command “OVS reset button”.

**Proposed COMPNET target**
- `01_GUIDE_MININET-SDN/tools/ovs_reset.sh`  
  (or `00_TOOLS/mininet/ovs_reset.sh` and referenced from the guide)

#### Line-range review: `WEEK5/scripts/ovs_reset.sh`
- **Lines 1–2:** strict Bash mode.
- **Lines ~10–60:** CLI options:
  - `--help`, `--dry-run`, `--force`
  - colour output, *but tolerates non-TTY*.
- **Lines ~62–90:** root privilege check (OVS reset really needs sudo).
- **Lines ~92–150:** controlled teardown:
  - kills Mininet/OVS related processes only (does not carpet-bomb the system),
  - deletes bridges with `ovs-vsctl list-br`.
- **Lines ~152–190:** service restart logic:
  - tries `systemctl` if present,
  - falls back to `service` where appropriate.
- **Lines ~192–230:** sanity verification:
  - confirms no stale bridges remain,
  - prints what it did.

**What to revise before porting**
- Ensure distro portability: Ubuntu/Debian vs Fedora service names.
- Add a prominent warning banner:
  - “This will disrupt local OVS setups outside the lab”.

**Minimal integration recipe**
1. Copy script with minimal edits (paths, banners).
2. Add it to the Mininet guide as the official “if everything is broken” step.
3. Add a 2-line diagnostic: `mn -c` first, then `ovs_reset.sh` only if needed.

---

### R3 — Adopt Docker Compose healthchecks + `depends_on: condition: service_healthy` where it prevents race conditions

**netEN sources (examples):**
- `WEEK9/docker/docker-compose.yml` (FTP server + clients; *service_healthy gating*)
- `WEEK10/docker/docker-compose.yml` (multi-service lab with healthchecks)
- `WEEK8/docker/docker-compose.yml` (proxy/backends; healthchecks)
- `WEEK14/docker/docker-compose.yml` (integration lab; healthchecks + multi-network)

**Why it is worth porting**
COMPNET contains several docker-compose scenarios where:
- a “client” container starts immediately and tries to connect,
- but the server is not yet ready,
- and the client script has no retry → **flaky labs**.

The healthcheck + `service_healthy` pattern makes labs much more deterministic.

**Concrete COMPNET pain points**
Example: `03_LECTURES/C11/assets/scenario-ftp-nat-firewall/docker-compose.yml` starts `client` after `ftp`, but `depends_on` only enforces *start order*, not readiness. The Python client does **not** retry.

**Proposed COMPNET targets (high impact)**
- Add healthchecks to:
  - `C11 scenario-ftp-nat-firewall` (ftp service)
  - `C11 scenario-ssh-provision` (node1 SSH daemon)
  - `C11 scenario-dns-ttl-caching` (resolver/auth)
- For scenarios with a dedicated “client” container:
  - update `depends_on` to `condition: service_healthy` (supported by modern docker compose)

#### Line-range review: `WEEK9/docker/docker-compose.yml`
- **FTP server service:**
  - installs `pyftpdlib` at runtime (ok for labs, but can be moved to Dockerfile),
  - exposes control port and a small passive range,
  - defines a **healthcheck** that TCP-connects to the service port.
- **Clients:**
  - use `depends_on: condition: service_healthy` to start only after server is reachable,
  - run scripted commands automatically (useful for automated demos/tests).

**What to revise before porting**
- Replace “runtime `pip install`” with a small Dockerfile in COMPNET (faster and more predictable).
- Keep “automatic client actions” as an *optional* profile to avoid removing manual exploration.

---

### R4 — Port the `.env` auto-port allocator (`generate_env.sh`) for multi-service labs (prevents student port collisions)

**netEN source:**
- `WEEK13/scripts/generate_env.sh`

**Why it is worth porting**
Port collisions are *the* most common Docker lab failure in student machines, especially when multiple labs are run in the same week (WebGoat, DVWA, Mosquitto, etc.).

COMPNET currently tends to use **fixed host ports** in compose files (e.g., S13 pentest). netEN’s approach is better: it generates a `.env` choosing available ports.

**Proposed COMPNET targets**
- `04_SEMINARS/S13/` (pentest stack) — add optional `.env` + port allocator
- Potentially `03_LECTURES/C13/assets/scenario-iot-basic/` if adding TLS listener (see R7)

#### Line-range review: `WEEK13/scripts/generate_env.sh`
- **Lines 1–2:** strict mode.
- **Lines ~10–30:** argument parsing:
  - output file path,
  - optional “preferred” ports as inputs.
- **Lines ~32–60:** function that checks if a port is free
  - uses `ss`/`lsof` style checks (depending on system).
- **Lines ~62–120:** chooses ports:
  - if preferred is free → keep it,
  - else search next available in a safe range.
- **Lines ~122–end:** writes `.env` with key/value pairs.

**What to revise before porting**
- Make the port-check method robust across distros and WSL:
  - prefer `python -c` socket bind test (no dependencies) as fallback.
- Add deterministic bounds (e.g., “only choose in 18000–18999 unless override”).
- Add a “do not overwrite existing .env unless --force” safeguard.

**Minimal integration recipe**
1. Place the script in `00_TOOLS/docker/generate_env.sh`.
2. In S13 compose, change ports from hard-coded to `${VAR:-default}`.
3. Provide a make target (or a tiny wrapper script) to run generator and then compose.

---

### R5 — Replace *real exploit primitives* with a safe simulation stub for the vsftpd “backdoor” demo

**netEN sources:**
- `WEEK13/docker/Dockerfile.vulnerable`
- `WEEK13/docker/entrypoint_vsftpd.sh`
- (compose uses it) `WEEK13/docker/docker-compose.yml`

**Why it is worth porting**
In security teaching, the pedagogical goal is usually:
- observe unexpected open ports,
- practise scanning, logging, and containment,
- understand version fingerprinting and patching logic.

netEN achieves this by exposing a **safe stub backdoor** (a TCP listener that prints a banner). It explicitly states that **no real exploitation is implemented**.

This approach reduces the risk of teaching a working exploit chain while preserving the learning objectives.

**Where COMPNET currently stands**
- COMPNET S13 includes an FTP backdoor exploit exercise script targeting vsftpd 2.3.4.  
  That crosses into a “working exploit primitive” style demo.

**Proposed COMPNET target**
- In `04_SEMINARS/S13/assets/`, add an *alternative* vsftpd service:
  - either build from netEN’s Dockerfile,
  - or provide a “safe backdoor stub” container separate from vsftpd.
- Keep the current material as “optional / instructor-only” if needed, but the default student path should remain defensive.

#### Line-range review: `entrypoint_vsftpd.sh`
- **Strict mode** prevents partial startup.
- Starts a background loop that:
  - listens on `BACKDOOR_PORT` via `nc`,
  - prints a static banner explaining it is a safe stub,
  - logs connections into `/artifacts/vsftpd_backdoor.log`.
- Then execs vsftpd normally.

**What to revise before porting**
- Ensure `nc` flavour detection remains robust across Debian/BusyBox.
- Add rate limiting (sleep) to avoid log flooding during scans.

---

### R6 — Add a defensive “vulnerability checker” with structured JSON output (teaches *enumeration*, not exploitation)

**netEN source:**
- `WEEK13/python/exercises/ex_04_vuln_checker.py`

**Why it is worth porting**
COMPNET S13 already covers scanning. netEN adds a *defensive* tool that:
- fingerprints banners / headers,
- detects intentionally vulnerable targets (DVWA),
- outputs a structured JSON report,
- explicitly avoids exploitation.

This is a better bridge from “scanning” to “report writing”, which is the real-world professional skill.

**Proposed COMPNET targets**
- `04_SEMINARS/S13/` as an extra script in the scanning/enumeration section.
- Optionally integrate with `report_generator.py` (R8) to create a one-click lab report.

#### Line-range review highlights
- Defines dataclasses `Finding` and `Report` → good structured outputs.
- Implements:
  - `tcp_banner()` (generic banner read),
  - `http_probe()` (raw HTTP request and header parsing),
  - MQTT reachability via TCP connect only (safe).
- Produces human-readable output *and* optional `--json-out`.

**What to revise before porting**
- Replace hard-coded string heuristics with clearly labelled “heuristics”.
- Ensure timeouts are configurable for slow systems.

---

### R7 — Upgrade the IoT MQTT scenario with *TLS as an optional second listener* + a CLI MQTT test client

**netEN sources:**
- `WEEK13/configs/mosquitto/mosquitto.conf` (plaintext + TLS listener)
- `WEEK13/python/exercises/ex_02_mqtt_client.py` (CLI publish/subscribe; TLS support)

**Why it is worth porting**
COMPNET already has an IoT MQTT scenario (`C13 scenario-iot-basic`) but only on plaintext `1883` with anonymous access. Adding TLS as an optional variant enables:

- a clean “security upgrade” narrative,
- comparison of plaintext vs TLS at packet level,
- demonstration of CA trust, certificate validation, and common misconfigurations.

**Proposed COMPNET target**
- Extend `03_LECTURES/C13/assets/scenario-iot-basic/`:
  - update `mosquitto.conf` to include an additional listener `8883`,
  - add a `configs/certs/` directory generated by a small script,
  - add a `tools/mqtt_client.py` (adapt from netEN) for manual testing.

#### Line-range review: `mosquitto.conf`
- Defines two listeners:
  - `1883` plaintext for lab simplicity,
  - `8883` TLS with server-auth only.
- Uses `cafile`, `certfile`, `keyfile`.
- Keeps `allow_anonymous true` (acceptable for labs; clearly label as lab-only).

#### Line-range review: `ex_02_mqtt_client.py`
- Uses `argparse` for clear CLI.
- Implements both publish and subscribe modes.
- TLS mode:
  - requires `--cafile`,
  - supports `--insecure` (explicitly warned as not recommended).
- Prints a readable configuration header and formats JSON payloads nicely.

**Critical fix before porting**
In `netEN`, the certificate directory is generated by a Makefile target; it is not present as static files.  
In COMPNET, you should ship a **scripted** cert generator (e.g., `scripts/generate_mqtt_certs.sh`) so students do not have to guess.

---

### R8 — Add “pcap_stats” as a light-weight PCAP summary tool (dpkt-based), plus optional tshark conversation summaries

**netEN sources:**
- `WEEK1/python/exercises/ex_1_04_pcap_stats.py` (dpkt summary)
- `WEEK7/python/utils/traffic_analysis.py` (tshark conv tables)

**Why it is worth porting**
COMPNET already has a strong `validate_pcap.py` tool (project-oriented). netEN provides two complementary ideas:

1. A **zero-Wireshark** / **low-dependency** pcap summary (dpkt), useful early in the course.
2. A “best-effort” tshark summary that does **not** fail if tshark is missing, which is student-friendly.

**Proposed COMPNET targets**
- `00_TOOLS/pcap/pcap_stats.py` (based on netEN Week1)
- `00_TOOLS/pcap/pcap_tshark_summary.py` (based on netEN Week7)

#### Line-range review: `ex_1_04_pcap_stats.py`
- Reads pcap with `dpkt.pcap.Reader`.
- Counts:
  - total packets,
  - per-protocol distribution (IPv4/IPv6/TCP/UDP/ICMP/ARP),
  - total bytes.
- Produces a deterministic, parseable printout.

**What to revise before porting**
- Add a `--json` option for machine-readable output.
- Add graceful fallback when dpkt is not installed (print “install dpkt”).

#### Line-range review: `traffic_analysis.py`
- Wraps `tshark` conv tables; saves output into artefacts.
- If `tshark` is missing, it prints guidance but does not crash the entire lab run.

---

### R9 — Port the dynamic subnetting quiz generator and the reusable IP calculation helpers (as an *optional* practice mode)

**netEN sources:**
- `WEEK5/python/exercises/ex_5_03_quiz_generator.py`
- `WEEK5/python/utils/net_utils.py`

**Why it is worth porting**
COMPNET already contains formative quizzes, but netEN’s generator is different: it creates **fresh random subnetting questions** each run. That is pedagogically valuable because:

- it supports deliberate practice without memorising fixed answers,
- it can generate “near-miss” distractors systematically,
- it can be used during seminars as a live warm-up activity.

**Proposed COMPNET targets**
- Add `00_APPENDIX/formative/generators/subnet_quiz_generator.py`
- Optionally expose it via `00_APPENDIX/formative/run_quiz.py --generate subnetting`

#### Line-range review highlights: `ex_5_03_quiz_generator.py`
- Uses dataclasses (`QuizQuestion`) and typed functions → maintainable.
- Implements multiple question archetypes:
  - network/broadcast/host range,
  - subnet count and host capacity,
  - VLSM reasoning,
  - IPv6 compression / prefix logic.
- CLI supports:
  - interactive,
  - `--num-questions`,
  - deterministic seed (good for reproducible assessment).

#### Line-range review highlights: `net_utils.py`
- Provides correct handling for edge cases:
  - `/31` and `/32` semantics,
  - avoids enumerating hosts for large networks,
  - includes wildcard masks, summarisation helpers, IPv6 type/scope.

**What to revise before porting**
- Split into two layers:
  - `ipcalc_core.py` (pure logic; no printing),
  - `cli_tools.py` (prints/formatting),
  to keep COMPNET scripts simple while reusing robust logic underneath.

---

### R10 — Add a didactic “endianness + framing + CRC” exercise with a real selftest mode

**netEN source:**
- `WEEK9/python/exercises/ex_9_01_endianness.py`

**Why it is worth porting**
COMPNET already has a strong `struct` parsing example in the Python self-study guide, but netEN’s script adds:

- a deliberately designed custom binary header,
- explicit “wrong endianness” decoding demonstration,
- CRC32 to connect “bit/byte representation” with “integrity checks”.

This makes it a strong bridge between “programming bytes” and “network protocol design”.

**Proposed COMPNET target**
- `00_APPENDIX/a)PYTHON_self_study_guide/examples/04_endianness_and_framing_crc.py`
  - and/or a lecture addon in C09 (encoding/binary formats).

**Key design notes worth keeping**
- `--selftest` mode that asserts correctness (“All tests passed”).
- Separation between encode/decode functions and CLI.

**What to revise before porting**
- Replace any locale-specific payload strings with neutral text, or make it explicit that UTF‑8 is part of the teaching point.

---

### R11 — Add a standalone HTTPS server exercise that *generates its own certificates* and offers a selftest (bridges C08 TLS and C10 HTTP/REST)

**netEN source:**
- `WEEK10/python/exercises/ex_10_01_https.py`

**Why it is worth porting**
COMPNET already teaches TLS via OpenSSL and HTTP/REST via separate scenarios. netEN’s script makes the bridge explicit:

- students see how TLS wraps HTTP at the server side,
- they can test with both `curl` and Python clients,
- they can inspect certificates and common pitfalls.

**Proposed COMPNET target**
- Either:
  - `03_LECTURES/C08/assets/scenario-https-python/` (TLS-centric placement), or
  - `03_LECTURES/C10/assets/scenario-https-rest-mini/` (REST-centric placement).

**Line-range review highlights**
- Certificate generation via `openssl` invoked from Python when needed.
- HTTP server implemented with `http.server` + SSL wrapping.
- Implements minimal REST-ish endpoints and a `--selftest`.

**What to revise before porting**
- Ensure OpenSSL dependency is clearly stated (and provide a “skip cert generation” fallback).
- Keep it optional: do not replace existing TLS/REST materials; this is a bridge module.

---

### R12 — Add a Week 14 “integration lab” docker topology (two networks + LB + /health + /lb-status) as a capstone *exercise scaffold*

**netEN sources:**
- `WEEK14/docker/docker-compose.yml`
- `WEEK14/python/apps/backend_server.py`
- `WEEK14/python/apps/lb_proxy.py`

**Why it is worth porting**
COMPNET C14 is currently revision-oriented. netEN offers an **integration scaffold** that ties together:

- container networking and segmentation,
- health checks,
- load balancing behaviour,
- basic observability (/health, /info, /lb-status).

This is ideal as a “capstone lab” or a project starter.

**Proposed COMPNET target**
- `03_LECTURES/C14/assets/scenario-integration-lab/`
  - include compose + backend_server + lb_proxy,
  - plus a short task sheet (“break it; observe; fix it”).

#### Line-range review: `WEEK14/docker/docker-compose.yml`
- Defines **two networks**:
  - backend_net: servers + load balancer,
  - frontend_net: client + load balancer.
- Uses static IPs → deterministic addressing for debugging.
- Uses healthchecks and `depends_on: condition: service_healthy` to avoid races.
- Provides a client container to run curl and record artefacts.

#### Line-range review: `backend_server.py`
- Implements endpoints for:
  - `/health` (for healthchecks),
  - `/info` (JSON diagnostics),
  - `/slow` (for latency experiments),
  - `/echo` (header introspection).
- Adds `X-Backend-ID` header → makes LB behaviour visible without packet capture.

#### Line-range review: `lb_proxy.py`
- More advanced than COMPNET’s current S11 simple LB:
  - supports multiple HTTP methods,
  - adds forwarding headers,
  - tracks backend health on repeated failure,
  - exposes `/lb-status` with backend stats.

**Porting stance**
Do **not** replace the simple S11 LB.  
Instead: keep the simple one for first principles, and add this as an advanced/optional capstone.

---

### R13 — Add “advanced HTTP proxies” as optional exercises: rate limiting and caching proxy (currently missing from COMPNET)

**netEN sources (exercise skeletons):**
- `WEEK8/python/exercises/ex04_rate_limiting.py`
- `WEEK8/python/exercises/ex05_caching_proxy.py`

**Why it is worth porting**
COMPNET covers HTTP basics, reverse proxies, and Nginx. What’s missing (and valuable) is a hands-on implementation of:

- application-level rate limiting (token bucket / leaky bucket concepts),
- caching proxy logic (Cache-Control, TTL, keying).

netEN includes the scaffolding. Even though they are TODO skeletons, the *idea* fills a real gap.

**Proposed COMPNET target**
- Add to `04_SEMINARS/S11` (proxy week) or `03_LECTURES/C10` (HTTP/REST week):
  - `assets/scenario-proxy-advanced/`
  - with a completed reference solution in `solutions/` and tasks in `README.md`.

**What must be revised before porting**
- These scripts contain TODOs and mixed-language comments; they need:
  - complete implementation (or keep as explicit student task),
  - unit tests or a simple harness to validate behaviour,
  - consistent English style and output conventions.

---

### R14 — Salvage the *idea* of RPC benchmarking, but rewrite the script (the current netEN script is not production-quality)

**netEN source (concept only):**
- `WEEK12/scripts/benchmark_rpc.sh`

**Value**
Comparing **JSON-RPC vs XML-RPC vs gRPC** on the same toy method is an excellent teaching device:
- serialisation overhead,
- request/response sizes,
- latency distribution under load.

**Why it cannot be ported as-is**
The script contains multiple typos and broken commands (`withrl`, malformed headers, invalid redirections). It would confuse students and fail in CI.

**Recommended COMPNET action**
- Implement a clean benchmarking script in COMPNET S12 (RPC week) that:
  - uses `curl` correctly,
  - records results to `artifacts/benchmark.csv`,
  - optionally plots simple summaries (median, p95),
  - includes a “sanity check” mode.

---


---

### R15 — Add a tiny “report generator” to turn JSON outputs into a Markdown lab report (teaches professional reporting)

**netEN source:**
- `WEEK13/python/utils/report_generator.py`

**Why it is worth porting**
Students routinely produce *artefacts* (pcaps, logs, JSON outputs) but often submit them as unstructured files. This script demonstrates a professional workflow:

- take structured JSON findings,
- generate a **short Markdown report** with timestamp,
- attach the key outputs (paths) so the report is auditable.

COMPNET has strong tooling, but does not currently ship a “turn results into a report” helper in the teaching flow.

**Proposed COMPNET targets**
- `04_SEMINARS/S13/tools/report_generator.py` (best fit: security reporting)
- optionally mirrored into `02_PROJECTS/00_common/tools/` if you want it for multiple projects.

#### Line-range review: `report_generator.py`
- **Lines 1–15:** imports + defines `generate_report()` as the main API.
- **Lines ~17–60:** loads JSON, extracts “findings”, builds Markdown text:
  - title,
  - timestamp,
  - per-finding bullet list.
- **Lines ~62–end:** writes to disk and returns output path.

**What to revise before porting**
- Add an explicit schema expectation (“what keys must exist in the JSON”).
- Add a `--template` option (future‑proofing), but keep default very simple.

**Minimal integration recipe**
1. In S13, run the vuln checker with `--json-out artifacts/report.json`.
2. Run report generator to output `artifacts/report.md`.
3. Tell students: “Submit `report.md` + referenced artefacts.”

---

### R16 — Add a standard “generate a pcap on demand” demo script (reduces Wireshark friction, improves early labs)

**netEN sources (examples):**
- `WEEK1/scripts/capture_demo.sh`
- (related patterns) `WEEK3/scripts/capture_traffic.sh`

**Why it is worth porting**
Early in the course, students often struggle with “I captured nothing” because:
- they captured on the wrong interface,
- they did not generate traffic,
- or the service was not reachable.

`capture_demo.sh` addresses this brutally simply:
- start `tcpdump`,
- generate a few TCP and UDP packets to known local ports with `nc`,
- stop capture,
- produce a pcap that *must* contain packets.

This is extremely useful as a “sanity pcap generator” to validate their toolchain and to feed into pcap analysis scripts (R8).

**Proposed COMPNET target**
- `00_TOOLS/pcap/capture_demo.sh`

#### Line-range review: `capture_demo.sh`
- Starts capture with a filter that is intentionally broad enough to see TCP+UDP traffic.
- Uses `nc` to generate:
  - a TCP connect attempt (SYN / RST path still appears in capture),
  - UDP datagrams (appear even with no listener).
- Stops tcpdump cleanly and prints where the pcap is stored.

**What to revise before porting**
- Add a `--iface` argument for systems where `-i any` is not permitted.
- Add a `--filter` argument so later labs can focus on specific ports/protocols.
- Make output directory default to `artifacts/` if present (COMPNET convention).

---

### R17 — Provide an “advanced” OS‑Ken SDN controller variant (policy + ARP handling + default L2 learning + flow timeouts)

**netEN source:**
- `WEEK6/seminar/python/controllers/sdn_policy_controller.py`

**Why it is worth porting**
COMPNET already introduces SDN control, but the current OS‑Ken controller example is intentionally minimal.

netEN’s controller adds *teaching depth* without adding black magic:

- an explicit policy table with constants students can tweak,
- correct and explicit ARP handling (so the lab does not “mysteriously break”),
- flow timeouts to illustrate why flows expire,
- “policy rules” *and* a default L2 learning switch mode so the rest of the network still works.

This is excellent as an **advanced extension** after the basic controller is understood.

**Proposed COMPNET target**
- `04_SEMINARS/S06/2_sdn/S06_Part02D_Script_SDNOS_Ken_Policy_Controller.py`  
  (add as a new “Part D” rather than replacing the existing file)

#### Line-range review highlights
- **Lines 1–37:** documentation block with SDN architecture diagram and usage.
- **Lines 52–71:** “educational configuration constants”:
  - host IPs,
  - `ALLOW_UDP_TO_H3`,
  - flow timeouts.
- **Lines 97–130:** installs a table-miss rule that forwards unknown packets to controller.
- **Lines 136–186:** `_add_flow()` wrapper encapsulates OpenFlow flow_mod creation (clean teaching abstraction).
- **Lines 239–260:** ARP handling:
  - learns MACs,
  - forwards/floods ARP without installing long-lived flows (reasonable for teaching).
- **Lines 284–310:** allows h1↔h2 by installing a specific IPv4 match flow.
- **Lines 316–365:** policy for traffic to h3:
  - optionally allow UDP if configured,
  - otherwise install drop flows (empty actions list).
- **Lines 370–387:** default L2 learning switch behaviour for non-policy traffic.

**What to revise before porting**
- Align IPs and topology constants with COMPNET’s S06 addressing.
- Add a short “student exercises” section:
  1. “Allow UDP to h3” (toggle constant),
  2. “Block ICMP to h2 only” (match on `ip_proto=1`),
  3. “Add a hard timeout and observe”.


## 3. Items explicitly *not* recommended (already present or weaker than COMPNET)

This section exists so you can see that these were considered but rejected as “non-additive”.

1. **PlantUML tooling** (`APPENDIX(week0)/PlantUML/*`)  
   COMPNET already includes a maintained equivalent under `00_TOOLS/PlantUML(optional)/`.

2. **Week 11 docker demos for DNS/FTP/SSH**  
   Several are byte-identical or conceptually already covered in `C11` scenarios.

3. **Many early-week TCP/UDP echo scripts**  
   COMPNET includes richer and better-structured scenarios and seminar tasks for these.

4. **Simple transmission delay calculator** (`WEEK1/python/exercises/ex_1_04_transmission_delay.py`)  
   Correct but too trivial to justify adding as a dedicated COMPNET asset (unless you want it as a 5-minute warm-up).

---

## 4. Suggested implementation roadmap (minimise disruption)

### Phase A — Low-risk additions (new tools, no breaking changes)
1. Add `00_TOOLS/mininet/ovs_reset.sh` (R2).
2. Add `00_TOOLS/pcap/pcap_stats.py` and optional `pcap_tshark_summary.py` (R8).
3. Add `00_TOOLS/pcap/capture_demo.sh` (R16).
4. Add MQTT TLS optional assets + CLI client to IoT scenario (R7).
5. Add defensive vuln checker to S13 (R6).
6. Add the small Markdown `report_generator.py` helper to S13 (R15).
7. Add the “advanced OS‑Ken policy controller” as an extra SDN part (R17).
8. Add dynamic subnet quiz generator as optional (R9).

### Phase B — Reliability improvements (small edits to compose files)
1. Add healthchecks to docker-compose files where a client starts immediately (R3).
2. Add optional `.env` port generator to S13 (R4).

### Phase C — Capstone and runner framework (bigger structural change)
1. Introduce `00_TOOLS/lab_runner/` and pilot in 1–2 scenarios (R1).
2. Add Week 14 integration lab to C14 (R12).
3. Add advanced proxy exercises (R13) once you have reference solutions/tests.

---

## 5. References (contextual, not required for using the kit)

These references are included only to support the educational design choices (reproducibility, SDN teaching context, containerised labs).  
All DOIs are provided in the reference table.

*(Populated after DOI verification.)*


# PHASE B — Implementation status (COMPNET-EN)

**Status:** Completed (reliability improvements; small edits; no intended breaking changes)  
**Date:** 27 February 2026

This phase focuses on *race-condition reduction* in Docker labs and on making S13
more robust in environments where common host ports are already in use.

## B.1 Implemented improvements

### R3 — Healthchecks + `depends_on: condition: service_healthy` (client-start race reduction)

**Problem observed in practice**
Some scenarios start a “client” container immediately (or a controller that makes
a network connection immediately). If the server is not yet listening, students
see a failure that looks like a “network problem”, but it is only a start-up race.

**What was changed (files touched)**
Healthchecks were added to server-side services, and client-side services now
wait for “healthy” readiness instead of mere container start.

- `03_LECTURES/C10/assets/scenario-http-compose/docker-compose.yml`
  - Added healthchecks for `web` (port 8000) and `api` (port 5000).
  - `nginx` now waits for `web` + `api` to be **healthy** before starting.

- `03_LECTURES/C11/assets/scenario-dns-ttl-caching/docker-compose.yml`
  - Added healthchecks for `auth` (bind9) and `resolver` (unbound) using a
    minimal `/proc/1/comm` process-name probe.
  - `resolver` now waits for `auth` to be healthy; `client` waits for `resolver`.

- `03_LECTURES/C11/assets/scenario-ftp-baseline/docker-compose.yml`
  - Added healthcheck for `ftp` using a local TCP connect probe to port 2121.
  - `client` now waits for `ftp` to be healthy.

- `03_LECTURES/C11/assets/scenario-ftp-nat-firewall/docker-compose.yml`
  - Added healthcheck for `ftp` (TCP connect probe on 2121).
  - Added healthcheck for `natfw` (requires `ip_forward=1` and a MASQUERADE
    rule present).
  - `client` now waits for both `natfw` and `ftp` to be healthy.

- `03_LECTURES/C11/assets/scenario-ssh-provision/docker-compose.yml`
  - Added healthcheck for `node1` (PID 1 comm name `sshd`).
  - `controller` now waits for `node1` to be healthy.

- `03_LECTURES/C13/assets/scenario-iot-basic/docker-compose.yml`
  - Added healthcheck for `broker` using `mosquitto_pub` against localhost:1883.
  - `sensor` + `actuator` now wait for `broker` to be healthy.

- `03_LECTURES/C13/assets/scenario-iot-basic/docker-compose.cli.yml`
  - `mqtt-cli` now waits for `broker` to be healthy (when profile `cli` is used).

- `03_LECTURES/C13/assets/scenario-vulnerability-lab/docker-compose.yml`
  - Added healthcheck for `target` (TCP connect probe on 8080).
  - `attacker` now waits for `target` to be healthy.

**Why this is low-risk**
- No ports, networks, or volumes were changed.
- The “server logic” remains identical; only the orchestration order is improved.
- Healthchecks use conservative probes (TCP connect or PID1 comm string) to avoid
  dependencies on extra tooling inside images.

**Verification performed**
- YAML parse validation (`yaml.safe_load`) for each modified compose file.
- Sanity review of each healthcheck command to ensure it relies on commands that
  exist in the corresponding image (Python for python-slim containers; `/proc` for
  minimal images; mosquitto CLI for mosquitto).

---

### R4 — Optional `.env` host-port generator for S13 (port conflict mitigation)

**Problem observed in practice**
S13 publishes commonly-used host ports (`8080`, `8888`, `2121`). On student
machines, these are frequently already used by other labs, local services, or IDE
previews, causing “it doesn’t work” situations unrelated to the seminar content.

**What was added**
- `04_SEMINARS/S13/generate_env_ports.py` (executable; standard library only)
- `04_SEMINARS/S13/.env.example`
- `04_SEMINARS/S13/s13_env.py` (tiny parser used by S13 scripts)

**What was changed**
- `04_SEMINARS/S13/S13_Part02_Config_Docker_Compose_Pentest.yml`
  - Host port mappings now support variable expansion with safe defaults:
    - DVWA: `${DVWA_HOST_PORT:-8888}:80`
    - WebGoat: `${WEBGOAT_HOST_PORT:-8080}:8080`
    - vsftpd: `${VSFTPD_HOST_PORT:-2121}:21`
    - backdoor: `${VSFTPD_BACKDOOR_HOST_PORT:-6200}:6200`

- Documentation updates (to avoid “hard-coded port” assumptions):
  - `04_SEMINARS/S13/README.md`
  - `S13_Part01_Explanation_Pentest_Intro.md`
  - `S13_Part02_Tasks_Pentest.md`
  - `S13_Part07_Explanation_Exploitation.md`
  - `S13_Part08_Tasks_Exploitation.md`
  - `S13_Part09_Explanation_Exploit_Script.md`

- Script resilience updates (host-side tools now auto-read `.env` if present):
  - `S13_Part05_Script_Defensive_Vuln_Checker.py`
  - `S13_Part09_Script_FTP_Backdoor_Exploit.py`

**Important micro-fix included (correctness)**
While integrating `.env`, several Stage 3/Stage 4 commands mixed *container IPs*
with *host-published ports* (example: `172.20.0.10:8888`). These commands would
not work as written. They were corrected to either:
- use container IP + container port (e.g. DVWA on `172.20.0.10:80`, vsftpd on `:21`)
  where the text is clearly about the internal lab network, OR
- use `localhost:<published port>` where the text is explicitly about published ports.

**Verification performed**
- `python3 -m py_compile` for the new/modified S13 Python scripts.
- YAML parse validation for the updated S13 compose file.
- Updated `00_TOOLS/qa/executable_manifest.txt` to include the new executable
  `generate_env_ports.py`.


---

# PHASE C — Implementation status (COMPNET-EN)

**Status:** Completed (capstone + runner framework; pilot integrations; optional advanced proxy overlay)  
**Date:** 27 February 2026

This phase implements the larger structural/pedagogical additions proposed in the roadmap:

- a minimal **lab runner** framework to reduce classroom friction
- a **Week 14 integration capstone** lab (DNS → HTTP → TLS → proxy)
- optional **advanced proxy exercises** for C10, with reference config + a small test

## C.1 Added `00_TOOLS/lab_runner/` (R1 pilot)

**Added**
- `00_TOOLS/lab_runner/lab_runner.py` (Compose wrapper: list/up/down/ps/logs)
- `00_TOOLS/lab_runner/labs.json` (pilot lab registry)
- `00_TOOLS/lab_runner/README.md`

**Pilot integration**
- Registered labs:
  - `c10-http-compose` (default + advanced-proxy variant)
  - `c13-iot-basic` (default + tls/cli variants)
  - `c14-week14-integration` (default + tls variant)

**Verification performed**
- `python3 -m py_compile` on `lab_runner.py`
- JSON parse validation for `labs.json`

## C.2 Added Week 14 integration lab to C14 (R12)

**Added**
- `03_LECTURES/C14/assets/scenario-week14-integration-lab/` (Compose scenario)
- `03_LECTURES/C14/c14-week14-integration-lab.md` (handout)

**Scenario features**
- Authoritative DNS (BIND) + caching resolver (Unbound)
- Reverse proxy (nginx) routing:
  - `/` → `/app/` redirect
  - `/app/` → backend web (load-balanced)
  - `/api/` → backend API
- TLS termination overlay (`docker-compose.tls.yml`) with local cert generator
- Client toolbox container with dependency-free scripts:
  - `dns_query.py` (A-record + TTL)
  - `http_probe.py`
  - `smoke_test.py`

**Verification performed**
- YAML parse validation for both Compose files
- `python3 -m py_compile` for client scripts
- `bash -n` for `tls/generate_demo_certs.sh`

## C.3 Added C10 advanced proxy overlay + tests (R13)

**Added**
- `03_LECTURES/C10/assets/scenario-http-compose/advanced/`
  - overlay Compose file (adds `web2`)
  - `nginx.advanced.conf` enabling load balancing + forwarded headers + rate limit + caching
  - host-side `test_advanced_proxy.py` smoke test
  - reference solution copy

**Updated (backwards compatible)**
- `03_LECTURES/C10/assets/scenario-http-compose/web/server.py`
  - adds `X-Web-Instance` header (via `WEB_INSTANCE` env)
- `03_LECTURES/C10/assets/scenario-http-compose/README.md`
  - documents advanced overlay and lab runner usage

**Verification performed**
- `python3 -m py_compile` for new Python scripts
- YAML parse validation for overlay Compose file

## C.4 Documentation and manifests

- `00_TOOLS/README.md` updated to include the new `lab_runner/` tool.
- `03_LECTURES/C13/assets/scenario-iot-basic/README.md` updated with lab runner usage.
- `03_LECTURES/C14/README.md` updated to index the integration lab.
- `00_TOOLS/qa/executable_manifest.txt` updated to include new executable scripts (see Phase C commit set).

- `CHANGELOG.md` rewritten as an English-only high-level changelog (detailed notes remain in this file).
- Removed Markdown links to non-versioned `__pycache__/` folders in `00_APPENDIX/formative/` to satisfy link checks.


## Post-Phase C QA hardening (functional coherence)

This section captures *paranoid* post-integration repairs applied after Phase C + the expanded lab registry.

### C+.1 Fix: Docker lecture scenarios that previously failed at runtime (missing Python dependencies)

Several lecture Compose scenarios under `03_LECTURES/C11/assets/` executed Python scripts that import **third‑party packages**, but the containers were plain `python:*` images with **no build step** and **no `pip install`**. As a result, `docker compose up` would fail immediately with `ModuleNotFoundError`.

**Repaired (minimal-disruption approach):** add a tiny service-local `Dockerfile` that installs the required dependency, while keeping the original bind-mounts so students can still edit scripts live.

- `03_LECTURES/C11/assets/scenario-dns-ttl-caching/`
  - **Added** `client/Dockerfile` (installs `dnspython`)
  - **Updated** `docker-compose.yml` — `client` now uses `build: ./client` instead of a raw `python:*` image

- `03_LECTURES/C11/assets/scenario-ftp-baseline/`
  - **Added** `server/Dockerfile` (installs `pyftpdlib`)
  - **Updated** `docker-compose.yml` — `ftp` now uses `build: ./server`

- `03_LECTURES/C11/assets/scenario-ftp-nat-firewall/`
  - **Added** `ftp/Dockerfile` (installs `pyftpdlib`)
  - **Updated** `docker-compose.yml` — `ftp` now uses `build: ./ftp`

- `03_LECTURES/C11/assets/scenario-ssh-provision/`
  - **Added** `controller/Dockerfile` (installs `paramiko`)
  - **Updated** `docker-compose.yml` — `controller` now uses `build: ./controller`

**Notes**
- Dependencies are intentionally installed at image build time (one-off), rather than on every container start via `sh -c "pip install ... && ..."`.
- Bind-mount behaviour is preserved: scripts are still editable on the host and immediately visible in the container.

### C+.2 Repo hygiene: remove accidental bytecode artefacts from distributed archives

To keep the kit clean and deterministic (and to avoid students confusing `__pycache__` as “course content”), the following artefacts are excluded from the shipped archive:
- all `__pycache__/` directories
- all `*.pyc` files

### C+.3 Executability coherence for zip distribution

The repository’s QA system relies on `00_TOOLS/qa/executable_manifest.txt`. For archives generated outside Git, executable bits can be lost unless explicitly enforced and packaged correctly.

**Applied before packaging**
- `bash 00_TOOLS/qa/apply_permissions.sh`
- verified by `bash 00_TOOLS/qa/check_executability.sh`

