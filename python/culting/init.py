"""Init."""

import pathlib
import re
import typing as t

from . import (
    InitError,
    InitKwargs,
    __os__,
    logger,
)
from .commands import (
    Git,
    Python,
)



class Init:
    """Project init."""

    def __init__(self, **kwargs: t.Unpack[InitKwargs]) -> None:
        """Init."""
        self.kwargs = kwargs
        self._verify_empty()
        self.name = self._set_name()
        self.git = Git()
        self._init_git()
        self._create_venv()
        # self._set_package_files()

    def _verify_empty(self) -> None:
        path = self.kwargs["path"]
        self.proj_path = pathlib.Path(path).absolute()
        self.proj_path.mkdir(parents=True, exist_ok=True)
        if any(self.proj_path.iterdir()):
            err_msg = f"{self.proj_path} is not empty"
            raise InitError(err_msg)
        logger.debug(f"'{self.proj_path}' is empty")

    def _set_name(self) -> str:
        name = self.kwargs["name"]
        if name is None:
            name = self.proj_path.name
        valid_name = re.match(r"[a-z_][a-z0-9_]+$", name)
        if valid_name is None:
            err_msg = f"Name '{name}' is not PEP 8 / PEP 423 compliant"
            raise InitError(err_msg)
        if name.startswith("_"):
            logger.warning(f"Name '{name}' with leading underscore should be for special use")
        logger.info(f"Initializing package '{name}'")
        return name

    def _init_git(self) -> None:
        logger.info(f"Initializing Git repository in '{self.proj_path}'")
        self.git.init(proj_path=self.proj_path)

    def _create_venv(self) -> None:
        _sys_python = Python(binary_path=self.kwargs.get("python_path"))
        _venv_name = self.kwargs.get("venv")
        _venv_path = self.proj_path / _venv_name
        logger.info(f"Creating '{_venv_name}'")
        _ = _sys_python.execute(["-m", "venv", _venv_path])
        if __os__ == "linux":
            _venv_python_path = _venv_path / "bin/python"
        elif __os__ == "win32":
            _venv_python_path = _venv_path / "Script/python.exe"
        else:
            raise InitError
        self.python = Python(binary_path=str(_venv_python_path))
        logger.debug(f"venv python: '{self.python.binary}'")

    # def _set_sys_python(self) -> Python:
    #     _python_version = self.kwargs.get("python_version")
    #     for p in culting_conf.python.managers_priority:
    #         python_manager_mapped = python_managers_map.get(p)
    #         if python_manager_mapped is None:
    #             continue
    #         python_manager = python_manager_mapped()
    #         python_full_path = python_manager.get_full_path(python_version=_python_version)
    #         if python_full_path is None:
    #             continue
    #         logger.info(p)
    #         logger.info(python_full_path)
    #         break
    #
    #     # logger.info(_python_version)
    #     # logger.info(culting_conf.python.managers_priority)
    #     # pyenv = self.kwargs["pyenv"]
    #     # if pyenv is not None:
    #     #     ...
    #     # py = self.kwargs["py"]
    #     # if py is not None:
    #     #     ...
    #     # uv = self.kwargs["uv"]
    #     # if uv is not None:
    #     #     ...
    #     return Python()

    # def _set_package_files(self) -> None:
    #     src_pkg_dir = self.proj_path / culting_conf.package.src / self.name
    #     src_pkg_dir.mkdir(parents=True)
    #     # pkg_init_txt = (
    #     #     '"""Init."""\n\n'
    #     #     "import importlib.metadata\n"
    #     #     "\n\n\n"
    #     #     "__version__ = importlib.metadata.version(__name__)\n"
    #     #     "\n"
    #     #         "__all__: list[str] = []\n"
    #     # )
    #     # pkg_init_path = src_pkg_dir / "__init__.py"
    #     # with pkg_init_path.open("w") as file:
    #     #     file.write(pkg_init_txt)
    #     # pkg_main_txt = (
    #     #     '"""Main."""\n\n'
    #     #     "def main() -> None:\n"
    #     #     '    """Run entry point."""\n\n\n'
    #     #     'if __name__ == "__main__":\n'
    #     #     "    main()\n"
    #     # )
    #     # pkg_main_path = src_pkg_dir / "__main__.py"
    #     # with pkg_main_path.open("w") as file:
    #     #     file.write(pkg_main_txt)
    #     logger.info(f"Package '{self.name}' initialized in {self.proj_path}")





