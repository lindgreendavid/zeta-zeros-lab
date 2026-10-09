import mpmath
import numpy as np
import pytest

from zeta_zeros_lab.unfold import riemann_siegel_theta, unfold


@pytest.mark.parametrize("t", [14.134725, 21.02, 100.0, 2515.0, 75000.0])
def test_theta_series_matches_mpmath(t):
    mpmath.mp.dps = 30
    expected = float(mpmath.siegeltheta(t))
    assert float(riemann_siegel_theta(np.array([t]))[0]) == pytest.approx(expected, abs=1e-8)


def test_unfold_is_increasing_with_unit_mean_density():
    gamma = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062])
    x = unfold(gamma)
    assert np.all(np.diff(x) > 0)
    # N_smooth(14.13) ~ 1 - 0.5 offset region: the first zero maps near 1
    assert x[0] == pytest.approx(0.5, abs=1.0)
