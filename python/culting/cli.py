"""CLI."""

import re
import subprocess
import typing as t

import rich_click as click
from rich_click import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter

from . import (
    CommandNotFoundError,
    InitError,
    InitKwargs,
    __os__,
    __version__,
    culting_conf,
    logger,
)
from .commands import (
    Py,
    Pyenv,
    Python,
)



def _python_versions() -> tuple[str | None, list[str]]:
    try:
        _python_path = culting_conf.python.path
        _default_ver = Python(binary_path=_python_path or None).version
    except CommandNotFoundError:
        _default_ver = None
    # pyenv_vers = Pyenv().versions
    _py_vers = Py().versions
    _choice_vers = {_default_ver, *_py_vers} if _default_ver is not None else {*_py_vers}
    _sorted_choice_vers = sorted(
        sorted(_choice_vers),
        key=lambda v: (
            int(re.search(r"3\.(\d+)", v).group(1)), # pyright: ignore reportOptionalMemberAccess
        ),
    )
    return _default_ver, _sorted_choice_vers

python_default_ver, python_choice_vers = _python_versions()



class _CommandCustomHelp(click.RichCommand):

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
            )
            err_msg = f"Illegal usage: [{_options}] are mutually exclusive."
            raise click.UsageError(err_msg)
        return super().handle_parse_result( ctx, opts, args)



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
            "options": ["--python-version", "--python-path", "--venv", "--src"],
        },
        {
            "name": "Advanced Options",
            "options": ["--help"],
        },
    ],

}


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(__version__, "-V", "--version")
# @click.pass_context
# def cli(ctx: click.Context) -> None:
def cli() -> None:
    """Culting, a Python projects' manager."""



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
    # default=f"{python_default_ver}",
    default=python_default_ver,
    show_default=True,
    help="Specify a python version",
)
@click.option(
    "-p", "--python-path",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["python_version"],
    type=click.Path(),
    default=culting_conf.python.path,
    show_default=True,
    help="Specify path to a python binary",
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
    print(kwargs)
    if kwargs.get("python_version") is None and not kwargs.get("python_path"):
        err_msg = "no default python binary found, and none specified"
        logger.debug(err_msg)
        raise click.UsageError(err_msg)
    _python_version = kwargs.get("python_version")
    if _python_version != python_default_ver:
        try:
            if __os__ == "win32":
                kwargs["python_path"] = Py().get_version_path(version=_python_version)
        except CommandNotFoundError as err:
            logger.error(err)
            ctx.abort()

    # try:
    #     _python_path = culting_conf.python.path
    #     _default_ver = Python(binary_path=_python_path or None).version
    # except CommandNotFoundError:
    #     _default_ver = None

    # print(kwargs)
    # print(f"{kwargs.get('python_path') == culting_conf.python.path = }")
    # print(f"{kwargs.get('python_version') == python_default_ver = }")
    # from .init import Init
    # try:
    #     Init(**kwargs)
    # except (
    #     InitError,
    #     subprocess.CalledProcessError,
    #     CommandNotFoundError,
    # ) as err:
    #     logger.error(err)
    #     ctx.abort()



# @cli.command(cls=CommandWarning)
@cli.command()
def review() -> None:
    """Review project settings."""
    # from . import SupportedOs
    # logger.info(", ".join(f"'{o}'" for o in t.get_args(SupportedOs)))
    # logger.info(Python().version)
    # logger.info(Pyenv().versions)
    # logger.info(Py().versions)










