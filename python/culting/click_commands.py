"""Click commands."""

import os
import pathlib
import re
import subprocess
import typing as t
import urllib.request

import tomlkit as toml

from . import (
    platform_info,
    pyproject,
)


class CommandError(RuntimeError):
    """Command error."""


def _subprocess_run(cmd: list[pathlib.Path | str]) -> str:
    _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if _out.returncode != 0:
        raise CommandError(_out.stderr.strip())
    return _out.stdout.strip()


class NewProjectKwargs(t.TypedDict):
    """NewProject kwargs."""

    python_version: str
    src: str
    project_name: str


class NewProject:
    """New project."""

    gitignore_url = "https://github.com/github/gitignore/raw/refs/heads/main/Python.gitignore"

    def __init__(self, **kwargs: t.Unpack[NewProjectKwargs]) -> None:
        """Init."""
        self.python_version = kwargs.get("python_version")
        self.src = kwargs.get("src")
        self.project_name = kwargs.get("project_name")
        self._set_dir()
        self._set_python()
        self._init_git()
        self._set_files()
        self._init_venv()

    def _set_dir(self) -> None:
        project_name_re = re.match(r"[a-z][a-z0-9-_]+[a-z0-9]$", self.project_name)
        if project_name_re is None:
            err_msg = (
                f"Invalid argumant: [cyan]PROJECT_NAME[/cyan] '{self.project_name}'"
                "\n  [cyan]PROJECT_NAME[/cyan] must be PEP 8 and PEP 423 compliant."
            )
            raise CommandError(err_msg)
        self.project_dir = pathlib.Path(self.project_name).absolute()
        try:
            self.project_dir.mkdir()
            os.chdir(self.project_dir)
        except FileExistsError as err:
            err_msg = f"Directory already exists: '{self.project_name}'"
            raise CommandError(err_msg) from err

    # def _run(self, cmd: list[pathlib.Path | str]) -> str:
    #     _out = subprocess.run(cmd, check=False, capture_output=True, text=True)
    #     if _out.returncode != 0:
    #         raise NewProjectError(_out.stderr.strip())
    #     return _out.stdout.strip()

    def _set_python(self) -> None:
        python_version_re = re.match(r"(3.\d{1,2})(t?)$", self.python_version)
        if python_version_re is None:
            err_msg = f"Invalid python version: '{self.python_version}'"
            raise CommandError(err_msg)
        if platform_info.os == "linux":
            _subprocess_run([platform_info.python_manager, "local", self.python_version])
        else:
            raise NotImplementedError

    def _set_files(self) -> None:
        (self.project_dir / "LICENSE").touch()
        (self.project_dir / "requirements.in").touch()
        with urllib.request.urlopen(self.gitignore_url) as response: # noqa: S310
            _gitignore_bytes = response.read()
            (self.project_dir / ".gitignore").write_text(_gitignore_bytes.decode())
        tests_dir = (self.project_dir / "tests")
        tests_dir.mkdir()
        (tests_dir / "__init__.py").touch()
        package_dir = self.project_dir / "python" / self.project_name
        package_dir.mkdir(parents=True)
        (package_dir / "__init__.py").touch()
        (package_dir / "__main__.py").touch()
        _pyproject = pyproject.PyprojectToml(
            pkg_name=self.project_name,
            python_version=self.python_version,
            src=self.src,
            authors_info=[{"name": self.git_name, "email": self.git_email}],
        )
        with (self.project_dir / "pyproject.toml").open("w") as p:
            p.write(toml.dumps(_pyproject))

    def _init_git(self) -> None:
        (self.project_dir / "README.md").write_text(f"# {self.project_name}")
        _subprocess_run([platform_info.git, "init", "."])
        _subprocess_run([platform_info.git, "add", "README.md"])
        _subprocess_run([platform_info.git, "commit", "-m", "'Add README.md'"])
        _subprocess_run([platform_info.git, "tag", "-a", "v0.1.0", "-m", "Release version 0.1.0"])
        self.git_name = _subprocess_run([platform_info.git, "config", "user.name"])
        self.git_email = _subprocess_run([platform_info.git, "config", "user.email"])

    def _init_venv(self) -> None:
        if platform_info.os == "linux":
            _subprocess_run(["python", "-m", "venv", ".venv"])
        else:
            raise NotADirectoryError
        _subprocess_run([platform_info.venv_python, "-m", "pip", "install", "pip-tools"])
        Dependencies().pip_editable_mode()



class Dependencies:
    """Dependencies."""

    def add(self, libraries: tuple[str, ...]) -> None:
        """Add."""
        # _list_re = [re.match(r"(\w+)(.*)$", li).group(1) for li in self.list_]
        # print(_list_re)
        for library in libraries:
            library_re = re.match(r"([\w_-]+).*$", library)
            if library_re is None:
                raise CommandError
            print(library_re.group(1))

    def pip_editable_mode(self) -> None:
        """Pip editable mode."""
        self._pip_sync()
        _subprocess_run([platform_info.venv_python, "-m", "pip", "install", "-e", ".[dev]"])

    @property
    def list_(self) -> list[str]:
        """List."""
        with pathlib.Path("requirements.in").open("r") as r:
            requirements = r.read()
        requirements = sorted(requirements.splitlines())
        with pathlib.Path("requirements.in").open("w") as r:
            r.write("\n".join(requirements) + "\n")
        self._dup_libraries(requirements)
        return requirements

    def _dup_libraries(self, libs: list[str]) -> list[str]:
        lib_tuples = []
        for lib in libs:
            lib_re = re.match(r"(\w+)([~=><]*.*)", lib)
            if lib_re is None:
                raise CommandError
            lib_tuples.append(lib_re.groups())
        lib_names = [li[0] for li in lib_tuples]
        return ["".join(lib_tuple) for lib_tuple in lib_tuples if lib_names.count(lib_tuple[0]) > 1]



    def _pip_upgrade(self) -> None:
        _subprocess_run([platform_info.venv_python, "-m", "pip", "install", "--upgrade", "pip"])

    def _pip_compile(self) -> None:
        self._pip_upgrade()
        _subprocess_run([
            platform_info.venv_python,
            "-m",
            "piptools",
            "compile",
            "-o",
            "requirements.lock",
            "requirements.in",
            "--no-strip-extras",
        ])

    def _pip_sync(self) -> None:
        self._pip_compile()
        _subprocess_run([platform_info.venv_python, "-m", "piptools", "sync", "requirements.lock"])





