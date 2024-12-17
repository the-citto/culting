"""
Init.

Refs:
    sys.platform: https://docs.python.org/3/library/sys.html#sys.platform
    XDG Base Directory Specification: https://specifications.freedesktop.org/basedir-spec/latest/
"""

from ._exceptions import (
    InitError,
)
from ._logger import (
    logger,
)
from ._typing import (
    InitKwargs,
    PythonVersions,
)
from ._vars import (
    __os__,
    __version__,
    xdg_config_home,
    xdg_state_home,
)
from .defaults import (
    culting_conf,
)



__all__: list[str] = [
    "InitError",
    "InitKwargs",
    "PythonVersions",
    "__os__",
    "__version__",
    "culting_conf",
    "logger",
    "xdg_config_home",
    "xdg_state_home",
]




