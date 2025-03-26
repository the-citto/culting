"""Init."""

import importlib.metadata
import os
import pathlib
import re
import shutil
import sys
import typing as t

from pj_logging import set_logger


logger = set_logger(name=__name__, rich_panel_log=True)

class _Version(str):

    __slots__ = ()

    @property
    def as_tuple(self) -> tuple[int, ...]:
        version_re = re.match(r"(\d+).(\d+).(\d+)", self)
        if version_re is None:
            raise ValueError
        return tuple(map(int, version_re.groups()))

    @property
    def major(self) -> int:
        return self.as_tuple[0]

    @property
    def minor(self) -> int:
        return self.as_tuple[1]

    @property
    def patch(self) -> int:
        return self.as_tuple[2]


__version__: str = _Version(importlib.metadata.version(__name__))

os.environ["PYDANTIC_ERRORS_INCLUDE_URL"] = "0"
os.environ["MYPY_FORCE_COLOR"] = "1"
os.environ["CLICOLOR_FORCE"] = "1"


SupportedOs = t.Literal["linux", "win32"]

class ExecutableNotFoundError(FileNotFoundError):
    """Executable not found error."""

class PlatformInfo:
    """Platforme info."""

    def __init__(self) -> None:
        """Init."""
        try:
            self.os: SupportedOs = self._os
            # self.python_manager = self._python_manager
            # self.git = self._git
        except (NotImplementedError, ExecutableNotFoundError) as err:
            logger.exception(err) # noqa: TRY401
            sys.exit(1)

    @property
    def _os(self) -> SupportedOs:
        _os = t.cast(SupportedOs, sys.platform)
        if _os not in t.get_args(SupportedOs):
            err_msg = f"OS '{_os}' not supported."
            raise NotImplementedError(err_msg)
        return _os

    # @property
    # def python_version(self) -> str:
    #     """Python version."""
    #     _python_version = pathlib.Path(".python-version")
    #     if _python_version.is_file():
    #         with _python_version.open("r") as file:
    #             return file.read().strip()
    #     return ""

    @property
    def xdg_config_dir(self) -> pathlib.Path:
        """XDG config path."""
        if self._os == "linux":
            _xdg_config_dir = pathlib.Path.home() / ".config"
        elif self._os == "win32":
            _xdg_config_dir = pathlib.Path.home() / "Appdata/Local"
        else:
            raise RuntimeError
        _xdg_config_dir = _xdg_config_dir / "culting"
        _xdg_config_dir.mkdir(parents=True, exist_ok=True)
        return _xdg_config_dir

    @property
    def xdg_state_dir(self) -> pathlib.Path:
        """XDG state path."""
        if self._os == "linux":
            _xdg_state_dir = pathlib.Path.home() / ".local/state"
        elif self._os == "win32":
            _xdg_state_dir = pathlib.Path.home() / "Appdata/Local/Temp"
        else:
            raise RuntimeError
        _xdg_state_dir = _xdg_state_dir / "culting"
        _xdg_state_dir.mkdir(parents=True, exist_ok=True)
        return _xdg_state_dir

    @property
    def logfile_path(self) -> pathlib.Path:
        """Logfile path."""
        return self.xdg_state_dir / "culting.log"

    def _which_path(self, cmd: str | pathlib.Path) -> pathlib.Path:
        _path = shutil.which(cmd)
        if _path is None:
            err_msg = f"{cmd} not found."
            raise ExecutableNotFoundError(err_msg)
        return pathlib.Path(_path).absolute()

    @property
    def python_manager(self) -> pathlib.Path:
        """Python manager."""
        if self.os == "linux":
            return self._which_path("pyenv")
        if self.os == "win32":
            _python_version = pathlib.Path(".python-version")
            if _python_version.is_file():
                with _python_version.open("r") as file:
                    os.environ["PY_PYTHON"] = file.read().strip()
            return self._which_path("py.exe")
        raise RuntimeError

    @property
    def git(self) -> pathlib.Path:
        """Git."""
        if self.os == "linux":
            return self._which_path("git")
        if self.os == "win32":
            return self._which_path("git.exe")
        raise RuntimeError

    @property
    def _venv_dir(self) -> pathlib.Path:
        if self.os == "linux":
            return pathlib.Path(".venv/bin").absolute()
        if self.os == "win32":
            return pathlib.Path(".venv/Scripts").absolute()
        raise RuntimeError

    @property
    def venv_python(self) -> pathlib.Path:
        """Venv python path."""
        if self.os == "linux":
            return self._which_path(self._venv_dir / "python")
        if self.os == "win32":
            return self._which_path(self._venv_dir / "python.exe")
        raise RuntimeError



platform_info = PlatformInfo()

logger = set_logger(
    name=__name__,
    jsonl_log_file_path=platform_info.logfile_path,
    jsonl_log_file_size=1_000_000,
)



