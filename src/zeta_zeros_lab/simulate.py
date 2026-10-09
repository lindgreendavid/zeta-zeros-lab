"""Seeded GUE matrix ensemble: the calibrated null for every statistic.

A single zeta sample is one realization, so its distance from the GUE law means little
without knowing how large that distance typically is for a *genuine* GUE sample of the same
size. This module draws that reference distribution from random GUE matrices.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from zeta_zeros_lab.stats import SampleStats, pair_counts, spacings, summarize

MATRIX_SIZE = 800
CENTRAL_FRACTION = 0.5  # keep eigenvalues with |lambda| < 0.5 * (edge)


def gue_matrix_eigenvalues(rng: np.random.Generator, n: int = MATRIX_SIZE) -> NDArray[np.float64]:
    g = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) / np.sqrt(2)
    h = (g + g.conj().T) / np.sqrt(2)  # E|H_ij|^2 = 1 -> semicircle on [-2 sqrt(n), 2 sqrt(n)]
    return np.linalg.eigvalsh(h)


def unfold_semicircle(eigs: NDArray[np.float64], n: int = MATRIX_SIZE) -> NDArray[np.float64]:
    """Map the central part of the spectrum through the semicircle counting function."""
    u = eigs / (2 * np.sqrt(n))
    keep = np.abs(u) < CENTRAL_FRACTION
    u = u[keep]
    return n * (0.5 + (u * np.sqrt(1 - u**2) + np.arcsin(u)) / np.pi)


@dataclass(frozen=True)
class EnsembleSummary:
    n_replicates: int
    seed: int
    stats: list[SampleStats]


def simulate_ensemble(n_spacings: int, n_replicates: int, seed: int) -> EnsembleSummary:
    """Each replicate pools unfolded central spectra of several independent GUE matrices until
    `n_spacings` spacings are available, then computes exactly the statistics used for zeta."""
    rng = np.random.default_rng(seed)
    out: list[SampleStats] = []
    for _ in range(n_replicates):
        pooled: list[NDArray[np.float64]] = []
        counts = None
        total_spacings = 0
        while total_spacings < n_spacings:
            x = unfold_semicircle(gue_matrix_eigenvalues(rng))
            pooled.append(spacings(x))
            c = pair_counts(x)
            counts = c if counts is None else counts + c
            total_spacings += len(x) - 1
        all_spacings = np.concatenate(pooled)[:n_spacings]
        assert counts is not None
        n_points = total_spacings + len(pooled)
        out.append(summarize(all_spacings, counts, n_points))
    return EnsembleSummary(n_replicates=n_replicates, seed=seed, stats=out)
