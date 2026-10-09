"""Unfolding: map zero heights to a sequence with mean spacing exactly 1.

The smooth part of the zero-counting function is N_smooth(T) = theta(T)/pi + 1, where
theta is the Riemann-Siegel theta function. This module uses its asymptotic series

    theta(t) = (t/2) ln(t/(2 pi)) - t/2 - pi/8 + 1/(48 t) + 7/(5760 t^3) + 31/(80640 t^5)

(Edwards, *Riemann's Zeta Function*, Sec. 6.5), whose truncation error for t >= 14 is below
1e-9; `tests/test_unfold.py` checks it against mpmath's `siegeltheta`.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def riemann_siegel_theta(t: NDArray[np.float64]) -> NDArray[np.float64]:
    t = np.asarray(t, dtype=np.float64)
    return (
        0.5 * t * np.log(t / (2 * np.pi))
        - 0.5 * t
        - np.pi / 8
        + 1 / (48 * t)
        + 7 / (5760 * t**3)
        + 31 / (80640 * t**5)
    )


def unfold(gamma: NDArray[np.float64]) -> NDArray[np.float64]:
    """x_n = N_smooth(gamma_n); the unfolded spacings x_{n+1} - x_n have mean ~ 1."""
    return riemann_siegel_theta(gamma) / np.pi + 1.0
