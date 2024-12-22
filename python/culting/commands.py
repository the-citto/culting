"""
Commands.

First iteration of `culting` uses only `subprocess` calls,
this will allow calling various commands with their subcommands and options
with the feature of verifying that they are run within the project scope

Click reference:
    https://click.palletsprojects.com/en/stable/advanced/#forwarding-unknown-options
"""

import abc
import pathlib
import re
import shutil
import subprocess
import typing as t

from . import (
    CommandNotFoundError,
    InitError,
    __os__,
    logger,
)



class Command(abc.ABC):
    """Command."""

    def __init__(self) -> None:
        """Init."""
        self.binary = shutil.which(self.binary_name)
        if self.binary is None:
            err_msg = " ".join(self.binary_name)
            raise CommandNotFoundError(err_msg)

    @property
    @abc.abstractmethod
    def binary_name(self) -> str:
        """Binary name or fully qualified path."""

    def execute(self, command: list[t.Any]) -> str:
        """Execute."""
        _command = [self.binary, *command]
        proc = subprocess.Popen(
            _command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()
        if stderr:
            err_msg = stderr.decode("utf-8")
            raise subprocess.CalledProcessError(returncode=1, cmd=" ".join(map(str, command)), output=err_msg)
        return stdout.decode("utf-8")


class Python(Command):
    """Python."""

    @property
    def binary_name(self) -> str:
        """Binary name or fully qualified path."""
        _python = shutil.which("python")
        if _python is not None:
            return _python
        _py = shutil.which("py")
        if _py is not None:
            proc = subprocess.Popen(
                [_py, "--list-paths"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = proc.communicate()
            if stderr:
                err_msg = stderr.decode("utf-8")
                raise subprocess.CalledProcessError(returncode=1, cmd=" ".join(map(str, command)), output=err_msg)
            _stdout = stdout.decode("utf-8")
            _python_path_re = re.search(r"\* *([a-zA-Z]{1}:\\.*python.exe)", _stdout)
            if _python_path_re is not None:
                return _python_path_re.group(1)

        err_msg = "Python not found."
        raise CommandNotFoundError(err_msg)

    @property
    def version(self) -> str:
        """Version."""
        version_output = self.execute(["--version"])
        version_re = re.search(r"(3\.\d+)", version_output)
        if version_re is None:
            err_msg = "Python version not found"
            raise RuntimeError(err_msg)
        return version_re.group()


class PythonManager(Command, abc.ABC):
    """Python manager."""

    def __init__(self) -> None:
        """Init."""
        try:
            super().__init__()
        except CommandNotFoundError:
            self.binary = None

    @property
    def versions(self) -> list[str]:
        """Available versions."""
        if self.binary is None:
            return []
        versions_output = self.execute(self.versions_command)
        versions = re.findall(r"(3\.\d+)", versions_output)
        return sorted(
            set(versions),
            key=lambda v: int(v.split(".")[1]),
        )

    @property
    @abc.abstractmethod
    def versions_command(self) -> list[str]:
        """Command and options to get versions."""

class Pyenv(PythonManager):
    """Pyenv."""

    @property
    def binary_name(self) -> str:
        """Binary name or fully qualified path."""
        return "pyenv"

    @property
    def versions_command(self) -> list[str]:
        """Command and options to get versions."""
        return ["versions", "--skip-envs"]


class Py(PythonManager):
    """Py."""

    @property
    def binary_name(self) -> str:
        """Binary name or fully qualified path."""
        return "py"

    @property
    def versions_command(self) -> list[str]:
        """Command and options to get versions."""
        return ["--list-paths"]


class Uv(PythonManager):
    """Uv."""

    @property
    def binary_name(self) -> str:
        """Binary name or fully qualified path."""
        return "uv"

    @property
    def versions_command(self) -> list[str]:
        """Command and options to get versions."""
        return ["python", "list", "--only-installed"]






# class SysPython(Command):
#     """System python."""
#
#     def __init__(self, python_version: str) -> None:
#         """Init."""
#         self.python_version = python_version
#         super().__init__()
#
#     @property
#     def binary_name(self) -> str:
#         """Pyenv binary."""
#         if __os__ == "linux":
#             return f"python{self.python_version}"
#         if __os__ == "win32":
#             raise NotImplementedError
#             # return "py"
#         raise NotImplementedError
#
#     @property
#     def version(self) -> str:
#         """Return major.minor python version."""
#         command = ["--version"]
#         stdout = self.execute(command)
#         major_minor_re = re.search(r"Python (3.[0-9]+).", stdout)
#         if major_minor_re is None:
#             err_msg = f"Unexpected output '{stdout}"
#             raise InitError(err_msg)
#         _version = major_minor_re.group(1)
#         if _version in t.get_args(str):
#             version= t.cast(str, major_minor_re.group(1))
#         else:
#             err_msg = f"Invalid Python version '{_version}'"
#             raise InitError(err_msg)
#         if version != self.python_version:
#             self.__init__(python_version=version)
#         return version
#
#     @property
#     def system_versions(self) -> None:
#         """Return major.minor python versions found in the system."""
#         versions = self.execute(["versions"])
#         logger.info(versions)


class Git(Command):
    """Git."""

    @property
    def binary_name(self) -> str:
        """Git binary."""
        return "git"

    def init(self, proj_path: pathlib.Path) -> None:
        """Init repo."""
        if (proj_path / ".git").is_dir():
            logger.warning(f"'{proj_path.name}' is already a Git repository")
            return
        command = ["init", proj_path]
        logger.info(f"Git repository initialized in '{proj_path.name}'")
        _ = self.execute(command=command)

### win32
# uv ptython list --only-installed
# <python long name>    AppData\Roaming\uv\python\<python long name>\python.exe
# <python long name>    AppData\Local\Programs\Python312\python.exe
### linux







