# Prerequisites — Environment Setup

Student-facing documentation for configuring the lab environment before the first seminar. The default stack is WSL2 + Ubuntu + Docker Engine + Portainer CE, with Wireshark and Python 3.10+ on the host. Students complete this guide during week 0; the automated verification script confirms readiness.

## File Index

| File | Description | Lines |
|---|---|---|
| [`Prerequisites.md`](Prerequisites.md) | Full installation guide — WSL2, Ubuntu, Docker, Portainer, Wireshark, Python packages and auto-start configuration | 1158 |
| [`Prerequisites_CHECKS.md`](Prerequisites_CHECKS.md) | Self-assessment questions per section of the main guide — understanding checks with expandable answers | 264 |
| [`verify_lab_environment.sh`](verify_lab_environment.sh) | Automated Bash script that tests WSL2, Docker, Portainer, Python and network tools; exits with a pass/fail summary | 506 |
| `wireshark_capture_example.png` | Screenshot used within the prerequisites guide | — |

## Usage

After completing the manual setup steps in `Prerequisites.md`, run the verification script from within WSL/Ubuntu:

```bash
bash verify_lab_environment.sh
```

The script checks: WSL2 presence, Ubuntu version, Docker Engine status, Portainer container health, Python version and key packages and network tool availability. A colour-coded summary is printed at the end. If any component reports a failure, consult the corresponding section of `Prerequisites.md` or the troubleshooting appendix therein.

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
