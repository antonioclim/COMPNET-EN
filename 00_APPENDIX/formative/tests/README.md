# Export Function Tests

Unit tests for the quiz runner's export capabilities (JSON, Moodle GIFT, QTI). These validate that `run_quiz.py --export <format>` produces structurally correct output and that round-tripping through export/import preserves question content.

| File | Lines | Purpose |
|---|---|---|
| [`__init__.py`](__init__.py) | — | Package marker |
| [`test_quiz_exports.py`](test_quiz_exports.py) | 295 | Export format validation and round-trip checks |

## Usage

```bash
# from 00_APPENDIX/
make test-exports

# direct invocation
python3 formative/tests/test_quiz_exports.py
```

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Quiz runner | [`../run_quiz.py`](../run_quiz.py) | Code under test |
| Quiz source | [`../quiz.yaml`](../quiz.yaml) | Input data for export tests |
| Makefile targets | [`../../Makefile`](../../Makefile) | `make test-exports` and `make ci` invoke this file |

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_APPENDIX/formative/tests
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/formative/tests
```
