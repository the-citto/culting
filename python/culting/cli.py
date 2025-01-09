"""CLI."""

import importlib.metadata
import os
import typing as t

import rich_click as click
from rich_click import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter

from . import core
from .type_defs import InitKwargs


__version__ = importlib.metadata.version("culting")


click.rich_click.OPTION_GROUPS = {
    "culting": [
        {
            "name": "Advanced Options",
            "options": ["--wsl", "--debug", "--help", "--version"],
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
    "culting dev": [
        {
            "name": "Advanced Options",
            "options": ["--debug", "--help"],
        },
    ],
    "culting run": [
        {
            "name": "Advanced Options",
            "options": ["--debug", "--help"],
        },
    ],
    "culting install": [
        {
            "name": "Advanced Options",
            "options": ["--debug", "--help"],
        },
    ],
    "culting test": [
        {
            "name": "Advanced Options",
            "options": ["--debug", "--help"],
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


class CustomGroup(click.RichGroup):
    """Custom group."""

    # def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
    #     super().__init__(*args, **kwargs)
    #     print(self.context_class)

    # def __init__(
    #     self,
    #     name: t.Optional[str] = None,
    #     commands: t.Optional[
    #         t.Union[t.MutableMapping[str, Command], t.Sequence[Command]]
    #     ] = None,
    #     **attrs: t.Any,
    # ) -> None:
    #     super().__init__(name, **attrs)
    #
    #     if commands is None:
    #         commands = {}
    #     elif isinstance(commands, abc.Sequence):
    #         commands = {c.name: c for c in commands if c.name is not None}
    #
    #     #: The registered subcommands by their exported names.
    #     self.commands: t.MutableMapping[str, Command] = commands


#     def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
#         """Init."""
# #         self.mutually_exclusive = set(mutually_exclusive)
# #         _help = kwargs.get("help", "")
# #         if self.mutually_exclusive:
# #             _mutually_exclusive = [f"--{e.replace('_', '-')}" for e in self.mutually_exclusive]
# #             ex_str = ", ".join(_mutually_exclusive)
# #             kwargs["help"] = _help + (
# #                 "\b\n\nNOTE: This argument is mutually exclusive with "
# #                 "arguments: [" + ex_str + "]."
# #             )
#         print(kwargs)
#         # print(kwargs.get("wsl"))
#         super().__init__(*args, **kwargs)

    # def list_commands(self, ctx: Context) -> t.List[str]:
    #     return super().list_commands(ctx)

    # def get_command(self, ctx: click.Context, cmd_name: str) -> t.Optional[click.Command]:
    #     # print(cmd_name)
    #     print(ctx)
    #     print(self.context_class)
    #     # if not ctx.params.get("wsl", False):
    #     #     return self.commands.get(cmd_name)
    #     # if cmd_name == "init" and ctx.params.get("wsl", False):
    #     #     # print("wsl")
    #     #     _cmd = self.commands.get(cmd_name)
    #     #     if _cmd is not None:
    #     #         for param in _cmd.params:
    #     #             if param.name == "python_version":
    #     #                 param.default = "foo"
    #     #                 param.show_default = True
    #     #                 param.type=click.Choice(["3.11", "3.12"])
    #     #                 # type=click.Choice(python_choice_vers),
    #     #                 # show_default="None" if python_default_ver is None else True,
    #     #                 # default=python_default_ver,
    #     #                 # print(dir(param))
    #     # # print(dir(self.commands.get(cmd_name)))
    #     return self.commands.get(cmd_name)


    def invoke(self, ctx: click.Context):
        print(self.commands)
    #     print(ctx.params)
        print(ctx)
    #     # print(ctx.invoked_subcommand)
        super().invoke(ctx)
    # #     print(ctx.invoked_subcommand)
    # #     print("invoke")
    #
    # def add_command(self, cmd: click.Command, name: str | None = None) -> None:
    #     """Customize add_command."""
    #     click.Group.add_command(self, cmd, name=name)
    #     # print(self.ctx)
    #     self.invoke_without_command = True
    #     self.context_settings = {
    #         "help_option_names": ["-h", "--help"],
    #         "show_default": True,
    #     }
    #     # print("add_command")
    # #     print(self.name)
    # #     for param in self.params:
    # #         if param.name == "wsl" and cmd.name == "init":
    # #             print(param.name)
    # #             print(self)
    # #             # print(cmd)
    # #             # print(cmd.invoke)
    # #             # # print(dir(param))
    # #             # print(param.to_info_dict())
    #             # # print(param.valu)
    #     # if cmd.name == "init":
    #     #     print(cmd.name)
    #     #     print(cmd.params)
    #
    #     # name = name or cmd.name
    #     # if name is None:
    #     #     err_msg = "Command has no name."
    #     #     raise TypeError(err_msg)
    #     # # _check_multicommand(self, name, cmd, register=True)
    #     # self.commands[name] = cmd



@click.group(
    cls=CustomGroup,
    invoke_without_command=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "show_default": True,
    },
)
@click.version_option(__version__, "-V", "--version")
@click.option("-d", "--debug", is_flag=True, help="Show debug messages.")
@click.option(
    "-w", "--wsl",
    is_flag=True,
    hidden=not(core.__os__ == "linux" and "WSL" in os.uname().release),
    help="Special usage for Windows projects from WSL.")
@click.pass_context
def cli(ctx: click.Context, *, debug: bool, wsl: bool) -> None:
    """Culting, a Python projects' manager."""
    print(ctx.params)
    if wsl:
        core.__os__ = "wsl"
    core_ = core.Core()
    click.echo(core_.xdg_config_home)
    click.echo(core_.xdg_state_home)
    # print(ctx)
    if ctx.invoked_subcommand is None:
        ctx.get_help()
#     if debug:
#         stderr_handler = logging.getHandlerByName("stderr")
#         if stderr_handler is not None:
#             stderr_handler.setLevel(logging.DEBUG)
#             logger.debug("On.")



# def _python_versions() -> tuple[str | None, str | None, list[str]]:
#     _default_path: str | None
#     try:
#         if culting_conf.python.path:
#             _default_path = culting_conf.python.path
#             _default_ver = Python(binary_path=_default_path).version
#         else:
#             _python = Python()
#             _default_path = _python.binary
#             _default_ver = _python.version
#     except CommandNotFoundError:
#         _default_ver = None
#         _default_path = None
#     _pyenv_vers = Pyenv().versions
#     _py_vers = Py().versions
#     _choice_vers = {_default_ver, *_py_vers, *_pyenv_vers} if _default_ver is not None else {*_py_vers, *_pyenv_vers}
#     _sorted_choice_vers = sorted(
#         sorted(_choice_vers),
#         key=lambda v: int(re.search(r"3\.(\d+)", v).group(1)), # type: ignore[union-attr]
#     )
#     return _default_ver, _default_path, _sorted_choice_vers

# python_default_ver, python_default_path, python_choice_vers = _python_versions()

class _CommandCustomHelp(click.RichCommand):

    # @t.override
    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:  # type: ignore[override]
        # if python_default_ver is None:
        #     logger.warning("No default Python version found")
        # elif python_default_ver.endswith("t"):
        #     logger.warning("The default Python version is a free-threading build")
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
    # type=click.Choice(python_choice_vers),
    # default=python_default_ver,
    # show_default="None" if python_default_ver is None else True,
    help="Specify a python version",
)
@click.option(
    "-p", "--python-path",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["python_version"],
#     type=click.Path(),
#     default=python_default_path,
#     show_default="None" if python_default_path is None else True,
    help="Specify path to a python binary",
)
@click.option(
    "--venv",
    # default=culting_conf.package.venv,
    help="Specify venv name.",
)
@click.option(
    "--src",
    # default=culting_conf.package.src,
    help="Specify src folder name.",
)
@click.option(
    "--readme",
    # default=culting_conf.package.readme,
    help="Specify README file name.",
)
@click.option(
    "--license", "license_template",
#     default=culting_conf.package.license,
#     type=click.Choice(t.get_args(LicenseFile)),
    help="Specify license.",
)
@click.pass_context
def init(
    ctx: click.Context,
    path: str,
    **kwargs: t.Unpack[InitKwargs],
) -> None:
    """Init project."""
#     logger.debug(kwargs)
#     _python_version = kwargs.get("python_version")
#     _python_path = kwargs.get("python_path")
#     if _python_version is None and _python_path is None:
#         err_msg = "no default python binary found, and none specified"
#         logger.error(err_msg)
#         ctx.abort()
#     if _python_version is not None and _python_version != python_default_ver:
#         try:
#             if __os__ == "linux":
#                 kwargs["python_path"] = Pyenv().get_version_path(version=_python_version)
#             elif __os__ == "win32":
#                 kwargs["python_path"] = Py().get_version_path(version=_python_version)
#         except CommandNotFoundError as err:
#             logger.error(err)
#             ctx.abort()
#     logger.debug(kwargs)
#     from .init import Init
#     try:
#         Init(**kwargs)
#     except (
#         InitError,
#         CommandNotFoundError,
#     ) as err:
#         logger.error(err)
#         ctx.abort()
#
#
#
# # @cli.command(context_settings={"ignore_unknown_options": True})
# # @click.pass_context
# # def dev(ctx: click.Context) -> None:
# #     """Set up developement environment."""
# #     from .exceptions import PackageError
# #     try:
# #         from .package.dev import Dev
# #         Dev()
# #     except (PackageError, RunError) as err:
# #         logger.error(err)
# #         ctx.abort()
#
#
#
# @cli.command(context_settings={"ignore_unknown_options": True})
# @click.argument("package_args", nargs=-1, type=click.UNPROCESSED)
# @click.pass_context
# def run(ctx: click.Context, package_args: tuple[str, ...]) -> None:
#     """Run package."""
#     from .exceptions import PackageError
#     try:
#         from .package.run import Run
#         Run(package_args)
#     except (PackageError, RunError) as err:
#         logger.error(err)
#         ctx.abort()
#
#
#
# @cli.command(context_settings={"ignore_unknown_options": True})
# @click.argument("libraries", nargs=-1, required=True, type=click.UNPROCESSED)
# @click.pass_context
# def install(ctx: click.Context, libraries: tuple[str, ...]) -> None:
#     """Install libraries."""
#     from .exceptions import PackageError
#     try:
#         from .package.install import Install
#         Install(libraries)
#     except PackageError as err:
#         logger.error(err)
#         ctx.abort()


@cli.command()
@click.pass_context
def test(ctx: click.Context) -> None:
    """Test package."""
#     from .exceptions import PackageError
#     try:
#         from .package.test import Test
#         Test()
#     except PackageError as err:
#         logger.error(err)
#         ctx.abort()




# import logging
# import re
# import typing as t

# from rich_click import RichContext
# from rich_click.rich_help_formatter import RichHelpFormatter
#
# from .commands import (
#     Py,
#     Pyenv,
#     Python,
# )
# from .defaults import culting_conf
# from .exceptions import (
#     CommandNotFoundError,
#     InitError,
#     RunError,
# )
# from .logger import logger
# from .types import (
#     InitKwargs,
#     LicenseFile,
# )
# from .variables import (
#     __os__,
#     __version__,
# )




