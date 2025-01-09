"""Package init."""

# import pathlib
#
# import tomlkit as toml
#
# from culting.commands import Python
# from culting.defaults import culting_conf
# from culting.exceptions import PackageError
# from culting.variables import __os__
#
#
# _pyproject_path = pathlib.Path("pyproject.toml")
# if not _pyproject_path.is_file():
#     err_msg = "'pyproject.toml' not found in the current directory."
#     raise PackageError(err_msg)
#
# with _pyproject_path.open("r") as file:
#     _pyproject_toml = toml.load(file)
#
# if _pyproject_toml.get("tool", {}).get("culting") is None:
#     err_msg = "'culting' section not present in 'pyproject.toml'"
#     raise PackageError(err_msg)
#
# _package_name = _pyproject_toml.get("project", {}).get("name")
#
# if _package_name is None:
#     err_msg = ""
#     raise PackageError(err_msg)
#
# _package_path = pathlib.Path(
#     culting_conf.package.venv,
#     "bin" if __os__ == "linux" else "Scripts",
#     _package_name if __os__ == "linux" else f"{_package_name}.exe",
# )
# if not _package_path.is_file():
#     err_msg = f"'{_package_path}' not found."
#     raise PackageError(err_msg)
#
# _python_path = pathlib.Path(
#     culting_conf.package.venv,
#     "bin" if __os__ == "linux" else "Scripts",
#     "python" if __os__ == "linux" else "python.exe",
# )
#
# if not _python_path.is_file():
#     err_msg = f"'{_python_path}' not found"
#     raise PackageError(err_msg)
#
# _binary_path = str(_python_path.absolute())
#
# pkg_python = Python(binary_path=_binary_path)
# pkg_name = _package_name


