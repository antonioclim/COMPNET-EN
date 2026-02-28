# PORTAINER/S19 — Portainer Guide for S19

Distributed auction with bids, timers, state transitions and an event log. The guide in this directory documents the expected container architecture, published ports and Portainer-specific debugging strategies for the E2 execution of project S19.

## Contents

| File | Description |
|---|---|
| [`PORTAINER_GUIDE_S19.md`](PORTAINER_GUIDE_S19.md) | Container map, bid-observation checklist, deadline checks and console commands |

## Cross-References

The project brief lives in the parent [`01_network_applications/`](../../../) directory. The Portainer overview map is at [`../../../../../00_TOOLS/Portainer/PROJECTS/PROJECTS_PORTAINER_MAP.md`](../../../../../00_TOOLS/Portainer/PROJECTS/PROJECTS_PORTAINER_MAP.md).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/01_network_applications/assets/PORTAINER/S19
```
