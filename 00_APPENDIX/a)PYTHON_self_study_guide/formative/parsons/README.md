# Parsons Problem Definitions

YAML source files for Parsons problems — exercises where students reorder shuffled code lines into a correct program. Each file targets a specific networking concept and is consumed by [`../parsons_runner.py`](../parsons_runner.py).

| File | Topic | Format |
|---|---|---|
| [`parsons_bytes.yaml`](parsons_bytes.yaml) | Byte/string conversion and encoding | YAML (Parsons schema) |
| [`parsons_socket.yaml`](parsons_socket.yaml) | TCP socket creation and communication | YAML (Parsons schema) |

## Usage

From the guide root (`a)PYTHON_self_study_guide/`):

```bash
make parsons           # all problems
make parsons-socket    # socket problems only
make parsons-bytes     # bytes problems only
```

Or invoke the runner directly:

```bash
python3 formative/parsons_runner.py formative/parsons/parsons_socket.yaml
```

## Pedagogical Context

Parsons problems reduce cognitive load compared with writing code from scratch: students focus on sequencing and logic rather than syntax recall. This approach is grounded in worked-example research (Sweller, 1988) and is especially effective for students transitioning from other languages who recognise patterns but lack Python muscle memory.

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Parsons runner script | [`../parsons_runner.py`](../parsons_runner.py) | Executes these YAML definitions |
| Parsons documentation | [`../../../docs/parsons_problems.md`](../../../docs/parsons_problems.md) | Explains the pedagogy and format |
| Socket examples | [`../../examples/01_socket_tcp.py`](../../examples/01_socket_tcp.py) | Reference implementation for socket ordering |
| Bytes examples | [`../../examples/02_bytes_vs_str.py`](../../examples/02_bytes_vs_str.py) | Reference implementation for encoding ordering |

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/formative/parsons"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/formative/parsons
```
