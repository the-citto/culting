"""CLI."""

import os
import pathlib
import re
import subprocess
import typing as t

import rich
import rich.align
import rich.panel
import rich_click as click
from rich_click import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter

from . import (
    __version__,
    click_commands,
    logger,
    platform_info,
)


click.rich_click.OPTION_GROUPS = {
    "culting": [
        {
            "name": "Advanced Options",
            "options": ["--wsl", "--debug", "--help", "--version"],
        },
    ],
}

click.rich_click.COMMAND_GROUPS = {
    "culting": [
        {
            "name": "Culting Commands",
            "commands": [
                "new",
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
    # logger.info(os.environ.get("PY_PYTHON"))
    if ctx.invoked_subcommand is None:
        ctx.get_help()


@cli.command()
@click.argument("project-name", type=str)
@click.option("-p", "--python-version", prompt=True)
@click.pass_context
def new(ctx: click.Context, python_version: str, project_name: str) -> None:
    """Create new culting project."""
    try:
        click_commands.NewProject(python_version, project_name)
    except click_commands.NewProjectError as err:
        logger.exception(err)
        ctx.abort()
    # project_dir = project_name.lower()
    # project_dir_re = re.match(r"[a-z][a-z0-9-_]+$", project_dir)
    # if project_dir_re is None:
    #     err_msg = f"Invalid project name: '{project_name}'"
    #     logger.error(err_msg)
    #     ctx.abort()
    # python_version_re = re.match(r"3.[\d]{1,2}t?$", python_version)
    # if python_version_re is None:
    #     err_msg = f"Invalid python version: '{python_version}'"
    #     logger.error(err_msg)
    #     ctx.abort()
    # if platform_info.os == "linux":
    #     pyenv_root = os.environ.get("PYENV_ROOT")
    #     if pyenv_root is None:
    #         raise RuntimeError
    #     pyenv_shim = pathlib.Path(pyenv_root) / f"shims/python{python_version}"
    #     if not pyenv_shim.exists():
    #         err_msg = f"Python version not found: '{python_version}'"
    #         logger.error(err_msg)
    #         ctx.abort()
    #     cmd = [pyenv_shim, "-V"]
    # elif platform_info.os == "win32":
    #     os.environ["PY_PYTHON"] = python_version
    #     cmd = [platform_info.python_manager, "-V"]
    # else:
    #     raise RuntimeError
    # _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
    # if _out.returncode != 0:
    #     logger.error(_out.stderr.strip())
    #     ctx.abort()
    # if _out.returncode == 0:
    #     pathlib.Path(".python-version").write_text(python_version)


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
    _forwarding(
        cmd=[platform_info.venv_python],
        ctx=ctx,
    )


@forwarding_command
@forwarding_argument
@click.pass_context
def pip(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
    """Pip.

    Ensure to run the `pip` executable inside the virtual environment `.venv`.
    """
    cmd = [platform_info.venv_python, "-m", "pip", "install", "--upgrade", "pip", "-q"]
    subprocess.call(cmd)
    _ = cmd_args
    _forwarding(
        cmd=[platform_info.venv_python, "-m", "pip"],
        ctx=ctx,
    )


@forwarding_command
@forwarding_argument
@click.pass_context
def pip_compile(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
    """Pip-compile."""
    _ = cmd_args
    _forwarding(
        cmd=[platform_info.venv_python, "-m", "piptools", "compile"],
        ctx=ctx,
    )


@forwarding_command
@forwarding_argument
@click.pass_context
def pip_sync(ctx: click.Context, cmd_args: t.Iterable[str]) -> None:
    """Pip-sync."""
    _ = cmd_args
    _forwarding(
        cmd=[platform_info.venv_python, "-m", "piptools", "sync"],
        ctx=ctx,
    )

# @cli.command(context_settings={"ignore_unknown_options": True})
# @click.argument("cmd_args", nargs=-1, type=click.UNPROCESSED)
# def pip(cmd_args: t.Iterable[str]) -> None:
#     """Project's pip."""
#     cmd = [platform_info.venv_python, "-m", "pip", "install", "--upgrade", "pip", "-q"]
#     subprocess.call(cmd)
#     cmd = [
#         platform_info.venv_python,
#         "-m", "pip",
#         *cmd_args,
#     ]
#     subprocess.call(cmd)
#
#
# @cli.command(context_settings={"ignore_unknown_options": True})
# @click.argument("cmd_args", nargs=-1, type=click.UNPROCESSED)
# def pip_compile(cmd_args: t.Iterable[str]) -> None:
#     """Pip-compile."""
#     cmd = [
#         platform_info.venv_python,
#         "-m", "piptools", "compile",
#         *cmd_args,
#     ]
#     subprocess.call(cmd)
#
#
# @cli.command(context_settings={"ignore_unknown_options": True})
# @click.argument("cmd_args", nargs=-1, type=click.UNPROCESSED)
# def pip_sync(cmd_args: t.Iterable[str]) -> None:
#     """Pip-sync."""
#     cmd = [
#         platform_info.venv_python,
#         "-m", "piptools", "sync",
#         *cmd_args,
#     ]
#     subprocess.call(cmd)






