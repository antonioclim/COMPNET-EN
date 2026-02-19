# Scenario: Line coding (NRZ, NRZI and Manchester)

## Goal

This scenario explains why line coding is used at the physical layer and shows, conceptually, how the same bit sequence can be represented as a signal using:

- NRZ (Non-Return-to-Zero)
- NRZI (Non-Return-to-Zero Inverted)
- Manchester encoding

The focus is conceptual rather than hardware-level fidelity.

## Requirements

- Python 3.8+
- No external packages

## Steps

1. Run the demo for a simple bit sequence:

```bash
python3 line_coding_demo.py 10110010
```

2. Try a sequence with long runs of identical bits:

```bash
python3 line_coding_demo.py 1111111100000000
```

3. Observe:

- NRZ can lose synchronisation when there are no transitions
- NRZI introduces transitions for certain patterns
- Manchester guarantees a transition in the middle of each bit

## What to submit (optional)

- A short screenshot of the output for the two sequences above
- 3–5 sentences explaining which encoding provides the most transitions and why that helps synchronisation
