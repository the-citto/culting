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
        path = kwargs["path"]
        self.proj_path = pathlib.Path(path).absolute()
        self.name = self._set_name(name=kwargs["name"])
        self.git = Git()
        self.git.init(proj_path=self.proj_path)
        self.python_version = self._set_python(python_version=kwargs["python_version"])
        logger.info(f"Package '{self.name}' initialized in {self.proj_path}")

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

    def _set_python(self, python_version: PythonVersions) -> str:
        python_version_path = self.proj_path / ".python-version"
        if not python_version and python_version_path.is_file():
            with python_version_path.open() as file:
                python_version_file = file.read().strip()
            if python_version_file in t.get_args(PythonVersions):
                python_version = t.cast(PythonVersions, python_version_file)
            else:
                warn_msg = f"Found '.python-version' file with invalid version '{python_version_file}'"
                warn_msg += "\n'.python-version' will be changed with the system's default python version"
                logger.warning(warn_msg)
        if __os__ == "linux":
            python_version_valid = Pyenv(python_version=python_version).major_minor
            with python_version_path.open("w") as file:
                file.write(python_version_valid)
            return python_version_valid
        raise NotImplementedError



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

    def execute(self, command: list[t.Any]) -> str:
        """Execute."""
        _command = [self.binary_path, *command]
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



class Git(Command):
    """Git."""

    @property
    def binary(self) -> str:
        """Git binary."""
        return "git"

    def init(self, proj_path: pathlib.Path) -> None:
        """Init repo."""
        if (proj_path / ".git").is_dir():
            return
        command = ["init", proj_path]
        _ = self.execute(command=command)


class Pyenv(Command):
    """Pyenv."""

    def __init__(self, python_version: PythonVersions) -> None:
        """Init."""
        self.python_version = python_version
        super().__init__()

    @property
    def binary(self) -> str:
        """Pyenv binary."""
        return f"python{self.python_version}"

    @property
    def major_minor(self) -> str:
        """Major.minor python version."""
        command = ["-V"]
        stdout = self.execute(command)
        major_minor_re = re.search(r"Python (3.[0-9]+).", stdout)
        if major_minor_re is None:
            err_msg = f"Unexpected output '{stdout}"
            raise InitError(err_msg)
        return major_minor_re.group(1)

class PyLauncher(Command):
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





