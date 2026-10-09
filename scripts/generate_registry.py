#!/usr/bin/env python3
"""Regenerate the frozen registry from the frozen zero blocks. Deterministic (seeded)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from zeta_zeros_lab.registry import build_registry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "reports" / "v0.1-zeta-registry.json",
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        json.dump(build_registry(), f, indent=1, sort_keys=True)
        f.write("\n")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
