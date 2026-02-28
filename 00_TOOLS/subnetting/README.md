# Subnetting utilities (optional)

## `subnet_quiz_generator.py`

A small CLI tool that generates practice questions for IPv4 subnetting.

It supports:

- **IPv4 basic** questions (network address, broadcast, first/last host, usable hosts, netmask).
- A simple **VLSM** scenario generator (allocate subnets by host requirements).

### Examples

```bash
# 10 IPv4 questions, interactive (shows your answer vs. the key)
python3 00_TOOLS/subnetting/subnet_quiz_generator.py --mode ipv4 --count 10

# Generate a Markdown handout (with answer key at the bottom)
python3 00_TOOLS/subnetting/subnet_quiz_generator.py --mode ipv4 --count 10 --markdown out.md --show-answers

# Generate one VLSM scenario
python3 00_TOOLS/subnetting/subnet_quiz_generator.py --mode vlsm --seed 42 --show-answers
```

### Pedagogical note

This tool is **optional**: it is designed as a rapid feedback mechanism for
students who need extra practice outside the seminar.
