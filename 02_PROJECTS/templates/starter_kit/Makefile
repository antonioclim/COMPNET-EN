# ═══════════════════════════════════════════════════════════════════════════════
# MAKEFILE — Computer Networks Project Orchestration
# ═══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   make help          - Show available targets
#   make setup         - Install dependencies
#   make quiz          - Run formative quiz
#   make test          - Run all tests
#   make lint          - Run code linting
#   make docker-up     - Start Docker environment
#   make clean         - Clean artefacts
#
# ═══════════════════════════════════════════════════════════════════════════════

# Configuration
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker-compose
PROJECT_ROOT := $(shell pwd)

# Directories
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs
FORMATIVE_DIR := formative
ARTIFACTS_DIR := artifacts
DOCKER_DIR := docker

# Files
REQUIREMENTS := requirements.txt
QUIZ_TEMPLATE := $(FORMATIVE_DIR)/quiz_template.yaml

# Colours for terminal output
COLOUR_RESET := \033[0m
COLOUR_GREEN := \033[32m
COLOUR_YELLOW := \033[33m
COLOUR_BLUE := \033[34m
COLOUR_CYAN := \033[36m

# ═══════════════════════════════════════════════════════════════════════════════
# DEFAULT TARGET
# ═══════════════════════════════════════════════════════════════════════════════

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "$(COLOUR_CYAN)╔═══════════════════════════════════════════════════════════════╗$(COLOUR_RESET)"
	@echo "$(COLOUR_CYAN)║  Computer Networks Project — Build Targets                    ║$(COLOUR_RESET)"
	@echo "$(COLOUR_CYAN)╚═══════════════════════════════════════════════════════════════╝$(COLOUR_RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOUR_GREEN)%-18s$(COLOUR_RESET) %s\n", $$1, $$2}'
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: setup
setup: ## Install Python dependencies
	@echo "$(COLOUR_BLUE)Installing dependencies...$(COLOUR_RESET)"
	$(PIP) install -r $(REQUIREMENTS)
	@echo "$(COLOUR_GREEN)✓ Dependencies installed$(COLOUR_RESET)"

.PHONY: setup-dev
setup-dev: setup ## Install development dependencies (including linters)
	@echo "$(COLOUR_BLUE)Installing development tools...$(COLOUR_RESET)"
	$(PIP) install ruff mypy pytest pytest-cov pre-commit
	pre-commit install
	@echo "$(COLOUR_GREEN)✓ Development tools installed$(COLOUR_RESET)"

.PHONY: verify
verify: ## Verify environment is correctly set up
	@echo "$(COLOUR_BLUE)Verifying environment...$(COLOUR_RESET)"
	@echo "Python version:"
	@$(PYTHON) --version
	@echo ""
	@echo "Checking required tools:"
	@command -v docker >/dev/null 2>&1 && echo "  ✓ Docker" || echo "  ✗ Docker (not found)"
	@command -v docker-compose >/dev/null 2>&1 && echo "  ✓ Docker Compose" || echo "  ✗ Docker Compose (not found)"
	@command -v git >/dev/null 2>&1 && echo "  ✓ Git" || echo "  ✗ Git (not found)"
	@$(PYTHON) -c "import yaml" 2>/dev/null && echo "  ✓ PyYAML" || echo "  ✗ PyYAML (pip install pyyaml)"
	@$(PYTHON) -c "import pytest" 2>/dev/null && echo "  ✓ Pytest" || echo "  ✗ Pytest (pip install pytest)"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# FORMATIVE ASSESSMENT TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: quiz
quiz: ## Run formative self-assessment quiz
	@echo "$(COLOUR_CYAN)Starting formative quiz...$(COLOUR_RESET)"
	@if [ -f "$(FORMATIVE_DIR)/run_quiz.py" ]; then \
		$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py $(QUIZ_TEMPLATE); \
	else \
		echo "$(COLOUR_YELLOW)Quiz runner not found. Run from project root.$(COLOUR_RESET)"; \
	fi

.PHONY: quiz-random
quiz-random: ## Run quiz with randomised questions
	@$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py $(QUIZ_TEMPLATE) --random

.PHONY: quiz-practice
quiz-practice: ## Run quiz in practice mode (with hints)
	@$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py $(QUIZ_TEMPLATE) --practice

.PHONY: quiz-lo
quiz-lo: ## Run quiz filtered by LO (usage: make quiz-lo LO=LO2)
	@if [ -z "$(LO)" ]; then \
		echo "$(COLOUR_YELLOW)Usage: make quiz-lo LO=LO2$(COLOUR_RESET)"; \
	else \
		$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py $(QUIZ_TEMPLATE) --lo $(LO); \
	fi

.PHONY: quiz-list
quiz-list: ## List available quizzes
	@$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py --list

.PHONY: quiz-export
quiz-export: ## Export quizzes to LMS format (Moodle/Canvas/JSON)
	@echo "$(COLOUR_BLUE)Exporting quizzes to LMS formats...$(COLOUR_RESET)"
	@$(PYTHON) $(FORMATIVE_DIR)/export_lms.py --all --format moodle
	@$(PYTHON) $(FORMATIVE_DIR)/export_lms.py --all --format canvas
	@$(PYTHON) $(FORMATIVE_DIR)/export_lms.py --all --format json
	@echo "$(COLOUR_GREEN)✓ Exports saved to $(FORMATIVE_DIR)/exports/$(COLOUR_RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: test
test: ## Run all tests
	@echo "$(COLOUR_BLUE)Running tests...$(COLOUR_RESET)"
	$(PYTHON) -m pytest $(TEST_DIR)/ -v --tb=short

.PHONY: test-smoke
smoke: ## Run smoke tests only (quick sanity check)
	@echo "$(COLOUR_BLUE)Running smoke tests...$(COLOUR_RESET)"
	@if [ -f "$(TEST_DIR)/test_smoke.py" ]; then \
		$(PYTHON) -m pytest $(TEST_DIR)/test_smoke.py -v; \
	else \
		$(PYTHON) $(TEST_DIR)/smoke_test.py; \
	fi

.PHONY: test-unit
test-unit: ## Run unit tests only
	$(PYTHON) -m pytest $(TEST_DIR)/ -v -m "not integration"

.PHONY: test-integration
test-integration: ## Run integration tests only
	$(PYTHON) -m pytest $(TEST_DIR)/ -v -m "integration"

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	$(PYTHON) -m pytest $(TEST_DIR)/ --cov=$(SRC_DIR) --cov-report=html --cov-report=term
	@echo "$(COLOUR_GREEN)Coverage report: htmlcov/index.html$(COLOUR_RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# LINTING AND CODE QUALITY
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: lint
lint: ## Run code linting with ruff
	@echo "$(COLOUR_BLUE)Running linter...$(COLOUR_RESET)"
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check $(SRC_DIR)/ $(TEST_DIR)/ --fix; \
	else \
		echo "$(COLOUR_YELLOW)Ruff not installed. Run: pip install ruff$(COLOUR_RESET)"; \
	fi

.PHONY: lint-check
lint-check: ## Check linting without auto-fix
	@ruff check $(SRC_DIR)/ $(TEST_DIR)/

.PHONY: format
format: ## Format code with ruff
	@ruff format $(SRC_DIR)/ $(TEST_DIR)/

.PHONY: typecheck
typecheck: ## Run type checking with mypy
	@echo "$(COLOUR_BLUE)Running type checker...$(COLOUR_RESET)"
	@if command -v mypy >/dev/null 2>&1; then \
		mypy $(SRC_DIR)/ --ignore-missing-imports; \
	else \
		echo "$(COLOUR_YELLOW)Mypy not installed. Run: pip install mypy$(COLOUR_RESET)"; \
	fi

.PHONY: check-all
check-all: lint typecheck test ## Run all checks (lint, typecheck, test)
	@echo "$(COLOUR_GREEN)✓ All checks passed$(COLOUR_RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: docker-up
docker-up: ## Start Docker containers
	@echo "$(COLOUR_BLUE)Starting Docker environment...$(COLOUR_RESET)"
	@if [ -f "$(DOCKER_DIR)/docker-compose.yml" ]; then \
		$(DOCKER_COMPOSE) -f $(DOCKER_DIR)/docker-compose.yml up -d; \
		$(DOCKER_COMPOSE) -f $(DOCKER_DIR)/docker-compose.yml ps; \
	else \
		echo "$(COLOUR_YELLOW)No docker-compose.yml found in $(DOCKER_DIR)/$(COLOUR_RESET)"; \
	fi

.PHONY: docker-down
docker-down: ## Stop Docker containers
	@echo "$(COLOUR_BLUE)Stopping Docker environment...$(COLOUR_RESET)"
	$(DOCKER_COMPOSE) -f $(DOCKER_DIR)/docker-compose.yml down

.PHONY: docker-logs
docker-logs: ## Show Docker container logs
	$(DOCKER_COMPOSE) -f $(DOCKER_DIR)/docker-compose.yml logs -f

.PHONY: docker-build
docker-build: ## Build Docker images
	$(DOCKER_COMPOSE) -f $(DOCKER_DIR)/docker-compose.yml build

.PHONY: docker-clean
docker-clean: ## Remove Docker containers and volumes
	$(DOCKER_COMPOSE) -f $(DOCKER_DIR)/docker-compose.yml down -v --remove-orphans
	docker system prune -f

# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: docs
docs: ## Generate documentation
	@echo "$(COLOUR_BLUE)Documentation is in $(DOCS_DIR)/$(COLOUR_RESET)"
	@ls -la $(DOCS_DIR)/

.PHONY: serve-docs
serve-docs: ## Serve documentation locally
	@$(PYTHON) -m http.server 8000 --directory $(DOCS_DIR)

# ═══════════════════════════════════════════════════════════════════════════════
# CLEAN TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: clean
clean: ## Clean generated artefacts
	@echo "$(COLOUR_BLUE)Cleaning artefacts...$(COLOUR_RESET)"
	rm -rf $(ARTIFACTS_DIR)/*.pcap
	rm -rf $(ARTIFACTS_DIR)/*.log
	rm -rf $(FORMATIVE_DIR)/results/*.json
	rm -rf $(FORMATIVE_DIR)/exports/*.xml
	rm -rf $(FORMATIVE_DIR)/exports/*.json
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	@echo "$(COLOUR_GREEN)✓ Clean complete$(COLOUR_RESET)"

.PHONY: clean-all
clean-all: clean docker-clean ## Clean everything including Docker
	@echo "$(COLOUR_GREEN)✓ Full clean complete$(COLOUR_RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# SUBMISSION TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: pre-submit
pre-submit: lint-check test smoke ## Run pre-submission checks
	@echo ""
	@echo "$(COLOUR_GREEN)╔═══════════════════════════════════════════════════════════════╗$(COLOUR_RESET)"
	@echo "$(COLOUR_GREEN)║  ✓ Pre-submission checks passed!                             ║$(COLOUR_RESET)"
	@echo "$(COLOUR_GREEN)╚═══════════════════════════════════════════════════════════════╝$(COLOUR_RESET)"
	@echo ""

.PHONY: archive
archive: clean ## Create submission archive
	@echo "$(COLOUR_BLUE)Creating submission archive...$(COLOUR_RESET)"
	@TIMESTAMP=$$(date +%Y%m%d_%H%M%S); \
	ARCHIVE_NAME="submission_$$TIMESTAMP.zip"; \
	zip -r $$ARCHIVE_NAME . \
		-x "*.git*" \
		-x "*__pycache__*" \
		-x "*.pyc" \
		-x "venv/*" \
		-x ".venv/*" \
		-x "*.egg-info/*" \
		-x ".pytest_cache/*" \
		-x "htmlcov/*"; \
	echo "$(COLOUR_GREEN)✓ Archive created: $$ARCHIVE_NAME$(COLOUR_RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: version
version: ## Show version information
	@echo "Project: Computer Networks"
	@echo "Makefile version: 1.0"
	@$(PYTHON) --version
	@git --version 2>/dev/null || echo "Git: not installed"
	@docker --version 2>/dev/null || echo "Docker: not installed"

.PHONY: tree
tree: ## Show project structure
	@if command -v tree >/dev/null 2>&1; then \
		tree -I '__pycache__|*.pyc|venv|.git|.pytest_cache|htmlcov' -L 3; \
	else \
		find . -type d \( -name __pycache__ -o -name venv -o -name .git \) -prune -o -type f -print | head -50; \
	fi
