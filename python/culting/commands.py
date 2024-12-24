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
    SupportedOs,
    __os__,
    logger,
)



class Command(abc.ABC):
    """Command."""

    def __init__(self, binary_path: str | None = None) -> None:
        """Init."""
        _binary = binary_path if binary_path is not None else self.default_binary
        self.binary = shutil.which(_binary)
        if self.binary is None:
            raise CommandNotFoundError(_binary)

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
            if shutil.which("py.exe"):
                return "py.exe"
            return "python.exe"
        raise NotImplementedError

    # @property
    # def binary_name(self) -> str:
    #     """Binary name or fully qualified path."""
    #     _python = shutil.which("python")
    #     # deal with pyenv-win .bat file, when global is not set returning a version example
    #     if _python is not None and not _python.lower().endswith(".bat"):
    #         return _python
    #     # Windows systems with PATH set for Py Launcher but not for Python
    #     _py = shutil.which("py")
    #     if _py is not None:
    #         proc = subprocess.Popen(
    #             [_py, "--list-paths"],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #         )
    #         stdout, stderr = proc.communicate()
    #         if stderr:
    #             err_msg = stderr.decode("utf-8")
    #             raise subprocess.CalledProcessError(returncode=1, cmd=" ".join(map(str, _py)), output=err_msg)
    #         _stdout = stdout.decode("utf-8")
    #         _python_path_re = re.search(r"\* *([a-zA-Z]{1}:\\.*python.exe)", _stdout)
    #         if _python_path_re is not None:
    #             return _python_path_re.group(1)
    #     err_msg = "Python not found."
    #     raise CommandNotFoundError(err_msg)

    @property
    def version(self) -> str:
        """Version."""
        version_output = self.execute(["--version"])
        version_re = re.search(r"(3\.\d+)", version_output)
        if version_re is None:
            err_msg = "Python version not found"
            raise CommandNotFoundError(err_msg)
        return version_re.group()



class PythonManager(Command, abc.ABC):
    """Python manager."""

    # def __init__(self) -> None:
    #     """Init."""
    #     try:
    #         super().__init__()
    #     except CommandNotFoundError:
    #         self.binary = None
    #
    # @property
    # @abc.abstractmethod
    # def versions(self) -> list[str]:
    #     """Available versions."""
    #     # if self.binary is None:
    #     #     return []
    #     # versions_output = self.execute(self.versions_command)
    #     # versions = re.findall(r"(3\.\d+)", versions_output)
    #     # return sorted(
    #     #     set(versions),
    #     #     key=lambda v: int(v.split(".")[1]),
    #     # )
    #
    # # @property
    # # @abc.abstractmethod
    # # def versions_command(self) -> list[str]:
    # #     """Command and options to get versions."""
    #
    # @abc.abstractmethod
    # def get_full_path(self, python_version: str) -> str | None:
    #     """Get full path of specified version."""



class Pyenv(PythonManager):
    """Pyenv."""

    @property
    def default_binary(self) -> str:
        """Binary name or fully qualified path."""
        if __os__ == "linux":
            return "pyenv"
        if __os__ == "win32":
            return "pyenv.bat"
        supported_os = ", ".join(f"'{o}'" for o in t.get_args(SupportedOs))
        err_msg = f"Supported [{supported_os}]"
        raise NotImplementedError(err_msg)

    # @property
    # def binary_name(self) -> str:
    #     """Binary name or fully qualified path."""
    #     return "pyenv"
    #
    # @property
    # def versions_command(self) -> list[str]:
    #     """Command and options to get versions."""
    #     return ["versions", "--skip-envs"]
    #
    # def get_full_path(self, python_version: str) -> str | None:
    #     """Get full path of specified version, if exists."""
    #     if self.binary is None:
    #         return None
    #     pyenv_root = self.execute(["root"])
    #     pyenv_version_paths = [
    #         path
    #         for path in pathlib.Path(pyenv_root, "versions").glob(f"{python_version}*")
    #         if re.search(re.escape(python_version) + r"\.\d+$", path.name) is not None
    #     ]
    #     if not pyenv_version_paths:
    #         return None
    #     max_version = max(pyenv_version_paths, key=lambda v: int(str(v).split(".")[-1]))
    #     return str(max_version)



class Py(PythonManager):
    """Py."""

    @property
    def default_binary(self) -> str:
        """Binary name or fully qualified path."""
        return "py.exe"

    # @property
    # def binary_name(self) -> str:
    #     """Binary name or fully qualified path."""
    #     return "py.exe"
    #
    # @property
    # def versions_command(self) -> list[str]:
    #     """Command and options to get versions."""
    #     return ["--list-paths"]
    #
    # def get_full_path(self, python_version: str) -> str | None:
    #     """Get full path of specified version, if exists."""
    #     if self.binary is None:
    #         return None
    #     py_list_paths = self.execute(["--list-paths"])
    #     python_path_re = re.search(re.escape(python_version) + r"[* ]+(.+python.exe)", py_list_paths)
    #     if python_path_re is None:
    #         return None
    #     return python_path_re.group(1)




# class Uv(PythonManager):
#
    # @property
    # def default_binary(self) -> str:
    #     """Binary name or fully qualified path."""
    #     raise NotImplementedError
    #  """Uv."""
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



class Git(Command):
    """Git."""

    @property
    def default_binary(self) -> str:
        """Binary name or fully qualified path."""
        raise NotImplementedError

    # @property
    # def binary_name(self) -> str:
    #     """Git binary."""
    #     return "git"
    #
    # def init(self, proj_path: pathlib.Path) -> None:
    #     """Init repo."""
    #     if (proj_path / ".git").is_dir():
    #         logger.warning(f"'{proj_path.name}' is already a Git repository")
    #         return
    #     command = ["init", proj_path]
    #     logger.info(f"Git repository initialized in '{proj_path.name}'")
    #     _ = self.execute(command=command)







