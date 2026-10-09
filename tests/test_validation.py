from pathlib import Path

import numpy as np
import pytest

from zeta_zeros_lab.validation import (
    ZeroBlock,
    check_sign_alternation,
    load_block,
    validate_block,
)

DATA = Path(__file__).parent.parent / "data"


def head(name: str, n: int) -> ZeroBlock:
    full = load_block(DATA / name)
    return ZeroBlock(full.first_index, full.gamma[:n])


@pytest.mark.parametrize("name", ["zeros-low.csv", "zeros-high.csv"])
def test_real_blocks_pass_validation(name):
    block = head(name, 300)
    assert validate_block(block) < 2.5
    assert check_sign_alternation(block) == 299


def test_first_zeros_match_published_values():
    block = head("zeros-low.csv", 5)
    assert block.gamma[0] == pytest.approx(14.134725141734693, abs=1e-12)


def test_missing_zero_is_detected_by_z_sign_alternation():
    block = head("zeros-low.csv", 200)
    kept = np.delete(block.gamma, 100)
    with pytest.raises(ValueError, match="sign change"):
        check_sign_alternation(ZeroBlock(1, kept))


def test_duplicated_zero_or_disorder_is_rejected():
    block = head("zeros-low.csv", 50)
    with pytest.raises(ValueError, match="increasing"):
        validate_block(ZeroBlock(1, np.insert(block.gamma, 10, block.gamma[10])))


def test_wrong_first_zeros_rejected():
    block = head("zeros-low.csv", 50)
    shifted = ZeroBlock(1, block.gamma + 1e-6)
    with pytest.raises(ValueError, match="published values"):
        validate_block(shifted)


def test_count_offset_screen_rejects_shifted_labelling():
    block = head("zeros-low.csv", 60)
    mislabelled = ZeroBlock(5, block.gamma)  # claims to start at n=5 but is n=1..
    with pytest.raises(ValueError, match="offset"):
        validate_block(mislabelled)


def test_load_block_rejects_nonconsecutive_indices(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("n,gamma\n1,14.13\n3,21.02\n")
    with pytest.raises(ValueError, match="consecutive"):
        load_block(bad)
