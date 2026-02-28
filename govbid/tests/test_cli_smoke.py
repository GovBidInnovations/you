"""Smoke tests for the CLI interface."""

from typer.testing import CliRunner
from govbid.cli import app


runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "govbid-engine" in result.stdout
