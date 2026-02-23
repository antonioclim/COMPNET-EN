# ============================================================================
# Python Networking Self-Study Guide — Makefile
# ============================================================================
# Automation for students transitioning from C/C++, JavaScript, Java, Kotlin
#
# Usage:
#   make help              # Show all available commands
#   make quiz              # Run full quiz
#   make quiz-quick        # 10 random questions
#   make parsons           # Run Parsons problems
#
# Version: 5.0 — January 2026
# Course: Computer Networks — ASE Bucharest, CSIE
# ============================================================================

.PHONY: help quiz quiz-quick quiz-random quiz-section \
        quiz-c quiz-java quiz-js quiz-kotlin \
        parsons parsons-socket parsons-bytes parsons-list \
        test test-all test-bytes test-struct test-smoke \
        view-rosetta view-misconceptions view-cheatsheet view-guide \
        view-troubleshooting \
        check install lint clean

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python3

# Directories
QUIZ_DIR := formative
PARSONS_DIR := formative/parsons
EXAMPLES_DIR := examples
TESTS_DIR := examples/tests
COMPARISONS_DIR := comparisons
CHEATSHEETS_DIR := cheatsheets
DOCS_DIR := docs

# Runners
QUIZ_RUNNER := $(QUIZ_DIR)/run_quiz.py
PARSONS_RUNNER := $(QUIZ_DIR)/parsons_runner.py
QUIZ_FILE := $(QUIZ_DIR)/quiz.yaml

# Colours for terminal output
COLOUR_RESET := \033[0m
COLOUR_BOLD := \033[1m
COLOUR_GREEN := \033[32m
COLOUR_YELLOW := \033[33m
COLOUR_CYAN := \033[36m

# ============================================================================
# HELP
# ============================================================================

help:
	@echo ""
	@echo "$(COLOUR_BOLD)🐍 Python Networking Self-Study Guide v5.0$(COLOUR_RESET)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "$(COLOUR_CYAN)QUIZ COMMANDS:$(COLOUR_RESET)"
	@echo "  make quiz             Run full assessment (31 questions)"
	@echo "  make quiz-quick       Quick assessment (10 random questions)"
	@echo "  make quiz-random      Randomised full quiz"
	@echo "  make quiz-section S=x Filter by section (e.g., S=socket)"
	@echo ""
	@echo "$(COLOUR_CYAN)BACKGROUND-SPECIFIC QUIZZES:$(COLOUR_RESET)"
	@echo "  make quiz-c           Questions for C/C++ programmers"
	@echo "  make quiz-java        Questions for Java programmers"
	@echo "  make quiz-js          Questions for JavaScript programmers"
	@echo "  make quiz-kotlin      Questions for Kotlin programmers"
	@echo ""
	@echo "$(COLOUR_CYAN)PARSONS PROBLEMS:$(COLOUR_RESET)"
	@echo "  make parsons          Run all Parsons problems"
	@echo "  make parsons-socket   Socket-specific problems"
	@echo "  make parsons-bytes    Bytes/encoding problems"
	@echo "  make parsons-list     List available problem files"
	@echo ""
	@echo "$(COLOUR_CYAN)VIEW DOCUMENTATION:$(COLOUR_RESET)"
	@echo "  make view-rosetta         Language comparison (Rosetta Stone)"
	@echo "  make view-misconceptions  Common mistakes by background"
	@echo "  make view-cheatsheet      Python quick reference"
	@echo "  make view-troubleshooting Error solutions guide"
	@echo "  make view-guide           Full networking guide"
	@echo ""
	@echo "$(COLOUR_CYAN)TESTING:$(COLOUR_RESET)"
	@echo "  make test             Run all tests"
	@echo "  make test-smoke       Run smoke tests only"
	@echo "  make test-bytes       Run bytes/string tests"
	@echo "  make test-struct      Run struct parsing tests"
	@echo ""
	@echo "$(COLOUR_CYAN)DEVELOPMENT:$(COLOUR_RESET)"
	@echo "  make check            Verify Python environment"
	@echo "  make install          Install required dependencies"
	@echo "  make lint             Check code style"
	@echo "  make clean            Remove generated files"
	@echo ""
	@echo "$(COLOUR_CYAN)EXAMPLES:$(COLOUR_RESET)"
	@echo "  make demo-tcp         Run TCP socket example"
	@echo "  make demo-bytes       Run bytes vs strings example"
	@echo "  make demo-struct      Run struct parsing example"
	@echo "  make demo-errors      Run error handling example"
	@echo ""

# ============================================================================
# QUIZ COMMANDS
# ============================================================================

quiz:
	@echo "$(COLOUR_BOLD)Running full quiz...$(COLOUR_RESET)"
	@$(PYTHON) $(QUIZ_RUNNER) --save

quiz-quick:
	@echo "$(COLOUR_BOLD)Running quick quiz (10 questions)...$(COLOUR_RESET)"
	@$(PYTHON) $(QUIZ_RUNNER) --quick --save

quiz-random:
	@echo "$(COLOUR_BOLD)Running randomised quiz...$(COLOUR_RESET)"
	@$(PYTHON) $(QUIZ_RUNNER) --random --save

# Section-specific quiz (usage: make quiz-section S=sockets)
quiz-section:
ifndef S
	@echo "$(COLOUR_YELLOW)Usage: make quiz-section S=<section_name>$(COLOUR_RESET)"
	@echo "Available sections: basic_syntax, bytes_and_strings, socket_programming,"
	@echo "                    error_handling, python_idioms, debugging"
else
	@echo "$(COLOUR_BOLD)Running quiz for section: $(S)$(COLOUR_RESET)"
	@$(PYTHON) $(QUIZ_RUNNER) --section "$(S)" --save
endif

# ============================================================================
# BACKGROUND-SPECIFIC QUIZZES
# ============================================================================

quiz-c:
	@echo "$(COLOUR_BOLD)Quiz for C/C++ programmers...$(COLOUR_RESET)"
	@$(PYTHON) $(QUIZ_RUNNER) --background c --save

quiz-java:
	@echo "$(COLOUR_BOLD)Quiz for Java programmers...$(COLOUR_RESET)"
	@$(PYTHON) $(QUIZ_RUNNER) --background java --save

quiz-js:
	@echo "$(COLOUR_BOLD)Quiz for JavaScript programmers...$(COLOUR_RESET)"
	@$(PYTHON) $(QUIZ_RUNNER) --background javascript --save

quiz-kotlin:
	@echo "$(COLOUR_BOLD)Quiz for Kotlin programmers...$(COLOUR_RESET)"
	@$(PYTHON) $(QUIZ_RUNNER) --background kotlin --save

# ============================================================================
# PARSONS PROBLEMS
# ============================================================================

parsons:
	@echo "$(COLOUR_BOLD)Running all Parsons problems...$(COLOUR_RESET)"
	@$(PYTHON) $(PARSONS_RUNNER)

parsons-socket:
	@echo "$(COLOUR_BOLD)Running socket Parsons problems...$(COLOUR_RESET)"
	@$(PYTHON) $(PARSONS_RUNNER) --file parsons_socket.yaml

parsons-bytes:
	@echo "$(COLOUR_BOLD)Running bytes/encoding Parsons problems...$(COLOUR_RESET)"
	@$(PYTHON) $(PARSONS_RUNNER) --file parsons_bytes.yaml

parsons-list:
	@echo "$(COLOUR_BOLD)Available Parsons problem files:$(COLOUR_RESET)"
	@$(PYTHON) $(PARSONS_RUNNER) --list

# ============================================================================
# VIEW DOCUMENTATION
# ============================================================================

# Detect pager (prefer less, fallback to more, then cat)
PAGER := $(shell command -v less 2>/dev/null || command -v more 2>/dev/null || echo cat)

view-rosetta:
	@echo "$(COLOUR_BOLD)Opening Rosetta Stone comparison...$(COLOUR_RESET)"
	@$(PAGER) $(COMPARISONS_DIR)/ROSETTA_STONE.md

view-misconceptions:
	@echo "$(COLOUR_BOLD)Opening misconceptions guide...$(COLOUR_RESET)"
	@$(PAGER) $(COMPARISONS_DIR)/MISCONCEPTIONS_BY_BACKGROUND.md

view-cheatsheet:
	@echo "$(COLOUR_BOLD)Opening Python quick reference...$(COLOUR_RESET)"
	@$(PAGER) $(CHEATSHEETS_DIR)/PYTHON_QUICK.md

view-troubleshooting:
	@echo "$(COLOUR_BOLD)Opening troubleshooting guide...$(COLOUR_RESET)"
	@$(PAGER) $(DOCS_DIR)/TROUBLESHOOTING.md

view-guide:
	@echo "$(COLOUR_BOLD)Opening full networking guide...$(COLOUR_RESET)"
	@$(PAGER) PYTHON_NETWORKING_GUIDE.md

# ============================================================================
# EXAMPLE DEMOS
# ============================================================================

demo-tcp:
	@echo "$(COLOUR_BOLD)Running TCP socket example...$(COLOUR_RESET)"
	@$(PYTHON) $(EXAMPLES_DIR)/01_socket_tcp.py --help 2>/dev/null || \
		echo "$(COLOUR_YELLOW)Run with: python $(EXAMPLES_DIR)/01_socket_tcp.py server$(COLOUR_RESET)"

demo-bytes:
	@echo "$(COLOUR_BOLD)Running bytes vs strings example...$(COLOUR_RESET)"
	@$(PYTHON) $(EXAMPLES_DIR)/02_bytes_vs_str.py

demo-struct:
	@echo "$(COLOUR_BOLD)Running struct parsing example...$(COLOUR_RESET)"
	@$(PYTHON) $(EXAMPLES_DIR)/03_struct_parsing.py

demo-errors:
	@echo "$(COLOUR_BOLD)Running error handling example...$(COLOUR_RESET)"
	@$(PYTHON) $(EXAMPLES_DIR)/04_error_handling.py

# ============================================================================
# TESTING
# ============================================================================

test: test-all

test-all:
	@echo "$(COLOUR_BOLD)Running all tests...$(COLOUR_RESET)"
	@if command -v pytest >/dev/null 2>&1; then \
		pytest $(TESTS_DIR)/ -v; \
	else \
		$(PYTHON) -m pytest $(TESTS_DIR)/ -v 2>/dev/null || \
		($(PYTHON) $(TESTS_DIR)/test_smoke.py && \
		 $(PYTHON) $(TESTS_DIR)/test_bytes_vs_str.py && \
		 $(PYTHON) $(TESTS_DIR)/test_struct_parsing.py); \
	fi

test-smoke:
	@echo "$(COLOUR_BOLD)Running smoke tests...$(COLOUR_RESET)"
	@$(PYTHON) $(TESTS_DIR)/test_smoke.py

test-bytes:
	@echo "$(COLOUR_BOLD)Running bytes/string tests...$(COLOUR_RESET)"
	@$(PYTHON) $(TESTS_DIR)/test_bytes_vs_str.py

test-struct:
	@echo "$(COLOUR_BOLD)Running struct parsing tests...$(COLOUR_RESET)"
	@$(PYTHON) $(TESTS_DIR)/test_struct_parsing.py

# ============================================================================
# DEVELOPMENT
# ============================================================================

check:
	@echo "$(COLOUR_BOLD)Checking Python environment...$(COLOUR_RESET)"
	@echo ""
	@echo "Python version:"
	@$(PYTHON) --version
	@echo ""
	@echo "Required modules:"
	@$(PYTHON) -c "import socket; print('  ✓ socket')" 2>/dev/null || echo "  ✗ socket (built-in)"
	@$(PYTHON) -c "import struct; print('  ✓ struct')" 2>/dev/null || echo "  ✗ struct (built-in)"
	@$(PYTHON) -c "import yaml; print('  ✓ pyyaml')" 2>/dev/null || echo "  ✗ pyyaml (run: make install)"
	@$(PYTHON) -c "import json; print('  ✓ json')" 2>/dev/null || echo "  ✗ json (built-in)"
	@$(PYTHON) -c "import argparse; print('  ✓ argparse')" 2>/dev/null || echo "  ✗ argparse (built-in)"
	@$(PYTHON) -c "import logging; print('  ✓ logging')" 2>/dev/null || echo "  ✗ logging (built-in)"
	@echo ""
	@echo "Optional modules:"
	@$(PYTHON) -c "import pytest; print('  ✓ pytest')" 2>/dev/null || echo "  ○ pytest (optional, for testing)"
	@$(PYTHON) -c "import ruff; print('  ✓ ruff')" 2>/dev/null || echo "  ○ ruff (optional, for linting)"
	@echo ""
	@echo "$(COLOUR_GREEN)Environment check complete.$(COLOUR_RESET)"

install:
	@echo "$(COLOUR_BOLD)Installing dependencies...$(COLOUR_RESET)"
	@pip install --user pyyaml pytest 2>/dev/null || \
		pip install pyyaml pytest --break-system-packages || \
		echo "$(COLOUR_YELLOW)Please install: pip install pyyaml pytest$(COLOUR_RESET)"

lint:
	@echo "$(COLOUR_BOLD)Checking code style...$(COLOUR_RESET)"
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check $(QUIZ_RUNNER) $(PARSONS_RUNNER) $(EXAMPLES_DIR)/*.py --ignore E501; \
	elif command -v flake8 >/dev/null 2>&1; then \
		flake8 $(QUIZ_RUNNER) $(PARSONS_RUNNER) $(EXAMPLES_DIR)/*.py --max-line-length=100; \
	else \
		$(PYTHON) -m py_compile $(QUIZ_RUNNER) $(PARSONS_RUNNER) && \
		$(PYTHON) -m py_compile $(EXAMPLES_DIR)/*.py && \
		echo "$(COLOUR_GREEN)Syntax OK$(COLOUR_RESET)"; \
	fi

clean:
	@echo "$(COLOUR_BOLD)Cleaning generated files...$(COLOUR_RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@rm -f $(QUIZ_DIR)/results/*.json 2>/dev/null || true
	@echo "$(COLOUR_GREEN)Clean complete.$(COLOUR_RESET)"

# ============================================================================
# STATISTICS
# ============================================================================

stats:
	@echo "$(COLOUR_BOLD)Guide Statistics:$(COLOUR_RESET)"
	@echo ""
	@echo "Quiz questions: $$(grep -c '  - id:' $(QUIZ_FILE) 2>/dev/null || echo 0)"
	@echo "Parsons problems: $$(grep -c '  - id:' $(PARSONS_DIR)/*.yaml 2>/dev/null || echo 0)"
	@echo "Python examples: $$(ls -1 $(EXAMPLES_DIR)/*.py 2>/dev/null | wc -l)"
	@echo "Test files: $$(ls -1 $(TESTS_DIR)/test_*.py 2>/dev/null | wc -l)"
	@echo "HTML presentations: $$(ls -1 PRESENTATIONS_EN/*.html 2>/dev/null | wc -l)"
	@echo ""

# ============================================================================
# End of Makefile
# ============================================================================
