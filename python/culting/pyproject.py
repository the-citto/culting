"""Pyproject."""

import typing as t

import tomlkit as toml
import tomlkit.items

from . import (
    SupportedOs,
    platform_info,
)


class AuthorInfo(t.TypedDict):
    """Author info."""

    name: str
    email: str


class ProjectType:
    """Project type."""

    cli: str


class PyprojectToml:
    """Pyproject toml document."""

    venv_name = ".venv"

    def __new__(
        cls,
        pkg_name: str,
        python_version: str,
        authors_info: t.Iterable[AuthorInfo],
        src: str = "src",
    ) -> toml.TOMLDocument:
        """Return pyproject.toml document."""
        cls.pkg_name = pkg_name
        cls.python_version = python_version
        cls.os = platform_info.os
        cls.authors_info = authors_info
        cls.src = src
        doc = toml.document()
        doc.add(toml.nl())
        doc["build-system"] = cls._build_system()
        doc["project"] = cls._project()
        doc["tool"] = cls._tool()
        doc.add(toml.nl())
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
        project["requires-python"] = f">={cls.python_version}"
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
        urls.add(toml.comment('"Homepage" = ""'))
        urls.add(toml.comment('"Repository" = ""'))
        urls.add(toml.comment('"Documentation" = ""'))
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
        find["where"] = [cls.src]
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
    def _mypy(cls, os_: SupportedOs = platform_info.os) -> tomlkit.items.Table:
        mypy = toml.table()
        mypy["strict"] = True
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
        lint["per-file-ignores"] = cls._ruff_lint_per_file_ignore()
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
    def _ruff_lint_per_file_ignore(cls) -> tomlkit.items.Table:
        pattern = toml.array().multiline(multiline=True)
        pattern.add_line("S101", comment="Use of `assert` detected")
        ruff_lint_per_file_ignore = toml.table()
        ruff_lint_per_file_ignore["tests/**/*.py"] = pattern
        return ruff_lint_per_file_ignore

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


