"""Command line interface for the GovBid engine.

This module uses Typer to expose a minimal CLI for generating and
validating dossiers as well as rendering human-readable reports and
checking coverage gating. The CLI is designed to be simple and
composable so it can be wrapped by a web API later on.
"""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich import print

from govbid.config.settings import settings
from govbid.policy_packs.loader import load_policy_pack
from govbid.dossier.builder import build_dossier_skeleton
from govbid.dossier.validator import load_json, validate_dossier_minimums
from govbid.output.render_markdown import render_dossier_markdown
from govbid.coverage.loader import load_coverage_bundle
from govbid.coverage.gate import gate_coverage


app = typer.Typer(add_completion=False)


def _schemas_dir() -> Path:
    """Return the path to the schemas directory relative to this module."""
    return Path(__file__).resolve().parent / "schemas"


@app.command("version")
def version() -> None:
    """Print the current engine version."""
    from govbid import __version__
    print(f"govbid-engine {__version__}")


# Define ``dossier`` subcommands
dossier_app = typer.Typer()
app.add_typer(dossier_app, name="dossier")


@dossier_app.command("new")
def dossier_new(out: Path = typer.Option(..., "--out", help="Path to write dossier.json")) -> None:
    """Generate a new dossier skeleton from the authoritative template."""
    policy = load_policy_pack(settings.default_policy_pack)
    template_path = _schemas_dir() / "GovBid_DOSSIER_Template_v2.1.0.json"
    dossier = build_dossier_skeleton(policy_pack=policy, template_path=template_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(dossier, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[green]Wrote[/green] {out}")


@dossier_app.command("validate")
def dossier_validate(
    inp: Path = typer.Option(..., "--in", help="Path to dossier.json"),
) -> None:
    """Validate a dossier for required tabs and control metadata."""
    dossier = load_json(inp)
    ok, msgs = validate_dossier_minimums(dossier)
    if ok:
        print(f"[green]VALID[/green] {inp}")
        raise typer.Exit(code=0)
    print(f"[red]INVALID[/red] {inp}")
    for m in msgs:
        print(f"- {m}")
    raise typer.Exit(code=2)


@dossier_app.command("render")
def dossier_render(
    inp: Path = typer.Option(..., "--in", help="Path to dossier.json"),
    out: Path = typer.Option(..., "--out", help="Path to write report.md"),
) -> None:
    """Render a dossier into a Markdown report."""
    dossier = load_json(inp)
    md = render_dossier_markdown(dossier)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"[green]Wrote[/green] {out}")


# Define ``coverage`` subcommands
coverage_app = typer.Typer()
app.add_typer(coverage_app, name="coverage")


@coverage_app.command("gate")
def coverage_gate(
    state_name: str = typer.Option("", "--state", help="State name, e.g. New York"),
    county_fips: str = typer.Option("", "--county-fips", help="County FIPS, e.g. 36093"),
) -> None:
    """Evaluate coverage gating based on a state name or county FIPS code."""
    policy = load_policy_pack(settings.default_policy_pack)
    bundle_path = _schemas_dir() / "GovBid_Coverage_Bundle_v2.0.0.json"
    bundle = load_coverage_bundle(bundle_path)
    # Optional version check – ensures the bundle version matches the policy expectations
    if str(bundle.get("version", "")) and str(bundle.get("version", "")) != policy.coverage_bundle_version_expected:
        raise typer.BadParameter(
            f"Coverage bundle version mismatch. Expected {policy.coverage_bundle_version_expected}, got {bundle.get('version')}"
        )
    res = gate_coverage(
        coverage_bundle=bundle,
        state_name=state_name or None,
        county_fips=county_fips or None,
    )
    print(json.dumps(res.__dict__, indent=2, ensure_ascii=False))
