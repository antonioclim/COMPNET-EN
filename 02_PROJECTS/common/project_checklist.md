# Project Completeness Checklist

Use this checklist before each stage submission.

---

## Stage 1 — Design

### Documentation
- [ ] `docs/specificatii.md` created (min 500 words)
- [ ] Architecture diagrams in `docs/diagrame/`
- [ ] `README.md` with project overview
- [ ] Implementation timeline documented

### Repository
- [ ] GitHub repository created
- [ ] `.gitignore` configured
- [ ] Initial commit pushed

### Submission
- [ ] `MANIFEST.txt` with valid signature
- [ ] Archive named correctly: `SURNAME_Firstname_GGGG_PXX_E1.zip`

---

## Stage 2 — Prototype

### Code
- [ ] `src/main.py` entry point exists
- [ ] Core functionality (min 50%) implemented
- [ ] Type hints on all public functions
- [ ] Docstrings on all public functions
- [ ] Subgoal labels in code sections

### Environment
- [ ] `requirements.txt` complete
- [ ] `docker/docker-compose.yml` (if applicable)
- [ ] Application starts without errors

### Testing
- [ ] `make smoke` passes
- [ ] Manual testing documented

### Documentation
- [ ] `docs/raport_progres.md` updated
- [ ] Progress committed to GitHub

### Submission
- [ ] `MANIFEST.txt` updated
- [ ] Archive named: `SURNAME_Firstname_GGGG_PXX_E2.zip`

---

## Stage 3 — Final Version

### Code
- [ ] All requirements implemented
- [ ] No TODO markers remaining
- [ ] Error handling complete
- [ ] Logging implemented (not print)

### Quality
- [ ] `make lint` passes
- [ ] No bare `except:` clauses
- [ ] No hardcoded configuration

### Testing
- [ ] `tests/test_smoke.py` passes
- [ ] Unit tests for core functions
- [ ] Integration tests (if applicable)
- [ ] >80% code coverage (recommended)

### Documentation
- [ ] `docs/documentatie_finala.md` complete
- [ ] `CHANGELOG.md` updated
- [ ] API documentation (if applicable)
- [ ] Performance analysis included

### Repository
- [ ] All code committed
- [ ] Git tag `v1.0-final` created
- [ ] Pushed to GitHub

### Submission
- [ ] `MANIFEST.txt` updated
- [ ] Archive named: `SURNAME_Firstname_GGGG_PXX_E3.zip`

---

## Stage 4 — Presentation

### Demo Preparation
- [ ] Application runs on clean machine
- [ ] Demo script prepared
- [ ] Backup plan if demo fails

### Presentation
- [ ] Slides ready (if required)
- [ ] Each team member knows all code
- [ ] Time limit practiced (10-15 min)

### Questions
- [ ] Reviewed theoretical concepts
- [ ] Prepared for "what if" questions
- [ ] Know limitations of implementation

---

## Common Mistakes to Avoid

### Code
- Using `print()` instead of `logging`
- Missing type hints
- Bare `except:` clauses
- Hardcoded IP addresses/ports
- Committed `__pycache__` or `.pyc` files

### Documentation
- Missing diagrams
- Incomplete README
- No installation instructions
- Missing changelog

### Submission
- Wrong archive naming
- Missing MANIFEST.txt
- Not pushing to GitHub
- Late submission

---

*Use this checklist before EVERY submission!*
