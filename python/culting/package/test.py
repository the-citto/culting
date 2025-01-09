"""Test."""

# import os
# import re
# import subprocess
# import typing as t
#
# import rich
# import rich.panel
# import rich.text
# import rich_click as click
#
# from culting.package import (
#     pkg_python,
# )
#
#
# class Test:
#     """Test package."""
#
#     def __init__(self) -> None:
#         """Init."""
#         self.python_binary = t.cast(str, pkg_python.binary)
#         self._pytest()
#         # self._coverage()
#         self._mypy()
#         self._ruff()
#
#     def _pytest(self) -> None:
#         _pytest_out = subprocess.run(
#             [
#                 self.python_binary, "-m", "pytest", "--color=yes",
#                 # "--cov", "--cov-report", "term-missing",
#             ],
#             check=False,
#             capture_output=True,
#             text=True,
#         )
#         _pytest_out_stdout = _pytest_out.stdout
#         _coverage_re = re.compile(r"(-+ coverage.+\n)([\s\S]+)(\n{3})")
#         panel = rich.panel.Panel(
#             renderable=rich.text.Text.from_ansi(_coverage_re.sub("", _pytest_out_stdout)),
#             title="Pytest",
#             border_style="red" if _pytest_out.returncode == 1 else "green",
#             title_align="left",
#             # title_align=click.RichHelpConfiguration.align_errors_panel,
#         )
#         rich.print(panel)
#         _coverage_search = _coverage_re.search(_pytest_out_stdout)
#         if _coverage_search is not None:
#             panel = rich.panel.Panel(
#                 renderable=_coverage_search.group(2),
#                 title="Coverage",
#                 border_style="white",
#                 title_align=click.RichHelpConfiguration.align_errors_panel,
#             )
#             rich.print(panel)
#
#     def _mypy(self) -> None:
#         _tmp_env = os.environ.copy()
#         _tmp_env["MYPY_FORCE_COLOR"] = "1"
#         _mypy_out = subprocess.run(
#             [self.python_binary, "-m", "mypy", "."],
#             check=False,
#             capture_output=True,
#             text=True,
#             env=_tmp_env,
#         )
#         panel = rich.panel.Panel(
#             rich.text.Text.from_ansi(_mypy_out.stdout),
#             title="Mypy",
#             border_style="red" if _mypy_out.returncode == 1 else "blue",
#             title_align=click.RichHelpConfiguration.align_errors_panel,
#             # expand=False,
#         )
#         rich.print(panel)
#
#
#     def _ruff(self) -> None:
#         _tmp_env = os.environ.copy()
#         _tmp_env["CLICOLOR_FORCE"] = "1"
#         _ruff_out = subprocess.run(
#             [self.python_binary, "-m", "ruff", "check"],
#             check=False,
#             capture_output=True,
#             text=True,
#             env=_tmp_env,
#         )
#         panel = rich.panel.Panel(
#             rich.text.Text.from_ansi(_ruff_out.stdout),
#             title="Ruff",
#             border_style="red" if _ruff_out.returncode == 1 else "magenta",
#             title_align=click.RichHelpConfiguration.align_errors_panel,
#             # expand=False,
#         )
#         rich.print(panel)
#
#
#
#
#
#
#
# # * ``black`` (might be a gray)
# # * ``red``
# # * ``green``
# # * ``yellow`` (might be an orange)
# # * ``blue``
# # * ``magenta``
# # * ``cyan``
# # * ``white`` (might be light gray)
# # * ``bright_black``
# # * ``bright_red``
# # * ``bright_green``
# # * ``bright_yellow``
# # * ``bright_blue``
# # * ``bright_magenta``
# # * ``bright_cyan``
# # * ``bright_white``




