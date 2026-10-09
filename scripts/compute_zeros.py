#!/usr/bin/env python3
"""Compute consecutive nontrivial zeta zeros (imaginary parts) with mpmath and freeze them.

Usage: compute_zeros.py START COUNT OUTPUT.csv
The zeros are computed independently by mpmath.zetazero(n); the analysis never trusts a
block until `zeta_zeros_lab.validation` confirms it is complete (no missed/duplicated zero).
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath

mpmath.mp.dps = 18


def main() -> None:
    start, count, out = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="\n") as f:
        f.write("n,gamma\n")
        for n in range(start, start + count):
            gamma = mpmath.zetazero(n).imag
            f.write(f"{n},{mpmath.nstr(gamma, 17)}\n")
            if n % 100 == 0:
                f.flush()
    print(f"wrote {count} zeros to {out}")


if __name__ == "__main__":
    main()
