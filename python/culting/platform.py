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
        cls._add_build_system()
        cls._add_project()
        cls._add_tool()
        return cls.doc

    @classmethod
    def _add_culting(cls, tool: tomlkit.items.Table) -> None:
        tool_culting = toml.table()
        tool["culting"] = tool_culting

    @classmethod
    def _add_package_data(cls, setuptools: tomlkit.items.Table) -> None:
        package_data = toml.table()
        package_data["placeholder"] = ["py.typed"]
        setuptools["package-data"] = package_data

    @classmethod
    def _add_setuptools(cls, tool: tomlkit.items.Table) -> None:
        setuptools = toml.table()
        cls._add_package_data(setuptools)
        tool["setuptools"] = setuptools

    @classmethod
    def _add_setuptools_scm(cls, tool: tomlkit.items.Table) -> None:
        setuptools_scm = toml.table()
        tool["setuptools_scm"] = setuptools_scm

    @classmethod
    def _add_tool(cls) -> None:
        tool = toml.table()
        cls._add_setuptools_scm(tool)
        cls._add_setuptools(tool)

        cls._add_culting(tool)
        cls.doc["tool"] = tool

    @classmethod
    def _add_build_system(cls) -> None:
        build_system = toml.table()
        build_system["requires"] = ["setuptools", "setuptools-scm"]
        build_system["build-backend"] = "setuptools.build_meta"
        cls.doc["build-system"] = build_system

    @classmethod
    def _add_keywords(cls, project: tomlkit.items.Table) -> None:
        keywords = toml.array()
        project["keywords"] = keywords

    @classmethod
    def _add_dynamic(cls, project: tomlkit.items.Table) -> None:
        dynamic = toml.array()
        dynamic.extend(["version", "dependencies"])
        project["dynamic"] = dynamic.multiline(multiline=True)

    @classmethod
    def _add_authors(cls, project: tomlkit.items.Table) -> None:
        authors = toml.array()
        cls._add_author(authors)
        project["authors"] = authors.multiline(multiline=True)

    @classmethod
    def _add_author(cls, authors: tomlkit.items.Array) -> None:
        author = toml.inline_table()
        author["name"] = ""
        author["email"] = ""
        authors.add_line(author, newline=True)

    @classmethod
    def _add_classifiers(cls, project: tomlkit.items.Table) -> None:
        classifiers = toml.array()
        classifiers.extend([
            "License :: OSI Approved :: MIT License",
            "Typing :: Typed",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
        ])
        project["classifiers"] = classifiers.multiline(multiline=True)

    @classmethod
    def _add_tests(cls, optional_dependencies: tomlkit.items.Table) -> None:
        tests = toml.array()
        tests.extend([
            "coverage",
            "pytest",
            "pytest-cov",
            "pytest-ruff",
            "pytest-mypy",
            "pytest-pyright",
        ])
        optional_dependencies["tests"] = tests.multiline(multiline=True)

    @classmethod
    def _add_dev(cls, optional_dependencies: tomlkit.items.Table) -> None:
        dev = toml.array()
        dev.extend([
            "culting[tests]",
            "ipython",
        ])
        optional_dependencies["dev"] = dev.multiline(multiline=True)

    @classmethod
    def _add_optional_dependencies(cls, project: tomlkit.items.Table) -> None:
        optional_dependencies = toml.table()
        cls._add_tests(optional_dependencies)
        cls._add_dev(optional_dependencies)
        project["optional-dependencies"] = optional_dependencies

    @classmethod
    def _add_urls(cls, project: tomlkit.items.Table) -> None:
        urls = toml.table()
        urls["Homepage"] = ""
        urls["Repository"] = ""
        urls["Documentation"] = ""
        project["urls"] = urls

    @classmethod
    def _add_scripts(cls, project: tomlkit.items.Table) -> None:
        scripts = toml.table()
        project["scripts"] = scripts

    @classmethod
    def _add_gui_scripts(cls, project: tomlkit.items.Table) -> None:
        gui_scripts = toml.table()
        project["gui-scripts"] = gui_scripts

    @classmethod
    def _add_project(cls) -> None:
        project = toml.table()
        project["name"] = "placeholder"
        project["description"] = ""
        project["readme"] = "README.md"
        cls._add_keywords(project)
        project["requires-python"] = ""
        cls._add_dynamic(project)
        project.add(toml.nl())
        cls._add_authors(project)
        cls._add_classifiers(project)
        cls._add_optional_dependencies(project)
        cls._add_urls(project)
        cls._add_scripts(project)
        cls._add_gui_scripts(project)
        cls.doc["project"] = project


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




# [tool.setuptools.dynamic]
# dependencies = { file = ["requirements.lock"] }
#
# [tool.setuptools.packages.find]
# where = ["python"]
#
# [tool.pytest.ini_options]
# addopts = "--strict-markers --no-header --tb=no --cov --cov-report term-missing"
# testpaths = ["tests"]
#
# [tool.coverage.run]
# omit = ["tests/*"]
#
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
















