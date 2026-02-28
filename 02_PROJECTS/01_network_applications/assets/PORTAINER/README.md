# 01_network_applications/assets/PORTAINER — Per-Project Portainer Guides

Twenty debugging and observation guides, one per S-project, showing how to use the Portainer container dashboard during E2 development and troubleshooting. Each guide documents the expected container architecture, published ports, log-observation strategies and console commands specific to that project.

## Guide Index

| Subdirectory | Guide file | Project |
|---|---|---|
| [`S01/`](S01/) | `PORTAINER_GUIDE_S01.md` | Multi-client TCP chat |
| [`S02/`](S02/) | `PORTAINER_GUIDE_S02.md` | FTP-style file transfer |
| [`S03/`](S03/) | `PORTAINER_GUIDE_S03.md` | Raw HTTP/1.1 server |
| [`S04/`](S04/) | `PORTAINER_GUIDE_S04.md` | Forward HTTP proxy |
| [`S05/`](S05/) | `PORTAINER_GUIDE_S05.md` | HTTP load balancer |
| [`S06/`](S06/) | `PORTAINER_GUIDE_S06.md` | TCP pub/sub broker |
| [`S07/`](S07/) | `PORTAINER_GUIDE_S07.md` | UDP DNS resolver |
| [`S08/`](S08/) | `PORTAINER_GUIDE_S08.md` | SMTP/POP3 email system |
| [`S09/`](S09/) | `PORTAINER_GUIDE_S09.md` | TCP tunnel multiplexer |
| [`S10/`](S10/) | `PORTAINER_GUIDE_S10.md` | Network file sync |
| [`S11/`](S11/) | `PORTAINER_GUIDE_S11.md` | REST microservices |
| [`S12/`](S12/) | `PORTAINER_GUIDE_S12.md` | TLS messaging |
| [`S13/`](S13/) | `PORTAINER_GUIDE_S13.md` | gRPC service |
| [`S14/`](S14/) | `PORTAINER_GUIDE_S14.md` | DV routing in Mininet |
| [`S15/`](S15/) | `PORTAINER_GUIDE_S15.md` | IoT gateway |
| [`S16/`](S16/) | `PORTAINER_GUIDE_S16.md` | Collaborative text editing |
| [`S17/`](S17/) | `PORTAINER_GUIDE_S17.md` | In-memory object store |
| [`S18/`](S18/) | `PORTAINER_GUIDE_S18.md` | Resource reservation |
| [`S19/`](S19/) | `PORTAINER_GUIDE_S19.md` | Distributed auction |
| [`S20/`](S20/) | `PORTAINER_GUIDE_S20.md` | Database-backed object service |

## Portainer Access

| Setting | Value |
|---|---|
| Dashboard URL | `http://localhost:9050` |
| Login | `stud` / `studstudstud` |

## Cross-References

| Related area | Path | Relationship |
|---|---|---|
| Portainer installation guide | [`../../../../00_TOOLS/Portainer/INIT_GUIDE/`](../../../../00_TOOLS/Portainer/INIT_GUIDE/) | First-time Portainer setup |
| Portainer project overview map | [`../../../../00_TOOLS/Portainer/PROJECTS/PROJECTS_PORTAINER_MAP.md`](../../../../00_TOOLS/Portainer/PROJECTS/PROJECTS_PORTAINER_MAP.md) | Summary with container counts and benefit tiers |
| Project briefs | [`../../`](../../) | Each S{NN} brief defines the Docker Compose topology that Portainer observes |

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/01_network_applications/assets/PORTAINER
```
