"""Tests for coverage gating logic."""

from govbid.coverage.gate import gate_coverage


def test_needs_data_when_no_input() -> None:
    result = gate_coverage(coverage_bundle={"coverage_map": {"coverage": {}}})
    assert result.status == "NEEDS_DATA"
