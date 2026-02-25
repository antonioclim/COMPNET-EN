# 00_common/docker — Tester Container Templates

Base Docker image and entrypoint script for the `tester` service that every RC2026 project includes alongside its application container.

## File/Folder Index

| Name | Description |
|---|---|
| [`tester_base/`](tester_base/) | Dockerfile and entrypoint script for the reference tester container |

## Design Rationale

Centralising the tester pattern ensures that all projects follow the same capture-and-validate workflow: start `tcpdump`, execute `pytest -m e2`, stop the capture and run PCAP validation. Students extend or adapt this base for project-specific test scenarios.

## Cross-References

The CI workflow in [`../ci/github_actions_e2.yml`](../ci/github_actions_e2.yml) invokes this container. The entrypoint calls [`../tools/validate_pcap.py`](../tools/validate_pcap.py) as its final step. The container lifecycle is documented in [`../assets/puml/fig-tester-container-lifecycle.puml`](../assets/puml/fig-tester-container-lifecycle.puml).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/00_common/docker
```
