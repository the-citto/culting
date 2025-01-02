"""Run."""

import pathlib

import tomlkit as toml

from .commands import Python
from .defaults import culting_conf
from .exceptions import RunError
from .variables import __os__


class Run:
    """Run package."""

    def __init__(self, package_args: tuple[str, ...]) -> None:
        """Init."""
        self.package_name = self._check_package()
        self.package_args = ["-m", self.package_name, *package_args]
        self.python = self._check_python()
        self.python.run(command=self.package_args)

    def _check_python(self) -> Python:
        _python_path = pathlib.Path(
            culting_conf.package.venv,
            "bin" if __os__ == "linux" else "Scripts",
            "python" if __os__ == "linux" else "python.exe",
        )
        if not _python_path.is_file():
            err_msg = f"'{_python_path}' not found"
            raise RunError(err_msg)
        _binary_path = str(_python_path.absolute())
        return Python(binary_path=_binary_path)

    def _check_package(self) -> str:
        _pyproject_path = pathlib.Path("pyproject.toml")
        if not _pyproject_path.is_file():
            err_msg = "'pyproject.toml' not found in the current directory."
            raise RunError(err_msg)
        with _pyproject_path.open("r") as file:
            _pyproject_toml = toml.load(file)
        if _pyproject_toml.get("tool", {}).get("culting") is None:
            err_msg = "'culting' section not present in 'pyproject.toml'"
            raise RunError(err_msg)
        _package_name = _pyproject_toml.get("project", {}).get("name")
        if _package_name is None:
            err_msg = ""
            raise RunError(err_msg)
        _package_path = pathlib.Path(
            culting_conf.package.venv,
            "bin" if __os__ == "linux" else "Scripts",
            _package_name,
        )
        if not _package_path.is_file():
            err_msg = f"'{_package_path}' not found."
            raise RunError(err_msg)
        return _package_name


