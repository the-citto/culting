"""Init."""

from .cli import cli


__all__ = [
    "cli",
]



# import pathlib
# import sys
# import typing as t
#
# import pydantic
# from pj_logging.pj_logging import set_logger

# logger = set_logger(
#     name=__name__,
# )


# class XdgDirs(pydantic.BaseModel):
#
#     __xdg_config_home__: pathlib.Path
#     __xdg_state_home__: pathlib.Path


# SupportedOs = t.Literal["linux", "win32"]
#
# class SystemDetails(pydantic.BaseModel):
#
#     # os: SupportedOs = pydantic.Field(exclude=True)
#     os: SupportedOs
#
#     # @pydantic.computed_field # type: ignore [prop-decorator]
#     # @property
#     # def __os__(self) -> SupportedOs:
#     #     return self.os
#
#     @pydantic.computed_field # type: ignore [prop-decorator]
#     @property
#     def xdg_config_home(self) -> pathlib.Path:
#         if self.os == "linux":
#             return pathlib.Path.home() / ".config" / __name__
#         if self.os == "win32":
#             return pathlib.Path.home() / "AppData" / __name__
#         raise NotImplementedError
#
#     @pydantic.computed_field # type: ignore [prop-decorator]
#     @property
#     def xdg_state_home(self) -> pathlib.Path:
#         if self.os == "linux":
#             return pathlib.Path.home() / ".local/state" / __name__
#         if self.os == "win32":
#             return pathlib.Path.home() / "AppData/Temp" / __name__
#         raise NotImplementedError

# system_details = SystemDetails(os=t.cast(SupportedOs, sys.platform))
# # system_details = SystemDetails(__os__=t.cast(SupportedOs, sys.platform))
# print(system_details.model_dump())

    # linux: XdgDirs = XdgDirs(
    # __xdg_config_home__=pathlib.Path.home() / ".config" / __name__,
    #     __xdg_state_home__=pathlib.Path.home() / ".local/state" / __name__,
    # )
    # win32: XdgDirs = XdgDirs(
    #     __xdg_config_home__=pathlib.Path.home() / "AppData" / __name__,
    #     __xdg_state_home__=pathlib.Path.home() / "AppData/Temp" / __name__,
    # )


# xdg_paths = XdgOs(
#     linux
#         "__xdg_config_home__": pathlib.Path.home() / ".config" / __name__,
#         "__xdg_state_home__": pathlib.Path.home() / ".local/state" / __name__,
#     },
#     "win32": {
#         "__xdg_config_home__": pathlib.Path.home() / "AppData" / __name__,
#         "__xdg_state_home__": pathlib.Path.home() / "AppData/Temp" / __name__,
#     },
# })


# SupportedOs = t.Literal[tuple(xdg_paths)]
# # SupportedOs = t.Literal["linux", "win32"]
#
# SupportedOs
#
# __os__: SupportedOs = t.cast(SupportedOs, sys.platform)
#
# if __os__ not in xdg_paths:
#     err_msg = f"unsupported '{__os__}'"
#     raise NotImplementedError(err_msg)


# if __os__ == ""

# if __os__ == "linux":
#     __xdg_config_home__ = pathlib.Path.home() / ".config" / __name__
#     __xdg_state_home__ = pathlib.Path.home() / ".local/state" / __package__
# elif __os__ == "win32":
#     _xdg_config_home = "AppData"
#     _xdg_state_home = "AppData/Temp"
# else:
#     err_msg = f"unsupported '{__os__}'"
#     raise NotImplementedError(err_msg)

# __xdg_config_home__ = pathlib.Path.home() / _xdg_config_home / __name__
# __xdg_config_home__.mkdir(parents=True, exist_ok=True)
# __xdg_state_home__ = pathlib.Path.home() / _xdg_state_home / __package__
# __xdg_state_home__.mkdir(parents=True, exist_ok=True)
#
# logfile_path = __xdg_state_home__ / f"{__package__}.log"
#
# # conffile_path = __xdg_config_home__ / f"{__package__}.conf"


