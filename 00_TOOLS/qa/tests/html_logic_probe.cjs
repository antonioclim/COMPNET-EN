// Limited DOM/timer/clipboard doubles for actual inline JavaScript.
// This does not test rendering, native keyboard activation or browser accessibility.
'use strict';
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const cases = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

class Element {
  constructor(x, parent = null) {
    this.tag = x.tag; this.attrs = x.attrs; this.parent = parent;
    this.textContent = x.text; this.innerHTML = x.text;
    this.children = x.children.map(c => new Element(c, this));
    this.style = {}; this.disabled = false; this.dataset = {};
    this.hidden = 'hidden' in this.attrs; this.inert = 'inert' in this.attrs;
    for (const [k, v] of Object.entries(this.attrs)) {
      if (k.startsWith('data-')) this.dataset[k.slice(5).replace(/-([a-z])/g, (_, a) => a.toUpperCase())] = v;
    }
    this._classes = new Set((this.attrs.class || '').split(/\s+/).filter(Boolean));
    this.classList = {
      add: (...cs) => cs.forEach(c => this._classes.add(c)),
      remove: (...cs) => cs.forEach(c => this._classes.delete(c)),
      contains: c => this._classes.has(c),
      toggle: (c, b) => { if (b === undefined) b = !this._classes.has(c); b ? this._classes.add(c) : this._classes.delete(c); return b; }
    };
  }
  get className() { return [...this._classes].join(' '); }
  set className(s) { this._classes = new Set(s.split(/\s+/).filter(Boolean)); }
  all() { return [this, ...this.children.flatMap(c => c.all())]; }
  matches(sel) {
    if (sel.includes(',')) return sel.split(',').some(s => this.matches(s.trim()));
    const id = sel.match(/#([\w-]+)/);
    if (id && this.attrs.id !== id[1]) return false;
    const attr = sel.match(/\[([\w-]+)(?:=["']?([^\]"']+)["']?)?\]/);
    if (attr && (!(attr[1] in this.attrs) || (attr[2] !== undefined && this.attrs[attr[1]] !== attr[2]))) return false;
    const tag = sel.match(/^[a-z]+/i);
    if (tag && this.tag !== tag[0]) return false;
    return [...sel.matchAll(/\.([\w-]+)/g)].every(m => this._classes.has(m[1]));
  }
  querySelectorAll(sel) {
    if (sel.includes(',')) return this.children.flatMap(c => c.all()).filter(n => n.matches(sel));
    if (sel.includes(' ')) { const [a, ...r] = sel.split(/\s+/); return this.querySelectorAll(a).flatMap(n => n.querySelectorAll(r.join(' '))); }
    return this.children.flatMap(c => c.all()).filter(n => n.matches(sel));
  }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  closest(sel) { let n = this; while (n) { if (n.matches(sel)) return n; n = n.parent; } return null; }
  appendChild(n) { n.parent = this; n.owner = this.owner; this.children.push(n); }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  getAttribute(k) { return this.attrs[k]; }
  focus() { this.owner.activeElement = this; }
  contains(n) { return this.all().includes(n); }
}

function setup(c) {
  const tree = new Element(c.dom), timers = [], events = {};
  let selected = false;
  const document = {
    body: tree.querySelector('body'), head: tree.querySelector('head'), documentElement: { scrollHeight: 1000 },
    activeElement: null,
    getElementById: id => tree.all().find(n => n.attrs.id === id) || null,
    querySelector: s => tree.querySelector(s), querySelectorAll: s => tree.querySelectorAll(s),
    createElement: tag => { const n = new Element({ tag, attrs: {}, text: '', children: [] }); n.owner = document; return n; },
    addEventListener: (k, f) => { events[k] = f; },
    createRange: () => ({ selectNodeContents() { selected = true; } })
  };
  tree.all().forEach(n => { n.owner = document; });
  const window = { scrollY: 0, innerHeight: 500, addEventListener() {}, getSelection: () => ({ removeAllRanges() {}, addRange() {} }) };
  const navigator = { clipboard: { writeText: () => Promise.resolve() } };
  const context = vm.createContext({ document, window, navigator, console,
    setTimeout: f => { timers.push(f); return timers.length; },
    IntersectionObserver: class { observe() {} }
  });
  vm.runInContext(c.script, context, { timeout: 1000 });
  events.DOMContentLoaded?.();
  return { tree, context, document, navigator, events, selected: () => selected,
    run: s => vm.runInContext(s, context, { timeout: 1000 }),
    flush: () => { while (timers.length) timers.shift()(); }
  };
}

(async () => {
  const report = { method: 'Actual inline JavaScript with limited DOM/timer/clipboard doubles; no native browser', decks: 0, quiz_items: 0, clipboard_buttons: 0, toc_passed: false };
  for (const c of cases) {
    const t = setup(c);
    if (c.toc) {
      const panel = t.document.getElementById('tocPanel'), trigger = t.document.getElementById('tocTrigger');
      assert(panel.hidden && panel.inert, c.path);
      t.run('setToc(true)'); assert(!panel.hidden && !panel.inert);
      assert.equal(trigger.getAttribute('aria-expanded'), 'true');
      assert.equal(t.document.activeElement, panel.querySelector('button'));
      const controls = panel.querySelectorAll('a,button');
      let trapped = false;
      controls[0].focus();
      t.events.keydown({ key: 'Tab', shiftKey: true, preventDefault() { trapped = true; } });
      assert(trapped); assert.equal(t.document.activeElement, controls.at(-1));
      trapped = false;
      t.events.keydown({ key: 'Tab', shiftKey: false, preventDefault() { trapped = true; } });
      assert(trapped); assert.equal(t.document.activeElement, controls[0]);
      t.events.keydown({ key: 'Escape' });
      assert(panel.hidden && panel.inert); assert.equal(t.document.activeElement, trigger);
      report.toc_passed = true; continue;
    }
    const slides = t.document.querySelectorAll('.slide');
    assert.equal(t.run('totalSlides'), slides.length, c.path);
    for (let i = 1; i <= slides.length; i++) {
      t.run(`goToSlide(${i})`);
      assert.equal(slides.filter(s => s.classList.contains('active')).length, 1, c.path);
      assert.equal(slides.filter(s => !s.inert).length, 1, c.path);
    }
    t.run('goToSlide(2); goToSlide(3)'); t.flush();
    assert.deepEqual(slides.filter(s => s.classList.contains('active')).map(s => s.dataset.slide), ['3'], c.path);
    const options = t.document.querySelectorAll('.quiz-option');
    const groups = new Map();
    for (const option of options) {
      assert.equal(option.tag, 'button', c.path);
      let p = option.parent; while (p && !p.attrs.id) p = p.parent;
      if (!groups.has(p.attrs.id)) groups.set(p.attrs.id, p.querySelectorAll('.quiz-option'));
    }
    for (const [id, opts] of groups) {
      const correct = opts.filter(o => o.dataset.correct === 'true'); assert.equal(correct.length, 1, `${c.path} ${id}`);
      t.context.choice = correct[0]; t.run(`selectOption(choice, ${JSON.stringify(id)});checkAnswer(${JSON.stringify(id)})`);
      assert(t.document.getElementById(id + '-feedback').classList.contains('success'));
      const wrong = opts.find(o => o !== correct[0]); t.context.choice = wrong;
      t.run(`selectOption(choice, ${JSON.stringify(id)});checkAnswer(${JSON.stringify(id)})`);
      assert(t.document.getElementById(id + '-feedback').classList.contains('error'));
      assert.equal(opts.filter(o => o.getAttribute('aria-pressed') === 'true').length, 1, c.path);
      assert.equal(wrong.getAttribute('aria-pressed'), 'true');
      const before = t.run('currentSlide');
      t.events.keydown({ key: ' ', target: wrong, preventDefault() { throw new Error('global handler intercepted native button'); } });
      assert.equal(t.run('currentSlide'), before);
      report.quiz_items++;
    }
    const buttons = t.tree.all().filter(n => (n.attrs.onclick || '').startsWith('copyCode('));
    for (const button of buttons) {
      t.context.copyButton = button; let resolve;
      t.navigator.clipboard.writeText = () => new Promise(r => { resolve = r; });
      const original = button.textContent;
      const pending = t.run('copyCode(copyButton)');
      assert.equal(button.textContent, original, c.path);
      resolve(); await pending; assert.equal(button.textContent, 'Copied!'); t.flush();
      t.navigator.clipboard.writeText = () => Promise.reject(new Error('clipboard denied'));
      await t.run('copyCode(copyButton)');
      assert.equal(button.textContent, 'Selected: copy manually'); assert(t.selected());
      report.clipboard_buttons++;
    }
    report.decks++;
  }
  process.stdout.write(JSON.stringify(report));
})().catch(error => { console.error(error); process.exitCode = 1; });
