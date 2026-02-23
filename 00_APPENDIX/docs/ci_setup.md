# 🔄 CI/CD Setup Guide — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This guide explains how to set up and use the Continuous Integration pipeline for the Week 0 kit.

---

## Overview

The CI pipeline automatically validates:

| Check | Description | Tool |
|-------|-------------|------|
| **Syntax** | Python files compile without errors | `py_compile` |
| **Linting** | Code style and potential bugs | `ruff` |
| **YAML** | Quiz and config files are valid | `pyyaml` |
| **JSON** | LMS export files are valid | `json` |
| **Tests** | Smoke tests pass | `pytest` |
| **Docs** | Required documentation exists | `bash` |

---

## Quick Start

### Local Validation

Run all checks locally before pushing:

```bash
# Using Make (recommended)
make all

# Or run individually
make lint      # Code linting
make test      # Smoke tests
make validate  # YAML/JSON validation
```

### GitHub Actions

The CI pipeline runs automatically on:
- Push to `main`, `develop`, or `master` branches
- Pull requests to these branches
- Manual trigger (workflow_dispatch)

---

## Pipeline Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        CI PIPELINE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │   Lint   │───▶│   Test   │    │   Quiz   │    │   Docs   │  │
│  │          │    │          │    │Validation│    │  Check   │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │               │               │               │         │
│       └───────────────┴───────────────┴───────────────┘         │
│                              │                                   │
│                       ┌──────────┐                              │
│                       │ Summary  │                              │
│                       └──────────┘                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Configuration Files

### Linting Configuration

Create `ruff.toml` in the repository root:

```toml
# ruff.toml — Linting configuration
# See: https://docs.astral.sh/ruff/configuration/

[lint]
# Enable rules
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
]

# Ignore specific rules
ignore = [
    "E501",  # Line too long (handled by formatter)
    "E402",  # Module level import not at top of file
    "B008",  # Do not perform function calls in argument defaults
]

# Allow fix for all enabled rules
fixable = ["ALL"]
unfixable = []

[lint.per-file-ignores]
# Tests can have more relaxed rules
"**/tests/*.py" = ["B", "C4"]

[format]
# Use double quotes for strings
quote-style = "double"

# Indent with spaces
indent-style = "space"

# Target Python 3.11
target-version = "py311"
```

### Alternative: flake8 Configuration

Create `.flake8` in the repository root:

```ini
[flake8]
max-line-length = 120
extend-ignore = E501,E402
exclude =
    .git,
    __pycache__,
    .venv,
    build,
    dist
per-file-ignores =
    **/tests/*.py: B,C4
```

---

## Setting Up GitHub Actions

### Step 1: Enable Actions

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Actions** → **General**
3. Select "Allow all actions and reusable workflows"
4. Save changes

### Step 2: Add Workflow File

The workflow file is already at `.github/workflows/ci.yml`. Commit and push it:

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow"
git push
```

### Step 3: View Results

1. Go to the **Actions** tab in your repository
2. Click on the latest workflow run
3. View detailed logs for each job

---

## Adding Status Badge

Add this badge to your README.md:

```markdown
![CI Status](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)
```

---

## Troubleshooting CI Failures

### Lint Failures

```bash
# Run linter locally to see issues
ruff check . --output-format=full

# Auto-fix issues
ruff check . --fix
```

### Test Failures

```bash
# Run tests with verbose output
python -m pytest PYTHON_self_study_guide/examples/tests/ -v

# Or use the built-in runner
python PYTHON_self_study_guide/examples/tests/test_smoke.py
```

### YAML Validation Failures

```bash
# Check specific file
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"

# See detailed error
python -c "
import yaml
try:
    yaml.safe_load(open('formative/quiz.yaml'))
    print('Valid')
except yaml.YAMLError as e:
    print(f'Error: {e}')
"
```

---

## Local Development Setup

### Install Development Dependencies

```bash
pip install ruff pyyaml pytest
```

### Pre-commit Hook (Optional)

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Install and activate:

```bash
pip install pre-commit
pre-commit install
```

---

## CI Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHON_VERSION` | Python version for tests | `3.11` |

---

## Extending the Pipeline

### Adding New Checks

Edit `.github/workflows/ci.yml` and add a new job:

```yaml
  new-check:
    name: My New Check
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - name: Run check
        run: |
          echo "Running my check..."
          # Your commands here
```

### Adding to Makefile

```makefile
my-check:
    @echo "Running my check..."
    # Your commands here
```

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)

---

*CI/CD Setup Guide — Week 0 | Computer Networks | ASE-CSIE*
*Version: 1.5.0 | Date: 2026-01-24*
