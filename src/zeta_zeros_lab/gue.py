"""Exact GUE reference distributions (bulk scaling limit, mean spacing 1).

Gap probability E(s) = P(no eigenvalue in an interval of length s) is the Fredholm
determinant det(I - K_s) of the sine kernel K(x, y) = sin(pi (x-y)) / (pi (x-y)) on L^2(0, s),
evaluated by Gauss-Legendre quadrature (Bornemann, *Markov Process. Related Fields* 16 (2010);
Gaudin 1961, Mehta, *Random Matrices*, Ch. 6). The nearest-neighbour spacing CDF follows from
E'(s) = -(1 - F(s)), i.e. F(s) = 1 + E'(s), and the density is p(s) = E''(s).

This replaces the Wigner surmise (which is only approximate) as the GUE reference; the
surmise is used in tests purely as a loose cross-check.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import trapezoid

GRID_MAX = 5.0
GRID_STEP = 0.001
QUAD_NODES = 48


def gap_probability(s: float, nodes: int = QUAD_NODES) -> float:
    """E(s) = det(I - K_s) for the sine kernel."""
    if s <= 0:
        return 1.0
    t, w = np.polynomial.legendre.leggauss(nodes)
    x = 0.5 * s * (t + 1)
    weights = 0.5 * s * w
    kernel = np.sinc(x[:, None] - x[None, :])
    root = np.sqrt(weights)
    matrix = np.eye(nodes) - root[:, None] * kernel * root[None, :]
    return float(np.linalg.det(matrix))


@lru_cache(maxsize=1)
def _tables() -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    grid = np.arange(0.0, GRID_MAX + GRID_STEP / 2, GRID_STEP, dtype=np.float64)
    gap = np.array([gap_probability(float(s)) for s in grid])
    cdf = 1.0 + np.gradient(gap, GRID_STEP, edge_order=2)
    cdf[0] = 0.0
    pdf = np.gradient(cdf, GRID_STEP, edge_order=2)
    return grid, cdf, pdf


def gue_cdf(s: NDArray[np.float64] | float) -> NDArray[np.float64]:
    grid, cdf, _ = _tables()
    return np.interp(np.asarray(s, dtype=np.float64), grid, cdf, right=1.0)


def gue_pdf(s: NDArray[np.float64] | float) -> NDArray[np.float64]:
    grid, _, pdf = _tables()
    return np.interp(np.asarray(s, dtype=np.float64), grid, pdf, right=0.0)


def gue_spacing_moments() -> tuple[float, float]:
    """(mean, variance) of the exact GUE spacing law, by quadrature of the survival function."""
    grid, cdf, _ = _tables()
    survival = 1.0 - cdf
    mean = float(trapezoid(survival, grid))
    second = float(2.0 * trapezoid(grid * survival, grid))
    return mean, second - mean**2


def poisson_cdf(s: NDArray[np.float64] | float) -> NDArray[np.float64]:
    return 1.0 - np.exp(-np.asarray(s, dtype=np.float64))


def poisson_pdf(s: NDArray[np.float64] | float) -> NDArray[np.float64]:
    return np.exp(-np.asarray(s, dtype=np.float64))


def gue_pair_correlation(r: NDArray[np.float64] | float) -> NDArray[np.float64]:
    """R2(r) = 1 - (sin(pi r) / (pi r))^2 (Dyson; Montgomery's conjecture for the zeta zeros)."""
    return np.asarray(1.0 - np.sinc(np.asarray(r, dtype=np.float64)) ** 2, dtype=np.float64)
