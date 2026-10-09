import numpy as np
import pytest

from zeta_zeros_lab.gue import poisson_cdf
from zeta_zeros_lab.stats import (
    gue_pair_bin_average,
    ks_distance,
    pair_centers,
    pair_counts,
    pair_density,
    rms_distance,
    spacing_histogram,
    spacings,
    summarize,
)


def test_ks_distance_zero_for_perfect_sample_and_large_for_wrong_law():
    rng = np.random.default_rng(1)
    sample = rng.exponential(size=20000)
    assert ks_distance(sample, poisson_cdf) < 0.02
    assert ks_distance(np.full(100, 5.0), poisson_cdf) > 0.9


def test_pair_counts_on_integer_lattice():
    x = np.arange(100, dtype=float)
    counts = pair_counts(x)
    assert counts.sum() == 99 + 98 + 97  # lags 1, 2, 3 (3.0 inclusive)
    assert counts[10] == 99  # lag exactly 1.0 lands in bin [1.0, 1.1)


def test_pair_density_of_poisson_like_points_is_flat_near_one():
    rng = np.random.default_rng(2)
    x = np.cumsum(rng.exponential(size=20000))
    r2 = pair_density(pair_counts(x), len(x))
    assert np.mean(r2) == pytest.approx(1.0, abs=0.02)


def test_pair_bin_average_shapes():
    assert len(pair_centers()) == 30
    avg = gue_pair_bin_average()
    assert avg[0] < 0.05 and avg[-1] == pytest.approx(1.0, abs=0.05)


def test_rms_and_histogram_and_summarize():
    assert rms_distance(np.array([1.0, 2.0]), np.array([1.0, 4.0])) == pytest.approx(np.sqrt(2.0))
    rng = np.random.default_rng(3)
    x = np.cumsum(rng.exponential(size=5000))
    sp = spacings(x)
    hist = spacing_histogram(sp)
    assert len(hist) == 30
    assert hist[0] == pytest.approx(1.0, abs=0.15)
    s = summarize(sp, pair_counts(x), len(x))
    assert s.ks_poisson < s.ks_gue  # genuine Poisson data is closer to Poisson
    assert s.r2_rms_poisson < s.r2_rms_gue
    assert s.variance == pytest.approx(1.0, abs=0.1)
