# 00_common/assets/puml — Shared Architecture Diagrams (PlantUML)

Six PlantUML source files that document the RC2026 assessment infrastructure: CI pipelines, the E2 validation workflow, tester container lifecycle and the expected student-repository layout.

## File Index

| File | Subject | Lines |
|---|---|---|
| [`fig-ci-github-actions.puml`](fig-ci-github-actions.puml) | GitHub Actions E2 workflow (checkout → build → upload) | 42 |
| [`fig-e2-pipeline-overview.puml`](fig-e2-pipeline-overview.puml) | End-to-end E2 execution pipeline | 52 |
| [`fig-pcap-validation-architecture.puml`](fig-pcap-validation-architecture.puml) | PCAP validation architecture (tshark filters → rule engine) | 68 |
| [`fig-project-assessment-phases.puml`](fig-project-assessment-phases.puml) | E1/E2/E3 phase relationships and deliverables | 48 |
| [`fig-student-repo-structure.puml`](fig-student-repo-structure.puml) | Minimum student-repository directory tree | 63 |
| [`fig-tester-container-lifecycle.puml`](fig-tester-container-lifecycle.puml) | Tester container: start → tcpdump → pytest → validate → exit | 53 |

## Usage

Render all diagrams via the parent script:

```bash
bash ../render.sh
```

Output PNGs appear in `../images/`.

## Cross-References

These diagrams illustrate the standards in [`../../README_STANDARD_RC2026.md`](../../README_STANDARD_RC2026.md) and the CI template in [`../../ci/github_actions_e2.yml`](../../ci/github_actions_e2.yml).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/00_common/assets/puml
```
