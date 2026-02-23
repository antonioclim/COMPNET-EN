# Makefile — Week 0 Orchestration
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
# Version: 1.6.0 | Date: 2026-01-25
#
# Usage:
#   make help      - Show available targets
#   make quiz      - Run formative quiz
#   make test      - Run smoke tests
#   make lint      - Run code linter
#   make validate  - Validate all files
#   make export    - Export quiz to all formats
#   make clean     - Clean generated files

.PHONY: help quiz test lint validate export clean verify all

# Configuration
PYTHON := python3
QUIZ_DIR := formative
EXAMPLES_DIR := PYTHON_self_study_guide/examples
TESTS_DIR := $(EXAMPLES_DIR)/tests

# Colours for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
CYAN := \033[0;36m
NC := \033[0m

# Default target
.DEFAULT_GOAL := help

#═══════════════════════════════════════════════════════════════════════════════
# HELP
#═══════════════════════════════════════════════════════════════════════════════

help:
	@echo ""
	@echo "$(CYAN)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(CYAN)  Week 0 — Computer Networks Lab Kit$(NC)"
	@echo "$(CYAN)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@echo ""
	@echo "  $(YELLOW)quiz$(NC)       - Run formative quiz (interactive)"
	@echo "  $(YELLOW)quiz-review$(NC) - Show quiz answers (review mode)"
	@echo "  $(YELLOW)quiz-random$(NC) - Run quiz with randomised questions"
	@echo ""
	@echo "  $(YELLOW)test$(NC)       - Run smoke tests for Python examples"
	@echo "  $(YELLOW)test-exports$(NC) - Run export function unit tests"
	@echo "  $(YELLOW)lint$(NC)       - Run code linter (ruff or flake8)"
	@echo "  $(YELLOW)validate$(NC)   - Validate all YAML, JSON and Python files"
	@echo ""
	@echo "  $(YELLOW)export$(NC)     - Export quiz to all formats (JSON, Moodle, QTI)"
	@echo "  $(YELLOW)export-json$(NC) - Export quiz to JSON only"
	@echo "  $(YELLOW)export-moodle$(NC) - Export quiz to Moodle GIFT format"
	@echo ""
	@echo "  $(YELLOW)verify$(NC)     - Run environment verification script"
	@echo "  $(YELLOW)clean$(NC)      - Remove generated files and caches"
	@echo ""
	@echo "  $(YELLOW)all$(NC)        - Run lint, test and validate"
	@echo ""

#═══════════════════════════════════════════════════════════════════════════════
# QUIZ TARGETS
#═══════════════════════════════════════════════════════════════════════════════

quiz:
	@echo "$(CYAN)Running formative quiz...$(NC)"
	@$(PYTHON) $(QUIZ_DIR)/run_quiz.py

quiz-review:
	@echo "$(CYAN)Quiz review mode (answers shown)...$(NC)"
	@$(PYTHON) $(QUIZ_DIR)/run_quiz.py --show-answers

quiz-random:
	@echo "$(CYAN)Running randomised quiz...$(NC)"
	@$(PYTHON) $(QUIZ_DIR)/run_quiz.py --random

quiz-bloom-%:
	@echo "$(CYAN)Running quiz filtered by Bloom level: $*$(NC)"
	@$(PYTHON) $(QUIZ_DIR)/run_quiz.py --bloom $*

quiz-validate:
	@echo "$(CYAN)Validating quiz structure...$(NC)"
	@$(PYTHON) $(QUIZ_DIR)/run_quiz.py --validate

#═══════════════════════════════════════════════════════════════════════════════
# TEST TARGETS
#═══════════════════════════════════════════════════════════════════════════════

test:
	@echo "$(CYAN)Running smoke tests...$(NC)"
	@$(PYTHON) $(TESTS_DIR)/test_smoke.py
	@echo "$(GREEN)✓ Smoke tests passed$(NC)"

test-verbose:
	@echo "$(CYAN)Running smoke tests (verbose)...$(NC)"
	@$(PYTHON) -m pytest $(TESTS_DIR)/test_smoke.py -v 2>/dev/null || $(PYTHON) $(TESTS_DIR)/test_smoke.py

test-exports:
	@echo "$(CYAN)Running export function tests...$(NC)"
	@if [ -f "$(QUIZ_DIR)/tests/test_quiz_exports.py" ]; then \
		$(PYTHON) $(QUIZ_DIR)/tests/test_quiz_exports.py; \
		echo "$(GREEN)✓ Export tests passed$(NC)"; \
	else \
		echo "$(YELLOW)⚠ Export tests not found$(NC)"; \
	fi

test-all: test test-exports
	@echo "$(GREEN)✓ All tests passed$(NC)"

#═══════════════════════════════════════════════════════════════════════════════
# LINT TARGETS
#═══════════════════════════════════════════════════════════════════════════════

lint:
	@echo "$(CYAN)Running linter...$(NC)"
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check $(EXAMPLES_DIR)/*.py $(QUIZ_DIR)/*.py --ignore E501; \
	elif command -v flake8 >/dev/null 2>&1; then \
		flake8 $(EXAMPLES_DIR)/*.py $(QUIZ_DIR)/*.py --max-line-length=120; \
	else \
		echo "$(YELLOW)⚠ No linter found. Install with: pip install ruff$(NC)"; \
		$(PYTHON) -m py_compile $(EXAMPLES_DIR)/*.py $(QUIZ_DIR)/*.py; \
		echo "$(GREEN)✓ Syntax check passed$(NC)"; \
	fi

lint-fix:
	@echo "$(CYAN)Running linter with auto-fix...$(NC)"
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check $(EXAMPLES_DIR)/*.py $(QUIZ_DIR)/*.py --fix --ignore E501; \
	else \
		echo "$(YELLOW)⚠ ruff not found. Install with: pip install ruff$(NC)"; \
	fi

#═══════════════════════════════════════════════════════════════════════════════
# VALIDATE TARGETS
#═══════════════════════════════════════════════════════════════════════════════

validate: validate-python validate-yaml validate-json
	@echo "$(GREEN)✓ All validations passed$(NC)"

validate-python:
	@echo "$(CYAN)Validating Python syntax...$(NC)"
	@find . -name "*.py" -type f -exec $(PYTHON) -m py_compile {} \;
	@echo "$(GREEN)✓ Python syntax valid$(NC)"

validate-yaml:
	@echo "$(CYAN)Validating YAML files...$(NC)"
	@$(PYTHON) -c "import yaml; yaml.safe_load(open('$(QUIZ_DIR)/quiz.yaml'))"
	@echo "$(GREEN)✓ YAML valid$(NC)"

validate-json:
	@echo "$(CYAN)Validating JSON files...$(NC)"
	@if [ -f "$(QUIZ_DIR)/quiz.json" ]; then \
		$(PYTHON) -c "import json; json.load(open('$(QUIZ_DIR)/quiz.json'))"; \
		echo "$(GREEN)✓ JSON valid$(NC)"; \
	else \
		echo "$(YELLOW)⚠ quiz.json not found (optional)$(NC)"; \
	fi

#═══════════════════════════════════════════════════════════════════════════════
# EXPORT TARGETS
#═══════════════════════════════════════════════════════════════════════════════

export: export-json export-moodle
	@echo "$(GREEN)✓ All exports completed$(NC)"

export-json:
	@echo "$(CYAN)Exporting quiz to JSON...$(NC)"
	@$(PYTHON) $(QUIZ_DIR)/run_quiz.py --export json
	@echo "$(GREEN)✓ JSON export completed$(NC)"

export-moodle:
	@echo "$(CYAN)Exporting quiz to Moodle GIFT...$(NC)"
	@$(PYTHON) $(QUIZ_DIR)/run_quiz.py --export moodle
	@echo "$(GREEN)✓ Moodle export completed$(NC)"

export-qti:
	@echo "$(CYAN)Exporting quiz to QTI...$(NC)"
	@$(PYTHON) $(QUIZ_DIR)/run_quiz.py --export qti
	@echo "$(GREEN)✓ QTI export completed$(NC)"

#═══════════════════════════════════════════════════════════════════════════════
# VERIFY ENVIRONMENT
#═══════════════════════════════════════════════════════════════════════════════

verify:
	@echo "$(CYAN)Running environment verification...$(NC)"
	@if [ -f "../00_TOOLS/Prerequisites/verify_lab_environment.sh" ]; then \
		bash ../00_TOOLS/Prerequisites/verify_lab_environment.sh; \
	else \
		echo "$(RED)✗ verify_lab_environment.sh not found$(NC)"; \
		exit 1; \
	fi

#═══════════════════════════════════════════════════════════════════════════════
# CLEAN
#═══════════════════════════════════════════════════════════════════════════════

clean:
	@echo "$(CYAN)Cleaning generated files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*_export.json" -delete 2>/dev/null || true
	@find . -type f -name "*_moodle.gift" -delete 2>/dev/null || true
	@find . -type f -name "*_qti.xml" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Clean completed$(NC)"

#═══════════════════════════════════════════════════════════════════════════════
# COMBINED TARGETS
#═══════════════════════════════════════════════════════════════════════════════

all: lint test validate
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  ✓ All checks passed!$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"

ci: lint validate test test-exports
	@echo "$(GREEN)✓ CI pipeline completed$(NC)"

# Alias for common typos
tests: test
quizz: quiz
linter: lint
