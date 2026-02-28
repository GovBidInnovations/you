"""Coverage gating logic.

Coverage gating ensures that solicitations are only pursued in states
and counties that are explicitly allowed by the coverage bundle. This
implementation follows the authoritative rules: only ``states_by_name``
and ``counties_by_fips`` are used for gating. If neither a state nor
county is provided, the result is ``NEEDS_DATA``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class CoverageResult:
    """Represents the result of a coverage gate check."""

    status: str  # IN_COVERAGE | OUT_OF_COVERAGE | NEEDS_DATA
    evidence: Optional[str] = None  # state name or county FIPS used
    note: Optional[str] = None


def gate_coverage(
    *,
    coverage_bundle: Dict[str, Any],
    state_name: Optional[str] = None,
    county_fips: Optional[str] = None,
) -> CoverageResult:
    """Check whether a location is covered by the coverage bundle.

    Args:
        coverage_bundle: Parsed coverage bundle JSON.
        state_name: Optional state name to check.
        county_fips: Optional county FIPS code to check.

    Returns:
        CoverageResult: The result of the gate check.
    """
    coverage = (
        coverage_bundle.get("coverage_map", {}).get("coverage", {})
    )
    states = set(coverage.get("states_by_name", []) or [])
    counties = coverage.get("counties_by_fips", []) or []
    county_fips_set = {c.get("fips") for c in counties if isinstance(c, dict)}
    if county_fips:
        if county_fips in county_fips_set:
            return CoverageResult(status="IN_COVERAGE", evidence=f"county_fips:{county_fips}")
        return CoverageResult(status="OUT_OF_COVERAGE", evidence=f"county_fips:{county_fips}")
    if state_name:
        if state_name in states:
            return CoverageResult(status="IN_COVERAGE", evidence=f"state:{state_name}")
        return CoverageResult(status="OUT_OF_COVERAGE", evidence=f"state:{state_name}")
    return CoverageResult(status="NEEDS_DATA", note="Provide state_name or county_fips for gating.")
