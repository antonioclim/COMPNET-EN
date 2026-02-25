# 00_common/ci — GitHub Actions Template

A single workflow template for automating the E2 gate in student repositories.

## File Index

| File | Description | Lines |
|---|---|---|
| [`github_actions_e2.yml`](github_actions_e2.yml) | GitHub Actions workflow: checkout, `docker compose up --build`, upload `artifacts/` | 27 |

## Usage

Students copy this file into their repository:

```bash
mkdir -p .github/workflows
cp github_actions_e2.yml .github/workflows/e2.yml
```

The workflow triggers on `push` and `pull_request`, builds the Docker Compose stack, runs E2 tests via the tester container and uploads `artifacts/` as a GitHub Actions artefact.

## Cross-References

The workflow assumes the student repository follows the structure defined in [`../README_STANDARD_RC2026.md`](../README_STANDARD_RC2026.md). The tester container it invokes is based on [`../docker/tester_base/`](../docker/tester_base/). The pipeline architecture is documented in [`../assets/puml/fig-ci-github-actions.puml`](../assets/puml/fig-ci-github-actions.puml).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/00_common/ci
```
