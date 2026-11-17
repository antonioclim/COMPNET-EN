"""Regressions for observed ownership, grading and export failures."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
SELF = ROOT / '00_APPENDIX/a)PYTHON_self_study_guide'


def load(path, name):
    assert path.is_file(), f'Missing canonical source: {path}'
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_retry_transfers_live_socket_ownership():
    module = load(SELF / 'examples/04_error_handling.py', 'compnet_retry')
    with socket.socket() as server:
        server.settimeout(2)
        server.bind(('127.0.0.1', 0))
        server.listen(1)
        client = module.connect_with_retry('127.0.0.1', server.getsockname()[1], timeout=2, max_retries=1)
        assert client is not None
        with client, server.accept()[0] as peer:
            peer.settimeout(2)
            client.sendall(b'alive')
            assert peer.recv(5) == b'alive'


def test_bytes_demo_does_not_destroy_existing_temp_file(tmp_path):
    module = load(SELF / 'examples/02_bytes_vs_str.py', 'compnet_bytes')
    sentinel = tmp_path / 'test_packet.bin'
    sentinel.write_bytes(b'existing user data')
    with patch.object(tempfile, 'tempdir', str(tmp_path)), contextlib.redirect_stdout(io.StringIO()):
        module.binary_file_example()
    assert sentinel.read_bytes() == b'existing user data'
    assert list(tmp_path.iterdir()) == [sentinel]


def test_declared_exports_exist():
    for filename in ('01_socket_tcp.py', '02_bytes_vs_str.py', '03_struct_parsing.py'):
        module = load(SELF / 'examples' / filename, 'compnet_exports_' + filename[:2])
        assert all(hasattr(module, name) for name in module.__all__)


def self_quiz():
    return load(SELF / 'formative/run_quiz.py', 'compnet_self_quiz')


@pytest.mark.parametrize('expected,wrong', [('range', 'r'), ('decode', 'd'), ('f', 'definitely_wrong_f')])
def test_fill_answers_are_whole_values(expected, wrong):
    module = self_quiz()
    q = {'type': 'fill_blank', 'correct': [expected]}
    assert not module.check_answer(q, wrong)
    assert module.check_answer(q, ' ' + expected.upper() + ' ')


@pytest.mark.parametrize('expected,answer', [(True, 't'), (False, 'f'), ('true', 'true'), ('false', 'f')])
def test_boolean_normalisation(expected, answer):
    assert self_quiz().check_answer({'type': 'true_false', 'correct': expected}, answer)


def test_interrupted_session_distinguishes_unattempted():
    module = self_quiz()
    q = [{'id': f'q{i}', 'type': 'multiple_choice', 'stem': 'Choose A', 'options': {'a': 'A', 'b': 'B'}, 'correct': 'a'} for i in range(3)]
    with patch('builtins.input', side_effect=['a', '', 'quit']), contextlib.redirect_stdout(io.StringIO()):
        result = module.run_quiz(q)
    assert (result['correct'], result['attempted'], result['unattempted']) == (1, 1, 2)
    assert result['session_status'] == 'incomplete' and result['passed'] is False


def test_weighted_score_and_threshold_are_used():
    module = self_quiz()
    q = [{'id': 'hard', 'difficulty': 'advanced', 'type': 'multiple_choice', 'stem': 'A', 'options': {'a': 'A'}, 'correct': 'a'},
         {'id': 'easy', 'difficulty': 'basic', 'type': 'multiple_choice', 'stem': 'A', 'options': {'a': 'A', 'b': 'B'}, 'correct': 'a'}]
    with patch('builtins.input', side_effect=['a', '', 'b']), contextlib.redirect_stdout(io.StringIO()):
        result = module.run_quiz(q, scoring={'advanced': {'weight': 2}, 'basic': {'weight': 1}}, passing_score=70)
    assert result['earned_points'] == 2 and result['planned_points'] == 3
    assert result['percentage'] == pytest.approx(200 / 3)
    assert result['passed'] is False


def week0():
    return load(ROOT / '00_APPENDIX/formative/run_quiz.py', 'compnet_week0_quiz')


def bank():
    return yaml.safe_load((ROOT / '00_APPENDIX/formative/quiz.yaml').read_text(encoding='utf-8'))


def test_semantic_validation_rejects_empty_duplicate_and_invalid_answers():
    module = week0()
    for bad in (None, [], {}, {'metadata': [], 'questions': []}):
        assert module.validate_quiz_structure(bad)[0] is False
    q = bank()
    q['questions'].append(copy.deepcopy(q['questions'][0]))
    assert not module.validate_quiz_structure(q)[0]
    q = bank(); q['metadata']['passing_score'] = 200
    assert not module.validate_quiz_structure(q)[0]
    q = bank(); q['questions'][0]['correct'] = 'missing-option'
    assert not module.validate_quiz_structure(q)[0]
    for points in (0, -1, float('nan'), float('inf'), True):
        q = bank(); q['questions'][0]['points'] = points
        assert not module.validate_quiz_structure(q)[0]


def test_gift_fill_suffix_remains_outside_answer_block():
    module = week0()
    q = {'id': 'fill', 'type': 'fill_blank', 'stem': "data.___('utf-8')", 'correct': ['decode']}
    exported = '\n'.join(module._build_gift_fill(q, 'week0'))
    assert "data.{=decode}('utf-8')" in exported
    assert module._escape_gift_text('~=#{}:') == r'\~\=\#\{\}\:'


def test_qti_package_has_choices_responses_and_scoring(tmp_path):
    module = week0(); q = bank()
    q['questions'][0]['stem'] = 'A & B < C "quoted"'
    target = tmp_path / 'quiz.zip'
    module.export_to_qti(q, target)
    with zipfile.ZipFile(target) as package:
        assert package.testzip() is None
        manifest = ET.fromstring(package.read('imsmanifest.xml'))
        xml = ET.fromstring(package.read('assessment.xml'))
        assert manifest.find('.//{*}resource').attrib['href'] == 'assessment.xml'
    items = xml.findall('.//{*}item')
    assert len(items) == len(q['questions'])
    assert 'A & B < C "quoted"' in [x.text for x in xml.findall('.//{*}mattext')]
    for item, question in zip(items, q['questions']):
        assert item.find('.//{*}resprocessing') is not None
        assert item.find('.//{*}setvar').text == '100'
        if question['type'] == 'multiple_choice':
            choices = item.findall('.//{*}response_label')
            assert len(choices) == len(question['options'])
            correct = item.find('.//{*}varequal').text
            labels = {x.attrib['ident']: x.find('.//{*}mattext').text for x in choices}
            assert labels[correct] == question['options'][question['correct']]
        else:
            assert item.find('.//{*}response_str') is not None


def test_parsons_canonical_solutions_compile_with_declared_context():
    import json
    data = json.loads((ROOT / '00_APPENDIX/formative/parsons_problems.json').read_text())
    for problem in data['problems']:
        blocks = {b['id']: b['code'] for b in problem['blocks']}
        code = problem.get('context_before', '')
        code += '\n'.join(' ' * problem.get('base_indent', 0) + blocks[ident] for ident in problem['correct_order'])
        compile(code, problem['id'], 'exec')


def test_week0_skipping_does_not_inflate_score():
    module = week0(); questions = bank()
    with patch('builtins.input', return_value=''), patch.object(module, 'display_question', side_effect=[True] + [None] * 9), contextlib.redirect_stdout(io.StringIO()):
        result = module.run_quiz(questions)
    assert result['score'] == 10 and result['passed'] is False
    assert (result['answered'], result['skipped'], result['unattempted']) == (1, 9, 0)


def test_week0_interrupted_session_has_no_verdict():
    module = week0()
    with patch('builtins.input', return_value=''), patch.object(module, 'display_question', side_effect=[True, EOFError]), contextlib.redirect_stdout(io.StringIO()) as output:
        result = module.run_quiz(bank())
    assert result['session_status'] == 'incomplete' and result['passed'] is False
    assert result['unattempted'] == 9 and 'no pass/readiness verdict' in output.getvalue()


def test_week0_json_question_mirror_matches_canonical_yaml():
    module = week0()
    mirror = {q['id']: q for q in json.loads((ROOT / '00_APPENDIX/formative/quiz.json').read_text())['questions']}
    source = bank()['questions']
    assert set(mirror) == {q['id'] for q in source}
    for question in source:
        for key, value in module._build_json_question(question).items():
            assert mirror[question['id']][key] == value, (question['id'], key)


def test_ping_parser_and_bounded_subprocess_contract():
    import subprocess
    module = load(SELF / 'examples/05_ping_latency.py', 'compnet_ping')
    assert module.parse_ping_rtt('64 bytes from ::1: time=0.125 ms') == 0.125
    assert module.parse_ping_rtt('time<1 ms') == 1.0  # a displayed upper bound
    assert module.parse_ping_rtt('Destination Host Unreachable') is None
    with patch.object(module.shutil, 'which', return_value='/usr/bin/ping'), patch.object(module.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'time=0.125 ms', '')) as process:
        result = module.run_ping('::1', 2, 0.5)
    assert len(result) == 2 and all(r.succeeded for r in result)
    assert process.call_args.args[0][-1] == '::1'
    assert process.call_args.kwargs.get('shell', False) is False
    with pytest.raises(ValueError):
        module.run_ping('127.0.0.1; touch unwanted')


def test_parsons_interruption_and_skip_scoring():
    module = load(SELF / 'formative/parsons_runner.py', 'compnet_parsons')
    questions = [{'id': 'first'}, {'id': 'second'}]
    with patch.object(module, 'display_problem', return_value=[]), patch.object(module, 'get_answer', side_effect=EOFError), contextlib.redirect_stdout(io.StringIO()):
        result = module.run_problems(questions)
    assert result['attempted'] == 0 and result['unattempted'] == 2
    assert result['session_status'] == 'incomplete'
    with contextlib.redirect_stdout(io.StringIO()) as output:
        module.display_results({'total': 10, 'correct': 1, 'attempted': 1,
                                'skipped': 9, 'unattempted': 0, 'session_status': 'complete'})
    assert '1/10 (10%)' in output.getvalue()
    assert 'Excellent!' not in output.getvalue()
