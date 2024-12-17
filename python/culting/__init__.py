"""
Init.

Refs:
    sys.platform: https://docs.python.org/3/library/sys.html#sys.platform
    XDG Base Directory Specification: https://specifications.freedesktop.org/basedir-spec/latest/
"""

from ._exceptions import (
    CommandNotFoundError,
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
    __xdg_config_home__,
    __xdg_state_home__,
)
from .defaults import (
    culting_conf,
)



__all__: list[str] = [
    "CommandNotFoundError",
    "InitError",
    "InitKwargs",
    "PythonVersions",
    "__os__",
    "__version__",
    "__xdg_config_home__",
    "__xdg_state_home__",
    "culting_conf",
    "logger",
]




