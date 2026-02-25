# Annotated Python Examples

Runnable, heavily commented Python scripts illustrating the networking concepts that students encounter during the 14-week laboratory course. Each script is self-contained and designed for study, not production use; comments explain not just *what* the code does but *why* it differs from equivalent C, Java or JavaScript patterns.

| File | Topic | Lines | Key concepts |
|---|---|---|---|
| [`01_socket_tcp.py`](01_socket_tcp.py) | TCP client and server | 307 | `socket()`, `bind()`, `listen()`, `accept()`, `connect()` |
| [`02_bytes_vs_str.py`](02_bytes_vs_str.py) | Byte/string conversion | 472 | `encode()`, `decode()`, `bytes` vs `str`, UTF-8 |
| [`03_struct_parsing.py`](03_struct_parsing.py) | Binary protocol parsing | 428 | `struct.pack()`, `struct.unpack()`, network byte order |
| [`04_error_handling.py`](04_error_handling.py) | Network error scenarios | 515 | `try/except`, timeout, connection refused, `OSError` |
| [`tests/`](tests/) | Automated verification | 3 files | pytest smoke, bytes and struct correctness |

## Usage

```bash
# run an individual example
python3 examples/01_socket_tcp.py

# run all smoke tests
make test

# run full test suite
python3 -m pytest examples/tests/ -v
```

Each script includes inline instructions for running its demonstrations (some require two terminals for client/server pairs).

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Networking guide — Step 1 (sockets) | [`../PYTHON_NETWORKING_GUIDE.md`](../PYTHON_NETWORKING_GUIDE.md) | Theory behind `01_socket_tcp.py` |
| Networking guide — Step 2 (data types) | [`../PYTHON_NETWORKING_GUIDE.md`](../PYTHON_NETWORKING_GUIDE.md) | Theory behind `02_bytes_vs_str.py` |
| Rosetta Stone | [`../comparisons/ROSETTA_STONE.md`](../comparisons/ROSETTA_STONE.md) | Same algorithms in C, JS, Java, Kotlin |
| Cheatsheet | [`../cheatsheets/PYTHON_QUICK.md`](../cheatsheets/PYTHON_QUICK.md) | Quick-reference companion for these scripts |
| Parsons problems | [`../formative/parsons/`](../formative/parsons/) | Reordering exercises derived from these examples |
| Seminar S01 | [`../../../04_SEMINARS/S01/`](../../../04_SEMINARS/S01/) | First lab session where socket code is exercised |
| Seminar S04 | [`../../../04_SEMINARS/S04/`](../../../04_SEMINARS/S04/) | Binary protocol framing lab |

**Suggested sequence:** read the guide section → study the example → attempt the Parsons problem → take the quiz.

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/examples"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/examples
```
