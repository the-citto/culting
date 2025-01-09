"""Init."""

# import pathlib
# import re
# import typing as t
#
# import tomlkit as toml
#
# from .commands import (
#     Git,
#     Python,
#     Wget,
# )
# from .defaults import (
#     pkg_init_py,
#     pkg_main_py,
#     tst_first_test,
#     tst_init_py,
# )
# from .exceptions import (
#     InitError,
# )
# from .logger import logger
# from .pyproject import culting_pyproj
# from .types import (
#     InitKwargs,
# )
# from .variables import (
#     __os__,
# )
#
#
# class Init:
#     """Project init."""
#
#     def __init__(self, **kwargs: t.Unpack[InitKwargs]) -> None:
#         """Init."""
#         self.kwargs = kwargs
#         self.proj_path = self._set_proj_path()
#         self.name = self._set_name()
#         self.readme = self._set_readme()
#         self.user_name, self.user_email = self._init_git()
#         self.license = self._set_license()
#         self.gitignore = self._set_gitignore()
#         self.requirements_in = self._set_requirements_in()
#         self.python = self._set_venv_python()
#         self._set_base_venv()
#         self.pkg_path, self.tests_path = self._set_base_folders()
#         self._set_py_typed()
#         self._set_dunder_files()
#         self.pyproject = self._set_pyproject()
#         self._set_pip_tools()
#         self._set_requirements()
#         self._set_dev()
#         logger.info(f"Package '{self.name}' set up, happy coding!")
#         # logger.info(f"Package '{self.name}' set up 🏗️ happy coding!\n")
#
#     def _set_dev(self) -> None:
#         self.python.run([
#             "-m",
#             "pip",
#             "install",
#             "-e",
#             f"{self.proj_path}[dev]",
#             "-c",
#             f"{self.proj_path}/requirements.lock",
#             "--quiet",
#         ])
#
#     def _set_requirements(self) -> None:
#         self.python.run([
#             "-m",
#             "piptools",
#             "compile",
#             "-o",
#             f"{self.proj_path}/requirements.lock",
#             f"{self.proj_path}/requirements.in",
#             "--no-strip-extras",
#             "--quiet",
#         ])
#
#     def _set_pip_tools(self) -> None:
#         self.python.execute(["-m", "pip", "install", "pip-tools"])
#
#     def _set_pyproject(self) -> pathlib.Path:
#         _pyproject = culting_pyproj
#         _pyproject.project.name = self.name
#         _pyproject.project.requires_python = f">={self.python.version}"
#         _pyproject.tool.ruff.lint.isort.known_first_party = [self.name]
#         _toml_dump = _pyproject.toml_dump()
#         _toml_dump["tool"]["setuptools"]["package-data"][self.name] = ["py.typed"] # type: ignore [index]
#         _toml_dump["project"]["scripts"][self.name] = f"{self.name}:__main__.main" # type: ignore [index]
#         _pyproject_path = self.proj_path / "pyproject.toml"
#         with _pyproject_path.open("w") as file:
#             toml.dump(_toml_dump, file)
#         logger.debug("pyproject.toml done")
#         return _pyproject_path
#
#     def _set_py_typed(self) -> None:
#         (self.pkg_path / "py.typed").touch()
#         logger.debug("py.typed done")
#
#     def _set_requirements_in(self) -> pathlib.Path:
#         _requirements_in = self.proj_path / "requirements.in"
#         _requirements_in.touch()
#         logger.debug("requirements.in done")
#         return _requirements_in
#
#     def _set_dunder_files(self) -> None:
#         (self.pkg_path / "__init__.py").write_text(pkg_init_py)
#         (self.pkg_path / "__main__.py").write_text(pkg_main_py)
#         (self.tests_path / "__init__.py").write_text(tst_init_py.format(pkg_name=self.name))
#         (self.tests_path / "test_init.py").write_text(tst_first_test.format(pkg_name=self.name))
#
#     def _set_base_folders(self) -> tuple[pathlib.Path, pathlib.Path]:
#         _src = self.kwargs["src"]
#         self.scr = self.proj_path / _src
#         _pkg_path = self.scr / self.name
#         _pkg_path.mkdir(parents=True)
#         _tests_path = self.proj_path / "tests"
#         _tests_path.mkdir(parents=True)
#         return _pkg_path, _tests_path
#
#
#     def _set_base_venv(self) -> None:
#         self.python.execute(["-m", "pip", "install", "--upgrade", "pip", "pip-tools"])
#
#     def _init_git(self) -> tuple[str, str]:
#         _git = Git()
#         logger.debug(f"Initializing Git repository in '{self.proj_path}'")
#         return _git.init(proj_path=self.proj_path)
#
#     def _set_gitignore(self) -> pathlib.Path:
#         Wget().gitignore(proj_path=self.proj_path)
#         logger.debug(".gitignore done")
#         return self.proj_path / ".gitignore"
#
#     def _set_license(self) -> pathlib.Path:
#         _license_template = self.kwargs["license_template"]
#         _license_path = self.proj_path / "LICENSE"
#         Wget().license(
#             license_template=_license_template,
#             license_path=_license_path,
#             user_name=self.user_name,
#         )
#         logger.debug(f"{_license_template} LICENSE done")
#         return _license_path
#
#     def _set_readme(self) -> str:
#         _readme = self.kwargs["readme"]
#         _title = self.name.replace("_", " ").strip().capitalize()
#         _readme_path = self.proj_path / _readme
#         _readme_path.write_text(f"# {_title}")
#         logger.debug(f"'{_readme_path}' created")
#         return _readme
#
#     def _set_name(self) -> str:
#         _name = self.kwargs.get("name")
#         if _name is None:
#             _name = self.proj_path.name
#         _valid_name = re.match(r"[a-z_][a-z0-9_]+$", _name)
#         if _valid_name is None:
#             err_msg = f"Name '{_name}' is not PEP 8 / PEP 423 compliant"
#             raise InitError(err_msg)
#         if _name.startswith("_"):
#             logger.warning(f"'{_name}' - names with leading underscore are reserved for special use")
#         logger.info(f"Initializing package '{_name}'")
#         return _name
#
#     def _set_proj_path(self) -> pathlib.Path:
#         _path = self.kwargs["path"]
#         _proj_path = pathlib.Path(_path).absolute()
#         _proj_path.mkdir(parents=True, exist_ok=True)
#         if any(_proj_path.iterdir()):
#             err_msg = f"'{_proj_path}' is not empty"
#             raise InitError(err_msg)
#         logger.debug(f"'{_proj_path}' created")
#         return _proj_path
#
#     def _set_venv_python(self) -> Python:
#         _sys_python = Python(binary_path=self.kwargs.get("python_path"))
#         _venv_name = self.kwargs["venv"]
#         _venv_path = self.proj_path / _venv_name
#         logger.debug(f"Creating '{_venv_name}'")
#         _ = _sys_python.execute(["-m", "venv", _venv_path])
#         if __os__ == "linux":
#             _venv_python_path = _venv_path / "bin/python"
#         elif __os__ == "win32":
#             _venv_python_path = _venv_path / "Scripts/python.exe"
#         else:
#             raise InitError
#         _python = Python(binary_path=str(_venv_python_path))
#         logger.debug(f"venv python: '{_python.binary}'")
#         return _python






