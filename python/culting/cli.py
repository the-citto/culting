"""CLI."""

import abc
import os
import pathlib
import shutil
import subprocess
import typing as t

import click



class CommandNotFoundError(ImportError):
    """Binary not found."""

class InitWarning(Warning):
    """Init warning."""

    def __init__(self, message: str, /, output: str | None = None) -> None:
        """Init."""
        super().__init__(message)
        self.output = output


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
    # if git_path is None and sys.platform == "linux":
    #     git_path = "git"
    try:
        init_git_msg = Git(git_path).init()
        if init_git_msg is not None:
            click.secho(init_git_msg, fg="green")
    except CommandNotFoundError as err:
        click.secho(err.__class__.__name__, fg="red", nl=False)
        click.echo(f": {err}")
    except subprocess.CalledProcessError as err:
        click.secho(err.__class__.__name__, fg="red", nl=False)
        click.echo(f": {err}")
        click.echo(err.output)
    except InitWarning as warn:
        click.secho(warn.__class__.__name__, fg="yellow", nl=False)
        click.echo(f": {warn}")
        click.echo(warn.output)





class Command(abc.ABC):
    """Abstract class for commands."""

    binary: os.PathLike | str

    def __init__(self, command_name: os.PathLike | str | None = None, /) -> None:
        """Init."""
        if command_name is not None:
            self.binary = command_name
        self._verify_command()

    def _verify_command(self) -> None:
        self.binary_path = shutil.which(self.binary)
        if self.binary_path is None:
            err_msg = f"'{self.binary}' not found."
            raise CommandNotFoundError(err_msg)

    def _run_command(self, command_args: t.Iterable[str] = ()) -> str:
        process_command = [str(self.binary_path), *command_args]
        process = subprocess.Popen(
            process_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        if stderr:
            err_msg = stderr.decode("utf-8")
            raise subprocess.CalledProcessError(returncode=1, cmd=" ".join(process_command), output=err_msg)
        return stdout.decode("utf-8")

    @abc.abstractmethod
    def init(self) -> str:
        """Run command for project init."""


class Git(Command):
    """Git."""

    binary = "git"

    def init(self) -> str:
        """Init git repo if not present."""
        if pathlib.Path(".git").is_dir():
            warn_msg = "This is already a Git repository."
            warn_output = "Verify if the project needs to be initialized.\n"
            raise InitWarning(warn_msg, output=warn_output)
        return self._run_command(command_args=["init"])



# git = Git(command_name="foo")
# git = Git()
# git.init()
# Git("/usr/bin/git").init()






# def init_git(bin_path: str) -> str | None:
#     """Init Git."""
#     if pathlib.Path(".git").is_dir():
#         return None
#     _bin_path = shutil.which(bin_path)
#     if _bin_path is None:
#         err_msg = f"'{bin_path}' not found."
#         raise CommandNotFoundError(err_msg)
#     command = [_bin_path, "init"]
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()
#     if stderr:
#         err_msg = stderr.decode("utf-8")
#         raise subprocess.CalledProcessError(returncode=1, cmd=" ".join(command), output=err_msg)
#     return stdout.decode("utf-8")







