# Portainer PROJECTS — Map for Seminar-Linked Project Work

Index and rationale for using Portainer during project development and marking. The RC2026 project format standardises `docker/docker-compose.yml` based submissions, so students frequently run multiple containers (service, tester and sometimes support services). Portainer on `http://localhost:9050` provides a single view of container state and logs across all projects.

## File and Folder Index

| Name | Type | Description | Metric |
|---|---|---|---|
| [`README.md`](README.md) | Markdown | Orientation for the project integration map (this file) | — |
| [`PROJECTS_PORTAINER_MAP.md`](PROJECTS_PORTAINER_MAP.md) | Markdown | Per-project index, debugging checklist pointers and suggested Portainer views | 71 lines |

## Visual Overview

```
┌─────────────────────────────┐
│ 02_PROJECTS/.../brief.md     │
│ + docker/docker-compose.yml  │
└───────────────┬─────────────┘
                ▼
┌─────────────────────────────┐
│ docker compose up            │
│ (service + tester + helpers) │
└───────────────┬─────────────┘
                ▼
┌─────────────────────────────┐
│ Portainer (localhost:9050)   │
│ containers · networks · logs │
└─────────────────────────────┘
```

## Usage

Read the map first:

```bash
sed -n '1,120p' PROJECTS_PORTAINER_MAP.md
```

Then open the per-project Portainer walkthroughs located alongside the project briefs:

- `02_PROJECTS/01_network_applications/assets/PORTAINER/SNN/PORTAINER_GUIDE_SNN.md` (one folder per seminar-linked project)

## Design Rationale

The project map is kept under `00_TOOLS/Portainer/` because it describes tool usage rather than project content. The per-project walkthroughs live under `02_PROJECTS/.../assets/PORTAINER/` so they can reference the exact Compose files and expected container names for each submission.

## Cross-References and Contextual Connections

### Prerequisites and Dependency Links

| Prerequisite | Path | Why |
|---|---|---|
| Portainer installed on port 9050 | [`../INIT_GUIDE/`](../INIT_GUIDE/) | The map assumes the dashboard URL and credentials |
| Project briefs and Compose test rig | [`../../../02_PROJECTS/01_network_applications/`](../../../02_PROJECTS/01_network_applications/) | The Portainer views depend on how each project defines containers |

### Lecture, Seminar, Project and Quiz Mapping

| This folder | Lecture foundation | Seminar usage | Project usage | Quiz |
|---|---|---|---|---|
| `PROJECTS_PORTAINER_MAP.md` | — | Applies across seminar-linked project work (S01–S15) | Entry point to the per-project Portainer guides in [`../../../02_PROJECTS/01_network_applications/assets/PORTAINER/`](../../../02_PROJECTS/01_network_applications/assets/PORTAINER/) | Not assessed directly |

### Downstream Dependencies

| Dependent | Path | Relationship |
|---|---|---|
| Portainer parent README | [`../README.md`](../README.md) | Links to this project map |
| Per-project Portainer guides | [`../../../02_PROJECTS/01_network_applications/assets/PORTAINER/`](../../../02_PROJECTS/01_network_applications/assets/PORTAINER/) | Reuse URL, credentials and UI assumptions documented here |

### Suggested Learning Sequence

**Suggested sequence:** [`../INIT_GUIDE/`](../INIT_GUIDE/) → this folder (project map) → a specific project guide under `02_PROJECTS/.../assets/PORTAINER/`

## Selective Clone Instructions

**Method A — Git sparse-checkout (requires Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Portainer/PROJECTS
```

If you want the per-project Portainer guides as well:

```bash
git sparse-checkout add 02_PROJECTS/01_network_applications/assets/PORTAINER
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/Portainer/PROJECTS
```

## Version and Provenance

The mapping document tracks the RC2026 project structure and should be updated if project submission requirements or the Compose test rig change.
