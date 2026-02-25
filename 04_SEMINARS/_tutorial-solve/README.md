# _tutorial-solve — Reference Solutions

This directory contains reference solutions and sample outputs for selected seminars. Students should attempt each exercise independently before consulting these materials. Solutions are added incrementally; not all seminars have solutions available.

## Folder Index

| Directory | Corresponding Seminar | Contents |
|---|---|---|
| [`s1/`](s1/) | [`../S01/`](../S01/) — Wireshark, netcat, traffic debugging | 3 files: output for Parts 02 (basic tools), 04 (netcat) and 06 (Wireshark) |
| [`s2/`](s2/) | [`../S02/`](../S02/) — TCP/UDP socket programming | 1 file: completed TCP server template |

## File Detail

| File | Description |
|---|---|
| [`s1/S01_Part02_Output_Basic_Tools.txt`](s1/S01_Part02_Output_Basic_Tools.txt) | Expected output from CLI network tool exercises |
| [`s1/S01_Part04_Output_Netcat_Activity.txt`](s1/S01_Part04_Output_Netcat_Activity.txt) | Expected netcat session output |
| [`s1/S01_Part06_Output_Wireshark_Activity.md`](s1/S01_Part06_Output_Wireshark_Activity.md) | Expected Wireshark capture analysis |
| [`s2/S02_Part02_Solution_TCP_Server_Template.py`](s2/S02_Part02_Solution_TCP_Server_Template.py) | Completed TCP server template (Python) |

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| S01 tasks | [`../S01/`](../S01/) | Exercises whose solutions are in `s1/` |
| S02 template | [`../S02/S02_Part02_Template_TCP_Server.py`](../S02/S02_Part02_Template_TCP_Server.py) | The template that `s2/` solves |

No other repository components depend on this directory. It is strictly supplementary.

## Selective Clone

**Method A — Git sparse-checkout (requires Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 04_SEMINARS/_tutorial-solve
```

**Method B — Direct download**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/04_SEMINARS/_tutorial-solve
```

---

*Course: COMPNET-EN — ASE Bucharest, CSIE*
