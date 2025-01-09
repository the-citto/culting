"""
Core.

Refs:
    XDG Base Directory Specification: https://specifications.freedesktop.org/basedir-spec/latest/
"""

import pathlib
import shutil
import subprocess
import sys
import typing as t

from .type_defs import SupportedOs


__os__:SupportedOs = t.cast(SupportedOs, sys.platform)

if __os__ not in t.get_args(SupportedOs):
    err_msg = f"OS '{__os__}' not supported."
    raise SystemExit(err_msg)


class Core:
    """Core base Culting functionalities."""

    def __init__(self) -> None:
        """Init."""

    @property
    def _wsl_appdata(self) -> pathlib.Path:
        _pwsh = shutil.which("pwsh.exe")
        if _pwsh is None:
            err_msg = "pwsh.exe not found"
            raise ProcessLookupError(err_msg)
        _win_username = subprocess.run(
            f"{_pwsh} -Command 'echo $Env:USERNAME'",
            check=True,
            shell=True,
            capture_output=True,
        )
        return pathlib.Path("/mnt/c/Users", _win_username.stdout.decode("utf-8").rstrip(), "AppData")

    @property
    def xdg_config_home(self) -> pathlib.Path:
        """XDG config home OS-dependent path."""
        if __os__ == "linux":
            _config = pathlib.Path.home() / ".config"
        elif __os__ == "win32":
            _config = pathlib.Path.home() / "Appdata/Local"
        elif __os__ == "wsl":
            _config = self._wsl_appdata / "Local"
        else:
            raise NotImplementedError
        _xdg_config_home = _config / "culting"
        _xdg_config_home.mkdir(parents=True, exist_ok=True)
        return _xdg_config_home

    @property
    def xdg_state_home(self) -> pathlib.Path:
        """XDG state home OS-dependent path."""
        if __os__ == "linux":
            _state = pathlib.Path.home() / ".local/state"
        elif __os__ == "win32":
            _state = pathlib.Path.home() / "Appdata/Local/Temp"
        elif __os__ == "wsl":
            _state = self._wsl_appdata / "Local/Temp"
        else:
            raise NotImplementedError
        _xdg_state_home = _state / "culting"
        _xdg_state_home.mkdir(parents=True, exist_ok=True)
        return _xdg_state_home





