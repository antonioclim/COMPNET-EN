# Continuous Integration Setup Guide

> **Purpose:** Guide for setting up and using CI/CD for Computer Networks projects  
> **Applies to:** All projects P01-P20  
> **Last Updated:** January 2026

---

## Overview

This guide explains how to configure GitHub Actions for automated testing, linting and Docker builds in your Computer Networks project.

---

## Quick Start

### 1. Enable GitHub Actions

GitHub Actions is enabled by default for all repositories. The workflow file at `.github/workflows/ci.yml` will automatically run when you push code.

### 2. View CI Status

After pushing code:
1. Go to your repository on GitHub
2. Click the **Actions** tab
3. View the latest workflow run

### 3. Add Status Badge to README

Add this badge to your `README.md`:

```markdown
![CI Status](https://github.com/[username]/[repo]/actions/workflows/ci.yml/badge.svg)
```

---

## CI Pipeline Stages

The CI pipeline runs these checks in sequence:

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Lint   │───►│  Test   │───►│ Docker  │───►│ Summary │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │
     ▼              ▼              ▼
  Ruff           Pytest       Build &
  Mypy           Coverage     Test Images
```

### Stage Details

| Stage | Tools | What It Checks | Required to Pass |
|-------|-------|----------------|------------------|
| **Lint** | Ruff, Mypy | Code style, type hints | Yes |
| **Test** | Pytest | Unit tests, smoke tests | Yes |
| **Syntax** | py_compile | Python syntax validity | Yes |
| **Security** | Bandit, Safety | Security issues, vulnerabilities | No (advisory) |
| **Quiz** | Custom | Formative quiz file validity | No |
| **Docker** | Docker Compose | Container builds | Only on main branch |

---

## Local Development Setup

### Install Development Tools

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install project dependencies
pip install -r requirements.txt

# Install development tools
pip install ruff mypy pytest pytest-cov bandit safety pre-commit

# Set up pre-commit hooks
pre-commit install
```

### Run Checks Locally

```bash
# Run linting
make lint
# or: ruff check src/ tests/

# Run type checking
make typecheck
# or: mypy src/

# Run tests
make test
# or: pytest tests/ -v

# Run all checks
make check-all
```

---

## Linting Configuration

### Ruff Configuration

The project uses **Ruff** for linting and formatting. Configuration is in `ruff.toml`:

```toml
# Key settings
line-length = 100
target-version = "py310"

[lint]
select = ["E", "F", "W", "I", "N", "D", "UP", "B", "C4", "SIM"]
ignore = ["E501", "D100", "D104"]

[lint.per-file-ignores]
"tests/*" = ["D103", "S101"]
```

### Common Linting Errors

| Code | Meaning | Fix |
|------|---------|-----|
| E501 | Line too long | Split into multiple lines |
| F401 | Unused import | Remove the import |
| F841 | Unused variable | Remove or use the variable |
| W291 | Trailing whitespace | Remove trailing spaces |
| I001 | Import order | Run `ruff check --fix` |

### Auto-Fix Issues

```bash
# Auto-fix all fixable issues
ruff check src/ tests/ --fix

# Format code
ruff format src/ tests/
```

---

## Type Checking with Mypy

### Configuration

Type checking configuration is in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_ignores = true
ignore_missing_imports = true
```

### Common Type Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| Missing return type | Function needs `-> Type` | Add return type hint |
| Incompatible types | Type mismatch | Check variable types |
| Missing type annotation | Parameter needs type | Add `param: Type` |

### Example Fixes

```python
# Before (missing types)
def process_packet(data):
    return data.decode()

# After (with types)
def process_packet(data: bytes) -> str:
    return data.decode()
```

---

## Test Configuration

### Pytest Settings

Configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "integration: marks tests as integration tests",
    "slow: marks tests as slow",
]
```

### Test Structure

```
tests/
├── __init__.py
├── test_smoke.py       # Quick sanity checks (MUST PASS)
├── test_unit.py        # Unit tests for individual functions
├── test_integration.py # Integration tests (requires Docker)
└── conftest.py         # Shared fixtures
```

### Writing Tests

```python
import pytest

def test_validate_port_valid():
    """Test that valid ports are accepted."""
    assert validate_port(8080) is True
    assert validate_port(1) is True
    assert validate_port(65535) is True

def test_validate_port_invalid():
    """Test that invalid ports are rejected."""
    assert validate_port(0) is False
    assert validate_port(-1) is False
    assert validate_port(70000) is False

@pytest.mark.integration
def test_docker_connection():
    """Test Docker connectivity (requires Docker)."""
    # This test only runs when explicitly requested
    pass
```

---

## Pre-commit Hooks

### Configuration

The `.pre-commit-config.yaml` file configures automatic checks before each commit:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
```

### Usage

```bash
# Install hooks (one time)
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Skip hooks for a commit (not recommended)
git commit --no-verify -m "message"
```

---

## Troubleshooting CI Failures

### Lint Failures

**Problem:** Ruff reports errors

**Solution:**
```bash
# View errors
ruff check src/ tests/

# Auto-fix
ruff check src/ tests/ --fix

# Check specific file
ruff check src/main.py
```

### Test Failures

**Problem:** Pytest tests fail

**Solution:**
```bash
# Run with verbose output
pytest tests/ -v --tb=long

# Run specific test
pytest tests/test_smoke.py::TestEnvironment::test_python_version -v

# Debug with print statements
pytest tests/ -v -s
```

### Docker Failures

**Problem:** Docker build fails in CI

**Solution:**
1. Test locally first: `docker-compose build`
2. Check Dockerfile syntax
3. Verify base images are available
4. Check for secrets in build context

---

## GitHub Actions Secrets

For private configurations (API keys, credentials), use GitHub Secrets:

1. Go to repository **Settings**
2. Click **Secrets and variables** → **Actions**
3. Add secret with **New repository secret**

Access in workflow:
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

**Never commit secrets to the repository!**

---

## Customising the Pipeline

### Skip CI for Documentation Changes

The workflow already ignores:
- `**.md` files
- `docs/**` directory
- `.gitignore`

### Add Custom Tests

Add new test files to `tests/` directory. They will be automatically discovered.

### Disable Jobs

Comment out jobs in `.github/workflows/ci.yml`:

```yaml
# docker:
#   name: Docker Build
#   ...
```

---

## Best Practices

1. **Run checks locally** before pushing
2. **Fix lint errors immediately** — do not let them accumulate
3. **Write tests** for new functionality
4. **Keep CI green** — fix failures promptly
5. **Review security warnings** even if advisory-only

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `make lint` | Run linter |
| `make test` | Run all tests |
| `make smoke` | Run smoke tests only |
| `make check-all` | Run all checks |
| `pre-commit run --all-files` | Run pre-commit hooks |

---

*CI Setup Guide v1.0 — Computer Networks, ASE Bucharest*
