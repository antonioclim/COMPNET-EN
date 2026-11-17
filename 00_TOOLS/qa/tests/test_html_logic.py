"""Execute real inline JS with a limited DOM double, never a native browser."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': 'document', 'attrs': {}, 'text': '', 'children': []}
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'text': '', 'children': []}
        self.stack[-1]['children'].append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]['tag'] == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        for node in self.stack:
            node['text'] += data


def test_inline_slide_and_toc_control_logic(tmp_path):
    node = shutil.which('node')
    assert node, 'Node.js is required for the documented HTML control-logic tests'
    paths = sorted((ROOT / '00_APPENDIX/a)PYTHON_self_study_guide/PRESENTATIONS_EN').glob('*.html'))
    paths.append(ROOT / '01_GUIDE_MININET-SDN/SETUP-GUIDE-COMPNET-EN.html')
    assert len(paths) == 11
    fixtures = []
    for path in paths:
        source = path.read_text(encoding='utf-8')
        parser = Tree(); parser.feed(source)
        scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', source, re.S | re.I)
        fixtures.append({'path': str(path.relative_to(ROOT)), 'dom': parser.root, 'script': '\n'.join(scripts), 'toc': path.name.startswith('SETUP-')})
    fixture = tmp_path / 'html_logic.json'
    fixture.write_text(json.dumps(fixtures), encoding='utf-8')
    result = subprocess.run([node, str(Path(__file__).with_name('html_logic_probe.cjs')), str(fixture)], capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report['decks'] == 10 and report['toc_passed']
    assert report['quiz_items'] == 21 and report['clipboard_buttons'] == 5
