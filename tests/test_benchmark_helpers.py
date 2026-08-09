from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "benchmark_latency.py"
spec = importlib.util.spec_from_file_location("benchmark_latency", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_percentile_single_and_interpolated() -> None:
    assert module.percentile([5.0], 0.95) == 5.0
    assert module.percentile([10.0, 20.0], 0.5) == 15.0
    assert module.percentile([1.0, 2.0, 3.0, 4.0], 0.95) == pytest.approx(3.85)
