"""Dossier validation utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

from jsonschema import Draft202012Validator


def validate_json_schema(*, instance: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, list[str]]:
    """Validate an instance against a JSON schema.

    Returns a tuple of ``(is_valid, error_messages)``. If the instance
    conforms to the schema, ``is_valid`` will be True and the list of
    messages will be empty.
    """
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if not errors:
        return True, []
    msgs = []
    for err in errors:
        path = ".".join([str(p) for p in err.path]) if err.path else "<root>"
        msgs.append(f"{path}: {err.message}")
    return False, msgs


def validate_dossier_minimums(dossier: Dict[str, Any]) -> Tuple[bool, list[str]]:
    """Perform lightweight validation checks on the dossier structure.

    Ensures that certain tabs exist and that control metadata has been
    stamped. This does not perform full JSON schema validation.
    """
    msgs: list[str] = []
    tabs = dossier.get("tabs", {})
    required_tabs = ["CONTROL_SHEET", "EVIDENCE_LEDGER", "GUBES_GATES"]
    for t in required_tabs:
        if t not in tabs:
            msgs.append(f"Missing required tab: {t}")
    ctrl = tabs.get("CONTROL_SHEET", {})
    if isinstance(ctrl, dict):
        if not ctrl.get("prime_directive_version"):
            msgs.append("CONTROL_SHEET.prime_directive_version missing")
        if not ctrl.get("dossier_template_version"):
            msgs.append("CONTROL_SHEET.dossier_template_version missing")
    else:
        msgs.append("CONTROL_SHEET must be an object")
    return (len(msgs) == 0), msgs


def load_json(path: Path) -> Dict[str, Any]:
    """Load and parse a JSON file from disk."""
    return json.loads(path.read_text(encoding="utf-8"))
