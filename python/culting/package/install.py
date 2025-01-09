"""Install."""

# import pathlib
#
# from culting.exceptions import InstallError
# from culting.logger import logger
# from culting.package import (
#     pkg_python,
# )
#
#
# class Install:
#     """Install libraries."""
#
#     def __init__(self, libraries: tuple[str, ...]) -> None:
#         """Init."""
#         self.requirements_in_path, self.requirements_in= self._get_requirements_in()
#         _new_libraries = self._add_requirements_in(libraries)
#         if _new_libraries:
#             self._compile_requirements()
#             self._install_dev()
#             logger.info(f"Installed: {', '.join(_new_libraries)}")
#
#     def _add_requirements_in(self, libraries: tuple[str, ...]) -> list[str] | None:
#         logger.debug(f"Verifying new libraries: {', '.join(libraries)}")
#         _new_libraries = []
#         for _library in libraries:
#             if _library in self.requirements_in:
#                 logger.warning(f"'{_library}' already present in 'requirements.in'")
#             else:
#                 _new_libraries.append(_library)
#         if not _new_libraries:
#             logger.warning("No new libraries to add")
#             return None
#         _all_libs = sorted([*self.requirements_in, *_new_libraries])
#         self.requirements_in_path.write_text(f"{'\n'.join(_all_libs)}\n")
#         return _new_libraries
#
#     def _get_requirements_in(self) -> tuple[pathlib.Path, list[str]]:
#         _requirements_in_path = pathlib.Path("requirements.in").absolute()
#         if not _requirements_in_path.is_file():
#             err_msg = f"'{_requirements_in_path}' not found"
#             raise InstallError(err_msg)
#         with _requirements_in_path.open("r") as file:
#             _requirements_in = file.read().split()
#         _requirements_in = [r for r in _requirements_in if r]
#         logger.debug(_requirements_in)
#         return _requirements_in_path, _requirements_in
#
#     def _install_dev(self) -> None:
#         pkg_python.run([
#             "-m",
#             "pip",
#             "install",
#             "-e",
#             ".[dev]",
#             "-c",
#             "requirements.lock",
#             "--quiet",
#         ])
#
#     def _compile_requirements(self) -> None:
#         pkg_python.run([
#             "-m",
#             "piptools",
#             "compile",
#             "-o",
#             "requirements.lock",
#             "requirements.in",
#             "--no-strip-extras",
#             "--quiet",
#         ])
#
#
#
# # def is_canonical(version: str) -> bool:
# #     """Is canonical."""
# #     import re
# #     return re.match(
# #r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
# #         version,
# #     ) is not None









