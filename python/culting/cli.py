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
)



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
            "name": "Developers Corner",
            "options": ["--python-version", "--venv", "--src"],
        },
        {
            "name": "Advanced Options",
            "options": ["--help"],
        },
    ],

}


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
            _mutually_exclusive = [self.name, *self.mutually_exclusive]
            _options = ", ".join(
                f"--{e.replace('_', '-')}"
                for e in _mutually_exclusive
            )
            err_msg = f"Illegal usage: [{_options}] are mutually exclusive."
            raise click.UsageError(err_msg)
        return super().handle_parse_result( ctx, opts, args)



@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(__version__, "-V", "--version")
def cli() -> None:
    """Culting, a Python projects' manager."""




py_default_ver = Python().version
# pyenv_vers = Pyenv().versions
# py_vers = Py().versions
# # uv_vers = Uv().versions
# choice_vers = sorted(
#     {py_default_ver, *pyenv_vers, *py_vers},
#     key=lambda v: int(v.split(".")[1]),
# )

@cli.command()
@click.argument("path", type=click.Path(), default=".")
@click.option(
    "-n", "--name",
    required=False,
    help="Set the package name, defaults to the directory name. Must be PEP 8 and PEP 423 compliant.",
)
@click.option(
    "-p", "--python-version",
    # type=click.Choice(choice_vers),
    default=py_default_ver,
    show_default=True,
    help="Specify a python version",
)
@click.option(
    "--venv",
    default=culting_conf.package.venv,
    show_default=True,
    help="Specify venv name.",
)
@click.option(
    "--src",
    default=culting_conf.package.src,
    show_default=True,
    help="Specify src folder name.",
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
    # from . import SupportedOs
    # logger.info(", ".join(f"'{o}'" for o in t.get_args(SupportedOs)))
    # logger.info(Python().version)
    # logger.info(Pyenv().versions)
    # logger.info(Py().versions)










