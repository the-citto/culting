"""CLI."""

import os
import shutil
import subprocess
import typing as t

import click
import pygit2

from . import __version__



class CommandNotFoundError(ImportError):
    """Binary not found."""

class InitWarning(Warning):
    """Init warning."""

    def __init__(self, message: str, /, output: str | None = None) -> None:
        """Init."""
        super().__init__(message)
        self.output = output


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(__version__, "-V", "--version")

def cli() -> None:
    """Cli."""


@cli.command()
@click.argument("project-path", type=click.Path())
def init(project_path: str) -> None:
    """Init project."""
    # pygit2.init_repository(path=project_path)
    Pyenv()
    # if git_path is None and sys.platform == "linux":
    #     git_path = "git"
    # try:
    #     init_git_msg = Git(git_path).init()
    #     if init_git_msg is not None:
    #         click.secho(init_git_msg, fg="green")
    # except CommandNotFoundError as err:
    #     click.secho(err.__class__.__name__, fg="red", nl=False)
    #     click.echo(f": {err}")
    # except subprocess.CalledProcessError as err:
    #     click.secho(err.__class__.__name__, fg="red", nl=False)
    #     click.echo(f": {err}")
    #     click.echo(err.output)
    # except InitWarning as warn:
    #     click.secho(warn.__class__.__name__, fg="yellow", nl=False)
    #     click.echo(f": {warn}")
    #     click.echo(warn.output)




class Command:
    """Command."""

    binary: os.PathLike | str

    def _verify_command(self) -> None:
        binary_path = shutil.which(self.binary)
        if binary_path is None:
            err_msg = f"'{self.binary}' not found."
            raise CommandNotFoundError(err_msg)

    def _run_command(self, *, command_args: t.Iterable[str] = ()) -> str:
        process_command = [str(self.binary), *command_args]
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


class Pyenv(Command):
    """Pyenv."""

    binary = "pyenv"

    def __init__(self) -> None:
        """Init."""
        self._verify_command()
        command_args = ["versions"]
        print(self._run_command(command_args=command_args))


    # def init_project(self) -> str:
    #     """Init."""
    #     return ""



# class Command(abc.ABC):
#     """Abstract class for commands."""
#
#     binary: os.PathLike | str
#
#     def __init__(self, binary: os.PathLike | str | None = None, /) -> None:
#         """Init."""
#         if binary is not None:
#             self.binary = binary
#         self._verify_command()
#
#     def _verify_command(self) -> None:
#         binary_path = shutil.which(self.binary)
#         if binary_path is None:
#             err_msg = f"'{self.binary}' not found."
#             raise CommandNotFoundError(err_msg)
#
#     def _run_command(self, *, command_args: t.Iterable[str] = ()) -> str:
#         process_command = [str(self.binary), *command_args]
#         process = subprocess.Popen(
#             process_command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )
#         stdout, stderr = process.communicate()
#         if stderr:
#             err_msg = stderr.decode("utf-8")
#             raise subprocess.CalledProcessError(returncode=1, cmd=" ".join(process_command), output=err_msg)
#         return stdout.decode("utf-8")
#
#     @abc.abstractmethod
#     def init(self) -> str:
#         """Run command for project init."""





# class Git(Command):
#     """Git."""
#
#     binary = "git"
#
#     def init(self) -> str:
#         """Init git repo if not present."""
#         command_args=["init"]
#         if pathlib.Path(".git").is_dir():
#             warn_msg = "This is already a Git repository."
#             stdout = self._run_command(command_args=command_args)
#             raise InitWarning(warn_msg, output=stdout)
#         return self._run_command(command_args=command_args)








