"""
Commands.

First iteration of `culting` uses only `subprocess` calls,
this will allow calling various commands with their subcommands and options
with the feature of verifying that they are run within the project scope

Click reference:
    https://click.palletsprojects.com/en/stable/advanced/#forwarding-unknown-options
"""

import abc
import os
import pathlib
import re
import shutil
import subprocess
import typing as t

from . import (
    CommandNotFoundError,
    __os__,
)



class Command(abc.ABC):
    """Command."""

    def __init__(self, binary_path: str | None = None) -> None:
        """Init."""
        _binary = binary_path if binary_path is not None else self.default_binary
        self.binary = shutil.which(_binary)
        if self.binary is None:
            err_msg = f"Not found '{_binary}'"
            raise CommandNotFoundError(err_msg)

    @property
    @abc.abstractmethod
    def default_binary(self) -> str:
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
        return stdout.decode("utf-8").rstrip()


class Python(Command):
    """Python."""

    @property
    def default_binary(self) -> str:
        """Binary name or fully qualified path."""
        if __os__ == "linux":
            return "python"
        if __os__ == "win32":
            return "python.exe"
        raise NotImplementedError

    @property
    def version(self) -> str:
        """Version."""
        version_output = self.execute(["-VV"])
        version_re = re.search(r"(3\.\d+)", version_output)
        if version_re is None:
            err_msg = "Python version not found"
            raise CommandNotFoundError(err_msg)
        _version = version_re.group(1)
        free_thread_re = re.search("free-threading", version_output)
        if free_thread_re is not None:
            _version += "t"
        return _version


class Git(Command):
    """Git."""

    @property
    def default_binary(self) -> str:
        """Binary name or fully qualified path."""
        if __os__ == "linux":
            return "git"
        if __os__ == "win32":
            return "git.exe"
        raise NotImplementedError

    def init(self, proj_path: pathlib.Path) -> None:
        """Init repo."""
        command = ["init", proj_path]
        _ = self.execute(command=command)



class PythonManager(Command, abc.ABC):
    """Python manager."""

    def __init__(self) -> None:
        """Init."""
        try:
            super().__init__()
        except CommandNotFoundError:
            self.binary = None

    @property
    @abc.abstractmethod
    def versions(self) -> list[str]:
        """Available versions."""

    @abc.abstractmethod
    def get_version_path(self, version: str) -> str:
        """Get version path."""


class Pyenv(PythonManager):
    """Pyenv."""

    @property
    def default_binary(self) -> str:
        """Binary name or fully qualified path."""
        if __os__ == "linux":
            return "pyenv"
        return ""

    @property
    def versions(self) -> list[str]:
        """Available versions."""
        if self.binary is None:
            return []
        _versions_output = self.execute(["versions"])
        _pyenv_versions = re.findall(r"(3\.\d+)\.\d+(t*)", _versions_output)
        return [f"{v[0]}{v[1]}" for v in _pyenv_versions]

    def get_version_path(self, version: str) -> str:
        """Get version path."""
        os.environ["PYENV_VERSION"] = version
        return self.execute(["which", f"python{version}"])


class Py(PythonManager):
    """Py."""

    @property
    def default_binary(self) -> str:
        """Binary name or fully qualified path."""
        if __os__ == "win32":
            return "py.exe"
        return ""

    @property
    def versions(self) -> list[str]:
        """Available versions."""
        if self.binary is None:
            return []
        _versions_output = self.execute(["--list-paths"])
        return re.findall(r"(3\.\d+t*)", _versions_output)

    def get_version_path(self, version: str) -> str:
        """Get version path."""
        # versions_output = self.execute(["--list-paths"])
        # version_path_re = re.search(r"-V:" + re.escape(version) + r"[ *]+(.+exe)", versions_output)
        # if version_path_re is None:
        #     raise CommandNotFoundError
        # return version_path_re.group(1)
        _version_help = self.execute([f"-{version}", "--help"])
        _version_re = re.search(r"usage: (.+exe)", _version_help)
        if _version_re is None:
            raise ValueError
        return _version_re.group(1)




# class Uv(PythonManager):
#
#     @property
#     def binary_name(self) -> str:
#         """Binary name or fully qualified path."""
#         return "uv"
#
#     @property
#     def versions_command(self) -> list[str]:
#         """Command and options to get versions."""
#         return ["python", "list", "--only-installed"]
#
#     @property
#     def versions(self) -> list[str]:
#         """Available versions."""
#         if self.binary is None:
#             return []
#         versions_output = self.execute(self.versions_command)
#         uv_python_dir = self.execute(["python", "dir"]).strip()
#         versions = re.findall(re.escape(uv_python_dir) + r".*(3\.\d+)\.\d", versions_output)
#         return sorted(
#             set(versions),
#             key=lambda v: int(v.split(".")[1]),
#         )
#
#     def get_full_path(self, python_version: str) -> str | None:
#         """Get full path of specified version, if exists."""
#         if self.binary is None:
#             return None
#         err_msg = "UV not implemented yet."
#         raise NotImplementedError(err_msg)







