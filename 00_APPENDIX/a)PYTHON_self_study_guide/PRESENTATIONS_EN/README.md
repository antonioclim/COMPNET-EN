# HTML Slide Presentations — Python for Networking

Ten self-contained HTML slide decks covering the progression from environment setup to debugging best practices. Each file opens directly in any modern browser; no build step or server is required.

| File | Module | Topic |
|---|---|---|
| [`01_introduction_setup.html`](01_introduction_setup.html) | 01 | Python installation, virtual environments and first script |
| [`02_reading_python_code.html`](02_reading_python_code.html) | 02 | Syntax orientation for C/Java/JS programmers |
| [`03_data_types_networking.html`](03_data_types_networking.html) | 03 | `bytes`, `str`, encoding and network data |
| [`04_socket_programming.html`](04_socket_programming.html) | 04 | TCP/UDP sockets, `bind`, `listen`, `connect` |
| [`05_code_organisation.html`](05_code_organisation.html) | 05 | Modules, packages, `if __name__` guard |
| [`06_cli_interfaces.html`](06_cli_interfaces.html) | 06 | `argparse`, command-line tools for networking |
| [`07_packet_analysis.html`](07_packet_analysis.html) | 07 | Scapy basics and pcap reading |
| [`08_concurrency.html`](08_concurrency.html) | 08 | Threading, `select`, async patterns for servers |
| [`09_http_protocols.html`](09_http_protocols.html) | 09 | HTTP requests, JSON handling, REST interaction |
| [`10_debugging_best_practices.html`](10_debugging_best_practices.html) | 10 | `logging`, `pdb`, common network debugging |

## Usage

Open any file in a browser:

```bash
xdg-open 04_socket_programming.html    # Linux
open 04_socket_programming.html         # macOS
start 04_socket_programming.html        # Windows (PowerShell)
```

## Cross-References

| Related resource | Path | Relationship |
|---|---|---|
| Full networking guide | [`../PYTHON_NETWORKING_GUIDE.md`](../PYTHON_NETWORKING_GUIDE.md) | Textual companion covering the same 10 modules in depth |
| Runnable examples | [`../examples/`](../examples/) | Working code that supplements slides 03, 04 and 08 |
| Cheatsheet | [`../cheatsheets/PYTHON_QUICK.md`](../cheatsheets/PYTHON_QUICK.md) | Quick reference for concepts in slides 04, 06 and 07 |
| Optional HTML lectures | [`../../b)optional_LECTURES/`](../../b%29optional_LECTURES/) | Course-level theory slides (distinct from this Python-specific set) |

**Suggested sequence:** skim the relevant slide deck before the matching guide section, then work through the examples.

## Selective Clone

**Method A — sparse-checkout (Git 2.25+):**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_APPENDIX/a)PYTHON_self_study_guide/PRESENTATIONS_EN"
```

**Method B — browse on GitHub:**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_APPENDIX/a)PYTHON_self_study_guide/PRESENTATIONS_EN
```
