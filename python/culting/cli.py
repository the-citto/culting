"""CLI."""

import subprocess
import typing as t

import rich_click as click

from . import (
    CommandNotFoundError,
    InitError,
    InitKwargs,
    PythonVersions,
    __version__,
    logger,
)



@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    # invoke_without_command=True,
)
@click.version_option(__version__, "-V", "--version")
def cli() -> None:
    """Culting, a Python projects' manager."""


help_name = "Set the package name, PEP 8 and PEP 423 compliant. Defaults to directory name"
help_python_version = """
Set Python version.

\b
If not specified the system default will be used.
"""

@cli.command()
@click.argument("path", type=click.Path(), default=".")
@click.option("--name", type=str, required=False, help=help_name)
@click.option(
    "--python-version",
    type=click.Choice(t.get_args(PythonVersions)),
    default="",
    # required=False,
    help=help_python_version,
)
@click.pass_context
def init(ctx: click.Context, **kwargs: t.Unpack[InitKwargs]) -> None:
    """Init project."""
    from .init import Init
    try:
        Init(**kwargs)
    except (
        InitError,
        subprocess.CalledProcessError,
        CommandNotFoundError,
    ) as err:
        logger.error(err)
        ctx.abort()










