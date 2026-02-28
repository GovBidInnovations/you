"""Render a dossier into Markdown.

This module takes the structured dossier JSON and produces a
human‑readable Markdown report. The format is intentionally simple
and deterministic so that downstream consumers can rely on stable
structures for parsing if needed.
"""

from __future__ import annotations

from typing import Any, Dict


def render_dossier_markdown(dossier: Dict[str, Any]) -> str:
    """Render a dossier into a Markdown string.

    Args:
        dossier: The structured dossier dictionary.

    Returns:
        A Markdown document representing the dossier.
    """
    tabs = dossier.get("tabs", {})
    ctrl = tabs.get("CONTROL_SHEET", {}) if isinstance(tabs, dict) else {}
    bid_decision = ""
    if isinstance(ctrl, dict):
        bid_decision = ctrl.get("bid_decision", "") or ""
    lines: list[str] = []
    lines.append("# GovBid Dossier Report")
    lines.append("")
    lines.append(f"- Policy Pack: `{dossier.get('policy_pack_id', '')}`")
    lines.append(f"- Prime Directive: `{dossier.get('prime_directive_version', '')}`")
    lines.append(f"- Template Version: `{dossier.get('template_version', '')}`")
    lines.append(f"- BID DECISION: `{bid_decision}`")
    lines.append("")
    if "GUBES_GATES" in tabs:
        lines.append("## GUBES Gates")
        lines.append("```json")
        lines.append(_pretty_json(tabs["GUBES_GATES"]))
        lines.append("```")
        lines.append("")
    if "EVIDENCE_LEDGER" in tabs:
        lines.append("## Evidence Ledger")
        lines.append("```json")
        lines.append(_pretty_json(tabs["EVIDENCE_LEDGER"]))
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def _pretty_json(obj: Any) -> str:
    import json
    return json.dumps(obj, indent=2, ensure_ascii=False)
