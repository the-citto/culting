"""CLI."""

import click
from rich import print as rprint



@click.group()
def cli() -> None:
    """Cli."""
    rprint("Welcome.")


