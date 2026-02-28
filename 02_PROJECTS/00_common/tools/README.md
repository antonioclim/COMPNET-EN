# 00_common/tools — PCAP Validation Engine

The PCAP validation script and the full set of per-project rule files that define what constitutes a passing E2 capture. Students copy these into their repositories; the tester container and CI pipeline invoke them automatically.

## File/Folder Index

| Name | Description | Metric |
|---|---|---|
| [`validate_pcap.py`](validate_pcap.py) | Python script: loads a JSON rule file, runs `tshark` with each display filter, checks packet-count thresholds | 173 lines |
| [`pcap_rules/`](pcap_rules/) | Per-project JSON rule files (S01–S20 and A01–A10) | 31 files total (30 JSON rules plus this folder index) |

## Usage

```bash
python validate_pcap.py --project S01 --pcap artifacts/pcap/traffic_e2.pcap
```

The script reads `pcap_rules/S01.json`, iterates over each rule, invokes `tshark` with the specified display filter and compares the packet count against the threshold condition (e.g. `>= 1`, `== 0`). Exit code 0 indicates all rules passed; non-zero indicates at least one failure.

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
