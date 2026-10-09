"""Completeness and correctness checks for a frozen block of zeta zeros.

A block is trusted only if (1) the heights are strictly increasing and indices consecutive,
(2) the counting function agrees with the Riemann-von Mangoldt smooth count to within the
known size of S(T) -- a missed or duplicated zero shifts n - N_smooth(gamma_n) by a whole
integer for every later zero, which this detects -- and (3) for the lowest block the first
five zeros match the classical published values.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from zeta_zeros_lab.unfold import unfold

# Maximum tolerated |n - N_smooth(gamma_n)|. The argument term S(T) = N(T) - N_smooth(T)
# satisfies |S(T)| < 1 for all T below ~1e4 in practice and remains below ~2 well past 1e5;
# a missed zero would add a whole unit on top of that, so 2.5 is a loose, safe screen.
MAX_COUNT_OFFSET = 2.5

KNOWN_FIRST_ZEROS = (
    14.134725141734693790,
    21.022039638771554993,
    25.010857580145688763,
    30.424876125859513210,
    32.935061587739189031,
)


@dataclass(frozen=True)
class ZeroBlock:
    first_index: int
    gamma: NDArray[np.float64]

    @property
    def n(self) -> int:
        return len(self.gamma)

    @property
    def indices(self) -> NDArray[np.int64]:
        return np.arange(self.first_index, self.first_index + self.n)


def load_block(path: Path) -> ZeroBlock:
    with path.open() as f:
        rows = list(csv.DictReader(f))
    indices = [int(r["n"]) for r in rows]
    if indices != list(range(indices[0], indices[0] + len(indices))):
        raise ValueError(f"{path}: zero indices are not consecutive")
    return ZeroBlock(first_index=indices[0], gamma=np.array([float(r["gamma"]) for r in rows]))


def validate_block(block: ZeroBlock) -> float:
    """Raise ValueError if the block fails a check; return the max count offset observed."""
    if not np.all(np.diff(block.gamma) > 0):
        raise ValueError("heights are not strictly increasing")
    offset = block.indices - unfold(block.gamma)
    worst = float(np.max(np.abs(offset)))
    if worst > MAX_COUNT_OFFSET:
        raise ValueError(f"counting-function offset {worst:.3f} exceeds {MAX_COUNT_OFFSET}")
    if block.first_index == 1:
        known = np.array(KNOWN_FIRST_ZEROS)
        if not np.allclose(block.gamma[:5], known, rtol=0, atol=1e-9):
            raise ValueError("first five zeros do not match the published values")
    return worst


def check_sign_alternation(block: ZeroBlock, limit: int | None = None) -> int:
    """Rigorous completeness test via Hardy's Z function (real, with a sign change at each
    simple zero on the critical line).

    Evaluate Z at the midpoint of every gap between consecutive listed zeros. If no zero were
    missed or duplicated, consecutive gap midpoints lie in consecutive sign-intervals of Z and
    their signs strictly alternate. A single missed zero merges two intervals into one gap and
    always breaks the alternation (the merged midpoint repeats the sign of a neighbouring
    gap). Returns the number of gaps checked; raises ValueError on the first violation.
    """
    import mpmath

    mpmath.mp.dps = 18
    gamma = block.gamma if limit is None else block.gamma[: limit + 1]
    previous = 0
    for k in range(len(gamma) - 1):
        mid = 0.5 * (gamma[k] + gamma[k + 1])
        z = mpmath.siegelz(mid)
        sign = 1 if z > 0 else -1
        if previous != 0 and sign == previous:
            raise ValueError(
                f"Z has no sign change between zeros n={block.first_index + k - 1} and "
                f"n={block.first_index + k + 1}: a zero is missing or duplicated"
            )
        previous = sign
    return len(gamma) - 1
