#!/usr/bin/env python3
"""Line coding demo (NRZ, NRZI and Manchester).

This script prints a simple text representation of three line coding schemes.
It is designed for teaching and quick experimentation.
"""

import sys


def nrz(bits: str) -> str:
    # 1 -> high, 0 -> low
    return "".join("‾" if b == "1" else "_" for b in bits)


def nrzi(bits: str, start_high: bool = False) -> str:
    # 1 -> transition, 0 -> no transition
    level = start_high
    out = []
    for b in bits:
        if b == "1":
            level = not level
        out.append("‾" if level else "_")
    return "".join(out)


def manchester(bits: str) -> str:
    # A common convention: 1 = low→high, 0 = high→low (mid-bit transition)
    out = []
    for b in bits:
        if b == "1":
            out.append("_‾")
        else:
            out.append("‾_")
    return "".join(out)


def validate(bits: str) -> None:
    if not bits or any(ch not in "01" for ch in bits):
        raise ValueError("Bits must be a non-empty string containing only 0 and 1.")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <bits>  (example: {sys.argv[0]} 10110010)")
        return 2

    bits = sys.argv[1].strip()
    try:
        validate(bits)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return 2

    print(f"Bits:         {bits}")
    print(f"NRZ:          {nrz(bits)}")
    print(f"NRZI:         {nrzi(bits)}")
    print(f"Manchester:   {manchester(bits)}")
    print()
    print("Legend: '_' = low level, '‾' = high level (conceptual)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
