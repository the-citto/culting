"""CLI."""

import subprocess
import typing as t

import rich_click as click

from . import (
    CommandNotFoundError,
    InitError,
    InitKwargs,
    __version__,
    culting_conf,
    logger,
)
from .commands import (
    Py,
    Pyenv,
    Python,
    Uv,
)



advanced_use = {
    "name": "Advanced options",
    "options": ["--help"],
}
click.rich_click.OPTION_GROUPS = {
    "culting": [
        {
            "name": "Advanced Options",
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
            "name": "Python Versions",
            "options": ["--default", "--pyenv", "--py", "--uv"],
            "table_styles": {
                "row_styles": ["white", "bright_green", "bright_blue", "bright_magenta"],
            },
        },
        {
            "name": "Development",
            "options": ["--venv", "--src"],
        },
        {
            "name": "Advanced Options",
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
        print(opts)
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            _mutually_exclusive = [self.name, *self.mutually_exclusive]
            _options = ", ".join(
                f"--{e.replace('_', '-')}"
                for e in _mutually_exclusive
            )
            err_msg = f"Illegal usage: [{_options}] are mutually exclusive."
            raise click.UsageError(err_msg)
        return super().handle_parse_result( ctx, opts, args)



python_system_version = Python().version
pyenv_versions = Pyenv().versions
py_versions = Py().versions
uv_versions = Uv().versions

help_name = """\
Set the package name, PEP 8 and PEP 423 compliant.

\b
Defaults to directory name.
"""
help_python_version = """\
Specify a python version via `{package_manager}`
\b

"""

@cli.command()
@click.argument("path", type=click.Path(), default=".")
@click.option("--name", type=str, required=False, help=help_name)
@click.option(
    "--default",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["pyenv", "py", "uv"],
    is_flag=True,
    help=f"Default `system` python '{python_system_version}'\n\n\b",
)
@click.option(
    "--pyenv",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["default", "py", "uv"],
    type=click.Choice(pyenv_versions),
    required=False,
    help=help_python_version.format(package_manager="pyenv"),
)
@click.option(
    "--py",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["default", "pyenv", "uv"],
    type=click.Choice(py_versions),
    required=False,
    help=help_python_version.format(package_manager="py"),
)
@click.option(
    "--uv",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["default", "pyenv", "py"],
    type=click.Choice(uv_versions),
    required=False,
    help=help_python_version.format(package_manager="uv"),
)
@click.option(
    "--venv",
    default=culting_conf.package.venv,
    show_default=True,
    help="Specify `venv` name.",
)
@click.option(
    "--src",
    default=culting_conf.package.src,
    show_default=True,
    help="Specify `src` folder name.",
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










