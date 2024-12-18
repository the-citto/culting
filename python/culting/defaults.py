"""Defaults."""

import pydantic
import tomlkit as toml

from . import __xdg_config_home__



conf_default_path = __xdg_config_home__ / "culting-default.toml"
conf_custom_path = __xdg_config_home__ / "culting.toml"



class SetupConf(pydantic.BaseModel):
    """Setup config."""

    no_path_warning: bool = False


class GitConf(pydantic.BaseModel):
    """Git config."""

    use_email: bool = True


class PyenvConf(pydantic.BaseModel):
    """Pyenv config."""


class PyLauncherConf(pydantic.BaseModel):
    """Py launcher config."""



class CultingConf(pydantic.BaseModel):
    """All config."""

    setup: SetupConf = SetupConf()
    git: GitConf = GitConf()
    pyenv: PyenvConf = PyenvConf()
    pylauncher: PyLauncherConf = PyLauncherConf()




with conf_default_path.open("w") as file:
    toml.dump(CultingConf().model_dump(), file, sort_keys=True)


if conf_custom_path.is_file():
    with conf_custom_path.open("r") as file:
        toml_value = toml.load(file).value
        culting_conf = CultingConf(**toml_value)
else:
    culting_conf = CultingConf()



