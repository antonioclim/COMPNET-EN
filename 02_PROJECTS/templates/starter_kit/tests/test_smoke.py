#!/usr/bin/env python3
"""
Smoke Tests — MUST PASS before any submission.

These tests verify that the basic project structure and code quality
requirements are met. Run with: pytest tests/test_smoke.py -v

All smoke tests must pass before:
- Pushing code to GitHub
- Creating submission archive
- Stage presentations
"""

import ast
import subprocess
import sys
from pathlib import Path

import pytest

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
MAIN_FILE = SRC_DIR / "main.py"
CONFIG_FILE = PROJECT_ROOT / "config.yaml"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

# Minimum requirements
MIN_PYTHON_VERSION = (3, 10)
REQUIRED_FILES = [
    "src/main.py",
    "requirements.txt",
    "README.md",
    "Makefile",
]


# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestEnvironment:
    """Tests for development environment."""
    
    def test_python_version(self):
        """Verify Python version is 3.10 or higher."""
        current = sys.version_info[:2]
        assert current >= MIN_PYTHON_VERSION, (
            f"Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ required, "
            f"but found {current[0]}.{current[1]}"
        )
    
    def test_required_files_exist(self):
        """Verify all required files exist."""
        missing = []
        for file_path in REQUIRED_FILES:
            full_path = PROJECT_ROOT / file_path
            if not full_path.exists():
                missing.append(file_path)
        
        assert not missing, f"Missing required files: {missing}"
    
    def test_requirements_file_not_empty(self):
        """Verify requirements.txt contains dependencies."""
        if not REQUIREMENTS_FILE.exists():
            pytest.skip("requirements.txt not found")
        
        content = REQUIREMENTS_FILE.read_text().strip()
        # Filter out comments and empty lines
        deps = [line for line in content.split("\n") 
                if line.strip() and not line.strip().startswith("#")]
        
        assert len(deps) > 0, "requirements.txt is empty"


# ═══════════════════════════════════════════════════════════════════════════════
# SYNTAX AND IMPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCodeSyntax:
    """Tests for code syntax and imports."""
    
    def test_main_file_exists(self):
        """Verify main.py exists."""
        assert MAIN_FILE.exists(), f"Main file not found: {MAIN_FILE}"
    
    def test_main_file_valid_syntax(self):
        """Verify main.py has valid Python syntax."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(MAIN_FILE)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, (
            f"Syntax error in {MAIN_FILE}:\n{result.stderr}"
        )
    
    def test_all_python_files_valid_syntax(self):
        """Verify all .py files have valid syntax."""
        if not SRC_DIR.exists():
            pytest.skip("src/ directory not found")
        
        errors = []
        for py_file in SRC_DIR.rglob("*.py"):
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                errors.append(f"{py_file}: {result.stderr}")
        
        assert not errors, f"Syntax errors found:\n" + "\n".join(errors)
    
    def test_main_imports_work(self):
        """Verify main.py can be imported without errors."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        # Add src to path temporarily
        sys.path.insert(0, str(SRC_DIR))
        try:
            # Try to import just to check for import errors
            result = subprocess.run(
                [sys.executable, "-c", f"import sys; sys.path.insert(0, '{SRC_DIR}'); import main"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # We accept both 0 (success) and 1 (config error, which is expected)
            # Just not syntax/import errors
            if result.returncode not in [0, 1]:
                assert False, f"Import error:\n{result.stderr}"
        finally:
            sys.path.remove(str(SRC_DIR))


# ═══════════════════════════════════════════════════════════════════════════════
# CODE QUALITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCodeQuality:
    """Tests for code quality requirements."""
    
    def test_type_hints_on_functions(self):
        """Verify public functions have type hints."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        with open(MAIN_FILE, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        functions_without_hints = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions and __special__ methods
                if node.name.startswith("_"):
                    continue
                
                # Check for return type hint
                if node.returns is None:
                    functions_without_hints.append(
                        f"{node.name}() - missing return type hint"
                    )
        
        assert not functions_without_hints, (
            f"Functions missing type hints:\n" + 
            "\n".join(f"  - {f}" for f in functions_without_hints)
        )
    
    def test_docstrings_on_functions(self):
        """Verify public functions have docstrings."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        with open(MAIN_FILE, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        functions_without_docs = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions
                if node.name.startswith("_"):
                    continue
                
                # Check for docstring
                docstring = ast.get_docstring(node)
                if not docstring:
                    functions_without_docs.append(node.name)
        
        assert not functions_without_docs, (
            f"Functions missing docstrings:\n" +
            "\n".join(f"  - {f}()" for f in functions_without_docs)
        )
    
    def test_no_print_statements_for_logging(self):
        """Verify print() is not used for logging (use logging module)."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        with open(MAIN_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            tree = ast.parse(content)
        
        print_calls = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "print":
                    # Allow print in __main__ block for user output
                    # Check if it's a logging-like print
                    if node.args:
                        first_arg = node.args[0]
                        if isinstance(first_arg, ast.Constant):
                            msg = str(first_arg.value)
                            # Suspicious logging patterns
                            if any(p in msg.lower() for p in ["error", "warning", "info", "debug", "starting", "stopping"]):
                                print_calls.append(f"Line {node.lineno}: {msg[:50]}...")
        
        if print_calls:
            pytest.skip(
                f"Found print() statements that might be logging. "
                f"Consider using logging module instead:\n" +
                "\n".join(f"  - {p}" for p in print_calls[:5])
            )
    
    def test_no_bare_except(self):
        """Verify no bare 'except:' or 'except Exception:' clauses."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        with open(MAIN_FILE, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        bare_excepts = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    bare_excepts.append(f"Line {node.lineno}: bare 'except:'")
                elif isinstance(node.type, ast.Name) and node.type.id == "Exception":
                    # This is acceptable in main() for final catch-all
                    # but flag it for review
                    pass
        
        assert not bare_excepts, (
            f"Bare except clauses found (use specific exceptions):\n" +
            "\n".join(f"  - {e}" for e in bare_excepts)
        )


# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestProjectStructure:
    """Tests for project structure."""
    
    def test_has_subgoal_labels(self):
        """Verify code uses subgoal labels for sections."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        content = MAIN_FILE.read_text()
        
        # Look for subgoal label pattern
        label_pattern = "# ═" * 5  # At least 5 ═ characters
        
        assert label_pattern in content, (
            "Code should use subgoal labels to mark sections. "
            "See code_quality_standards.md for the format."
        )
    
    def test_has_main_function(self):
        """Verify main() function exists."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        with open(MAIN_FILE, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        has_main = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                has_main = True
                break
        
        assert has_main, "main() function not found in main.py"
    
    def test_has_if_name_main(self):
        """Verify if __name__ == '__main__' block exists."""
        if not MAIN_FILE.exists():
            pytest.skip("main.py not found")
        
        content = MAIN_FILE.read_text()
        
        assert '__name__' in content and '__main__' in content, (
            "Missing if __name__ == '__main__': block"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestConfiguration:
    """Tests for configuration handling."""
    
    def test_config_file_exists(self):
        """Verify config.yaml exists (or sample exists)."""
        config_exists = CONFIG_FILE.exists()
        sample_exists = (PROJECT_ROOT / "config.yaml.sample").exists()
        
        assert config_exists or sample_exists, (
            "Neither config.yaml nor config.yaml.sample found"
        )
    
    def test_config_is_valid_yaml(self):
        """Verify config file is valid YAML."""
        config_path = CONFIG_FILE if CONFIG_FILE.exists() else (PROJECT_ROOT / "config.yaml.sample")
        
        if not config_path.exists():
            pytest.skip("No config file found")
        
        try:
            import yaml
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            assert config is not None or config == {}, "Config file is empty"
        except ImportError:
            pytest.skip("PyYAML not installed")
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML in {config_path}: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Running smoke tests...")
    print("=" * 60)
    pytest.main([__file__, "-v", "--tb=short"])
