"""Test statistics, all computed identically for the zeta zeros and for simulated GUE."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from zeta_zeros_lab.gue import gue_cdf, gue_pair_correlation, poisson_cdf

PAIR_MAX_LAG = 3.0
PAIR_BIN_WIDTH = 0.1
SMALL_SPACING_CUTOFF = 0.25
HIST_MAX = 3.0
HIST_BIN_WIDTH = 0.1


def spacings(unfolded: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.diff(unfolded)


def ks_distance(
    sample: NDArray[np.float64], cdf: Callable[[NDArray[np.float64]], NDArray[np.float64]]
) -> float:
    """Kolmogorov-Smirnov distance sup |F_n - F|. Used as a *distance*, never a p-value:
    zeta spacings are not independent, so KS p-values are not valid here."""
    x = np.sort(sample)
    n = len(x)
    f = cdf(x)
    upper = np.arange(1, n + 1) / n - f
    lower = f - np.arange(0, n) / n
    return float(max(upper.max(), lower.max()))


def pair_counts(unfolded: NDArray[np.float64]) -> NDArray[np.float64]:
    """Count ordered pairs (j != k) with 0 < x_k - x_j <= PAIR_MAX_LAG, binned; each unordered
    pair contributes to +lag and -lag symmetrically, so only positive lags are histogrammed."""
    n_bins = round(PAIR_MAX_LAG / PAIR_BIN_WIDTH)
    counts = np.zeros(n_bins)
    x = np.sort(unfolded)
    right = np.searchsorted(x, x + PAIR_MAX_LAG, side="right")
    for j in range(len(x)):
        diffs = x[j + 1 : right[j]] - x[j]
        counts += np.histogram(diffs, bins=n_bins, range=(0.0, PAIR_MAX_LAG))[0]
    return counts


def pair_density(counts: NDArray[np.float64], n_points: int) -> NDArray[np.float64]:
    """Empirical R2 estimate: pairs per point per unit lag. Edge effects are O(lag / n)."""
    return counts / (n_points * PAIR_BIN_WIDTH)


def pair_centers() -> NDArray[np.float64]:
    n_bins = round(PAIR_MAX_LAG / PAIR_BIN_WIDTH)
    return np.asarray((np.arange(n_bins) + 0.5) * PAIR_BIN_WIDTH, dtype=np.float64)


def gue_pair_bin_average() -> NDArray[np.float64]:
    """Theoretical R2 averaged over each bin (not merely sampled at its centre)."""
    fine = 20
    n_bins = round(PAIR_MAX_LAG / PAIR_BIN_WIDTH)
    offsets = (np.arange(fine) + 0.5) / fine * PAIR_BIN_WIDTH
    edges = np.arange(n_bins) * PAIR_BIN_WIDTH
    return np.asarray(
        gue_pair_correlation(edges[:, None] + offsets[None, :]).mean(axis=1), dtype=np.float64
    )


def rms_distance(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
    return float(np.sqrt(np.mean((a - b) ** 2)))


@dataclass(frozen=True)
class SampleStats:
    n_spacings: int
    mean_spacing: float
    variance: float
    small_fraction: float
    ks_gue: float
    ks_poisson: float
    r2_rms_gue: float
    r2_rms_poisson: float


def summarize(
    spacing: NDArray[np.float64], counts: NDArray[np.float64], n_points: int
) -> SampleStats:
    r2 = pair_density(counts, n_points)
    return SampleStats(
        n_spacings=len(spacing),
        mean_spacing=float(spacing.mean()),
        variance=float(spacing.var(ddof=1)),
        small_fraction=float(np.mean(spacing < SMALL_SPACING_CUTOFF)),
        ks_gue=ks_distance(spacing, gue_cdf),
        ks_poisson=ks_distance(spacing, poisson_cdf),
        r2_rms_gue=rms_distance(r2, gue_pair_bin_average()),
        r2_rms_poisson=rms_distance(r2, np.ones_like(r2)),
    )


def spacing_histogram(spacing: NDArray[np.float64]) -> NDArray[np.float64]:
    """Density histogram on [0, HIST_MAX]; spacings beyond HIST_MAX are counted but not binned."""
    n_bins = round(HIST_MAX / HIST_BIN_WIDTH)
    counts, _ = np.histogram(spacing, bins=n_bins, range=(0.0, HIST_MAX))
    return counts / (len(spacing) * HIST_BIN_WIDTH)
