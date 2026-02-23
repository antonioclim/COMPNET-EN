#!/usr/bin/env python3
"""
Parsons Problems Runner for Python Networking Self-Study.

Parsons problems are code-ordering exercises where students arrange
shuffled code blocks into the correct sequence. This helps develop
understanding of program structure without requiring typing.

Usage:
    python parsons_runner.py                      # Run all problems
    python parsons_runner.py --file parsons_socket.yaml  # Specific file
    python parsons_runner.py --random             # Random order
    python parsons_runner.py --limit 3            # Limit problems

Course: Computer Networks — ASE Bucharest, CSIE
Version: 5.0 — January 2026
"""

import yaml
import random
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# ANSI COLOURS
# ═══════════════════════════════════════════════════════════════════════════════

class Colours:
    """ANSI colour codes for terminal output."""
    
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
        """Disable colours for non-TTY environments."""
        cls.HEADER = cls.BLUE = cls.CYAN = cls.GREEN = ''
        cls.YELLOW = cls.RED = cls.BOLD = cls.DIM = cls.RESET = ''


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_problems(file_path: Path) -> Dict[str, Any]:
    """
    Load Parsons problems from a YAML file.
    
    Args:
        file_path: Path to the YAML file containing problems.
        
    Returns:
        Dictionary with metadata and problems list.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file is not valid YAML.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def find_problem_files(directory: Path) -> List[Path]:
    """
    Find all Parsons problem YAML files in a directory.
    
    Args:
        directory: Directory to search.
        
    Returns:
        List of paths to YAML files starting with 'parsons_'.
    """
    return sorted(directory.glob('parsons_*.yaml'))


# ═══════════════════════════════════════════════════════════════════════════════
# PROBLEM DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def display_problem(problem: Dict[str, Any], index: int, total: int) -> List[Dict]:
    """
    Display a Parsons problem and return shuffled blocks.
    
    Args:
        problem: Problem dictionary from YAML.
        index: Current problem number (1-indexed).
        total: Total number of problems.
        
    Returns:
        List of shuffled blocks (including distractors).
    """
    c = Colours
    
    print(f"\n{c.BOLD}{c.BLUE}{'═' * 70}{c.RESET}")
    print(f"{c.BOLD}Problem {index}/{total}: {problem['title']}{c.RESET}")
    print(f"{c.DIM}Difficulty: {problem.get('difficulty', 'unknown')}{c.RESET}")
    print(f"{c.BLUE}{'─' * 70}{c.RESET}\n")
    
    print(f"{c.CYAN}{problem['instructions']}{c.RESET}\n")
    
    # Combine blocks and distractors, then shuffle
    all_blocks = problem['blocks'].copy()
    distractors = problem.get('distractors', [])
    all_blocks.extend(distractors)
    random.shuffle(all_blocks)
    
    # Display shuffled blocks with letters
    print(f"{c.BOLD}Available code blocks:{c.RESET}\n")
    for i, block in enumerate(all_blocks):
        letter = chr(ord('A') + i)
        indent_marker = '→' * block.get('indent', 0)
        if indent_marker:
            indent_marker = f" {c.DIM}{indent_marker}{c.RESET}"
        print(f"  {c.YELLOW}{letter}){c.RESET} {block['code']}{indent_marker}")
    
    print()
    return all_blocks


def get_answer(num_blocks: int) -> Tuple[List[str], bool]:
    """
    Get the user's answer as a sequence of letters.
    
    Args:
        num_blocks: Number of available blocks.
        
    Returns:
        Tuple of (list of letters, whether user wants to quit).
    """
    c = Colours
    max_letter = chr(ord('A') + num_blocks - 1)
    
    print(f"{c.DIM}Enter the correct order as letters (e.g., A C B D){c.RESET}")
    print(f"{c.DIM}Type 'skip' to skip, 'quit' to exit{c.RESET}")
    
    while True:
        answer = input(f"\n{c.YELLOW}Your answer: {c.RESET}").strip().upper()
        
        if answer.lower() == 'quit':
            return [], True
        
        if answer.lower() == 'skip':
            return ['SKIP'], False
        
        # Parse letters
        letters = [c for c in answer.replace(' ', '').replace(',', '') if c.isalpha()]
        
        # Validate
        valid = all(
            'A' <= letter <= max_letter
            for letter in letters
        )
        
        if valid and letters:
            return letters, False
        
        print(f"{c.RED}Please enter valid letters from A to {max_letter}{c.RESET}")


def check_answer(
    problem: Dict[str, Any],
    shuffled_blocks: List[Dict],
    answer_letters: List[str]
) -> Tuple[bool, List[int]]:
    """
    Check if the user's answer matches the correct order.
    
    Args:
        problem: Problem dictionary.
        shuffled_blocks: List of blocks in shuffled order.
        answer_letters: User's answer as list of letters.
        
    Returns:
        Tuple of (is_correct, user's block IDs).
    """
    # Convert letters to block IDs
    user_ids = []
    for letter in answer_letters:
        idx = ord(letter) - ord('A')
        if 0 <= idx < len(shuffled_blocks):
            user_ids.append(shuffled_blocks[idx]['id'])
    
    correct_ids = problem['correct_order']
    return user_ids == correct_ids, user_ids


def display_feedback(
    problem: Dict[str, Any],
    shuffled_blocks: List[Dict],
    is_correct: bool,
    user_ids: List[int],
    skipped: bool = False
) -> None:
    """
    Display feedback after an answer.
    
    Args:
        problem: Problem dictionary.
        shuffled_blocks: List of blocks in shuffled order.
        is_correct: Whether the answer was correct.
        user_ids: User's answer as block IDs.
        skipped: Whether the problem was skipped.
    """
    c = Colours
    
    if skipped:
        print(f"\n{c.YELLOW}⏭  Skipped{c.RESET}")
    elif is_correct:
        print(f"\n{c.GREEN}✓ Correct!{c.RESET}")
    else:
        print(f"\n{c.RED}✗ Not quite right{c.RESET}")
        
        # Show what they got wrong
        correct_ids = problem['correct_order']
        print(f"\n{c.DIM}Your order:    {user_ids}{c.RESET}")
        print(f"{c.DIM}Correct order: {correct_ids}{c.RESET}")
        
        # Check for distractors
        distractor_ids = {d['id'] for d in problem.get('distractors', [])}
        used_distractors = [uid for uid in user_ids if uid in distractor_ids]
        if used_distractors:
            print(f"\n{c.YELLOW}⚠ You included distractor blocks: {used_distractors}{c.RESET}")
            for d in problem.get('distractors', []):
                if d['id'] in used_distractors:
                    print(f"  {c.DIM}• {d['code']} — {d.get('hint', 'This should not be included')}{c.RESET}")
    
    # Show correct solution
    print(f"\n{c.BOLD}Correct solution:{c.RESET}")
    id_to_block = {b['id']: b for b in problem['blocks']}
    for block_id in problem['correct_order']:
        block = id_to_block.get(block_id, {'code': '???', 'indent': 0})
        indent = '    ' * block.get('indent', 0)
        print(f"  {c.CYAN}{indent}{block['code']}{c.RESET}")
    
    # Show explanation
    if 'explanation' in problem:
        print(f"\n{c.BOLD}Explanation:{c.RESET}")
        for line in problem['explanation'].strip().split('\n'):
            print(f"  {c.DIM}{line}{c.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_problems(
    problems: List[Dict[str, Any]],
    randomise: bool = False,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Run a set of Parsons problems interactively.
    
    Args:
        problems: List of problem dictionaries.
        randomise: Whether to randomise problem order.
        limit: Maximum number of problems to run.
        
    Returns:
        Results dictionary with scores and details.
    """
    c = Colours
    
    if randomise:
        problems = random.sample(problems, min(len(problems), limit or len(problems)))
    elif limit:
        problems = problems[:limit]
    
    results = {
        'total': len(problems),
        'correct': 0,
        'skipped': 0,
        'answers': []
    }
    
    print(f"\n{c.BOLD}{c.HEADER}{'═' * 70}{c.RESET}")
    print(f"{c.BOLD}{c.HEADER}  🧩 Parsons Problems — {len(problems)} Exercises{c.RESET}")
    print(f"{c.BOLD}{c.HEADER}{'═' * 70}{c.RESET}")
    print(f"\n{c.DIM}Arrange the code blocks in the correct order.{c.RESET}")
    print(f"{c.DIM}Some blocks may be distractors (incorrect code).{c.RESET}")
    
    try:
        for i, problem in enumerate(problems, 1):
            shuffled = display_problem(problem, i, len(problems))
            answer_letters, quit_requested = get_answer(len(shuffled))
            
            if quit_requested:
                print(f"\n{c.YELLOW}Exiting early.{c.RESET}")
                break
            
            skipped = answer_letters == ['SKIP']
            
            if skipped:
                results['skipped'] += 1
                display_feedback(problem, shuffled, False, [], skipped=True)
            else:
                is_correct, user_ids = check_answer(problem, shuffled, answer_letters)
                if is_correct:
                    results['correct'] += 1
                display_feedback(problem, shuffled, is_correct, user_ids)
            
            results['answers'].append({
                'problem_id': problem['id'],
                'correct': not skipped and is_correct if not skipped else False,
                'skipped': skipped
            })
            
            if i < len(problems):
                input(f"\n{c.DIM}Press Enter for next problem...{c.RESET}")
    
    except KeyboardInterrupt:
        print(f"\n\n{c.YELLOW}Interrupted.{c.RESET}")
    
    return results


def display_results(results: Dict[str, Any]) -> None:
    """Display final results summary."""
    c = Colours
    
    answered = results['total'] - results['skipped']
    if answered > 0:
        percentage = (results['correct'] / answered) * 100
    else:
        percentage = 0
    
    print(f"\n{c.BOLD}{c.HEADER}{'═' * 70}{c.RESET}")
    print(f"{c.BOLD}{c.HEADER}  📊 Results{c.RESET}")
    print(f"{c.BOLD}{c.HEADER}{'═' * 70}{c.RESET}\n")
    
    if percentage >= 80:
        emoji = '🌟'
        message = "Excellent! You understand the code structure well."
    elif percentage >= 60:
        emoji = '👍'
        message = "Good progress. Review the explanations for missed problems."
    else:
        emoji = '📚'
        message = "Keep practising. Review the correct solutions carefully."
    
    print(f"  {emoji} Score: {c.BOLD}{results['correct']}/{answered} ({percentage:.0f}%){c.RESET}")
    print(f"  {c.DIM}Skipped: {results['skipped']}{c.RESET}")
    print(f"\n  {message}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Main entry point for the Parsons runner."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Parsons Problems Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python parsons_runner.py                    # Run all problems
    python parsons_runner.py --file parsons_socket.yaml
    python parsons_runner.py --random --limit 5
        """
    )
    
    parser.add_argument('--file', '-f', type=Path,
                        help='Specific problem file to run')
    parser.add_argument('--random', '-r', action='store_true',
                        help='Randomise problem order')
    parser.add_argument('--limit', '-n', type=int,
                        help='Limit number of problems')
    parser.add_argument('--no-colour', '--no-color', action='store_true',
                        help='Disable coloured output')
    parser.add_argument('--list', '-l', action='store_true',
                        help='List available problem files')
    
    args = parser.parse_args()
    
    # Setup
    if args.no_colour or not sys.stdout.isatty():
        Colours.disable()
    
    # Find problem files
    script_dir = Path(__file__).parent
    parsons_dir = script_dir / 'parsons'
    
    if not parsons_dir.exists():
        print(f"{Colours.RED}Error: parsons/ directory not found{Colours.RESET}")
        sys.exit(1)
    
    problem_files = find_problem_files(parsons_dir)
    
    if args.list:
        print(f"\n{Colours.BOLD}Available problem files:{Colours.RESET}")
        for pf in problem_files:
            data = load_problems(pf)
            count = len(data.get('problems', []))
            print(f"  • {pf.name} ({count} problems)")
        sys.exit(0)
    
    # Load problems
    all_problems = []
    
    if args.file:
        file_path = parsons_dir / args.file if not args.file.is_absolute() else args.file
        if not file_path.exists():
            print(f"{Colours.RED}Error: File not found: {file_path}{Colours.RESET}")
            sys.exit(1)
        data = load_problems(file_path)
        all_problems = data.get('problems', [])
    else:
        for pf in problem_files:
            data = load_problems(pf)
            all_problems.extend(data.get('problems', []))
    
    if not all_problems:
        print(f"{Colours.YELLOW}No problems found.{Colours.RESET}")
        sys.exit(0)
    
    # Run
    results = run_problems(all_problems, randomise=args.random, limit=args.limit)
    display_results(results)


if __name__ == '__main__':
    main()
