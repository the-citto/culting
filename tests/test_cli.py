"""Test CLI."""

from click.testing import CliRunner

from culting.cli import (
    __version__,
    cli,
)


def test_version() -> None:
    """Test version."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    expected = f"version {__version__}"
    assert expected in result.output
    assert result.exit_code == 0







