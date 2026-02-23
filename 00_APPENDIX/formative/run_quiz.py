#!/usr/bin/env python3
"""
Quiz Runner for Week 0 Formative Assessment
============================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

A command-line tool for running interactive formative quizzes.
Supports multiple question types, Bloom level filtering, review mode
and LMS export (Moodle GIFT, Canvas QTI, JSON).

Usage:
    python run_quiz.py                    # Run full quiz
    python run_quiz.py --random           # Randomise question order
    python run_quiz.py --limit 5          # Run only 5 questions
    python run_quiz.py --bloom apply      # Filter by Bloom level
    python run_quiz.py --show-answers     # Review mode (show answers)
    python run_quiz.py --export json      # Export to JSON for LMS
    python run_quiz.py --export moodle    # Export to Moodle GIFT format
    python run_quiz.py --help             # Show all options

Requirements:
    pip install pyyaml

Version: 1.6.0
Date: 2026-01-25
"""

import yaml
import json
import random
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime

__all__ = [
    'load_quiz',
    'run_quiz',
    'export_to_json',
    'export_to_moodle_gift',
    'export_to_qti',
    'validate_quiz_structure'
]


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADING AND VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz data from YAML file."""
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_quiz_structure(quiz: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate quiz has required structure.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if 'metadata' not in quiz:
        errors.append("Missing 'metadata' section")
    else:
        meta = quiz['metadata']
        required_meta = ['week', 'topic', 'passing_score']
        for field in required_meta:
            if field not in meta:
                errors.append(f"Missing metadata field: {field}")
    
    if 'questions' not in quiz:
        errors.append("Missing 'questions' section")
    elif not quiz['questions']:
        errors.append("No questions defined")
    else:
        for i, q in enumerate(quiz['questions']):
            q_errors = _validate_question(q, i)
            errors.extend(q_errors)
    
    return (len(errors) == 0, errors)


def _validate_question(q: Dict[str, Any], index: int) -> List[str]:
    """Validate a single question structure."""
    errors = []
    required = ['id', 'type', 'stem', 'correct']
    
    for field in required:
        if field not in q:
            errors.append(f"Q{index+1}: Missing field '{field}'")
    
    if q.get('type') == 'multiple_choice' and 'options' not in q:
        errors.append(f"Q{index+1}: MC question missing 'options'")
    
    return errors


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION DISPLAY HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _format_question_header(q: Dict[str, Any], index: int) -> str:
    """Format the header line for a question."""
    bloom_badge = f"[{q.get('bloom_level', '?').upper()}]"
    diff_badge = f"({q.get('difficulty', '?')})"
    lo_badge = f"LO: {q.get('lo_ref', 'N/A')}"
    return f"Q{index}. {bloom_badge} {diff_badge} | {lo_badge}"


def _display_mc_options(options: Dict[str, str]) -> None:
    """Display multiple choice options."""
    for key, value in options.items():
        print(f"   {key}) {value}")


def _show_answer_mc(q: Dict[str, Any]) -> None:
    """Show answer for multiple choice in review mode."""
    print(f"\n   ✓ Correct answer: {q['correct']}")
    if 'explanation' in q:
        print(f"   📖 {q['explanation']}")


def _show_answer_fill(q: Dict[str, Any]) -> None:
    """Show answer for fill-blank in review mode."""
    correct = q['correct']
    if isinstance(correct, list):
        print(f"\n   ✓ Accepted answers: {', '.join(correct)}")
    else:
        print(f"\n   ✓ Correct answer: {correct}")
    if 'explanation' in q:
        print(f"   📖 {q['explanation']}")


def _get_user_answer(prompt: str) -> str:
    """Get answer from user with consistent formatting."""
    return input(prompt).strip().lower()


def _check_mc_answer(user_ans: str, correct: str, q: Dict[str, Any]) -> bool:
    """Check multiple choice answer and show feedback."""
    if user_ans == correct:
        print("   ✅ Correct!")
        if 'feedback' in q and 'correct' in q['feedback']:
            print(f"   💬 {q['feedback']['correct']}")
        return True
    else:
        print(f"   ❌ Wrong. Correct answer: {correct}")
        if 'explanation' in q:
            print(f"   📖 {q['explanation']}")
        if 'feedback' in q and 'incorrect' in q['feedback']:
            print(f"   💬 {q['feedback']['incorrect']}")
        return False


def _check_fill_answer(user_ans: str, correct: Any, q: Dict[str, Any]) -> bool:
    """Check fill-blank answer and show feedback."""
    if isinstance(correct, list):
        is_correct = user_ans in [c.lower() for c in correct]
    else:
        is_correct = user_ans == correct.lower()
    
    if is_correct:
        print("   ✅ Correct!")
        if 'feedback' in q and 'correct' in q['feedback']:
            print(f"   💬 {q['feedback']['correct']}")
        return True
    else:
        if isinstance(correct, list):
            print(f"   ❌ Wrong. Accepted: {', '.join(correct)}")
        else:
            print(f"   ❌ Wrong. Correct: {correct}")
        if 'explanation' in q:
            print(f"   📖 {q['explanation']}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN QUESTION HANDLER
# ═══════════════════════════════════════════════════════════════════════════════

def display_question(
    q: Dict[str, Any], 
    index: int, 
    show_answer: bool = False
) -> Optional[bool]:
    """Display a question and collect/evaluate answer.
    
    Returns:
        True if correct, False if wrong, None if skipped
    """
    print(f"\n{'─' * 60}")
    print(_format_question_header(q, index))
    print(f"{'─' * 60}")
    print(f"\n{q['stem']}\n")
    
    if q['type'] == 'multiple_choice':
        return _handle_mc_question(q, show_answer)
    elif q['type'] == 'fill_blank':
        return _handle_fill_question(q, show_answer)
    
    return None


def _handle_mc_question(q: Dict[str, Any], show_answer: bool) -> Optional[bool]:
    """Handle multiple choice question flow."""
    _display_mc_options(q['options'])
    
    if show_answer:
        _show_answer_mc(q)
        return None
    
    answer = _get_user_answer("\nYour answer (a/b/c/d or 's' to skip): ")
    
    if answer == 's':
        print("   ⏭️  Skipped")
        return None
    
    return _check_mc_answer(answer, q['correct'], q)


def _handle_fill_question(q: Dict[str, Any], show_answer: bool) -> Optional[bool]:
    """Handle fill-blank question flow."""
    if 'hint' in q:
        print(f"   💡 Hint: {q['hint']}")
    
    if show_answer:
        _show_answer_fill(q)
        return None
    
    answer = _get_user_answer("\nYour answer (or 's' to skip): ")
    
    if answer == 's':
        print("   ⏭️  Skipped")
        return None
    
    return _check_fill_answer(answer, q['correct'], q)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def get_feedback(score: float, scoring_config: Dict[str, Any]) -> str:
    """Get feedback message based on score."""
    levels = scoring_config.get('levels', [])
    for level in levels:
        range_min, range_max = level['range']
        if range_min <= score <= range_max:
            return f"{level['label']}: {level['feedback']}"
    return "Review the material and try again."


def _display_quiz_header(
    meta: Dict[str, Any], 
    num_questions: int, 
    bloom_filter: Optional[str], 
    show_answers: bool
) -> None:
    """Display quiz header with metadata."""
    print("\n" + "═" * 60)
    print(f"  📝 QUIZ: {meta.get('topic', 'Formative Assessment')}")
    print("═" * 60)
    print(f"  Questions: {num_questions}")
    print(f"  Passing score: {meta.get('passing_score', 70)}%")
    print(f"  Estimated time: {meta.get('estimated_time', '15 minutes')}")
    if bloom_filter:
        print(f"  Bloom filter: {bloom_filter.upper()}")
    if show_answers:
        print("  Mode: 📖 REVIEW (answers shown)")
    print("═" * 60)


def _display_quiz_results(
    correct: int, 
    answered: int, 
    skipped: int, 
    score: float, 
    passing_score: int, 
    passed: bool, 
    scoring: Dict[str, Any]
) -> None:
    """Display quiz results with feedback."""
    print("\n" + "═" * 60)
    print("  📊 RESULTS")
    print("═" * 60)
    print(f"  Correct: {correct}/{answered}")
    if skipped > 0:
        print(f"  Skipped: {skipped}")
    print(f"  Score: {score:.1f}%")
    print(f"  Passing: {passing_score}%")
    print(f"  Status: {'✅ PASSED' if passed else '❌ NEEDS REVIEW'}")
    
    if scoring:
        feedback = get_feedback(score, scoring)
        print(f"\n  💬 {feedback}")
    
    print("═" * 60 + "\n")


def run_quiz(
    quiz: Dict[str, Any], 
    randomise: bool = False, 
    limit: Optional[int] = None,
    bloom_filter: Optional[str] = None,
    show_answers: bool = False
) -> Dict[str, Any]:
    """Run the interactive quiz."""
    questions = list(quiz.get('questions', []))
    
    # Apply Bloom level filter
    if bloom_filter:
        bloom_filter = bloom_filter.lower()
        questions = [q for q in questions 
                     if q.get('bloom_level', '').lower() == bloom_filter]
        if not questions:
            print(f"No questions found for Bloom level: {bloom_filter}")
            return {'score': 0, 'total': 0, 'passed': False}
    
    if randomise:
        random.shuffle(questions)
        
    if limit and limit > 0:
        questions = questions[:limit]
    
    if not questions:
        print("No questions available.")
        return {'score': 0, 'total': 0, 'passed': False}
    
    meta = quiz.get('metadata', {})
    _display_quiz_header(meta, len(questions), bloom_filter, show_answers)
    
    input("\nPress Enter to start...")
    
    correct, answered, skipped = 0, 0, 0
    
    for i, q in enumerate(questions, 1):
        result = display_question(q, i, show_answers)
        if result is True:
            correct += 1
            answered += 1
        elif result is False:
            answered += 1
        else:
            skipped += 1
    
    score = (correct / answered) * 100 if answered > 0 else 0.0
    passing_score = meta.get('passing_score', 70)
    passed = score >= passing_score
    
    _display_quiz_results(correct, answered, skipped, score, 
                          passing_score, passed, quiz.get('scoring', {}))
    
    return {
        'score': score,
        'correct': correct,
        'answered': answered,
        'skipped': skipped,
        'total': len(questions),
        'passed': passed
    }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def _build_json_question(q: Dict[str, Any]) -> Dict[str, Any]:
    """Transform a single question to JSON export format."""
    question_data = {
        "id": q.get('id'),
        "type": q.get('type'),
        "bloom_level": q.get('bloom_level'),
        "learning_objective": q.get('lo_ref'),
        "stem": q.get('stem'),
        "points": q.get('points', 1)
    }
    
    if q['type'] == 'multiple_choice':
        question_data['options'] = [
            {"key": k, "text": v, "correct": k == q['correct']}
            for k, v in q['options'].items()
        ]
    elif q['type'] == 'fill_blank':
        correct = q['correct']
        question_data['correct_answers'] = (
            correct if isinstance(correct, list) else [correct]
        )
    
    if 'explanation' in q:
        question_data['explanation'] = q['explanation']
    if 'feedback' in q:
        question_data['feedback'] = q['feedback']
        
    return question_data


def export_to_json(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to JSON format for LMS import."""
    meta = quiz.get('metadata', {})
    
    export_data = {
        "metadata": {
            "title": f"Week {meta.get('week', 0)}: {meta.get('topic', 'Quiz')}",
            "description": "Formative assessment for Computer Networks",
            "version": meta.get('version', '1.0'),
            "date": datetime.now().isoformat(),
            "total_questions": len(quiz.get('questions', [])),
            "passing_score": meta.get('passing_score', 70)
        },
        "questions": [_build_json_question(q) for q in quiz.get('questions', [])]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported to JSON: {output_path}")


def _escape_gift_text(text: str) -> str:
    """Escape special characters for GIFT format."""
    return text.replace(':', '\\:').replace('~', '\\~').replace('=', '\\=')


def _build_gift_mc(q: Dict[str, Any], category: str) -> List[str]:
    """Build GIFT lines for multiple choice question."""
    lines = [f"$CATEGORY: {category}", ""]
    title = f"[{q.get('id', 'Q')}] {q.get('lo_ref', '')}"
    stem = _escape_gift_text(q['stem'])
    
    lines.append(f"::{title}::{stem} {{")
    for key, value in q['options'].items():
        value_escaped = value.replace('~', '\\~').replace('=', '\\=')
        prefix = '=' if key == q['correct'] else '~'
        lines.append(f"  {prefix}{value_escaped}")
    lines.append("}")
    lines.append("")
    
    return lines


def _build_gift_fill(q: Dict[str, Any], category: str) -> List[str]:
    """Build GIFT lines for fill-blank question."""
    lines = [f"$CATEGORY: {category}", ""]
    title = f"[{q.get('id', 'Q')}] {q.get('lo_ref', '')}"
    stem = q['stem'].replace('___', '{')
    correct = q['correct']
    correct_list = correct if isinstance(correct, list) else [correct]
    answers = ' '.join(f"={ans}" for ans in correct_list)
    
    lines.append(f"::{title}::{stem}{answers}}}")
    lines.append("")
    
    return lines


def export_to_moodle_gift(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle GIFT format."""
    meta = quiz.get('metadata', {})
    week = meta.get('week', 0)
    
    lines = [
        f"// Week {week} Quiz - Moodle GIFT Format",
        f"// Generated: {datetime.now().isoformat()}",
        ""
    ]
    
    for q in quiz.get('questions', []):
        category = f"Week{week}/{q.get('lo_ref', 'General')}"
        
        if q['type'] == 'multiple_choice':
            lines.extend(_build_gift_mc(q, category))
        elif q['type'] == 'fill_blank':
            lines.extend(_build_gift_fill(q, category))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Exported to Moodle GIFT: {output_path}")


def export_to_qti(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to QTI 1.2 format (Canvas compatible)."""
    print("⚠️  QTI export is simplified. For full Canvas import, use quiz.json")
    
    meta = quiz.get('metadata', {})
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2">',
        f'  <assessment title="Week {meta.get("week", 0)} Quiz">',
        '    <section>'
    ]
    
    for q in quiz.get('questions', []):
        xml_lines.append(f'      <item title="{q.get("id", "Q")}">')
        xml_lines.append(f'        <presentation><material>')
        xml_lines.append(f'          <mattext>{q["stem"]}</mattext>')
        xml_lines.append(f'        </material></presentation>')
        xml_lines.append('      </item>')
    
    xml_lines.extend([
        '    </section>',
        '  </assessment>',
        '</questestinterop>'
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    print(f"✅ Exported to QTI: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def _build_arg_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        description='Run Week 0 formative quiz for Computer Networks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_quiz.py                    # Run full quiz
  python run_quiz.py --random           # Randomise questions
  python run_quiz.py --limit 5          # Only 5 questions
  python run_quiz.py --bloom apply      # Only 'apply' level
  python run_quiz.py --show-answers     # Review mode
  python run_quiz.py --export json      # Export to JSON
  python run_quiz.py --validate         # Validate quiz structure
        """
    )
    parser.add_argument(
        '--quiz', '-q',
        type=Path,
        default=Path(__file__).parent / 'quiz.yaml',
        help='Path to quiz YAML file (default: ./quiz.yaml)'
    )
    parser.add_argument(
        '--random', '-r',
        action='store_true',
        help='Randomise question order'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        metavar='N',
        help='Limit to N questions'
    )
    parser.add_argument(
        '--bloom', '-b',
        choices=['remember', 'understand', 'apply', 'analyse', 'evaluate', 'create'],
        metavar='LEVEL',
        help='Filter by Bloom taxonomy level'
    )
    parser.add_argument(
        '--show-answers', '-a',
        action='store_true',
        help='Review mode: show answers without testing'
    )
    parser.add_argument(
        '--export', '-e',
        choices=['json', 'moodle', 'qti'],
        metavar='FORMAT',
        help='Export quiz to specified format'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output path for export'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate quiz structure and exit'
    )
    parser.add_argument(
        '--no-colour', '--no-color',
        action='store_true',
        help='Disable coloured output'
    )
    return parser


def _handle_export(quiz: Dict[str, Any], args) -> int:
    """Handle export mode."""
    output_path = args.output
    if not output_path:
        base = args.quiz.stem
        ext_map = {'json': '_export.json', 'moodle': '_moodle.gift', 'qti': '_qti.xml'}
        output_path = args.quiz.parent / f"{base}{ext_map[args.export]}"
    
    export_funcs = {
        'json': export_to_json,
        'moodle': export_to_moodle_gift,
        'qti': export_to_qti
    }
    export_funcs[args.export](quiz, output_path)
    return 0


def main() -> int:
    """Main entry point."""
    parser = _build_arg_parser()
    args = parser.parse_args()
    
    if not args.quiz.exists():
        print(f"Error: Quiz file not found: {args.quiz}")
        return 1
    
    try:
        quiz = load_quiz(args.quiz)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in quiz file\nDetails: {e}")
        return 1
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1
    
    # Validate mode
    if args.validate:
        is_valid, errors = validate_quiz_structure(quiz)
        if is_valid:
            print("✅ Quiz structure is valid")
            return 0
        else:
            print("❌ Quiz validation failed:")
            for err in errors:
                print(f"   - {err}")
            return 1
    
    # Export mode
    if args.export:
        return _handle_export(quiz, args)
    
    # Run quiz
    try:
        results = run_quiz(
            quiz,
            randomise=args.random,
            limit=args.limit,
            bloom_filter=args.bloom,
            show_answers=args.show_answers
        )
    except KeyboardInterrupt:
        print("\n\n👋 Quiz interrupted by user.")
        return 0
    
    if args.show_answers:
        return 0
    return 0 if results.get('passed', False) else 1


if __name__ == "__main__":
    sys.exit(main())
