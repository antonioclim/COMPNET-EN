# Primary Observability Tool (Week 11 — Load Balancing)

S11 is the most Portainer-intensive session. The round-robin load balancer runs three to five backend containers whose logs must be observed simultaneously. Portainer replaces the need for multiple terminal windows and makes the distribution pattern visible at a glance.

## File Index

| File | Description | Lines |
|---|---|---|
| [`S11_PORTAINER_GUIDE.md`](S11_PORTAINER_GUIDE.md) | Instructor notes — simultaneous log observation and round-robin verification | 147 |
| [`S11_PORTAINER_TASKS.md`](S11_PORTAINER_TASKS.md) | Student activity sheet — log capture, request distribution analysis | 136 |

## Cross-References

| Aspect | Link |
|---|---|
| Seminar | [`04_SEMINARS/S11/`](../../../04_SEMINARS/S11/) |
| Lecture | [`03_LECTURES/C12/`](../../../03_LECTURES/C12/) — E-mail (SMTP, POP3, IMAP) |
| Portainer setup | [`../INIT_GUIDE/PORTAINER_SETUP.md`](../INIT_GUIDE/PORTAINER_SETUP.md) |
| Parent guide | [`../README.md`](../README.md) |
| Instructor notes (Romanian) | [`00_APPENDIX/d)instructor_NOTES4sem/roCOMPNETclass_S11-instructor-outline-v2.md`](../../../00_APPENDIX/d%29instructor_NOTES4sem/roCOMPNETclass_S11-instructor-outline-v2.md) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Portainer/SEMINAR11
```

To also fetch the corresponding seminar materials:

```bash
git sparse-checkout add 04_SEMINARS/S11
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/Portainer/SEMINAR11
```
