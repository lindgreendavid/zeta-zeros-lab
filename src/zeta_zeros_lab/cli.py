"""Command-line entry point: print the headline statistics of the frozen registry."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    path = Path(__file__).resolve().parents[2] / "reports" / "v0.1-zeta-registry.json"
    registry = json.loads(path.read_text())
    for name, block in registry["blocks"].items():
        s = block["stats"]
        print(
            f"{name}: n={block['n_zeros']} ks_gue={s['ks_gue']:.4f} "
            f"ks_poisson={s['ks_poisson']:.4f} "
            f"r2_rms_gue={s['r2_rms_gue']:.4f} r2_rms_poisson={s['r2_rms_poisson']:.4f} "
            f"variance={s['variance']:.4f}"
        )


if __name__ == "__main__":
    main()
