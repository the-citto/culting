"""Test CLI."""

from click.testing import CliRunner

from culting.cli import cli
from culting.variables import __version__


def test_version() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    expected = f"version {__version__}"
    assert expected in result.output
    assert result.exit_code == 0







