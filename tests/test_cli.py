"""Test CLI."""
# pyright: reportMissingImports=false

from click.testing import CliRunner

from culting import __version__
from culting.cli import cli



def test_version() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    expected = f"version {__version__}"
    assert expected in result.output
    assert result.exit_code == 0







