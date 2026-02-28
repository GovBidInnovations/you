"""Dossier skeleton construction utilities.

The dossier builder loads the authoritative dossier template JSON and
builds an initial JSON structure that conforms to the expected schema.
It instantiates empty values for all fields defined in the template and
stamps control metadata based on the loaded policy pack.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from govbid.policy_packs.loader import PolicyPack
from govbid.util.files import require_file


def _load_dossier_template(template_path: Path) -> Dict[str, Any]:
    """Load the dossier template JSON from disk.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    require_file(template_path, hint="Place GovBid_DOSSIER_Template_v2.1.0.json in govbid/schemas/")
    return json.loads(template_path.read_text(encoding="utf-8"))


def build_dossier_skeleton(*, policy_pack: PolicyPack, template_path: Path) -> Dict[str, Any]:
    """Build a blank dossier based on the provided template and policy pack.

    Args:
        policy_pack: The policy pack describing expected template version.
        template_path: Path to the dossier template JSON.

    Returns:
        A dictionary representing the dossier skeleton.
    """
    template = _load_dossier_template(template_path)
    tpl_version = str(template.get("version", ""))
    if tpl_version and tpl_version != policy_pack.dossier_template_version_expected:
        raise ValueError(
            f"Dossier template version mismatch. Expected {policy_pack.dossier_template_version_expected}, got {tpl_version}."
        )
    workbook = template.get("workbook", {})
    tabs = workbook.get("tabs", [])
    dossier: Dict[str, Any] = {
        "schema": template.get("schema", "govbid.dossier"),
        "template_name": template.get("template_name", ""),
        "template_version": tpl_version,
        "policy_pack_id": policy_pack.policy_pack_id,
        "prime_directive_version": policy_pack.prime_directive_version,
        "tabs": {},
    }
    for tab in tabs:
        tab_name = tab.get("tab_name")
        fields = tab.get("fields", {})
        if not tab_name:
            continue
        dossier["tabs"][tab_name] = fields
    control = dossier["tabs"].get("CONTROL_SHEET")
    if isinstance(control, dict):
        control["prime_directive_version"] = policy_pack.prime_directive_version
        control["dossier_template_version"] = policy_pack.dossier_template_version_expected
    return dossier
