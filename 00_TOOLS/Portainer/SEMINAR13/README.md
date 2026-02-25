# Administrator vs Attacker Perspective (Week 13 — Penetration Testing)

S13 deploys a vulnerable lab environment with isolated attacker and target containers. Portainer gives the administrator (instructor) a bird's-eye view of the lab: which containers are running, what their network isolation looks like and whether any unexpected processes have started. Students working as attackers see only the CLI.

## File Index

| File | Description | Lines |
|---|---|---|
| [`S13_PORTAINER_GUIDE.md`](S13_PORTAINER_GUIDE.md) | Instructor notes — lab topology observation and isolation verification | 119 |
| [`S13_PORTAINER_TASKS.md`](S13_PORTAINER_TASKS.md) | Student activity sheet — security audit using Portainer's container and network views | 125 |

## Cross-References

| Aspect | Link |
|---|---|
| Seminar | [`04_SEMINARS/S13/`](../../../04_SEMINARS/S13/) |
| Lecture | [`03_LECTURES/C13/`](../../../03_LECTURES/C13/) — IoT and security |
| Portainer setup | [`../INIT_GUIDE/PORTAINER_SETUP.md`](../INIT_GUIDE/PORTAINER_SETUP.md) |
| Parent guide | [`../README.md`](../README.md) |
| Instructor notes (Romanian) | [`00_APPENDIX/d)instructor_NOTES4sem/roCOMPNETclass_S13-instructor-outline-v2.md`](../../../00_APPENDIX/d%29instructor_NOTES4sem/roCOMPNETclass_S13-instructor-outline-v2.md) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Portainer/SEMINAR13
```

To also fetch the corresponding seminar materials:

```bash
git sparse-checkout add 04_SEMINARS/S13
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/Portainer/SEMINAR13
```
