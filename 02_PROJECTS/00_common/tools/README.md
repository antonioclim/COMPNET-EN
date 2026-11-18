# 00_common/tools — PCAP Validation Engine

The PCAP validation script and the full set of per-project rule files that define the automatic measurements required of an E2 capture. Students copy these into their repositories; the tester container and CI pipeline invoke them automatically.

## File/Folder Index

| Name | Description | Metric |
|---|---|---|
| [`validate_pcap.py`](validate_pcap.py) | Python script: loads a JSON rule file, runs `tshark` with each display filter, checks declared frame, field or reassembled-message thresholds | — |
| [`pcap_rules/`](pcap_rules/) | Per-project JSON rule files (S01–S20 and A01–A10) | 31 files total (30 JSON rules plus this folder index) |

## Usage

```bash
python tools/validate_pcap.py --project S01 --pcap artifacts/pcap/traffic_e2.pcap
```

Run this command from the student project root. The script reads `tools/pcap_rules/S01.json`; from this tools directory instead, pass `--rules-dir pcap_rules` explicitly. A non-empty manifest with unique rule IDs is required.

Each rule declares a measurement: matching frames by default, distinct field values, decoded field occurrences or complete reassembled TCP command lines. Exit code **0** means all automatic capture checks passed, **1** means a criterion failed and **2** means an input or tool error. Application tests and every `manual_checks` item remain required for project acceptance. See the [scenario matrix](../E2_CAPTURE_EVIDENCE_MATRIX.md) and [rule schema](pcap_rules/README.md).

## Prerequisites

`tshark` must be installed and available on `PATH`. Inside Docker, the tester-base image includes it.

## Cross-References

| Related area | Path | Relationship |
|---|---|---|
| Rule files | [`pcap_rules/`](pcap_rules/) | One JSON file per project code |
| Tester container | [`../docker/tester_base/`](../docker/tester_base/) | `entrypoint.sh` calls this script |
| CI template | [`../ci/github_actions_e2.yml`](../ci/github_actions_e2.yml) | Workflow runs this via the tester container |
| Architecture diagram | [`../assets/puml/fig-pcap-validation-architecture.puml`](../assets/puml/fig-pcap-validation-architecture.puml) | Visual documentation of the validation pipeline |

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/00_common/tools
```
