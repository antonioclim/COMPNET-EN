# Multi-Stack Housekeeping (Week 10 — DNS, SSH, Port Forwarding)

S10 runs multiple Compose stacks (DNS resolver, SSH tunnel, port forwarding). Portainer helps students verify which containers are running, which networks exist and which ports are published — especially the distinction between published and exposed-only ports that is central to the SSH tunnel exercise.

## File Index

| File | Description | Lines |
|---|---|---|
| [`S10_PORTAINER_GUIDE.md`](S10_PORTAINER_GUIDE.md) | Instructor notes — multi-stack management and isolation verification | 124 |
| [`S10_PORTAINER_TASKS.md`](S10_PORTAINER_TASKS.md) | Student activity sheet — container and network inventory tables | 99 |

## Cross-References

| Aspect | Link |
|---|---|
| Seminar | [`04_SEMINARS/S10/`](../../../04_SEMINARS/S10/) |
| Lecture | [`03_LECTURES/C11/`](../../../03_LECTURES/C11/) — FTP, DNS and SSH |
| Portainer setup | [`../INIT_GUIDE/PORTAINER_SETUP.md`](../INIT_GUIDE/PORTAINER_SETUP.md) |
| Parent guide | [`../README.md`](../README.md) |
| Instructor notes (Romanian) | [`00_APPENDIX/d)instructor_NOTES4sem/roCOMPNETclass_S10-instructor-outline-v2.md`](../../../00_APPENDIX/d%29instructor_NOTES4sem/roCOMPNETclass_S10-instructor-outline-v2.md) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Portainer/SEMINAR10
```

To also fetch the corresponding seminar materials:

```bash
git sparse-checkout add 04_SEMINARS/S10
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/Portainer/SEMINAR10
```
