# RC2026 — Standardisation, automation and common criteria (for all projects)

This directory contains **common templates and tools** that make projects:
- verifiable through automatic capture checks, behaviour tests and explicit semantic evidence
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

### What a successful capture check means

The JSON manifest labels each measurement as frame presence/count, decoded field occurrences, distinct field values or reassembled TCP command lines. A zero exit status means these checks passed. It does not establish the complete application contract, network policy or assessment result: provide the required pytest assertions and complementary evidence listed in the brief.

For S06, S19 and S20 the provided logical command counter assumes LF/CRLF-delimited command tokens. It reassembles sequence numbers, removes identical retransmissions and rejects gaps or conflicting bytes. If E1 defines JSON or binary framing, adapt the decoder to that specification and include segmentation, coalescing, retransmission and negative-token tests. Do not change the rule into a substring search over packets.

For S12, encrypted TLS 1.3 handshake records cannot prove application delivery. Use client certificate-validation tests and application assertions. An optional `--tls-keylog PATH` uses secrets from the local test session to assist analysis; the secrets must remain outside Git.

The validator exits 0 for passed capture checks, 1 for an unmet criterion and 2 for missing/invalid input or a tool error. Empty rule lists and duplicate IDs are errors.

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

> The checklist covers all 30 projects (A01–A10 and S01–S20) in [`RC2026_VERIFICATION_INDEX.xlsx`](../RC2026_VERIFICATION_INDEX.xlsx). MUST/NF identifiers follow the order in each canonical brief.

### E2 scenario traceability

Use the [capture and semantic-evidence matrix](E2_CAPTURE_EVIDENCE_MATRIX.md) to identify the action that produces every rule for all 30 projects. Record the actual test and capture references in `docs/E2_pcap_analysis.md`.
