"""CLI."""

import pathlib
import subprocess
import typing as t

import rich
import rich.align
import rich.panel
import rich_click as click
from rich_click import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter

from . import (
    ExecutableNotFoundError,
    __version__,
    click_commands,
    logger,
    platform_info,
)


# click.rich_click.OPTION_GROUPS = {
#     "culting": [
#         {
#             "name": "Advanced Options",
#             "options": ["--wsl", "--debug", "--help", "--version"],
#         },
#     ],
# }

click.rich_click.COMMAND_GROUPS = {
    "culting": [
        {
            "name": "Commands",
            "commands": [
                "new",
                "dependencies",
            ],
        },
        {
            "name": "Forwarded commands",
            "commands": [
                "git",
                "python",
                "pyenv",
                "py",
                "pip",
                "pip-compile",
                "pip-sync",
            ],
        },
    ],
}

class _CommandCustomHelp(click.RichCommand):

    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        # self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)


@click.group(
    invoke_without_command=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "show_default": True,
    },
)
@click.version_option(__version__, "-V", "--version")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Culting, a Python projects' manager."""
    if ctx.invoked_subcommand is None:
        ctx.get_help()


@cli.command()
@click.argument("project-name", type=str)
@click.option(
    "-p", "--python-version",
    prompt=True,
    help="The python version to use for the new project.\b\n\nExample: 3.13",
)
@click.option(
    "-s", "--src",
    default="src",
    help="The default `src` could be an issue for multilanguage projects.",
)
@click.pass_context
def new(ctx: click.Context, **kwargs: t.Unpack[click_commands.NewProjectKwargs]) -> None:
    """Create new culting project.

    PROJECT_NAME must be PEP 8 and PEP 423 compliant.
    """
    try:
        click_commands.NewProject(**kwargs)
        logger.info(f"[green]Success.[/green]\n  Run [white]cd {kwargs.get('project_name')}[/white]\n\nEnjoy coding.")
    except click_commands.CommandError as err:
        logger.exception(err)
        ctx.abort()


# @cli.group(invoke_without_command=True)
# @click.pass_context
# def dependencies(ctx: click.Context) -> None:
#     """Dependencies management."""
#     if ctx.invoked_subcommand is None:
#         ctx.get_help()

@cli.group()
def dependencies() -> None:
    """Dependencies management."""


@dependencies.command(name="list")
def list_() -> None:
    """List libraries."""
    logger.info(click_commands.Dependencies().list_)


@dependencies.command(name="add")
@click.argument("libraries", nargs=-1)
def add_(libraries: tuple[str, ...]) -> None:
    """Add libraries."""
    try:
        click_commands.Dependencies().add(libraries)
    except click_commands.CommandError as err:
        logger.error(err)


forwarding_command = cli.command(
    cls=_CommandCustomHelp,
    context_settings={
        "ignore_unknown_options": True,
        "help_option_names": ["--hidden"],
    },
)
forwarding_argument = click.argument("cmd_args", nargs=-1, type=click.UNPROCESSED)

def _forwarding(
    cmd: t.Iterable[pathlib.Path | str],
    ctx: click.Context,
) -> None:
    cmd_args = ctx.params.get("cmd_args", ())
    cmd = [*cmd, *cmd_args]
    _out = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )
    if _out.returncode == 0:
        msg = _out.stdout.strip()
        title = "Out"
        msg_color = "white"
    else:
        msg = _out.stderr.strip()
        title = "Error"
        msg_color = "red"
    if "-h" in cmd_args or "--help" in cmd_args or "help" in cmd_args or not cmd_args:
        ctx.get_help()
    cmd_name = ctx.command.name
    panel = rich.panel.Panel(
        msg,
        title=f"{cmd_name} {title}".title(),
        border_style=msg_color,
        title_align="left",
    )
    rich.print(panel)
    if _out.returncode != 0:
        ctx.abort()



if platform_info.os == "linux":
    @forwarding_command
    @forwarding_argument
    @click.pass_context
    def pyenv(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
        """Pyenv."""
        _ = cmd_args
        _forwarding(
            cmd=[platform_info.python_manager],
            ctx=ctx,
        )
elif platform_info.os == "win32":
    @forwarding_command
    @forwarding_argument
    @click.pass_context
    def py(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
        """Py launcher."""
        _ = cmd_args
        _forwarding(
            cmd=[platform_info.python_manager],
            ctx=ctx,
        )


@forwarding_command
@forwarding_argument
@click.pass_context
def python(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
    """Python.

    Ensure to run the `python` executable inside the virtual environment `.venv`.
    """
    _ = cmd_args
    _forwarding(cmd=[platform_info.venv_python], ctx=ctx)


@forwarding_command
@forwarding_argument
@click.pass_context
def pip(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
    """Pip.

    Ensure to run the `pip` executable inside the virtual environment `.venv`.
    """
    try:
        cmd = [platform_info.venv_python, "-m", "pip", "install", "--upgrade", "pip", "-q"]
        subprocess.call(cmd)
        _ = cmd_args
        _forwarding(cmd=[platform_info.venv_python, "-m", "pip"], ctx=ctx)
    except ExecutableNotFoundError as err:
        logger.exception(err)


@forwarding_command
@forwarding_argument
@click.pass_context
def pip_compile(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
    """Pip-compile."""
    _ = cmd_args
    _forwarding(cmd=[platform_info.venv_python, "-m", "piptools", "compile"], ctx=ctx)


@forwarding_command
@forwarding_argument
@click.pass_context
def pip_sync(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
    """Pip-sync."""
    _ = cmd_args
    _forwarding(cmd=[platform_info.venv_python, "-m", "piptools", "sync"], ctx=ctx)






