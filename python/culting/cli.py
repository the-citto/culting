"""CLI."""

import logging
import re
import typing as t

import rich_click as click
from rich_click import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter

from .commands import (
    Py,
    Pyenv,
    Python,
)
from .defaults import culting_conf
from .exceptions import (
    CommandNotFoundError,
    InitError,
)
from .logger import logger
from .types import (
    InitKwargs,
    LicenseFile,
)
from .variables import (
    __os__,
    __version__,
)


click.rich_click.OPTION_GROUPS = {
    "culting": [
        {
            "name": "Advanced Options",
            "options": ["--debug", "--help", "--version"],
        },
    ],
    "culting init": [
        {
            "name": "Basic usage",
            "options": ["--name"],
        },
        {
            "name": "Package details",
            "options": [
                "--readme",
                "--license",
                "--src",
                "--venv",
            ],
        },
        {
            "name": "Developers Corner",
            "options": [
                "--python-path",
                "--python-version",
            ],
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
                "\b\n\nNOTE: This argument is mutually exclusive with "
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
                if e is not None
            )
            err_msg = f"Illegal usage: [{_options}] are mutually exclusive."
            raise click.UsageError(err_msg)
        return super().handle_parse_result( ctx, opts, args)


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
        "show_default": True,
    },
)
@click.version_option(__version__, "-V", "--version")
@click.option(
    "-d", "--debug",
    is_flag=True,
    help="Show debug messages.",
)
def cli(*, debug: bool) -> None:
    """Culting, a Python projects' manager."""
    if debug:
        stderr_handler = logging.getHandlerByName("stderr")
        if stderr_handler is not None:
            stderr_handler.setLevel(logging.DEBUG)
            click.echo()
            logger.debug("On.")


def _python_versions() -> tuple[str | None, str | None, list[str]]:
    _default_path: str | None
    try:
        if culting_conf.python.path:
            _default_path = culting_conf.python.path
            _default_ver = Python(binary_path=_default_path).version
        else:
            _python = Python()
            _default_path = _python.binary
            _default_ver = _python.version
    except CommandNotFoundError:
        _default_ver = None
        _default_path = None
    _pyenv_vers = Pyenv().versions
    _py_vers = Py().versions
    _choice_vers = {_default_ver, *_py_vers, *_pyenv_vers} if _default_ver is not None else {*_py_vers, *_pyenv_vers}
    _sorted_choice_vers = sorted(
        sorted(_choice_vers),
        key=lambda v: int(re.search(r"3\.(\d+)", v).group(1)), # type: ignore[union-attr]
    )
    return _default_ver, _default_path, _sorted_choice_vers

python_default_ver, python_default_path, python_choice_vers = _python_versions()


class _CommandCustomHelp(click.RichCommand):

    @t.override
    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:  # type: ignore[override]
        if python_default_ver is None:
            click.echo()
            logger.warning("No default Python version found")
        elif python_default_ver.endswith("t"):
            click.echo()
            logger.warning("The default Python version is a free-threading build")
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)


@cli.command(cls=_CommandCustomHelp)
@click.argument("path", type=click.Path(), default=".")
@click.option(
    "-n", "--name",
    required=False,
    help="Set the package name, defaults to the directory name. Must be PEP 8 and PEP 423 compliant.",
)
@click.option(
    "-v", "--python-version",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["python_path"],
    type=click.Choice(python_choice_vers),
    default=python_default_ver,
    show_default="None" if python_default_ver is None else True,
    help="Specify a python version",
)
@click.option(
    "-p", "--python-path",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["python_version"],
    type=click.Path(),
    default=python_default_path,
    show_default="None" if python_default_path is None else True,
    help="Specify path to a python binary",
)
@click.option("--venv", default=culting_conf.package.venv, help="Specify venv name.")
@click.option("--src", default=culting_conf.package.src, help="Specify src folder name.")
@click.option("--readme", default=culting_conf.package.readme, help="Specify README file name.")
@click.option(
    "--license", "license_template",
    default=culting_conf.package.license,
    type=click.Choice(t.get_args(LicenseFile)),
    help="Specify license.",
)
@click.pass_context
def init(ctx: click.Context, **kwargs: t.Unpack[InitKwargs]) -> None:
    """Init project."""
    logger.debug(kwargs)
    _python_version = kwargs.get("python_version")
    _python_path = kwargs.get("python_path")
    if _python_version is None and _python_path is None:
        err_msg = "no default python binary found, and none specified"
        logger.debug(err_msg)
        raise click.UsageError(err_msg)
    if _python_version is not None and _python_version != python_default_ver:
        try:
            if __os__ == "linux":
                kwargs["python_path"] = Pyenv().get_version_path(version=_python_version)
            elif __os__ == "win32":
                kwargs["python_path"] = Py().get_version_path(version=_python_version)
        except CommandNotFoundError as err:
            logger.error(err)
            ctx.abort()
    logger.debug(kwargs)
    from .init import Init
    try:
        Init(**kwargs)
    except (
        InitError,
        CommandNotFoundError,
    ) as err:
        logger.error(err)
        ctx.abort()



# # @cli.command(cls=CommandWarning)
# @cli.command()
# def review() -> None:
#     """Review project settings."""
#     # from . import SupportedOs
#     # logger.info(", ".join(f"'{o}'" for o in t.get_args(SupportedOs)))
#     # logger.info(Python().version)
#     # logger.info(Pyenv().versions)
#     # logger.info(Py().versions)










