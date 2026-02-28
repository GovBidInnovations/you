"""Utilities for loading policy packs.

Each policy pack lives in ``govbid/policy_packs/<pack_id>`` and must
include a ``pack.json`` that defines key metadata including the
expected dossier template and coverage bundle versions. Consumers
should use :func:`load_policy_pack` to load a policy pack by name.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PolicyPack:
    """Simple data container for policy pack metadata."""

    policy_pack_id: str
    name: str
    prime_directive_version: str
    dossier_template_version_expected: str
    coverage_bundle_version_expected: str


def load_policy_pack(policy_pack_id: str) -> PolicyPack:
    """Load a policy pack by its identifier.

    The pack definition is stored in ``govbid/policy_packs/<policy_pack_id>/pack.json``.
    If the pack cannot be found, a :class:`FileNotFoundError` is raised.

    Args:
        policy_pack_id: The identifier of the policy pack to load.

    Returns:
        PolicyPack: The parsed policy pack metadata.
    """
    base = Path(__file__).resolve().parent
    pack_path = base / policy_pack_id / "pack.json"
    if not pack_path.exists():
        raise FileNotFoundError(f"Policy pack not found: {pack_path}")
    data = json.loads(pack_path.read_text(encoding="utf-8"))
    return PolicyPack(
        policy_pack_id=data["policy_pack_id"],
        name=data["name"],
        prime_directive_version=data["prime_directive_version"],
        dossier_template_version_expected=data["dossier_template_version_expected"],
        coverage_bundle_version_expected=data["coverage_bundle_version_expected"],
    )