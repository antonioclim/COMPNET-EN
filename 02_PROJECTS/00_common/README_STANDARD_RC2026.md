# RC2026 — Standardisation, automation and common criteria (for all projects)

This directory contains **common templates and tools** that make projects:
- automatically verifiable (deterministic PCAP plus smoke tests)
- reproducible (Docker Compose or scripts)
- consistent across the catalogue (standard repository structure, standard names)

## Minimum recommended structure in the student repository

> This is the **minimum** structure assumed by the automatic assessment.

```
.
├─ README.md
├─ docs/
│  ├─ E1_specification.md
│  ├─ E1_phase0_observations.md
│  ├─ E2_pcap_analysis.md
│  └─ E3_final_documentation.md
├─ src/                  # application code / Python scripts
├─ scripts/              # (A-projects) Bash automation / orchestration
├─ tests/                # pytest (minimum: -m e2)
├─ docker/
│  └─ docker-compose.yml
├─ tools/
│  ├─ validate_pcap.py
│  └─ pcap_rules/
│     └─ <CODE>.json
├─ artifacts/
│  └─ pcap/
│     └─ traffic_e2.pcap
├─ Makefile              # targets: e2, pcap-validate, clean
└─ MANIFEST.txt          # list of delivered artefacts/files (E3)
```

## PCAP validation (tshark)

- Rules are stored in `tools/pcap_rules/<CODE>.json`
- Run:
  - `python tools/validate_pcap.py --project S01 --pcap artifacts/pcap/traffic_e2.pcap`

## Tester template (Docker)

In `docker/tester_base/` there is a starting point for a `tester` service that:
1) starts `tcpdump`
2) runs `pytest -m e2`
3) stops the capture
4) validates the PCAP via `tools/validate_pcap.py`

## CI (GitHub Actions)

In `ci/github_actions_e2.yml` there is a minimal workflow to run E2 and upload `artifacts/` as an artefact.

## E3 evidence (for verification without interpretation)

For E3 assessment to be **fast and deterministic**, `docs/E3_final_documentation.md` must contain a section:

- `## Evidence (ID → artefact/test/command)`

with a table where **every ID** from the project checklist (e.g. `M01..`, `NF01..`, plus relevant gates) is mapped to an **exact** proof.

### Minimum accepted format (template)

| ID | Requirement (summary) | Exact evidence (path + command) | Expected result |
|---|---|---|---|
| M01 | ... | `tests/test_*.py::test_*` / `tshark ...` / `config/...` | PASS |
| NF01 | ... | `config/...` / `logs/...` / `pcap ...` | PASS |

**Rule:** if an ID is missing from the table or the evidence is not reproducible, the criterion is marked **NO**.

> The complete checklist (per project, E1/E2/E3) is in the file `RC2026_VERIFICATION_INDEX.xlsx`.
