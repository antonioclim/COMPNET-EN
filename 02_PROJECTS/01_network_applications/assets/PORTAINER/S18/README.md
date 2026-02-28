# PORTAINER/S18 — Portainer Guide for S18

Resource reservation with holds, leases, wait queue and consistency. The guide in this directory documents the expected container architecture, published ports and Portainer-specific debugging strategies for the E2 execution of project S18.

## Contents

| File | Description |
|---|---|
| [`PORTAINER_GUIDE_S18.md`](PORTAINER_GUIDE_S18.md) | Container map, overlap-observation checklist, timer checks and console commands |

## Cross-References

The project brief lives in the parent [`01_network_applications/`](../../../) directory. The Portainer overview map is at [`../../../../../00_TOOLS/Portainer/PROJECTS/PROJECTS_PORTAINER_MAP.md`](../../../../../00_TOOLS/Portainer/PROJECTS/PROJECTS_PORTAINER_MAP.md).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/01_network_applications/assets/PORTAINER/S18
```
