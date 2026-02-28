"""Unit tests for dossier validation logic."""

import json
from pathlib import Path

from govbid.dossier.validator import validate_dossier_minimums


def test_validate_minimum_tabs() -> None:
    dossier = {
        "tabs": {
            "CONTROL_SHEET": {
                "prime_directive_version": "IPD-ProjectSys v1.0",
                "dossier_template_version": "2.1.0",
            },
            "EVIDENCE_LEDGER": {},
            "GUBES_GATES": {},
        }
    }
    ok, msgs = validate_dossier_minimums(dossier)
    assert ok, msgs
