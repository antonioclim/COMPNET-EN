# Unit Tests for Python Examples

Automated verification tests for the annotated code examples in [`../`](../). These tests confirm that the example scripts execute without error and produce expected output, serving both as regression checks and as executable documentation.

| File | Tests | Target |
|---|---|---|
| [`test_smoke.py`](test_smoke.py) | Import and basic execution checks for all example scripts | All `../0*.py` |
| [`test_bytes_vs_str.py`](test_bytes_vs_str.py) | Encoding round-trip and type-assertion tests | [`../02_bytes_vs_str.py`](../02_bytes_vs_str.py) |
| [`test_struct_parsing.py`](test_struct_parsing.py) | Pack/unpack correctness and byte-order verification | [`../03_struct_parsing.py`](../03_struct_parsing.py) |

## Usage

```bash
# from the guide root
make test           # runs test_smoke.py
make test-all       # runs all test files

# direct invocation
python3 -m pytest examples/tests/ -v
```

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Example scripts | [`../`](../) | Code under test |
| CI pipeline targets | [`../../Makefile`](../../Makefile) | `make test` and `make test-all` targets invoke these tests |
| Linter config | [`../../../ruff.toml`](../../../ruff.toml) | `E501` and `F401` relaxed for test files |

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/examples/tests"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/examples/tests
```
