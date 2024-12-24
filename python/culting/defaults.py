"""Defaults."""

import pydantic
import tomlkit as toml

from . import (
    __xdg_config_home__,
)



conf_default_path = __xdg_config_home__ / "culting-default.toml"
conf_custom_path = __xdg_config_home__ / "culting.toml"



class SetupConf(pydantic.BaseModel):
    """Setup config."""

    no_path_warning: bool = False


class GitConf(pydantic.BaseModel):
    """Git config."""

    use_email: bool = True


class PackageConf(pydantic.BaseModel):
    """Package config."""

    venv: str = ".venv"
    src: str = "python"


class PythonConf(pydantic.BaseModel):
    """Python config."""

    # managers_priority: t.Sequence[PythonManager] = ["pyenv", "py", "uv"]
    #
    # @pydantic.field_validator("managers_priority", mode="before")
    # @classmethod
    # def _validate_managers_priority(
    #     cls,
    #     managers_priority: tuple[PythonManager, ...],
    # ) -> tuple[PythonManager, ...]:
    #     if len(managers_priority) != len(set(managers_priority)):
    #         err_msg = f"Only unique entries allowd [{', '.join(managers_priority)}]"
    #         raise ValueError(err_msg)
    #     return managers_priority



class CultingConf(pydantic.BaseModel):
    """All config."""

    setup: SetupConf = SetupConf()
    python: PythonConf = PythonConf()
    git: GitConf = GitConf()
    package: PackageConf = PackageConf()




with conf_default_path.open("w") as file:
    toml.dump(CultingConf().model_dump(), file, sort_keys=True)


if conf_custom_path.is_file():
    with conf_custom_path.open("r") as file:
        toml_value = toml.load(file).value
        culting_conf = CultingConf(**toml_value)
else:
    culting_conf = CultingConf()



