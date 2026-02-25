# Instructor Seminar Notes (Romanian)

Romanian-language instructor outlines for seminars S01 through S13. Each seminar has two variants: one assuming a MININET-SDN virtual-machine environment, the other (`__noMININET-SDN_`) adapted for a Docker Desktop + Windows + Wireshark setup without Mininet. An earlier draft (`vi1`) is preserved for S01.

These notes are the primary Romanian-language teaching scripts. The corresponding English seminar materials live in [`04_SEMINARS/`](../../04_SEMINARS/).

## File Index

| Seminar | With Mininet | Without Mininet | Lines (w/ Mininet) | Topic |
|---|---|---|---|---|
| S01 | [`roCOMPNETclass_S01-instructor-outline-v3.md`](roCOMPNETclass_S01-instructor-outline-v3.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S01-instructor-outline-v3__noMININET-SDN_.md) | 429 | Network analysis |
| S02 | [`roCOMPNETclass_S02-instructor-outline-v2.md`](roCOMPNETclass_S02-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S02-instructor-outline-v2__noMININET-SDN_.md) | 456 | TCP/UDP socket programming, traffic analysis |
| S03 | [`roCOMPNETclass_S03-instructor-outline-v2.md`](roCOMPNETclass_S03-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S03-instructor-outline-v2__noMININET-SDN_.md) | 450 | Multi-client TCP, UDP broadcast/multicast/anycast |
| S04 | [`roCOMPNETclass_S04-instructor-outline-v2.md`](roCOMPNETclass_S04-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S04-instructor-outline-v2__noMININET-SDN_.md) | 538 | Custom protocols: text vs binary framing |
| S05 | [`roCOMPNETclass_S05-instructor-outline-v2.md`](roCOMPNETclass_S05-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S05-instructor-outline-v2__noMININET-SDN_.md) | 416 | IPv4/IPv6 subnetting, inter-subnet routing |
| S06 | [`roCOMPNETclass_S06-instructor-outline-v2.md`](roCOMPNETclass_S06-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S06-instructor-outline-v2__noMININET-SDN_.md) | 546 | Static routing, SDN / match-action policies |
| S07 | [`roCOMPNETclass_S07-instructor-outline-v2.md`](roCOMPNETclass_S07-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S07-instructor-outline-v2__noMININET-SDN_.md) | 462 | Packet capture, filtering, port scanning |
| S08 | [`roCOMPNETclass_S08-instructor-outline-v2.md`](roCOMPNETclass_S08-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S08-instructor-outline-v2__noMININET-SDN_.md) | 472 | HTTP on the wire, minimal server, reverse proxy |
| S09 | [`roCOMPNETclass_S09-instructor-outline-v2.md`](roCOMPNETclass_S09-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S09-instructor-outline-v2__noMININET-SDN_.md) | 436 | FTP: dual connections, active vs passive |
| S10 | [`roCOMPNETclass_S10-instructor-outline-v2.md`](roCOMPNETclass_S10-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S10-instructor-outline-v2__noMININET-SDN_.md) | 467 | DNS and SSH in Docker containers |
| S11 | [`roCOMPNETclass_S11-instructor-outline-v2.md`](roCOMPNETclass_S11-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S11-instructor-outline-v2__noMININET-SDN_.md) | 518 | Reverse proxy, load balancing with Compose |
| S12 | [`roCOMPNETclass_S12-instructor-outline-v2.md`](roCOMPNETclass_S12-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S12-instructor-outline-v2__noMININET-SDN_.md) | 526 | RPC: JSON-RPC, Protobuf, gRPC |
| S13 | [`roCOMPNETclass_S13-instructor-outline-v2.md`](roCOMPNETclass_S13-instructor-outline-v2.md) | [`…__noMININET-SDN_.md`](roCOMPNETclass_S13-instructor-outline-v2__noMININET-SDN_.md) | — | Vulnerability scanning and enumeration |

An earlier first-draft outline also exists:

| File | Lines | Note |
|---|---|---|
| [`roCOMPNETclass_S01-outline-vi1.md`](roCOMPNETclass_S01-outline-vi1.md) | — | Superseded by v3 |

Total: 27 files, approximately 13 280 lines.

## Variant Selection

```
┌─────────────────────────────────┐
│  Teaching environment decision  │
├────────────┬────────────────────┤
│  Mininet   │  Docker Desktop    │
│  (VM-based)│  (no Mininet)      │
├────────────┼────────────────────┤
│  *-v2.md   │  *__noMININET-     │
│  *-v3.md   │   SDN_.md          │
└────────────┴────────────────────┘
```

## Cross-References — Instructor Notes ↔ English Seminars

| Instructor note (Romanian) | English seminar |
|---|---|
| S01 | [`04_SEMINARS/S01/`](../../04_SEMINARS/S01/) |
| S02 | [`04_SEMINARS/S02/`](../../04_SEMINARS/S02/) |
| S03 | [`04_SEMINARS/S03/`](../../04_SEMINARS/S03/) |
| S04 | [`04_SEMINARS/S04/`](../../04_SEMINARS/S04/) |
| S05 | [`04_SEMINARS/S05/`](../../04_SEMINARS/S05/) |
| S06 | [`04_SEMINARS/S06/`](../../04_SEMINARS/S06/) |
| S07 | [`04_SEMINARS/S07/`](../../04_SEMINARS/S07/) |
| S08 | [`04_SEMINARS/S08/`](../../04_SEMINARS/S08/) |
| S09 | [`04_SEMINARS/S09/`](../../04_SEMINARS/S09/) |
| S10 | [`04_SEMINARS/S10/`](../../04_SEMINARS/S10/) |
| S11 | [`04_SEMINARS/S11/`](../../04_SEMINARS/S11/) |
| S12 | [`04_SEMINARS/S12/`](../../04_SEMINARS/S12/) |
| S13 | [`04_SEMINARS/S13/`](../../04_SEMINARS/S13/) |

### Related Resources

| Resource | Path | Relationship |
|---|---|---|
| English lectures | [`03_LECTURES/`](../../03_LECTURES/) | Theory each seminar implements |
| Quiz bank | [`../c)studentsQUIZes(multichoice_only)/`](../c%29studentsQUIZes%28multichoice_only%29/) | Student-facing questions aligned per week |
| Portainer guides | [`00_TOOLS/Portainer/`](../../00_TOOLS/Portainer/) | Docker management guides for seminar scenarios |
| Live coding guide | [`../LIVE_CODING_INSTRUCTOR_GUIDE.md`](../LIVE_CODING_INSTRUCTOR_GUIDE.md) | Technique notes for in-class demonstrations |

### Downstream Dependencies

No automated pipeline references these files. They serve as offline teaching scripts and are not consumed by CI or Makefile targets.

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/d)instructor_NOTES4sem"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/d)instructor_NOTES4sem
```

---

*Instructor notes — Computer Networks, ASE Bucharest, CSIE*
*Author: ing. dr. Antonio Clim*
