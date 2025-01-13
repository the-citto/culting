"""Core.

Refs:
    XDG Base Directory Specification: https://specifications.freedesktop.org/basedir-spec/latest/
"""

import abc
import logging
import pathlib
import sys
import typing as t

import tomlkit as toml
import tomlkit.items
from pj_logging.pj_logging import set_logger


SupportedOs = t.Literal["linux", "win32"]

__os__: SupportedOs = t.cast(SupportedOs, sys.platform)


class AuthorInfo(t.TypedDict):
    """Author info."""

    name: t.NotRequired[str]
    email: t.NotRequired[str]


class Platform(abc.ABC):
    """Platform.

    Stuff.
    """

    pkg_name: str = "culting"

    @classmethod
    @abc.abstractmethod
    def xdg_config_dirname(cls) -> str:
        """Define platform XDG config dirname."""

    @classmethod
    @abc.abstractmethod
    def xdg_state_dirname(cls) -> str:
        """Define platform XDG state dirname."""

    @classmethod
    def xdg_config_home(cls) -> pathlib.Path:
        """Create and return platform XDG config home path."""
        _xdg_config_home = pathlib.Path.home() / cls.xdg_config_dirname() / cls.pkg_name
        _xdg_config_home.mkdir(parents=True, exist_ok=True)
        return _xdg_config_home

    @classmethod
    def xdg_state_home(cls) -> pathlib.Path:
        """Create and return platform XDG state home path."""
        _xdg_state_home = pathlib.Path.home() / cls.xdg_state_dirname() / cls.pkg_name
        _xdg_state_home.mkdir(parents=True, exist_ok=True)
        return _xdg_state_home

    @classmethod
    def set_logger(cls) -> logging.Logger:
        """Set logger."""
        return set_logger(
            name=cls.pkg_name,
            jsonl_log_file_path=cls.xdg_state_home() / f"{cls.pkg_name}.log",
            jsonl_log_file_size=1_000_000,
            rich_panel_log=True,
        )

    # @classmethod
    # @abc.abstractmethod
    # def default_python_version(cls) -> str:
    #     """Return default python version."""


class LinuxPlatform(Platform):
    """Linux platform."""

    @classmethod
    def xdg_config_dirname(cls) -> str:
        """Create and return platform XDG config home path."""
        return ".config"

    @classmethod
    def xdg_state_dirname(cls) -> str:
        """Create and return platform XDG state home path."""
        return ".local/state"


class Win32Platform(Platform):
    """Win32 platform."""

    @classmethod
    def xdg_config_dirname(cls) -> str:
        """Create and return platform XDG config home path."""
        return "Appdata/Local"

    @classmethod
    def xdg_state_dirname(cls) -> str:
        """Create and return platform XDG state home path."""
        return "Appdata/Local/Temp"


if __os__ == "linux":
    platform_info = LinuxPlatform()
elif __os__ == "win32":
    platform_info = Win32Platform()
else:
    err_msg = f"OS '{__os__}' not supported."
    logger = set_logger(rich_panel_log=True)
    logger.error(err_msg)
    sys.exit(1)


# __xdg_config_home__ = _platform.xdg_config_home()
# __xdg_state_home__ = _platform.xdg_state_home()

logger = platform_info.set_logger()


class PyprojectToml:
    """Pyproject toml document."""

    def __new__(
        cls,
        pkg_name: str = "pkg_name",
        authors_info: t.Iterable[AuthorInfo] = [AuthorInfo(name="", email="")],
        os_: SupportedOs = __os__,
        venv_name: str = ".venv",
        src_name: str = "src",
    ) -> toml.TOMLDocument:
        """Return pyproject.toml document."""
        cls.os_ = os_
        cls.authors_info = authors_info
        cls.pkg_name = pkg_name
        cls.venv_name = venv_name
        cls.src_name = src_name
        doc = toml.document()
        doc.add(toml.nl())
        doc["build-system"] = cls._build_system()
        doc["project"] = cls._project()
        doc["tool"] = cls._tool()
        return doc

    @classmethod
    def _build_system(cls) -> tomlkit.items.Table:
        build_system = toml.table()
        build_system["requires"] = ["setuptools", "setuptools-scm"]
        build_system["build-backend"] = "setuptools.build_meta"
        return build_system

    @classmethod
    def _project(cls) -> tomlkit.items.Table:
        project = toml.table()
        project["name"] = cls.pkg_name
        project["description"] = ""
        project["readme"] = "README.md"
        project["keywords"] = cls._keywords()
        project["requires-python"] = ""
        project["dynamic"] = cls._dynamic()
        project.add(toml.nl())
        project["authors"] = cls._authors()
        project["classifiers"] = cls._classifiers()
        project["optional-dependencies"] = cls._optional_dependencies()
        project["urls"] = cls._urls()
        project["scripts"] = cls._scripts()
        project["gui-scripts"] = cls._gui_scripts()
        return project

    @classmethod
    def _keywords(cls) -> tomlkit.items.Array:
        return toml.array()

    @classmethod
    def _dynamic(cls) -> tomlkit.items.Array:
        dynamic = toml.array()
        dynamic.multiline(multiline=True)
        dynamic.extend(["version", "dependencies"])
        return dynamic

    @classmethod
    def _authors(cls) -> tomlkit.items.Array:
        authors = toml.array().multiline(multiline=True)
        for author_info in cls.authors_info:
            authors.add_line(cls._author(author_info), newline=True)
        return authors

    @classmethod
    def _author(cls, author_info: AuthorInfo) -> tomlkit.items.InlineTable:
        author = toml.inline_table()
        name = author_info.get("name")
        if name is not None:
            author["name"] = name
        email = author_info.get("email")
        if email is not None:
            author["email"] = email
        return author

    @classmethod
    def _classifiers(cls) -> tomlkit.items.Array:
        classifiers = toml.array().multiline(multiline=True)
        classifiers.extend([
            "License :: OSI Approved :: MIT License",
            "Typing :: Typed",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
        ])
        return classifiers

    @classmethod
    def _optional_dependencies(cls) -> tomlkit.items.Table:
        optional_dependencies = toml.table()
        optional_dependencies["tests"] = cls._tests()
        optional_dependencies["dev"] = cls._dev()
        return optional_dependencies

    @classmethod
    def _tests(cls) -> tomlkit.items.Array:
        tests = toml.array().multiline(multiline=True)
        tests.extend([
            "coverage",
            "pytest",
            "pytest-cov",
            "pytest-ruff",
            "pytest-mypy",
            "pytest-pyright",
        ])
        return tests

    @classmethod
    def _dev(cls) -> tomlkit.items.Array:
        dev = toml.array().multiline(multiline=True)
        dev.extend([
            "culting[tests]",
            "ipython",
        ])
        return dev

    @classmethod
    def _urls(cls) -> tomlkit.items.Table:
        urls = toml.table()
        urls["Homepage"] = ""
        urls["Repository"] = ""
        urls["Documentation"] = ""
        return urls

    @classmethod
    def _scripts(cls) -> tomlkit.items.Table:
        return toml.table()

    @classmethod
    def _gui_scripts(cls) -> tomlkit.items.Table:
        return toml.table()

    @classmethod
    def _tool(cls) -> tomlkit.items.Table:
        tool = toml.table()
        tool["setuptools_scm"] = cls._setuptools_scm()
        tool["setuptools"] = cls._setuptools()
        tool["pytest"] = cls._pytest()
        tool["coverage"] = cls._coverage()
        tool["mypy"] = cls._mypy()
        tool["pyright"] = cls._pyright()
        tool["ruff"] = cls._ruff()
        tool["culting"] = cls._culting()
        return tool

    @classmethod
    def _setuptools_scm(cls) -> tomlkit.items.Table:
        return toml.table()

    @classmethod
    def _setuptools(cls) -> tomlkit.items.Table:
        setuptools = toml.table()
        setuptools["package-data"] = cls._setuptools_package_data()
        setuptools["dynamic"] = cls._setuptools_dynamic()
        setuptools["packages"] = cls._setuptools_packages()
        return setuptools

    @classmethod
    def _setuptools_package_data(cls) -> tomlkit.items.Table:
        package_data = toml.table()
        package_data[cls.pkg_name] = ["py.typed"]
        return package_data

    @classmethod
    def _setuptools_dynamic(cls) -> tomlkit.items.Table:
        setuptools_dynamic = toml.table()
        setuptools_dynamic["dependencies"] = cls._setuptools_dynamic_dependencies()
        return setuptools_dynamic

    @classmethod
    def _setuptools_dynamic_dependencies(cls) -> tomlkit.items.InlineTable:
        dependencies = toml.inline_table()
        dependencies["file"] = ["requirements.lock"]
        return dependencies

    @classmethod
    def _setuptools_packages(cls) -> tomlkit.items.Table:
        setuptools_packages = toml.table()
        setuptools_packages["find"] = cls._setuptools_packages_find()
        return setuptools_packages

    @classmethod
    def _setuptools_packages_find(cls) -> tomlkit.items.Table:
        find = toml.table()
        find["where"] = [cls.src_name]
        return find

    @classmethod
    def _pytest(cls) -> tomlkit.items.Table:
        pytest = toml.table()
        pytest["ini_options"] = cls._pytest_ini_options()
        return pytest

    @classmethod
    def _pytest_ini_options(cls) -> tomlkit.items.Table:
        ini_options = toml.table()
        ini_options["addopts"] = "--strict-markers --no-header --tb=no --cov --cov-report term-missing"
        ini_options["testpaths"] = ["tests"]
        return ini_options

    @classmethod
    def _coverage(cls) -> tomlkit.items.Table:
        coverage = toml.table()
        coverage["run"] = cls._coverage_run()
        return coverage

    @classmethod
    def _coverage_run(cls) -> tomlkit.items.Table:
        coverage_run = toml.table()
        coverage_run["omit"] = ["tests/*"]
        return coverage_run

    @classmethod
    def _mypy(cls, os_: SupportedOs = __os__) -> tomlkit.items.Table:
        mypy = toml.table()
        mypy["strict"] = "true"
        if os_ == "linux":
            mypy["python_executable"] = f"{cls.venv_name}/bin/python"
        elif os_ == "win32":
            mypy["python_executable"] = f"{cls.venv_name}/Scripts/python.exe"
        mypy["exclude"] = cls._exclude()
        return mypy

    @classmethod
    def _pyright(cls) -> tomlkit.items.Table:
        pyright = toml.table()
        pyright["venvPath"] = "."
        pyright["venv"] = cls.venv_name
        pyright["exclude"] = cls._exclude()
        return pyright

    @classmethod
    def _ruff(cls) -> tomlkit.items.Table:
        ruff = toml.table()
        ruff["line-length"] = 120
        ruff["indent-width"] = 4
        ruff["exclude"] = cls._exclude()
        ruff["lint"] = cls._ruff_lint()
        return ruff

    @classmethod
    def _ruff_lint(cls) -> tomlkit.items.Table:
        lint = toml.table()
        lint["select"] = cls._ruff_lint_select()
        lint["ignore"] = cls._ruff_lint_ignore()
        lint["tests/**/*.py"] = cls._ruff_lint_per_file_ignore()
        lint["isort"] = cls._ruff_lint_isort()
        return lint

    @classmethod
    def _ruff_lint_select(cls) -> tomlkit.items.Array:
        lint_select = toml.array().multiline(multiline=True)
        lint_select.extend(["ALL"])
        return lint_select

    @classmethod
    def _ruff_lint_ignore(cls) -> tomlkit.items.Array:
        lint_ignore = toml.array().multiline(multiline=True)
        lint_ignore.add_line(
            "D203",
            comment=(
                "1 blank line required before class docstring"
                '\n    # "D211" # No blank lines allowed before class docstring'
                '\n    # "D212" # Multi-line docstring summary should start at the first line'
            ),
        )
        lint_ignore.add_line(
            "D213",
            comment=(
                "Multi-line docstring summary should start at the second line"
            ),
        )
        return lint_ignore

    @classmethod
    def _ruff_lint_per_file_ignore(cls) -> tomlkit.items.Array:
        pattern = toml.array().multiline(multiline=True)
        pattern.add_line("S101", comment="Use of `assert` detected")
        return pattern

    @classmethod
    def _ruff_lint_isort(cls) -> tomlkit.items.Table:
        ruff_isort = toml.table()
        ruff_isort["known-first-party"] = [cls.pkg_name]
        ruff_isort["lines-after-imports"] = 2
        return ruff_isort

    @classmethod
    def _exclude(cls) -> tomlkit.items.Array:
        exclude = toml.array().multiline(multiline=True)
        exclude.extend([
            "__pycache__",
            ".git",
            cls.venv_name,
        ])
        return exclude

    @classmethod
    def _culting(cls) -> tomlkit.items.Table:
        return toml.table()


print(toml.dumps(PyprojectToml(os_=__os__)))
print(platform_info.xdg_config_home())
# [tool.ruff.lint.isort]
# known-first-party = ["culting"]
# lines-after-imports = 2
















