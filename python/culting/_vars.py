"""Variables."""

import importlib.metadata
import pathlib
import sys

from ._typing import SupportedOs



if __package__ is None:
    raise RuntimeError

__version__: str = importlib.metadata.version(__package__)


_os = sys.platform
if _os == "linux":
    _xdg_config_home = ".config"
    _xdg_state_home = ".local/state"
elif _os == "win32":
    _xdg_state_home = "AppData"
    _xdg_config_home = "AppData/Temp"
else:
    err_msg = f"OS '{_os}'"
    raise NotImplementedError(err_msg)

__os__: SupportedOs = _os


__xdg_config_home__ = pathlib.Path.home() / _xdg_config_home / __package__
__xdg_state_home__ = pathlib.Path.home() / _xdg_state_home / __package__

__xdg_config_home__.mkdir(parents=True, exist_ok=True)
__xdg_state_home__.mkdir(parents=True, exist_ok=True)

logfile_path = __xdg_state_home__ / f"{__package__}.log"
conffile_path = __xdg_config_home__ / f"{__package__}.conf"


