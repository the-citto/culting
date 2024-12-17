"""Variables."""

import importlib.metadata
import pathlib
import sys



if __package__ is None:
    raise RuntimeError

__version__: str = importlib.metadata.version(__package__)
__os__: str = sys.platform


if __os__ == "linux":
    _xdg_config_home = ".config"
    _xdg_state_home = ".local/state"
elif __os__ == "win32":
    _xdg_state_home = "AppData"
    _xdg_config_home = "AppData/Temp"
else:
    err_msg = f"OS '{__os__}'"
    raise NotImplementedError(err_msg)


xdg_config_home = pathlib.Path.home() / _xdg_config_home / __package__
xdg_state_home = pathlib.Path.home() / _xdg_state_home / __package__

xdg_config_home.mkdir(parents=True, exist_ok=True)
xdg_state_home.mkdir(parents=True, exist_ok=True)

logfile_path = xdg_state_home / f"{__package__}.log"
conffile_path = xdg_config_home / f"{__package__}.conf"


