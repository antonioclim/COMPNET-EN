#!/usr/bin/env python3
"""
Interactive Quiz Runner for Python Networking Self-Study.

This module provides a command-line quiz system for self-assessment
of Python networking concepts. It supports multiple question types,
filtering by background and section, and detailed feedback.

Usage:
    python run_quiz.py                    # Full quiz
    python run_quiz.py --quick            # 10 random questions
    python run_quiz.py --background c     # C-programmer specific
    python run_quiz.py --section socket  # Topic filtering

Course: Computer Networks — ASE Bucharest, CSIE
Version: 5.0 — January 2026

Example:
    >>> from run_quiz import load_quiz, filter_questions
    >>> quiz = load_quiz(Path('quiz.yaml'))
    >>> filtered = filter_questions(quiz['questions'], background='c')
    >>> len(filtered) > 0
    True
"""

import yaml
import random
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# ANSI COLOUR CODES
# ═══════════════════════════════════════════════════════════════════════════════

class Colours:
    """
    ANSI escape codes for terminal colouring.
    
    Attributes:
        HEADER: Magenta colour for headers.
        BLUE: Blue colour for emphasis.
        CYAN: Cyan colour for information.
        GREEN: Green colour for success.
        YELLOW: Yellow colour for warnings.
        RED: Red colour for errors.
        BOLD: Bold text modifier.
        DIM: Dimmed text modifier.
        RESET: Reset all formatting.
    
    Example:
        >>> print(f"{Colours.GREEN}Success!{Colours.RESET}")
    """
    
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    @classmethod
    def disable(cls) -> None:
        """
        Disable all colours for non-TTY environments.
        
        Call this when output is not to a terminal (e.g., piped to file).
        """
        cls.HEADER = cls.BLUE = cls.CYAN = cls.GREEN = ''
        cls.YELLOW = cls.RED = cls.BOLD = cls.DIM = cls.RESET = ''


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING AND FILTERING
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(quiz_path: Path) -> Dict[str, Any]:
    """
    Load quiz data from a YAML file.
    
    Args:
        quiz_path: Path to the YAML file containing quiz questions.
        
    Returns:
        Dictionary containing 'metadata' and 'questions' keys.
        
    Raises:
        FileNotFoundError: If quiz_path does not exist.
        yaml.YAMLError: If the file is not valid YAML.
        
    Example:
        >>> quiz = load_quiz(Path('formative/quiz.yaml'))
        >>> 'questions' in quiz
        True
    """
    with open(quiz_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def filter_questions(
    questions: List[Dict[str, Any]],
    section: Optional[str] = None,
    background: Optional[str] = None,
    difficulty: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter questions by section, background or difficulty.
    
    Args:
        questions: List of question dictionaries.
        section: Optional section name (partial match).
        background: Optional target background (c, java, javascript, kotlin).
        difficulty: Optional difficulty level (basic, intermediate, advanced).
        
    Returns:
        Filtered list of questions matching all specified criteria.
        
    Example:
        >>> qs = [{'section': 'sockets', 'target_background': ['c']}]
        >>> len(filter_questions(qs, background='c'))
        1
        >>> len(filter_questions(qs, background='java'))
        0
    """
    filtered = questions
    
    if section:
        filtered = [
            q for q in filtered 
            if section.lower() in q.get('section', '').lower()
        ]
    
    if background:
        filtered = [
            q for q in filtered 
            if _matches_background(q, background)
        ]
    
    if difficulty:
        filtered = [
            q for q in filtered 
            if q.get('difficulty', '').lower() == difficulty.lower()
        ]
    
    return filtered


def _matches_background(question: Dict[str, Any], background: str) -> bool:
    """
    Check if a question matches the specified background.
    
    Args:
        question: Question dictionary with optional 'target_background' key.
        background: Background to match (e.g., 'c', 'java').
        
    Returns:
        True if question targets this background or 'all'.
    """
    targets = question.get('target_background', ['all'])
    targets_lower = [t.lower() for t in targets]
    return background.lower() in targets_lower or 'all' in targets_lower


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def display_question(question: Dict[str, Any], index: int, total: int) -> None:
    """
    Display a formatted question to the terminal.
    
    Args:
        question: Question dictionary with 'stem', 'type' and 'options'.
        index: Current question number (1-indexed).
        total: Total number of questions.
    """
    c = Colours
    
    _display_question_header(question, index, total)
    _display_question_stem(question)
    _display_question_options(question)


def _display_question_header(question: Dict[str, Any], index: int, total: int) -> None:
    """Display the question header with progress and metadata."""
    c = Colours
    section = question.get('section', 'general')
    difficulty = question.get('difficulty', 'basic')
    
    print(f"\n{c.BOLD}{c.BLUE}{'═' * 60}{c.RESET}")
    print(f"{c.BOLD}Question {index}/{total}{c.RESET}", end='')
    print(f"  {c.DIM}[{section} • {difficulty}]{c.RESET}")
    print(f"{c.BLUE}{'─' * 60}{c.RESET}\n")


def _display_question_stem(question: Dict[str, Any]) -> None:
    """Display the question stem (the actual question text)."""
    c = Colours
    print(f"{c.BOLD}{question['stem']}{c.RESET}\n")


def _display_question_options(question: Dict[str, Any]) -> None:
    """Display answer options based on question type."""
    c = Colours
    q_type = question.get('type', 'multiple_choice')
    
    if q_type == 'multiple_choice':
        for key, value in sorted(question.get('options', {}).items()):
            print(f"  {c.CYAN}{key}){c.RESET} {value}")
    elif q_type == 'true_false':
        print(f"  {c.CYAN}t){c.RESET} True")
        print(f"  {c.CYAN}f){c.RESET} False")
    elif q_type == 'fill_blank':
        print(f"  {c.DIM}(Type your answer){c.RESET}")
    
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# ANSWER HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

def get_answer(question: Dict[str, Any]) -> str:
    """
    Get and validate user answer for a question.
    
    Args:
        question: Question dictionary with type and options.
        
    Returns:
        Validated answer string, or 'skip'/'quit' for special commands.
    """
    c = Colours
    
    while True:
        prompt = f"{c.YELLOW}Your answer (or 'h' for hint, 's' to skip): {c.RESET}"
        answer = input(prompt).strip().lower()
        
        if answer == 'h':
            _show_hint(question)
            continue
        
        if answer in ('s', 'skip'):
            return 'skip'
        
        if answer in ('q', 'quit'):
            return 'quit'
        
        validated = _validate_answer(question, answer)
        if validated is not None:
            return validated
        
        _show_validation_error(question)


def _show_hint(question: Dict[str, Any]) -> None:
    """Display hint if available."""
    c = Colours
    hint = question.get('hint')
    if hint:
        print(f"\n{c.DIM}💡 Hint: {hint}{c.RESET}\n")
    else:
        print(f"\n{c.DIM}No hint available for this question.{c.RESET}\n")


def _validate_answer(question: Dict[str, Any], answer: str) -> Optional[str]:
    """
    Validate an answer against the question type.
    
    Returns:
        Normalised answer if valid, None if invalid.
    """
    q_type = question.get('type', 'multiple_choice')
    
    if q_type == 'multiple_choice':
        if answer in question.get('options', {}).keys():
            return answer
        return None
    
    if q_type == 'true_false':
        if answer in ('t', 'f', 'true', 'false'):
            return 't' if answer in ('t', 'true') else 'f'
        return None
    
    if q_type == 'fill_blank':
        return answer if answer else None
    
    return answer


def _show_validation_error(question: Dict[str, Any]) -> None:
    """Display error message for invalid answer."""
    c = Colours
    q_type = question.get('type', 'multiple_choice')
    
    if q_type == 'multiple_choice':
        options = ', '.join(question.get('options', {}).keys())
        print(f"{c.RED}Please enter one of: {options}{c.RESET}")
    elif q_type == 'true_false':
        print(f"{c.RED}Please enter 't' for True or 'f' for False{c.RESET}")
    else:
        print(f"{c.RED}Please enter an answer{c.RESET}")


def check_answer(question: Dict[str, Any], answer: str) -> bool:
    """
    Check if an answer is correct.
    
    Args:
        question: Question dictionary with 'correct' key.
        answer: User's answer (already validated).
        
    Returns:
        True if answer matches the correct answer.
    """
    normalise = lambda value: str(value).strip().casefold()
    kind = question.get('type')
    if kind == 'true_false':
        values = {'t': True, 'true': True, 'f': False, 'false': False}
        expected = question['correct']
        expected = expected if isinstance(expected, bool) else values.get(normalise(expected))
        supplied = values.get(normalise(answer))
        return expected is not None and supplied is not None and supplied == expected
    acceptable = question['correct']
    acceptable = acceptable if isinstance(acceptable, list) else [acceptable]
    return normalise(answer) in {normalise(value) for value in acceptable}


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def display_feedback(
    question: Dict[str, Any], 
    answer: str, 
    is_correct: bool
) -> None:
    """
    Display feedback after answering a question.
    
    Args:
        question: Question dictionary.
        answer: User's answer.
        is_correct: Whether the answer was correct.
    """
    c = Colours
    
    if answer == 'skip':
        print(f"\n{c.YELLOW}⏭  Skipped{c.RESET}")
        print(f"{c.DIM}Correct answer: {question['correct']}{c.RESET}")
    elif is_correct:
        print(f"\n{c.GREEN}✓ Correct!{c.RESET}")
    else:
        print(f"\n{c.RED}✗ Incorrect{c.RESET}")
        print(f"{c.DIM}Correct answer: {question['correct']}{c.RESET}")
    
    _show_explanation(question)
    _show_misconception_ref(question, is_correct)


def _show_explanation(question: Dict[str, Any]) -> None:
    """Display explanation if available."""
    c = Colours
    explanation = question.get('explanation')
    if explanation:
        print(f"\n{c.CYAN}📖 {explanation}{c.RESET}")


def _show_misconception_ref(question: Dict[str, Any], is_correct: bool) -> None:
    """Display misconception reference if answer was wrong."""
    c = Colours
    ref = question.get('misconception_ref')
    if ref and not is_correct:
        print(f"\n{c.DIM}📚 See: {ref}{c.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def run_quiz(
    questions: List[Dict[str, Any]],
    randomise: bool = False,
    limit: Optional[int] = None,
    scoring: Optional[Dict[str, Any]] = None,
    passing_score: float = 70
) -> Dict[str, Any]:
    """
    Run the interactive quiz and return results.
    
    Args:
        questions: List of question dictionaries.
        randomise: Whether to shuffle questions.
        limit: Maximum number of questions to ask.
        
    Returns:
        Results dictionary with keys: timestamp, total, correct, 
        skipped, by_section, answers.
    """
    questions = _prepare_questions(questions, randomise, limit)
    results = _initialise_results(len(questions))
    results['passing_score'] = passing_score
    weights = scoring or {}
    results['weights'] = {q['id']: float(weights.get(q.get('difficulty', 'basic'), {}).get('weight', 1)) for q in questions}
    results['planned_points'] = sum(results['weights'].values())
    results['earned_points'] = 0.0
    
    _display_quiz_header(len(questions))
    
    try:
        for i, question in enumerate(questions, 1):
            should_continue = _process_question(question, i, len(questions), results)
            if not should_continue:
                break
            
            if i < len(questions):
                input(f"\n{Colours.DIM}Press Enter for next question...{Colours.RESET}")
    
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{Colours.YELLOW}Quiz interrupted.{Colours.RESET}")

    results['attempted'] = len(results['answers']) - results['skipped']
    results['unattempted'] = results['total'] - len(results['answers'])
    results['session_status'] = 'complete' if results['unattempted'] == 0 else 'incomplete'
    results['percentage'] = 100 * results['earned_points'] / results['planned_points'] if results['planned_points'] else 0
    results['passed'] = results['session_status'] == 'complete' and results['percentage'] >= passing_score
    return results


def _prepare_questions(
    questions: List[Dict[str, Any]], 
    randomise: bool, 
    limit: Optional[int]
) -> List[Dict[str, Any]]:
    """Prepare question list with optional shuffle and limit."""
    if randomise:
        count = min(len(questions), limit or len(questions))
        return random.sample(questions, count)
    if limit:
        return questions[:limit]
    return questions


def _initialise_results(total: int) -> Dict[str, Any]:
    """Create initial results dictionary."""
    return {
        'timestamp': datetime.now().isoformat(),
        'total': total,
        'correct': 0,
        'skipped': 0,
        'by_section': {},
        'answers': []
    }


def _display_quiz_header(count: int) -> None:
    """Display the quiz welcome header."""
    c = Colours
    print(f"\n{c.BOLD}{c.HEADER}{'═' * 60}{c.RESET}")
    print(f"{c.BOLD}{c.HEADER}  🐍 Python Networking Quiz — {count} Questions{c.RESET}")
    print(f"{c.BOLD}{c.HEADER}{'═' * 60}{c.RESET}")
    print(f"\n{c.DIM}Commands: 'h'=hint, 's'=skip, 'q'=quit, Ctrl+C=abort{c.RESET}")


def _process_question(
    question: Dict[str, Any], 
    index: int, 
    total: int, 
    results: Dict[str, Any]
) -> bool:
    """
    Process a single question and update results.
    
    Returns:
        False if user wants to quit, True otherwise.
    """
    display_question(question, index, total)
    answer = get_answer(question)
    
    if answer == 'quit':
        print(f"\n{Colours.YELLOW}Quiz ended early.{Colours.RESET}")
        return False
    
    _update_section_stats(question, results)
    
    if answer == 'skip':
        results['skipped'] += 1
        is_correct = False
    else:
        is_correct = check_answer(question, answer)
        if is_correct:
            results['correct'] += 1
            results['earned_points'] += results['weights'][question['id']]
            section = question.get('section', 'general')
            results['by_section'][section]['correct'] += 1
    
    display_feedback(question, answer, is_correct)
    
    results['answers'].append({
        'question_id': question.get('id', f'q{index}'),
        'answer': answer,
        'correct': is_correct
    })
    
    return True


def _update_section_stats(question: Dict[str, Any], results: Dict[str, Any]) -> None:
    """Initialise or update section statistics."""
    section = question.get('section', 'general')
    if section not in results['by_section']:
        results['by_section'][section] = {'correct': 0, 'total': 0}
    results['by_section'][section]['total'] += 1


# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS DISPLAY AND EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def display_results(results: Dict[str, Any]) -> None:
    """
    Display final quiz results with section breakdown.
    
    Args:
        results: Results dictionary from run_quiz().
    """
    c = Colours
    
    answered = results['attempted']
    percentage = results['percentage']
    
    _display_results_header()
    _display_overall_score(results, answered, percentage)
    _display_section_breakdown(results)
    print()


def _display_results_header() -> None:
    """Display results section header."""
    c = Colours
    print(f"\n{c.BOLD}{c.HEADER}{'═' * 60}{c.RESET}")
    print(f"{c.BOLD}{c.HEADER}  📊 Quiz Results{c.RESET}")
    print(f"{c.BOLD}{c.HEADER}{'═' * 60}{c.RESET}\n")


def _display_overall_score(
    results: Dict[str, Any], 
    answered: int, 
    percentage: float
) -> None:
    """Display overall score with colour coding."""
    c = Colours
    
    print(f"  Correct answers: {results['correct']}/{answered} attempted")
    print(f"  Skipped: {results['skipped']}; unattempted: {results['unattempted']}; planned: {results['total']}")
    print(f"  Weighted score: {results['earned_points']:g}/{results['planned_points']:g} ({percentage:.1f}%)")
    print(f"  Passing threshold: {results['passing_score']:g}%")
    if results['session_status'] != 'complete':
        print("  Incomplete session: no readiness/pass verdict. Finish the remaining items.")
    elif results['passed']:
        print("  Threshold reached. Review feedback and verify the practical skills in the labs.")
    else:
        print("  Threshold not reached. Review missed and skipped questions.")


def _display_section_breakdown(results: Dict[str, Any]) -> None:
    """Display score breakdown by section."""
    c = Colours
    
    if not results['by_section']:
        return
    
    print(f"{c.BOLD}By Section:{c.RESET}")
    for section, data in sorted(results['by_section'].items()):
        if data['total'] > 0:
            pct = (data['correct'] / data['total'] * 100)
            bar = '█' * int(pct / 10) + '░' * (10 - int(pct / 10))
            print(f"  {section:25s} {bar} {pct:5.0f}%")


def save_results(results: Dict[str, Any], output_dir: Path) -> Path:
    """
    Save quiz results to a JSON file.
    
    Args:
        results: Results dictionary from run_quiz().
        output_dir: Directory to save results in.
        
    Returns:
        Path to the saved JSON file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    output_path = output_dir / f'quiz_results_{timestamp}.json'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Main entry point for the quiz runner.
    
    Parses command-line arguments and runs the quiz.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Python Networking Quiz Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_quiz.py                    # Full quiz
  python run_quiz.py --quick            # 10 random questions
  python run_quiz.py --background c     # Questions for C programmers
  python run_quiz.py --section socket   # Socket-related questions
  python run_quiz.py --difficulty basic # Beginner questions only
        """
    )
    
    parser.add_argument('--quick', '-q', action='store_true',
                        help='Quick mode: 10 random questions')
    parser.add_argument('--random', '-r', action='store_true',
                        help='Randomise question order')
    parser.add_argument('--limit', '-n', type=int,
                        help='Limit number of questions')
    parser.add_argument('--section', '-s',
                        help='Filter by section (partial match)')
    parser.add_argument('--background', '-b',
                        choices=['c', 'java', 'javascript', 'js', 'kotlin', 'all'],
                        help='Filter for programming background')
    parser.add_argument('--difficulty', '-d',
                        choices=['basic', 'intermediate', 'advanced'],
                        help='Filter by difficulty')
    parser.add_argument('--no-colour', '--no-color', action='store_true',
                        help='Disable coloured output')
    parser.add_argument('--save', action='store_true',
                        help='Save results to JSON file')
    parser.add_argument('--quiz-file', type=Path,
                        default=Path(__file__).parent / 'quiz.yaml',
                        help='Path to quiz YAML file')
    
    args = parser.parse_args()
    
    # Setup colours
    if args.no_colour or not sys.stdout.isatty():
        Colours.disable()
    
    # Normalise background
    if args.limit is not None and args.limit <= 0:
        parser.error('--limit must be positive')
    if args.background == 'all':
        args.background = None
    if args.background == 'js':
        args.background = 'javascript'
    
    # Load quiz
    try:
        quiz_data = load_quiz(args.quiz_file)
    except FileNotFoundError:
        print(f"{Colours.RED}Error: Quiz file not found: {args.quiz_file}{Colours.RESET}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"{Colours.RED}Error parsing quiz file: {e}{Colours.RESET}")
        sys.exit(1)
    
    # Filter questions
    questions = filter_questions(
        quiz_data.get('questions', []),
        section=args.section,
        background=args.background,
        difficulty=args.difficulty
    )
    
    if not questions:
        print(f"{Colours.YELLOW}No questions match the specified filters.{Colours.RESET}")
        sys.exit(1)
    
    # Determine limit
    limit = args.limit
    if args.quick:
        limit = min(10, len(questions))
        args.random = True
    
    # Run quiz
    results = run_quiz(questions, randomise=args.random, limit=limit,
                       scoring=quiz_data.get('scoring'),
                       passing_score=quiz_data.get('metadata', {}).get('passing_score', 70))
    
    # Display and optionally save results
    display_results(results)
    
    if args.save:
        output_dir = Path(__file__).parent / 'results'
        output_path = save_results(results, output_dir)
        print(f"{Colours.DIM}Results saved to: {output_path}{Colours.RESET}\n")


if __name__ == '__main__':
    main()
