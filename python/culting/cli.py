"""CLI."""

import subprocess
import typing as t

import rich_click as click

from . import (
    CommandNotFoundError,
    InitError,
    InitKwargs,
    __version__,
    logger,
)
from .commands import (
    Py,
    Pyenv,
    Python,
    Uv,
)



python_system_version = Python().version
pyenv_versions = Pyenv().versions
py_versions = Py().versions
uv_versions = Uv().versions
versions_click_options = [
    ("--pyenv-python", "green") if pyenv_versions else None,
    ("--py-python", "magenta") if py_versions else None,
    ("--uv-python", "bright_magenta") if uv_versions else None,
]

advanced_use = {
    "name": "Advanced options",
    "options": ["--help"],
}
click.rich_click.OPTION_GROUPS = {
    "culting": [
        {
            "name": "Advanced options",
            "options": ["--help", "--version"],
        },
    ],
    # "culting review": [],
    "culting init": [
        {
            "name": "Basic usage",
            "options": ["--name"],
        },
        {
            "name": "Python Managers",
            "options": [v[0] for v in versions_click_options if v is not None],
            "table_styles": {
                "row_styles": [v[1] for v in versions_click_options if v is not None],
            },
        },
        {
            "name": "Advanced options",
            "options": ["--help"],
        },
    ],

}

@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    # invoke_without_command=True,
)
@click.version_option(__version__, "-V", "--version")
def cli() -> None:
    """Culting, a Python projects' manager."""



class MutuallyExclusiveOption(click.Option):
    """Mutually exclusive option."""

    def __init__(self, *args: t.Any, mutually_exclusive: list[str], **kwargs: t.Any) -> None: # noqa: ANN401
        """Init."""
        self.mutually_exclusive = set(mutually_exclusive)
        _help = kwargs.get("help", "")
        if self.mutually_exclusive:
            _mutually_exclusive = [f"--{e.replace('_', '-')}" for e in self.mutually_exclusive]
            ex_str = ", ".join(_mutually_exclusive)
            kwargs["help"] = _help + (
                "\bNOTE: This argument is mutually exclusive with "
                "arguments: [" + ex_str + "]."
            )
        super().__init__(*args, **kwargs)

    def handle_parse_result(
            self,
            ctx: click.Context,
            opts: t.Mapping[str, t.Any],
            args: list[str],
    ) -> tuple[t.Any, list[str]]:
        """Hadle parse result."""
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            _options = ", ".join(
                f"--{e.replace('_', '-')}"
                for e in self.mutually_exclusive
            )
            err_msg = f"Illegal usage: [{_options}] are mutually exclusive."
            raise click.UsageError(err_msg)
        return super().handle_parse_result( ctx, opts, args)



help_name = """\
Set the package name, PEP 8 and PEP 423 compliant.

\b
Defaults to directory name.
"""
help_python_version = """\
Select a specific python version via `{package_manager}`.
"""
help_python_version += f"""
\b
If not specified the `system` default '{python_system_version}' will be used.
"""

@cli.command()
@click.argument("path", type=click.Path(), default=".")
@click.option("--name", type=str, required=False, help=help_name)
@click.option(
    "--pyenv-python",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["py_python", "uv_python"],
    type=click.Choice(pyenv_versions),
    hidden=not pyenv_versions,
    required=False,
    help=help_python_version.format(package_manager="pyenv"),
)
@click.option(
    "--py-python",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["pyenv_python", "uv_python"],
    type=click.Choice(py_versions),
    hidden=not py_versions,
    required=False,
    help=help_python_version.format(package_manager="py"),
)
@click.option(
    "--uv-python",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["pyenv_python", "uv_python"],
    type=click.Choice(uv_versions),
    hidden=not uv_versions,
    required=False,
    help=help_python_version.format(package_manager="uv"),
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


@cli.command()
def review() -> None:
    """Review project settings."""
    logger.info(Pyenv().versions)
    logger.info(Uv().versions)
    logger.info(Py().versions)










