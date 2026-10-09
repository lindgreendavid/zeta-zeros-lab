"""Assemble the frozen registry: statistics per block, reference curves, simulated null."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from zeta_zeros_lab.gue import (
    gue_cdf,
    gue_pair_correlation,
    gue_pdf,
    gue_spacing_moments,
    poisson_pdf,
)
from zeta_zeros_lab.simulate import gue_matrix_eigenvalues, simulate_ensemble, unfold_semicircle
from zeta_zeros_lab.stats import (
    SMALL_SPACING_CUTOFF,
    gue_pair_bin_average,
    pair_centers,
    pair_counts,
    spacing_histogram,
    spacings,
    summarize,
)
from zeta_zeros_lab.unfold import unfold
from zeta_zeros_lab.validation import ZeroBlock, load_block, validate_block

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
BLOCKS = {"low": "zeros-low.csv", "high": "zeros-high.csv"}
SMALL_FRACTION_THRESHOLD = 0.0737  # one third of the Poisson value 1 - exp(-0.25)
SAMPLE_POINTS = 61
N_REPLICATES = 150
SEED = 20260920
DIGITS = 9


def _r(values: Any) -> Any:
    return np.round(np.asarray(values, dtype=np.float64), DIGITS).tolist()


def block_entry(block: ZeroBlock) -> dict[str, Any]:
    offset = validate_block(block)
    x = unfold(block.gamma)
    sp = spacings(x)
    counts = pair_counts(x)
    stats = summarize(sp, counts, len(x))
    return {
        "first_index": block.first_index,
        "n_zeros": block.n,
        "gamma_min": _r(block.gamma[0]),
        "gamma_max": _r(block.gamma[-1]),
        "max_count_offset": _r(offset),
        "stats": {k: (_r(v) if isinstance(v, float) else v) for k, v in asdict(stats).items()},
        "spacing_histogram": _r(spacing_histogram(sp)),
        "pair_correlation": _r(counts / (len(x) * 0.1)),
    }


def evaluate_hypotheses(registry: dict[str, Any]) -> dict[str, Any]:
    """Apply the thresholds fixed in docs/research-protocol.md, verbatim."""
    blocks = registry["blocks"]
    null = registry["simulated_gue_null"]

    h1 = {
        name: b["stats"]["ks_gue"] < b["stats"]["ks_poisson"]
        and b["stats"]["r2_rms_gue"] < b["stats"]["r2_rms_poisson"]
        for name, b in blocks.items()
    }
    h2 = {
        name: b["stats"]["small_fraction"] < SMALL_FRACTION_THRESHOLD for name, b in blocks.items()
    }
    h3 = {
        name: {
            "ks_gue": b["stats"]["ks_gue"] <= null["ks_gue"]["q975"],
            "r2_rms_gue": b["stats"]["r2_rms_gue"] <= null["r2_rms_gue"]["q975"],
            "variance": null["variance"]["q025"]
            <= b["stats"]["variance"]
            <= null["variance"]["q975"],
        }
        for name, b in blocks.items()
    }
    low, high = blocks["low"]["stats"], blocks["high"]["stats"]
    h4 = {
        "ks_gue_improves": high["ks_gue"] < low["ks_gue"],
        "r2_rms_gue_improves": high["r2_rms_gue"] < low["r2_rms_gue"],
    }
    return {
        "H1": {"per_block": h1, "confirmed": all(h1.values())},
        "H2": {"per_block": h2, "confirmed": all(h2.values())},
        "H3": {
            "per_block": h3,
            "confirmed": all(all(v.values()) for v in h3.values()),
        },
        "H4": {"checks": h4, "confirmed": all(h4.values())},
    }


def sample_rows() -> dict[str, list[float]]:
    """Short seeded rows of unfolded points for the 'which row are the zeta zeros?' visual."""
    low = load_block(DATA_DIR / BLOCKS["low"])
    x = unfold(low.gamma)[:SAMPLE_POINTS]
    rng = np.random.default_rng(SEED + 1)
    poisson = np.concatenate([[0.0], np.cumsum(rng.exponential(size=SAMPLE_POINTS - 1))])
    gue = unfold_semicircle(gue_matrix_eigenvalues(np.random.default_rng(SEED + 2)))[:SAMPLE_POINTS]
    return {
        "zeta": _r(x - x[0]),
        "poisson": _r(poisson),
        "gue": _r(gue - gue[0]),
    }


def build_registry(data_dir: Path = DATA_DIR, n_replicates: int = N_REPLICATES) -> dict[str, Any]:
    blocks = {name: block_entry(load_block(data_dir / fname)) for name, fname in BLOCKS.items()}
    n_spacings = min(b["stats"]["n_spacings"] for b in blocks.values())
    ensemble = simulate_ensemble(n_spacings, n_replicates, SEED)

    def band(attr: str) -> dict[str, float]:
        v = np.array([getattr(s, attr) for s in ensemble.stats])
        return {
            "q025": _r(np.quantile(v, 0.025)),
            "q500": _r(np.quantile(v, 0.5)),
            "q975": _r(np.quantile(v, 0.975)),
        }

    grid = np.round(np.arange(0.0, 4.0 + 1e-9, 0.05), 2)
    mean, var = gue_spacing_moments()
    registry = {
        "schema_version": "0.1",
        "small_spacing_cutoff": SMALL_SPACING_CUTOFF,
        "blocks": blocks,
        "reference": {
            "gue_spacing_mean": _r(mean),
            "gue_spacing_variance": _r(var),
            "gue_small_fraction": _r(float(gue_cdf(SMALL_SPACING_CUTOFF))),
            "poisson_small_fraction": _r(1 - np.exp(-SMALL_SPACING_CUTOFF)),
            "spacing_grid": _r(grid),
            "gue_pdf": _r(gue_pdf(grid)),
            "gue_cdf": _r(gue_cdf(grid)),
            "poisson_pdf": _r(poisson_pdf(grid)),
            "pair_centers": _r(pair_centers()),
            "gue_pair_correlation": _r(gue_pair_bin_average()),
            "gue_pair_correlation_curve_x": _r(np.arange(0.0, 3.0 + 1e-9, 0.05)),
            "gue_pair_correlation_curve": _r(
                gue_pair_correlation(np.arange(0.0, 3.0 + 1e-9, 0.05, dtype=np.float64))
            ),
        },
        "simulated_gue_null": {
            "n_replicates": ensemble.n_replicates,
            "seed": ensemble.seed,
            "n_spacings": n_spacings,
            "ks_gue": band("ks_gue"),
            "r2_rms_gue": band("r2_rms_gue"),
            "variance": band("variance"),
            "small_fraction": band("small_fraction"),
        },
    }
    registry["samples"] = sample_rows()
    registry["hypotheses"] = evaluate_hypotheses(registry)
    return registry
