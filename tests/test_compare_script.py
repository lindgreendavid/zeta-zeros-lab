import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "compare_registry", Path(__file__).parent.parent / "scripts" / "compare_registry.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_equal_tolerates_tiny_float_noise_but_not_structure_changes():
    assert module.equal({"a": [1.0, 2.0]}, {"a": [1.0 + 1e-9, 2.0]})
    assert not module.equal({"a": [1.0]}, {"a": [1.1]})
    assert not module.equal({"a": 1}, {"b": 1})
    assert not module.equal({"a": True}, {"a": 1})
    assert not module.equal([1, 2], [1])
    assert module.equal("x", "x")
