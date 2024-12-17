"""Init."""

import pathlib
import re
import subprocess
import typing as t

import pygit2

from . import (
    InitError,
    InitKwargs,
    PythonVersions,
    __os__,
    logger,
)



class ProjInit:
    """Project init."""

    def __init__(self, **kwargs: t.Unpack[InitKwargs]) -> None:
        """Init."""
        path = kwargs.get("path")
        self.proj_path = pathlib.Path(path).absolute()
        name = kwargs.get("name")
        self._set_name(name=name)
        python_version = kwargs.get("python_version")
        self._set_python_version(python_version=python_version)
        self.git = Git(proj_path=self.proj_path)
        self.git.init()
        if __os__ == "linux":
            ...
        else:
            ...

    def _set_name(self, name: str | None) -> None:
        if name is None:
            self.name = self.proj_path.name
        else:
            self.name = name
        valid_name = re.match(r"[a-z_][a-z0-9_]+$", self.name)
        if valid_name is None:
            err_msg = f"Name '{self.name}' is not PEP 8 / PEP 423 compliant"
            raise InitError(err_msg)
        if self.name.startswith("_"):
            logger.warning(f"Name '{self.name}' with leading underscore should be for special use")
        logger.info(f"Initializing package '{self.name}'")

    def _set_python_version(self, python_version: PythonVersions | None) -> None:
        ...


class Git:
    """Git."""

    def __init__(self, proj_path: pathlib.Path) -> None:
        """Init."""
        self.proj_path = proj_path

    def init(self) -> None:
        """Init."""
        if not (self.proj_path / ".git").is_dir():
            self.repo = pygit2.init_repository(path=self.proj_path)
        else:
            self.repo = pygit2.repository.Repository(path=pygit2.utils.to_str(self.proj_path))
        self.repo.config.get_global_config()

    def name(self) -> str:
        """Git name."""
        logger.info(pygit2.config)
        return ""

class Pyenv:
    """Pyenv."""


class PyLauncher:
    """Py launcher."""


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
