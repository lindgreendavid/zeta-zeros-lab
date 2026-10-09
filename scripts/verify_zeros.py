#!/usr/bin/env python3
"""Full completeness verification of both frozen zero blocks (slow: ~4,000 Z evaluations)."""

from __future__ import annotations

from zeta_zeros_lab.registry import BLOCKS, DATA_DIR
from zeta_zeros_lab.validation import check_sign_alternation, load_block, validate_block


def main() -> None:
    for name, fname in BLOCKS.items():
        block = load_block(DATA_DIR / fname)
        offset = validate_block(block)
        gaps = check_sign_alternation(block)
        print(
            f"{name}: {block.n} zeros OK; max |n - N_smooth| = {offset:.3f}; "
            f"Z sign alternation verified on all {gaps} gaps"
        )


if __name__ == "__main__":
    main()
