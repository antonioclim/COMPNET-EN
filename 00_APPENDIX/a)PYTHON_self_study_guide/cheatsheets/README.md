# Python Networking Cheatsheet

Single-file quick reference for the Python constructs most frequently needed during laboratory sessions: socket API calls, `struct` format strings, `argparse` patterns and common encoding idioms.

| File | Lines | Content |
|---|---|---|
| [`PYTHON_QUICK.md`](PYTHON_QUICK.md) | 178 | Socket API, struct pack/unpack, argparse, bytes/str conversion |

## When to Use

Keep this open alongside the lab terminal. It is designed for lookup speed, not learning — students who need explanations should consult the [full guide](../PYTHON_NETWORKING_GUIDE.md) or the [Rosetta Stone](../comparisons/ROSETTA_STONE.md) first.

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Full networking guide | [`../PYTHON_NETWORKING_GUIDE.md`](../PYTHON_NETWORKING_GUIDE.md) | Expanded explanations of every cheatsheet entry |
| Rosetta Stone | [`../comparisons/ROSETTA_STONE.md`](../comparisons/ROSETTA_STONE.md) | Same patterns shown in C, JS, Java and Kotlin |
| Slide deck 04 | [`../PRESENTATIONS_EN/04_socket_programming.html`](../PRESENTATIONS_EN/04_socket_programming.html) | Visual walkthrough of socket API |

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/cheatsheets"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/cheatsheets
```
