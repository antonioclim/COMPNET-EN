#!/usr/bin/env python3
"""
Quiz Runner for Week 0 Formative Assessment
============================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

A command-line tool for running interactive formative quizzes.
Supports multiple question types, Bloom level filtering, review mode
and export (Moodle GIFT, QTI 1.2 packages and repository JSON).

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
import re
import math
import zipfile
import xml.etree.ElementTree as ET
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
    """Validate authoring contracts before running or exporting a bank."""
    errors = []
    if not isinstance(quiz, dict):
        return False, ["Quiz must be a mapping with metadata and questions"]
    meta = quiz.get('metadata')
    if not isinstance(meta, dict):
        errors.append("metadata must be a mapping")
    else:
        for field in ('week', 'topic', 'passing_score'):
            if field not in meta:
                errors.append(f"Missing metadata field: {field}")
        passing = meta.get('passing_score')
        if isinstance(passing, bool) or not isinstance(passing, (int, float)) or not 0 <= passing <= 100:
            errors.append("metadata.passing_score must be between 0 and 100")
        if not isinstance(meta.get('topic'), str) or not meta.get('topic', '').strip():
            errors.append("metadata.topic must be non-empty text")
        if not isinstance(meta.get('week'), int) or isinstance(meta.get('week'), bool) or meta['week'] < 0:
            errors.append("metadata.week must be a non-negative integer")
    questions = quiz.get('questions')
    if not isinstance(questions, list) or not questions:
        errors.append("questions must be a non-empty list")
    else:
        ids = set()
        for i, q in enumerate(questions):
            errors.extend(_validate_question(q, i))
            ident = q.get('id') if isinstance(q, dict) else None
            if isinstance(ident, str):
                if ident in ids:
                    errors.append(f"Q{i+1}: duplicate id {ident!r}")
                ids.add(ident)
    return not errors, errors


def _validate_question(q: Dict[str, Any], index: int) -> List[str]:
    prefix = f"Q{index+1}: "
    if not isinstance(q, dict):
        return [prefix + "question must be a mapping"]
    errors = []
    points = q.get('points', 1)
    if isinstance(points, bool) or not isinstance(points, (int, float)) or not math.isfinite(points) or points <= 0:
        errors.append(prefix + "points must be a positive finite number")
    for field in ('id', 'type', 'stem', 'correct'):
        if field not in q:
            errors.append(prefix + f"Missing field '{field}'")
    for field in ('id', 'stem'):
        if not isinstance(q.get(field), str) or not q.get(field, '').strip():
            errors.append(prefix + f"{field} must be non-empty text")
    if q.get('type') not in ('multiple_choice', 'fill_blank'):
        errors.append(prefix + "unsupported question type")
    elif q['type'] == 'multiple_choice':
        opts = q.get('options')
        if not isinstance(opts, dict) or len(opts) < 2:
            errors.append(prefix + "options must be a mapping of at least two choices")
        elif not all(isinstance(k, str) and k and isinstance(v, str) and v.strip() for k, v in opts.items()):
            errors.append(prefix + "option identifiers and text must be non-empty strings")
        elif not isinstance(q.get('correct'), str) or q['correct'] not in opts:
            errors.append(prefix + "correct must name an existing option")
    else:
        answers = q.get('correct')
        answers = answers if isinstance(answers, list) else [answers]
        if not answers or not all(isinstance(a, str) and a.strip() for a in answers):
            errors.append(prefix + "fill_blank correct must contain non-empty answer strings")
        if isinstance(q.get('stem'), str) and q['stem'].count('___') != 1:
            errors.append(prefix + "fill_blank stem must contain exactly one ___ marker")
    return errors


def _require_valid(quiz: Dict[str, Any]) -> None:
    valid, errors = validate_quiz_structure(quiz)
    if not valid:
        raise ValueError("Invalid quiz: " + "; ".join(errors))


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
    
    correct, answered, skipped, visited = 0, 0, 0, 0
    earned_points = 0.0
    planned_points = sum(float(q.get('points', 1)) for q in questions)
    try:
        input("\nPress Enter to start...")
        for i, q in enumerate(questions, 1):
            result = display_question(q, i, show_answers)
            visited += 1
            if result is True:
                correct += 1
                answered += 1
                earned_points += float(q.get('points', 1))
            elif result is False:
                answered += 1
            elif not show_answers:
                skipped += 1
    except (KeyboardInterrupt, EOFError):
        print("\nSession ended before all questions were visited.")

    unattempted = len(questions) - visited
    session_status = 'review' if show_answers else ('complete' if not unattempted else 'incomplete')
    score = (earned_points / planned_points) * 100 if planned_points > 0 else 0.0
    passing_score = meta.get('passing_score', 70)
    passed = session_status == 'complete' and score >= passing_score
    
    if session_status == 'complete':
        _display_quiz_results(correct, answered, skipped, score,
                              passing_score, passed, quiz.get('scoring', {}))
        print(f"Points: {earned_points:g}/{planned_points:g}; skipped questions earn zero.")
    else:
        print(f"Session: {session_status.upper()} — no pass/readiness verdict.")
        print(f"Answered: {answered}; skipped: {skipped}; unattempted: {unattempted}.")
    
    return {
        'score': score,
        'correct': correct,
        'answered': answered,
        'skipped': skipped,
        'total': len(questions),
        'earned_points': earned_points,
        'planned_points': planned_points,
        'unattempted': unattempted,
        'session_status': session_status,
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
    """Export the repository JSON interchange format (not an LMS import package)."""
    _require_valid(quiz)
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
    """Escape GIFT controls, including literal backslashes and line breaks."""
    return ''.join('\\' + c if c in '\\~=#{}:' else c for c in str(text)).replace('\n', '\\n')


def _build_gift_mc(q: Dict[str, Any], category: str) -> List[str]:
    lines = [f"$CATEGORY: {_escape_gift_text(category)}", ""]
    title = _escape_gift_text(f"[{q.get('id', 'Q')}] {q.get('lo_ref', '')}")
    lines.append(f"::{title}::[plain]{_escape_gift_text(q['stem'])} {{")
    for key, value in q['options'].items():
        prefix = '=' if key == q['correct'] else '~'
        lines.append(f"  {prefix}{_escape_gift_text(value)}")
    lines.extend(["}", ""])
    return lines


def _build_gift_fill(q: Dict[str, Any], category: str) -> List[str]:
    if q['stem'].count('___') != 1:
        raise ValueError("fill_blank requires exactly one ___ marker")
    prefix, suffix = q['stem'].split('___')
    correct = q['correct']
    answers = correct if isinstance(correct, list) else [correct]
    answer_block = ' '.join('=' + _escape_gift_text(a) for a in answers)
    title = _escape_gift_text(f"[{q.get('id', 'Q')}] {q.get('lo_ref', '')}")
    return [f"$CATEGORY: {_escape_gift_text(category)}", "",
            f"::{title}::[plain]{_escape_gift_text(prefix)}{{{answer_block}}}{_escape_gift_text(suffix)}", ""]


def export_to_moodle_gift(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle GIFT format."""
    _require_valid(quiz)
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
    """Write QTI 1.2 items, responses and scoring; .zip includes a manifest.

    Native LMS import is a separate acceptance step. A .xml output contains
    assessment XML only and is useful for inspection, not a packaged upload.
    """
    _require_valid(quiz)
    ns = 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2'
    ET.register_namespace('', ns)
    def sub(parent, tag, attrs=None, text=None):
        child = ET.SubElement(parent, '{' + ns + '}' + tag, attrs or {})
        child.text = text
        return child
    def material(parent, text):
        sub(sub(parent, 'material'), 'mattext', {'texttype': 'text/plain'}, text)
    root = ET.Element('{' + ns + '}questestinterop')
    assessment = sub(root, 'assessment', {'ident': 'compnet_week0', 'title': quiz['metadata']['topic']})
    section = sub(assessment, 'section', {'ident': 'main'})
    for i, q in enumerate(quiz['questions'], 1):
        item = sub(section, 'item', {'ident': f'item_{i}', 'title': q['id']})
        metadata = sub(sub(item, 'itemmetadata'), 'qtimetadata')
        for label, value in [('question_type', 'multiple_choice_question' if q['type'] == 'multiple_choice' else 'short_answer_question'), ('points_possible', '1')]:
            field = sub(metadata, 'qtimetadatafield')
            sub(field, 'fieldlabel', text=label)
            sub(field, 'fieldentry', text=value)
        presentation = sub(item, 'presentation')
        if q['type'] == 'multiple_choice':
            material(presentation, q['stem'])
            response = sub(presentation, 'response_lid', {'ident': 'response1', 'rcardinality': 'Single'})
            render = sub(response, 'render_choice', {'shuffle': 'No'})
            option_ids = {key: f'choice_{j}' for j, key in enumerate(q['options'], 1)}
            for key, value in q['options'].items():
                material(sub(render, 'response_label', {'ident': option_ids[key]}), value)
            correct = [option_ids[q['correct']]]
        else:
            prefix, suffix = q['stem'].split('___')
            material(presentation, prefix)
            response = sub(presentation, 'response_str', {'ident': 'response1', 'rcardinality': 'Single'})
            render = sub(response, 'render_fib', {'fibtype': 'String', 'prompt': 'Box', 'rows': '1'})
            sub(render, 'response_label', {'ident': 'blank1'})
            material(presentation, suffix)
            correct = q['correct'] if isinstance(q['correct'], list) else [q['correct']]
        processing = sub(item, 'resprocessing')
        sub(sub(processing, 'outcomes'), 'decvar', {'varname': 'SCORE', 'vartype': 'Decimal', 'defaultval': '0', 'minvalue': '0', 'maxvalue': '100'})
        condition = sub(processing, 'respcondition', {'continue': 'No'})
        conditionvar = sub(condition, 'conditionvar')
        alternatives = sub(conditionvar, 'or') if len(correct) > 1 else conditionvar
        for answer in correct:
            sub(alternatives, 'varequal', {'respident': 'response1', 'case': 'No'}, answer)
        sub(condition, 'setvar', {'varname': 'SCORE', 'action': 'Set'}, '100')
    ET.indent(root)
    assessment_bytes = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    if output_path.suffix.lower() == '.zip':
        cp = 'http://www.imsglobal.org/xsd/imscp_v1p1'
        manifest = ET.Element('{' + cp + '}manifest', {'identifier': 'compnet_week0_package'})
        ET.SubElement(manifest, '{' + cp + '}organizations')
        resources = ET.SubElement(manifest, '{' + cp + '}resources')
        resource = ET.SubElement(resources, '{' + cp + '}resource', {'identifier': 'assessment', 'type': 'imsqti_xmlv1p2', 'href': 'assessment.xml'})
        ET.SubElement(resource, '{' + cp + '}file', {'href': 'assessment.xml'})
        ET.indent(manifest)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as package:
            package.writestr('assessment.xml', assessment_bytes)
            package.writestr('imsmanifest.xml', ET.tostring(manifest, encoding='utf-8', xml_declaration=True))
    else:
        output_path.write_bytes(assessment_bytes)
    print(f"Exported QTI 1.2: {output_path}; verify the imported quiz in your LMS before use.")


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
        ext_map = {'json': '_export.json', 'moodle': '_moodle.gift', 'qti': '_qti.zip'}
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
    
    # All modes reject malformed banks before consuming their contents.
    is_valid, errors = validate_quiz_structure(quiz)
    if not is_valid:
        print("Quiz validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be positive")

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
