"""Click commands."""

import os
import pathlib
import re
import subprocess

from . import (
    logger,
    platform_info,
)


class NewProjectError(RuntimeError):
    """New project error."""



class NewProject:
    """New project."""

    def __init__(self, python_version: str, project_name: str) -> None:
        """Init."""
        self.python_version = python_version
        self.project_name = project_name.lower()
        # self._set_dir()
        self._set_python()

    def _set_dir(self) -> None:
        project_name_re = re.match(r"[a-z][a-z0-9-_]+$", self.project_name)
        if project_name_re is None:
            err_msg = f"Invalid project name: '{self.project_name}'"
            raise NewProjectError(err_msg)
        self.project_dir = pathlib.Path(self.project_name).absolute()
        if self.project_dir.is_dir():
            err_msg = f"Directory already exists: '{self.project_name}'"
            raise NewProjectError(err_msg)
        self.project_dir.mkdir()

    def _set_python(self) -> None:
        python_version_re = re.match(r"(3.[\d]{1,2})(t?)$", self.python_version)
        if python_version_re is None:
            err_msg = f"Invalid python version: '{self.python_version}'"
            raise NewProjectError(err_msg)
        _python_version, _threaded = python_version_re.groups()
        os.environ["PYENV_VERSION"] = self.python_version
        cmd = ["pyenv", "versions"]
        _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
        pyenv_version_re = re.search(r"\* " + re.escape(_python_version) + r"\.\d{1,2}" + _threaded + " ", _out.stdout)
        if pyenv_version_re is None:
            err_msg = f"Python version not installed: '{self.python_version}'"
            raise NewProjectError(err_msg)


        # os.environ["PYENV_VERSION"] = self.python_version
        # cmd = ["python", "-VV"]
        # _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
        #
        # # logger.error(_out.stderr.strip())
        # logger.info(_out.stdout.strip())
        # logger.info(_out.stdout.strip())
        # logger.info(python_version_re.groups())
        # # pyenv_version_re = re.search(r"(" + re.escape(self.python_version) + r").+", _out.stdout)
        # # print(re.escape(self.python_version) + r".+")
        # # print(_out.stdout)
        # if pyenv_version_re is None:
        #     print("None")
        # else:
        #     print(pyenv_version_re.groups())
        # os.environ["PYENV_VERSION"] = "3.15"
        # # cmd = ["python", "-VV"]
        # cmd = ["pyenv", "which", "python"]
        # _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
        # logger.error(_out.stderr.strip())
        # logger.info(_out.stdout.strip())

        # if platform_info.os == "linux":
        #     cmd = ["eval", '"$(pyenv init -)"']
        #     _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
        #     if _out.returncode != 0:
        #         logger.error(_out.stderr.strip())
        #
        #     cmd = [platform_info.python_manager, "shell", self.python_version]
        #     _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
        #     if _out.returncode != 0:
        #         logger.error(_out.stderr.strip())
#     ctx.abort()

#     pyenv_root = os.environ.get("PYENV_ROOT")
#     if pyenv_root is None:
#         raise RuntimeError
#     pyenv_shim = pathlib.Path(pyenv_root) / f"shims/python{python_version}"
#     if not pyenv_shim.exists():
#         err_msg = f"Python version not found: '{python_version}'"
#         logger.error(err_msg)
#         ctx.abort()
#     cmd = [pyenv_shim, "-V"]
# elif platform_info.os == "win32":
#     os.environ["PY_PYTHON"] = python_version
#     cmd = [platform_info.python_manager, "-V"]
# else:
#     raise RuntimeError
# _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
# if _out.returncode != 0:
#     logger.error(_out.stderr.strip())
#     ctx.abort()
# # if _out.returncode == 0:
# #     pathlib.Path(".python-version").write_text(python_version)




