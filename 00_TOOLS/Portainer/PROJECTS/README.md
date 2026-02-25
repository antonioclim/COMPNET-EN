# Portainer — Project Integration Map

Overview of how Portainer supports the RC2026 project work across all 15 seminar-linked projects. The RC2026 standard requires a `docker/docker-compose.yml` for every project, meaning every student submission runs at least two containers (service + tester). Portainer at `http://localhost:9050` shows all of them without further configuration.

## File Index

| File | Description | Lines |
|---|---|---|
| [`PROJECTS_PORTAINER_MAP.md`](PROJECTS_PORTAINER_MAP.md) | Per-project benefit tier map, container architecture overview and debugging checklist pointers | 71 |

## Cross-References

| Aspect | Link |
|---|---|
| Per-project Portainer guides | [`02_PROJECTS/01_network_applications/assets/PORTAINER/`](../../../02_PROJECTS/01_network_applications/assets/PORTAINER/) |
| Project briefs | [`02_PROJECTS/01_network_applications/`](../../../02_PROJECTS/01_network_applications/) |
| Portainer setup | [`../INIT_GUIDE/PORTAINER_SETUP.md`](../INIT_GUIDE/PORTAINER_SETUP.md) |
| Parent guide | [`../README.md`](../README.md) |

The per-project guides (one per seminar, S01–S15) live alongside the project briefs at `02_PROJECTS/01_network_applications/assets/PORTAINER/SNN/PORTAINER_GUIDE_SNN.md`. This file serves as the entry point and index.

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Portainer/PROJECTS
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/Portainer/PROJECTS
```
