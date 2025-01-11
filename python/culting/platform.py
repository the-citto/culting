"""
Core.

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



class Platform(abc.ABC):
    """Platform."""

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

    def __new__(cls) -> toml.TOMLDocument:
        """Return pyproject.toml document."""
        cls.doc = toml.document()
        cls.doc.add(toml.nl())
        cls.doc["build-system"] = cls._build_system()
        cls.doc["project"] = cls._project()
        cls.doc["tool"] = cls._tool()
        return cls.doc

    @classmethod
    def _build_system(cls) -> tomlkit.items.Table:
        build_system = toml.table()
        build_system["requires"] = ["setuptools", "setuptools-scm"]
        build_system["build-backend"] = "setuptools.build_meta"
        return build_system

    @classmethod
    def _project(cls) -> tomlkit.items.Table:
        project = toml.table()
        project["name"] = "placeholder"
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
        authors = toml.array()
        authors.multiline(multiline=True)
        authors.add_line(cls._author(), newline=True)
        return authors

    @classmethod
    def _author(cls) -> tomlkit.items.InlineTable:
        author = toml.inline_table()
        author["name"] = ""
        author["email"] = ""
        return author

    @classmethod
    def _classifiers(cls) -> tomlkit.items.Array:
        classifiers = toml.array()
        classifiers.extend([
            "License :: OSI Approved :: MIT License",
            "Typing :: Typed",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
        ])
        return classifiers.multiline(multiline=True)

    @classmethod
    def _optional_dependencies(cls) -> tomlkit.items.Table:
        optional_dependencies = toml.table()
        optional_dependencies["tests"] = cls._tests()
        optional_dependencies["dev"] = cls._dev()
        return optional_dependencies

    @classmethod
    def _tests(cls) -> tomlkit.items.Array:
        tests = toml.array()
        tests.extend([
            "coverage",
            "pytest",
            "pytest-cov",
            "pytest-ruff",
            "pytest-mypy",
            "pytest-pyright",
        ])
        return tests.multiline(multiline=True)

    @classmethod
    def _dev(cls) -> tomlkit.items.Array:
        dev = toml.array()
        dev.extend([
            "culting[tests]",
            "ipython",
        ])
        return dev.multiline(multiline=True)

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
        package_data["placeholder"] = ["py.typed"]
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
        find["where"] = ["src"]
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
    def _culting(cls) -> tomlkit.items.Table:
        return toml.table()


print(toml.dumps(PyprojectToml()))
print(platform_info.xdg_config_home())


# def _pyproject_toml_default() -> None:
    # doc["tool"] = tool
    # print(toml.dumps(doc))
    # print(platform_info.xdg_config_home())

# _pyproject_toml_default()

# def _config_toml_default() -> None:
#     doc = toml.document()
#     doc.add(toml.nl())
#     _python = toml.table()
#     _python["path"] = ""
#     doc["python"] = _python
#
#     doc.add(toml.nl())
#     print(platform_info.xdg_config_home())
#     print(toml.dumps(doc))
#
# _config_toml_default()






# [tool.mypy]
# plugins = ['pydantic.mypy']
# strict = true
# python_executable = ".venv/bin/python"
# exclude = [
#     "__pycache__",
#     ".git",
#     ".venv",
# ]
#
# [tool.pyright]
# venvPath = "."
# venv = ".venv"
# enableReachabilityAnalysis = false
# include = [
#     "python",
#     "tests",
# ]
# exclude = [
#     "__pycache__",
#     ".git",
#     ".venv",
# ]
#
# [tool.ruff]
# exclude = [
#     "__pycache__",
#     ".git",
#     ".venv",
# ]
# line-length = 120
# indent-width = 4
#
# [tool.ruff.lint]
# select = [
#     "ALL"
# ]
# ignore = [
#     "D203", # `one-blank-line-before-class`
#     "D212", # `multi-line-summary-first-line`
#     "ERA001", # Found commented-out code
#     "S602", # `subprocess` call with `shell=True` identified, security issue
#     # "S603", # `subprocess` call: check for execution of untrusted input # false positives
# ] # (D203) mutually exclusive with (D211) - (D212) mutually exclusive with (D213)
#
# [tool.ruff.lint.per-file-ignores]
# "tests/**/*.py" = [
#     "ANN401", # Dynamically typed expressions (typing.Any) are disallowed
#     "PLR2004", # Magic value used in comparison
#     "S101",
# ] # (S101) Use of `assert`
#
# [tool.ruff.lint.isort]
# known-first-party = ["culting"]
# lines-after-imports = 2
















