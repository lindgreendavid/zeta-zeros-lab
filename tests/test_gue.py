import numpy as np
import pytest
from scipy.integrate import quad

from zeta_zeros_lab.gue import (
    gap_probability,
    gue_cdf,
    gue_pair_correlation,
    gue_pdf,
    gue_spacing_moments,
    poisson_cdf,
    poisson_pdf,
)


def test_gap_probability_endpoints_and_convergence():
    assert gap_probability(0.0) == 1.0
    assert gap_probability(1.0, 32) == pytest.approx(gap_probability(1.0, 64), abs=1e-12)
    assert 0 < gap_probability(2.0) < gap_probability(1.0) < 1


def test_cdf_properties():
    s = np.linspace(0, 4, 200)
    f = gue_cdf(s)
    assert f[0] == 0.0
    assert np.all(np.diff(f) >= -1e-9)
    assert gue_cdf(np.array([4.9]))[0] == pytest.approx(1.0, abs=1e-6)
    assert gue_cdf(np.array([50.0]))[0] == 1.0


def test_exact_moments_match_published_gue_values():
    mean, var = gue_spacing_moments()
    assert mean == pytest.approx(1.0, abs=1e-9)
    assert var == pytest.approx(0.1800, abs=2e-4)


def test_pdf_integrates_to_one_and_is_consistent_with_cdf():
    total = quad(lambda x: float(gue_pdf(x)), 0, 4.9, limit=200)[0]
    assert total == pytest.approx(1.0, abs=1e-4)
    assert float(gue_pdf(np.array([0.0]))[0]) == pytest.approx(0.0, abs=1e-3)
    assert float(gue_pdf(np.array([99.0]))[0]) == 0.0


def test_close_to_wigner_surmise_but_not_identical():
    s = np.array([0.25, 0.5, 1.0, 2.0])
    surmise = [
        quad(lambda x: 32 / np.pi**2 * x * x * np.exp(-4 * x * x / np.pi), 0, v)[0] for v in s
    ]
    diff = np.abs(gue_cdf(s) - np.array(surmise))
    assert diff.max() < 0.01
    assert diff.max() > 1e-4  # the surmise really is only approximate


def test_small_s_repulsion_law():
    # p(s) ~ (pi^2/3) s^2 as s -> 0
    s = 0.1
    assert float(gue_pdf(np.array([s]))[0]) == pytest.approx(np.pi**2 / 3 * s**2, rel=0.1)


def test_poisson_and_pair_correlation():
    assert poisson_cdf(1.0) == pytest.approx(1 - np.exp(-1))
    assert poisson_pdf(0.0) == 1.0
    assert gue_pair_correlation(0.0) == pytest.approx(0.0, abs=1e-12)
    assert gue_pair_correlation(1.0) == pytest.approx(1.0, abs=1e-12)
    assert gue_pair_correlation(100.5) == pytest.approx(1.0, abs=1e-3)
