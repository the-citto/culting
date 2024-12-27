"""Defaults."""

import sys

import pydantic
import tomlkit as toml

from . import (
    __xdg_config_home__,
    logger,
)



conf_default_path = __xdg_config_home__ / "default.toml"
conf_custom_path = __xdg_config_home__ / "custom.toml"



class SetupConf(pydantic.BaseModel):
    """Setup config."""

    no_path_warning: bool = False


class GitConf(pydantic.BaseModel):
    """Git config."""

    use_email: bool = True


class PackageConf(pydantic.BaseModel):
    """Package config."""

    venv: str = ".venv"
    src: str = "src"

    @pydantic.field_validator("venv", "src")
    @classmethod
    def _valid_len(cls, field: str) -> str:
        min_len = 3
        if len(field) < min_len:
            err_msg = f"Parameter '{field}' is too short, at least {min_len} characters"
            raise ValueError(err_msg)
        return field


class PythonConf(pydantic.BaseModel):
    """Python config."""

    path: str = ""

    # @pydantic.field_validator("path")
    # @classmethod
    # def _valid_path(cls, path: str) -> str:
    #     if path and not pathlib.Path(path).is_file():
    #         err_msg = f"'{path}' not found."
    #         raise ValueError(err_msg)
    #     return path


class CultingConf(pydantic.BaseModel):
    """All config."""

    setup: SetupConf = SetupConf()
    python: PythonConf = PythonConf()
    git: GitConf = GitConf()
    package: PackageConf = PackageConf()




with conf_default_path.open("w") as file:
    toml.dump(CultingConf().model_dump(), file, sort_keys=True)


try:
    if conf_custom_path.is_file():
        with conf_custom_path.open("r") as file:
            toml_value = toml.load(file).value
            culting_conf = CultingConf(**toml_value)
    else:
        culting_conf = CultingConf()
except pydantic.ValidationError as err:
    logger.exception(err)
    sys.exit(1)


