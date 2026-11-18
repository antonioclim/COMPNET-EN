# Prerequisites — Environment Setup

Student-facing documentation for the **alternative WSL2 route**. The ASE classroom route uses the [MININET-SDN VirtualBox appliance](../../01_GUIDE_MININET-SDN/). Follow that guide and its [VM verifier](../../01_GUIDE_MININET-SDN/verify_mininet_vm.sh) when using the OVA.

For the WSL alternative, Docker Engine and the course Python environment run inside Ubuntu. Wireshark runs on Windows where required. Portainer is optional and uses loopback port 9050. Passing prerequisite checks does not certify every seminar.

## File Index

| File | Description |
|---|---|
| [`Prerequisites.md`](Prerequisites.md) | Full installation guide — WSL2, Ubuntu, Docker, Portainer, Wireshark, Python packages and auto-start configuration |
| [`Prerequisites_CHECKS.md`](Prerequisites_CHECKS.md) | Self-assessment questions per section of the main guide — understanding checks with expandable answers |
| [`verify_lab_environment.sh`](verify_lab_environment.sh) | Local prerequisite checks for WSL2, Docker, optional Portainer and Linux Python; no package installation or image pull |
| `wireshark_capture_example.webp` | Screenshot used within the prerequisites guide |

## Usage

After completing the manual setup steps in `Prerequisites.md`, run the verification script from within WSL/Ubuntu:

```bash
bash verify_lab_environment.sh
```

The script checks the WSL kernel, Ubuntu metadata, Docker daemon and Compose plugin, optional Portainer API, active Linux Python imports and network tools. Use `--online` only when you also want bounded HTTPS probes. Run it after activating `~/venvs/compnet-wsl`; Windows Python packages are not checked. Errors return exit 1; a wrong execution environment or invalid option returns exit 2. Subprocess prerequisite probes have a 15-second limit and a 2-second forced-stop grace, using GNU `timeout` from Ubuntu coreutils. It does not run Mininet/OpenFlow or a complete seminar.

## Design Rationale

The guide follows a sequential dependency chain (WSL2 → Ubuntu → Docker → Portainer → Wireshark → Python) where each step builds on the previous. The understanding checks in `Prerequisites_CHECKS.md` use expandable `<details>` blocks so that students can self-assess without being exposed to answers prematurely.

## Cross-References and Contextual Connections

### Downstream Dependencies

| Dependent | Path | What it needs |
|---|---|---|
| Root README | [`../../README.md`](../../README.md) | Links to `Prerequisites.md` and `verify_lab_environment.sh` |
| Portainer INIT_GUIDE | [`../Portainer/INIT_GUIDE/`](../Portainer/INIT_GUIDE/) | Docker must be installed first |
| All Docker-based seminars | [`04_SEMINARS/S08/`](../../04_SEMINARS/S08/) onwards | Docker Engine assumed operational |
| All projects | [`02_PROJECTS/`](../../02_PROJECTS/) | Docker Compose required for `make e2` |

### Related Materials

| Aspect | Link |
|---|---|
| Misconceptions supplement | [`00_APPENDIX/docs/misconceptions.md`](../../00_APPENDIX/docs/misconceptions.md) (referenced by `Prerequisites_CHECKS.md`) |
| Python self-study | [`00_APPENDIX/a)PYTHON_self_study_guide/`](../../00_APPENDIX/a%29PYTHON_self_study_guide/) |
| Portainer setup | [`../Portainer/INIT_GUIDE/PORTAINER_SETUP.md`](../Portainer/INIT_GUIDE/PORTAINER_SETUP.md) |

### Suggested Learning Sequence

**Suggested sequence:** this folder (week 0) → [`../Portainer/INIT_GUIDE/`](../Portainer/INIT_GUIDE/) → [`00_APPENDIX/a)PYTHON_self_study_guide/`](../../00_APPENDIX/a%29PYTHON_self_study_guide/) → [`04_SEMINARS/S01/`](../../04_SEMINARS/S01/)

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Prerequisites
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/Prerequisites
```
