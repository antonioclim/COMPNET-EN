# cheatsheets — Python Networking Quick Reference

Fast lookup notes for the Python constructs used repeatedly in COMPNET seminars: socket calls, `struct` packing, CLI argument parsing and byte/Unicode handling. The intended use is during lab work when syntax recall is the only blocker.

## File and Folder Index

| Name | Description | Metric |
|---|---|---|
| [`README.md`](README.md) | Orientation for the cheatsheet folder | — |
| [`PYTHON_QUICK.md`](PYTHON_QUICK.md) | Single-page cheatsheet (socket API, `struct`, `argparse`, `bytes`/`str`) | 178 lines |

## Usage

Open `PYTHON_QUICK.md` in a split view next to the terminal.

## Design Notes

The cheatsheet is separated from the long-form guide to keep lookup latency low during labs. Explanations are intentionally minimal; when a student cannot justify a construct, route them back to the bridge guide rather than extending the cheatsheet.

## Cross-References and Context

### Prerequisites and Dependencies

| Prerequisite | Path | Why |
|---|---|---|
| Bridge guide (explanations) | [`../PYTHON_NETWORKING_GUIDE.md`](../PYTHON_NETWORKING_GUIDE.md) | The cheatsheet assumes understanding, not first exposure |

### Lecture, Seminar, Project and Quiz Mapping

| Cheatsheet area | Lecture | Seminar | Project | Quiz |
|---|---|---|---|---|
| Socket API calls | [`../../../03_LECTURES/C03/c3-intro-network-programming.md`](../../../03_LECTURES/C03/c3-intro-network-programming.md) | [`../../../04_SEMINARS/S02/`](../../../04_SEMINARS/S02/) | [`../../../02_PROJECTS/01_network_applications/`](../../../02_PROJECTS/01_network_applications/) | [`../../c)studentsQUIZes(multichoice_only)/COMPnet_W02_Questions.md`](../../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W02_Questions.md) |
| `bytes` vs `str`, encoding and decoding | — (implementation-level, language specific) | [`../../../04_SEMINARS/S04/`](../../../04_SEMINARS/S04/) | [`../../../02_PROJECTS/01_network_applications/S06_tcp_pub_sub_broker_topics_and_deterministic_routing.md`](../../../02_PROJECTS/01_network_applications/S06_tcp_pub_sub_broker_topics_and_deterministic_routing.md) | [`../../c)studentsQUIZes(multichoice_only)/COMPnet_W04_Questions.md`](../../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W04_Questions.md) |
| `struct` packing and message framing | — | [`../../../04_SEMINARS/S04/`](../../../04_SEMINARS/S04/) | [`../../../02_PROJECTS/01_network_applications/S06_tcp_pub_sub_broker_topics_and_deterministic_routing.md`](../../../02_PROJECTS/01_network_applications/S06_tcp_pub_sub_broker_topics_and_deterministic_routing.md) | [`../../c)studentsQUIZes(multichoice_only)/COMPnet_W04_Questions.md`](../../c%29studentsQUIZes%28multichoice_only%29/COMPnet_W04_Questions.md) |

### Downstream Dependencies

No CI step depends on this folder. It is linked from other bridge-pack READMEs.

### Suggested Learning Sequence

Read the relevant section in `../PYTHON_NETWORKING_GUIDE.md` → keep `PYTHON_QUICK.md` open during `../../../04_SEMINARS/S02/` onward

## Selective Clone

Method A — Git sparse-checkout (requires Git ≥ 2.25)

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/cheatsheets"
```

Method B — Direct download (no Git required)

```text
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/cheatsheets
```

## Version and Provenance

| Item | Value |
|---|---|
| Scope | Optional student aid within the Python bridge pack |
| Primary source | `../PYTHON_NETWORKING_GUIDE.md` |
