#!/usr/bin/env python3
"""
Unit Tests for Quiz Runner Exports and Validation
==================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Tests for:
- JSON export format (Canvas/LMS compatible)
- Moodle GIFT export format
- Quiz validation functions

Run:
    python -m pytest test_quiz_exports.py -v
    python test_quiz_exports.py

Version: 1.0.0
Date: 2026-01-25
"""

import json
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from run_quiz import (
    export_to_json,
    export_to_moodle_gift,
    validate_quiz_structure,
    _build_json_question,
    _escape_gift_text
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

def get_sample_quiz() -> Dict[str, Any]:
    """Return a minimal valid quiz for testing."""
    return {
        'metadata': {
            'week': 0,
            'topic': 'Test Quiz',
            'version': '1.0.0',
            'passing_score': 70
        },
        'questions': [
            {
                'id': 'q01',
                'type': 'multiple_choice',
                'bloom_level': 'remember',
                'lo_ref': 'LO0.1',
                'stem': 'What is 2 + 2?',
                'options': {'a': '3', 'b': '4', 'c': '5', 'd': '6'},
                'correct': 'b',
                'explanation': 'Basic arithmetic'
            },
            {
                'id': 'q02',
                'type': 'fill_blank',
                'bloom_level': 'apply',
                'lo_ref': 'LO0.2',
                'stem': 'The port for HTTP is ___',
                'correct': ['80', '8080'],
                'hint': 'Standard web port'
            }
        ]
    }


def get_invalid_quiz_no_meta() -> Dict[str, Any]:
    """Return quiz missing metadata."""
    return {'questions': []}


def get_invalid_quiz_no_questions() -> Dict[str, Any]:
    """Return quiz with empty questions."""
    return {'metadata': {'week': 0, 'topic': 'Test', 'passing_score': 70}, 'questions': []}


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_validate_valid_quiz():
    """Valid quiz should pass validation."""
    quiz = get_sample_quiz()
    is_valid, errors = validate_quiz_structure(quiz)
    assert is_valid is True, f"Expected valid, got errors: {errors}"
    assert len(errors) == 0


def test_validate_missing_metadata():
    """Quiz without metadata should fail."""
    quiz = get_invalid_quiz_no_meta()
    is_valid, errors = validate_quiz_structure(quiz)
    assert is_valid is False
    assert any('metadata' in e.lower() for e in errors)


def test_validate_empty_questions():
    """Quiz with no questions should fail."""
    quiz = get_invalid_quiz_no_questions()
    is_valid, errors = validate_quiz_structure(quiz)
    assert is_valid is False
    assert any('question' in e.lower() for e in errors)


def test_validate_question_missing_fields():
    """Question missing required fields should fail."""
    quiz = {
        'metadata': {'week': 0, 'topic': 'Test', 'passing_score': 70},
        'questions': [{'id': 'q01'}]  # Missing type, stem, correct
    }
    is_valid, errors = validate_quiz_structure(quiz)
    assert is_valid is False
    assert len(errors) >= 2  # At least type, stem, correct missing


# ═══════════════════════════════════════════════════════════════════════════════
# JSON EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_export_json_creates_file():
    """JSON export should create valid file."""
    quiz = get_sample_quiz()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / 'test_export.json'
        export_to_json(quiz, output)
        
        assert output.exists(), "JSON file not created"
        
        with open(output) as f:
            data = json.load(f)
        
        assert 'metadata' in data
        assert 'questions' in data
        assert len(data['questions']) == 2


def test_export_json_mc_structure():
    """MC question should have options array with correct flag."""
    quiz = get_sample_quiz()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / 'test.json'
        export_to_json(quiz, output)
        
        with open(output) as f:
            data = json.load(f)
        
        mc_q = data['questions'][0]
        assert 'options' in mc_q
        assert len(mc_q['options']) == 4
        
        # Check exactly one correct
        correct_count = sum(1 for opt in mc_q['options'] if opt['correct'])
        assert correct_count == 1


def test_export_json_fill_blank_structure():
    """Fill-blank should have correct_answers array."""
    quiz = get_sample_quiz()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / 'test.json'
        export_to_json(quiz, output)
        
        with open(output) as f:
            data = json.load(f)
        
        fill_q = data['questions'][1]
        assert 'correct_answers' in fill_q
        assert isinstance(fill_q['correct_answers'], list)
        assert '80' in fill_q['correct_answers']


def test_build_json_question_helper():
    """Test the helper function directly."""
    q = {
        'id': 'test',
        'type': 'multiple_choice',
        'bloom_level': 'understand',
        'lo_ref': 'LO1',
        'stem': 'Test?',
        'options': {'a': 'A', 'b': 'B'},
        'correct': 'a'
    }
    result = _build_json_question(q)
    
    assert result['id'] == 'test'
    assert result['type'] == 'multiple_choice'
    assert len(result['options']) == 2


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE GIFT EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_export_moodle_creates_file():
    """Moodle export should create valid GIFT file."""
    quiz = get_sample_quiz()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / 'test.gift'
        export_to_moodle_gift(quiz, output)
        
        assert output.exists(), "GIFT file not created"
        
        content = output.read_text()
        assert '$CATEGORY:' in content
        assert '=' in content  # Correct answer marker


def test_export_moodle_mc_format():
    """MC question should have = for correct, ~ for wrong."""
    quiz = get_sample_quiz()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / 'test.gift'
        export_to_moodle_gift(quiz, output)
        
        content = output.read_text()
        
        # Should have one = (correct) and three ~ (wrong) for first question
        # Count in the MC block
        assert '=4' in content or '= 4' in content  # Correct answer is 4
        assert '~3' in content or '~ 3' in content  # Wrong answer


def test_escape_gift_text():
    """Special characters should be escaped."""
    text = "Test: with ~ and = symbols"
    escaped = _escape_gift_text(text)
    
    assert '\\:' in escaped
    assert '\\~' in escaped
    assert '\\=' in escaped


# ═══════════════════════════════════════════════════════════════════════════════
# TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> bool:
    """Run all tests and report results."""
    tests = [
        test_validate_valid_quiz,
        test_validate_missing_metadata,
        test_validate_empty_questions,
        test_validate_question_missing_fields,
        test_export_json_creates_file,
        test_export_json_mc_structure,
        test_export_json_fill_blank_structure,
        test_build_json_question_helper,
        test_export_moodle_creates_file,
        test_export_moodle_mc_format,
        test_escape_gift_text,
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("UNIT TESTS - Quiz Exports and Validation")
    print("=" * 60)
    
    for test in tests:
        try:
            test()
            print(f"✅ PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {test.__name__}")
            print(f"   Reason: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {test.__name__}")
            print(f"   {type(e).__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"RESULT: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
