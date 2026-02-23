# 📋 Changelog — Week 0 (Appendix)
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

All notable changes to the Week 0 prerequisite materials.

---

## [1.6.0] — 2026-01-25

### 🔧 Bug Fixes

- **CRITICAL:** Fixed `AicodeDecodeError` → `UnicodeDecodeError` in `01_socket_tcp.py:162`
- Fixed all "modulee" → "module" typos (6 instances across docs)
- Fixed all "administrator" → "administrator" typos (4 instances)
- Fixed all "Aicode" → "Unicode" typos (3 instances)
- Fixed all "Demonstrate" → "Demonstrate" typos (3 instances)
- Fixed all "Aderstanding" → "Understanding" typos in Prerequisites_CHECKS.md
- Fixed "minutess" → "minutes" typos throughout
- Fixed "Administrator" → "Administrator" in PowerShell context

### 📝 AI Decontamination

- Changed "Comprehensive guide" → "Complete guide" in PYTHON_self_study_guide/README.md
- Changed "Comprehensive Error Handling" → "Complete Error Handling" in file titles
- Changed "Comprehensive tests" → "Complete tests" in test file docstrings
- Removed 3 Oxford commas:
  - ROSETTA_STONE.md: "C, JavaScript, Java, and Kotlin" → "C, JavaScript, Java and Kotlin"
  - MISCONCEPTIONS_BY_BACKGROUND.md: Same fix
  - SELF_CHECK_CHECKPOINTS.md: Fixed listing

### 🔄 Code Refactoring

#### formative/run_quiz.py
- Split `display_question()` (95 lines) into:
  - `_format_question_header()` (5 lines)
  - `_display_mc_options()` (3 lines)
  - `_show_answer_mc()` (5 lines)
  - `_show_answer_fill()` (8 lines)
  - `_handle_mc_question()` (12 lines)
  - `_handle_fill_question()` (12 lines)
  - `_check_mc_answer()` (12 lines)
  - `_check_fill_answer()` (15 lines)
- Split `export_to_json()` into:
  - `_build_json_question()` (20 lines)
- Split `export_to_moodle_gift()` into:
  - `_escape_gift_text()` (2 lines)
  - `_build_gift_mc()` (12 lines)
  - `_build_gift_fill()` (10 lines)
- Split `main()` into:
  - `_build_arg_parser()` (45 lines)
  - `_handle_export()` (12 lines)
- Added `validate_quiz_structure()` function for quiz validation

#### PYTHON_self_study_guide/examples/01_socket_tcp.py
- Split `server()` (133 lines) into:
  - `_create_server_socket()` (7 lines)
  - `_handle_client_data()` (22 lines)
  - `_handle_connection()` (14 lines)
  - `_handle_server_error()` (10 lines)
- Split `client()` (90 lines) into:
  - `_send_and_receive()` (16 lines)
  - `_handle_client_error()` (20 lines)

### ✅ New Tests

- Added `formative/tests/test_quiz_exports.py`:
  - `test_validate_valid_quiz()`
  - `test_validate_missing_metadata()`
  - `test_validate_empty_questions()`
  - `test_validate_question_missing_fields()`
  - `test_export_json_creates_file()`
  - `test_export_json_mc_structure()`
  - `test_export_json_fill_blank_structure()`
  - `test_build_json_question_helper()`
  - `test_export_moodle_creates_file()`
  - `test_export_moodle_mc_format()`
  - `test_escape_gift_text()`

### 📚 Documentation Improvements

- Added `requirements.txt` with PyYAML, pytest, ruff dependencies
- Updated all version numbers to 1.6.0
- Added authorial voice anchor in peer_instruction.md (Q5 instructor notes)
- Updated glossary.md with 3 new terms: Backlog, Handshake, Loopback
- Fixed all cross-reference links in documentation

### 🎓 Pedagogical Enhancements

- All 5 Parsons problems verified with 2 distractors each
- LO traceability matrix confirmed complete
- Peer instruction timing standardised

---

## [1.5.0] — 2026-01-24

### Added
- Initial Week 0 complete structure
- Formative quiz system (quiz.yaml + run_quiz.py)
- GitHub Actions CI pipeline
- Makefile with standard targets
- All pedagogical documents (peer_instruction, misconceptions, etc.)

### Documentation
- Prerequisites.md complete setup guide
- PYTHON_NETWORKING_GUIDE.md (2200+ lines)
- 10 HTML presentation slides
- Code tracing and Parsons problems

---

## Version History Summary

| Version | Date | Major Changes |
|---------|------|---------------|
| 1.6.0 | 2026-01-25 | Bug fixes, refactoring, AI decontamination, unit tests |
| 1.5.0 | 2026-01-24 | Initial complete release |

---

*Changelog — Week 0 Prerequisites*
*Computer Networks — ASE Bucharest, CSIE*
