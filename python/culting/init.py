"""Init."""

import abc
import pathlib
import re
import shutil
import subprocess
import typing as t

from . import (
    CommandNotFoundError,
    InitError,
    InitKwargs,
    PythonVersions,
    __os__,
    logger,
)



class Init:
    """Project init."""

    def __init__(self, **kwargs: t.Unpack[InitKwargs]) -> None:
        """Init."""
        path = kwargs.get("path")
        self.proj_path = pathlib.Path(path).absolute()
        self.name = self._set_name(name=kwargs.get("name"))
        # python_version = kwargs.get("python_version")
        self._set_python_version(python_version=kwargs.get("python_version"))
        # self.git = Git(proj_path=self.proj_path)
        # self.git.init()
        if __os__ == "linux":
            ...
        else:
            ...

    def _set_name(self, name: str | None) -> str:
        if name is None:
            name = self.proj_path.name
        valid_name = re.match(r"[a-z_][a-z0-9_]+$", name)
        if valid_name is None:
            err_msg = f"Name '{name}' is not PEP 8 / PEP 423 compliant"
            raise InitError(err_msg)
        if name.startswith("_"):
            logger.warning(f"Name '{name}' with leading underscore should be for special use")
        logger.info(f"Initializing package '{name}'")
        return name

    def _set_python_version(self, python_version: PythonVersions | None) -> None:
        ...



class Command(abc.ABC):
    """Command."""

    def __init__(self) -> None:
        """Init."""
        self.binary_path = shutil.which(self.binary)
        if self.binary_path is None:
            raise CommandNotFoundError(self.binary)

    @property
    @abc.abstractmethod
    def binary(self) -> str:
        """Command binary name or fully qualified path."""


class Git(Command):
    """Git."""




class Pyenv:
    """Pyenv."""


class PyLauncher:
    """Py launcher."""

# class Git:
#     """Git."""
#
#     def __init__(self, proj_path: pathlib.Path) -> None:
#         """Init."""
#         self.proj_path = proj_path
#
#     def init(self) -> None:
#         """Init."""
#
#     def name(self) -> str:
#         """Git name."""
#         return ""


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
# class Command(abc.ABC):
#     """Command."""
#
#     _binary: os.PathLike | str
#
#     @property
#     def binary(self) -> os.PathLike | str:
#         """OS binary."""
#         return self._binary
#
#     def _verify(self) -> None:
#         binary_path = shutil.which(self.binary)
#         if binary_path is None:
#             err_msg = f"'{self.binary}' not found."
#             raise CommandNotFoundError(err_msg)
#
#     def _run(self, *, command_args: t.Iterable[str] = ()) -> str:
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
#
# class Git(Command):
#     """Git."""
#
#     _binary = "git"
#
#     # def __init__(self) -> None:
#     #     """Init."""
#     #     # super().__init__()
#
#     # @classmethod
#     def __new__(cls) -> None:
#         """New."""
#         print(cls.binary)
#         # return cls.binary
#         # return super().__init()
#
# class Pyenv(Command):
#     """Pyenv."""
#
#     binary = "pyenv"
#
#     def __init__(self) -> None:
#         """Init."""
#         self._verify_command()
#         command_args = ["versions"]
#         print(self._run_command(command_args=command_args))
#
#
#     def init_project(self) -> str:
#         """Init."""
#         return ""
#
#
#





