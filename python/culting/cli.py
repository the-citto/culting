"""CLI."""

import click
from rich import print as rprint



@click.group()
def cli() -> None:
    """Cli."""
    rprint("Welcome.")


@cli.command()
def list_commands() -> None:
    """List commands."""
    from . import sh
    git = sh.Git()
    rprint(git.bin)

