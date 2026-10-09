import json
from itertools import pairwise
from pathlib import Path

import numpy as np

from zeta_zeros_lab.registry import (
    BLOCKS,
    DATA_DIR,
    SMALL_FRACTION_THRESHOLD,
    block_entry,
    build_registry,
    evaluate_hypotheses,
    sample_rows,
)
from zeta_zeros_lab.validation import load_block

FROZEN = Path(__file__).parent.parent / "reports" / "v0.1-zeta-registry.json"


def frozen() -> dict:
    return json.loads(FROZEN.read_text())


def test_frozen_block_statistics_match_a_fresh_computation():
    registry = frozen()
    for name, fname in BLOCKS.items():
        fresh = block_entry(load_block(DATA_DIR / fname))
        expected = registry["blocks"][name]
        for key in ("first_index", "n_zeros", "gamma_min", "gamma_max"):
            assert fresh[key] == expected[key]
        for key, value in fresh["stats"].items():
            assert np.isclose(value, expected["stats"][key], atol=1e-8)
        assert np.allclose(fresh["spacing_histogram"], expected["spacing_histogram"], atol=1e-8)
        assert np.allclose(fresh["pair_correlation"], expected["pair_correlation"], atol=1e-8)


def test_frozen_hypotheses_follow_from_the_frozen_numbers():
    registry = frozen()
    assert evaluate_hypotheses(registry) == registry["hypotheses"]


def test_threshold_is_one_third_of_poisson_value():
    assert abs(SMALL_FRACTION_THRESHOLD - (1 - np.exp(-0.25)) / 3) < 1e-4


def test_samples_are_aligned_to_zero_and_increasing():
    rows = sample_rows()
    for row in rows.values():
        assert row[0] == 0.0
        assert all(b > a for a, b in pairwise(row))
    assert len(rows["zeta"]) == len(rows["poisson"]) == len(rows["gue"]) == 61


def test_small_build_has_expected_structure():
    registry = build_registry(n_replicates=2)
    assert set(registry["blocks"]) == {"low", "high"}
    assert registry["simulated_gue_null"]["n_replicates"] == 2
    assert set(registry["hypotheses"]) == {"H1", "H2", "H3", "H4"}
    assert len(registry["reference"]["gue_pdf"]) == len(registry["reference"]["spacing_grid"])


def test_published_headline_is_consistent_with_the_registry():
    """The README/report claims are asserted here so prose cannot drift from the data."""
    r = frozen()
    low, high = r["blocks"]["low"]["stats"], r["blocks"]["high"]["stats"]
    null = r["simulated_gue_null"]
    assert r["hypotheses"]["H1"]["confirmed"] and r["hypotheses"]["H2"]["confirmed"]
    assert not r["hypotheses"]["H3"]["confirmed"]
    assert r["hypotheses"]["H4"]["confirmed"]
    assert low["variance"] < null["variance"]["q025"]
    assert high["variance"] < null["variance"]["q025"]
    assert low["variance"] < high["variance"] < r["reference"]["gue_spacing_variance"]


def test_report_and_readme_numbers_match_the_registry():
    root = Path(__file__).parent.parent
    text = (root / "docs" / "research-report.md").read_text() + (root / "README.md").read_text()
    r = frozen()
    for block in r["blocks"].values():
        s = block["stats"]
        for key in ("ks_gue", "r2_rms_gue", "variance", "small_fraction"):
            assert f"{s[key]:.4f}" in text, key
    band = r["simulated_gue_null"]["variance"]
    assert f"{band['q025']:.4f}" in text and f"{band['q975']:.4f}" in text


def test_paper_numbers_match_the_registry():
    tex = (Path(__file__).parent.parent / "paper" / "paper.tex").read_text()
    r = frozen()
    for block in r["blocks"].values():
        s = block["stats"]
        for key in (
            "ks_gue",
            "r2_rms_gue",
            "variance",
            "small_fraction",
            "ks_poisson",
            "r2_rms_poisson",
        ):
            assert f"{s[key]:.4f}" in tex, key
    band = r["simulated_gue_null"]["variance"]
    assert f"{band['q025']:.3f}" in tex and f"{band['q975']:.3f}" in tex
