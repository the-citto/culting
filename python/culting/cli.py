"""CLI."""

import pathlib
import shutil
import subprocess
import sys

import click



class BinaryNotFoundError(ImportError):
    """Binary not found."""



@click.group()
def cli() -> None:
    """Cli."""


git_path_help = """
\b
Specify Git binary path if not present in $PATH.
Use this also when working in WSL and need to use Windows' git.exe.
"""
@cli.command()
@click.option("--git-path", type=str, help=git_path_help)
def init(git_path: str) -> None:
    """Init project."""
    if git_path is None and sys.platform == "linux":
        git_path = "git"
    try:
        init_git_msg = init_git(git_path)
        if init_git_msg is not None:
            click.secho(init_git_msg, fg="green")
    except BinaryNotFoundError as err:
        click.secho(err.__class__.__name__, fg="red", nl=False)
        click.echo(f": {err}")
    except subprocess.CalledProcessError as err:
        click.secho(err.__class__.__name__, fg="red", nl=False)
        click.echo(f": {err}")
        click.echo(err.output)





def init_git(bin_path: str) -> str | None:
    """Init Git."""
    if pathlib.Path(".git").is_dir():
        return None
    _bin_path = shutil.which(bin_path)
    if _bin_path is None:
        err_msg = f"'{bin_path}' not found."
        raise BinaryNotFoundError(err_msg)
    command = [_bin_path, "init"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        err_msg = stderr.decode("utf-8")
        raise subprocess.CalledProcessError(returncode=1, cmd=" ".join(command), output=err_msg)
    return stdout.decode("utf-8")







