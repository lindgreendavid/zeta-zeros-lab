import numpy as np
import pytest

from zeta_zeros_lab.simulate import (
    gue_matrix_eigenvalues,
    simulate_ensemble,
    unfold_semicircle,
)
from zeta_zeros_lab.stats import spacings


def test_semicircle_unfolding_gives_unit_mean_spacing():
    rng = np.random.default_rng(7)
    x = unfold_semicircle(gue_matrix_eigenvalues(rng))
    sp = spacings(x)
    assert len(x) > 400
    assert sp.mean() == pytest.approx(1.0, abs=0.03)


def test_ensemble_is_reproducible_and_gue_like():
    a = simulate_ensemble(600, 3, seed=11)
    b = simulate_ensemble(600, 3, seed=11)
    assert [s.ks_gue for s in a.stats] == [s.ks_gue for s in b.stats]
    for s in a.stats:
        assert s.n_spacings == 600
        assert s.ks_gue < s.ks_poisson
        assert s.r2_rms_gue < s.r2_rms_poisson
        assert s.variance == pytest.approx(0.18, abs=0.05)
