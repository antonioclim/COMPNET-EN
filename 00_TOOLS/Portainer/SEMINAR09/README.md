# Portainer Introduction (Week 9 — Multi-client FTP)

First proper encounter with Portainer during S09 Part 3, where the course transitions from single-process Python scripts to a multi-container Docker Compose stack (FTP server + two clients on an isolated bridge network). The two-to-three-minute introduction covers the Containers list, Networks view and log tailing.

## File Index

| File | Description | Lines |
|---|---|---|
| [`S09_PORTAINER_GUIDE.md`](S09_PORTAINER_GUIDE.md) | Instructor notes — timing, pedagogical objectives and suggested phrasing | 65 |
| [`S09_PORTAINER_TASKS.md`](S09_PORTAINER_TASKS.md) | Student activity sheet — fill-in tables and reflection questions | 74 |

## Cross-References

| Aspect | Link |
|---|---|
| Seminar | [`04_SEMINARS/S09/`](../../../04_SEMINARS/S09/) |
| Lecture | [`03_LECTURES/C11/`](../../../03_LECTURES/C11/) — FTP, DNS and SSH |
| Portainer setup | [`../INIT_GUIDE/PORTAINER_SETUP.md`](../INIT_GUIDE/PORTAINER_SETUP.md) |
| Parent guide | [`../README.md`](../README.md) |
| Instructor notes (Romanian) | [`00_APPENDIX/d)instructor_NOTES4sem/roCOMPNETclass_S09-instructor-outline-v2.md`](../../../00_APPENDIX/d%29instructor_NOTES4sem/roCOMPNETclass_S09-instructor-outline-v2.md) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Portainer/SEMINAR09
```

To also fetch the corresponding seminar materials:

```bash
git sparse-checkout add 04_SEMINARS/S09
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/Portainer/SEMINAR09
```
