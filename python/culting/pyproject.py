"""Pyproject."""

import sys

import pydantic
import tomlkit as toml

from .defaults import culting_conf
from .logger import logger
from .types import PypiClassifiers
from .variables import (
    __os__,
    __xdg_config_home__,
)


class BuildSystem(pydantic.BaseModel):
    """Build system."""

    requires: list[str] = ["setuptools"]
    build_backend: str = pydantic.Field(alias="build-backend", default="setuptools.build_meta")


class ProjectOptionalDependencies(pydantic.BaseModel):
    """Project optional dependencies."""

    tests: list[str] = [
        "coverage",
        "pytest",
        "pytest-cov",
        "pytest-mypy",
        "pytest-ruff",
        "pytest-pyright",
    ]

    @pydantic.computed_field # type: ignore [prop-decorator]
    @property
    def dev(self) -> list[str]:
        """Return optional dev dependencies."""
        return [*self.tests, "ipython"]


class ProjectUrls(pydantic.BaseModel):
    """Project URLs."""

    Homepage: str | None = None
    Documentation: str | None = None
    Repository: str | None = None
    Issues: str | None = None
    Changelog: str | None = None


class ProjectAuthor(pydantic.BaseModel):
    """Project author."""

    name: str | None = "placeholder"
    email: str | None = "placeholder@abc.com"


class ProjectScripts(pydantic.BaseModel):
    """Project scripts."""

    # pkg: str = pydantic.Field(alias=__package__, default=f"{__package__}:__main__.main")


class ProjectGuiScripts(pydantic.BaseModel):
    """Project GUI scripts."""

    # pkg: str = pydantic.Field(alias=f"{__package__}w", default=f"{__package__}:__main__.main")


class Project(pydantic.BaseModel):
    """Project pyproject."""

    name: str = f"{__package__}"
    description: str | None = None
    version: str = "0.1.0"
    requires_python: str | None = pydantic.Field(alias="requires-python", default=None)
    authors: list[ProjectAuthor] = [ProjectAuthor()]
    readme: str = "README.md"
    license: dict[str, str] = {"file": "LICENSE"}
    keywords: list[str] | None = None
    classifiers: list[PypiClassifiers] = [
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux" if __os__ == "linux" else "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
    ]
    urls: ProjectUrls = ProjectUrls()
    scripts: ProjectScripts = ProjectScripts()
    gui_scripts: ProjectScripts = pydantic.Field(
        alias="gui-scripts",
        default=ProjectScripts(),
    )
    dynamic: list[str] = ["dependencies"]
    optional_dependencies: ProjectOptionalDependencies = pydantic.Field(
        alias="optional-dependencies",
        default=ProjectOptionalDependencies(),
    )

    # @pydantic.field_validator("requires_python")
    # @classmethod
    # def _valid_requires_python(cls, requires_python: str | None) -> str | None:
    #     if requires_python is None:
    #         return None
    #     if re.match(r"3\.\d")
    #     return requires_python


class ToolSetuptoolsPackagesFind(pydantic.BaseModel):
    """Setuptools packages find."""

    where: list[str] = [culting_conf.package.src]
    include: list[str] | None = None
    exclude: list[str] | None = None
    namespaces: bool | None = None


class ToolSetuptoolsPackages(pydantic.BaseModel):
    """Setuptools packages."""

    find: ToolSetuptoolsPackagesFind = ToolSetuptoolsPackagesFind()


class ToolSetuptoolsPackageData(pydantic.BaseModel):
    """Setuptools package-data."""

    pkg: list[str] | None = pydantic.Field(
        # alias=__package__,
        default=None,
    )


class ToolSetuptoolsDynamic(pydantic.BaseModel):
    """Setuptools dynamic."""

    dependencies: dict[str, list[str]] = {"file": ["requirements.lock"]}


class ToolSetuptools(pydantic.BaseModel):
    """Setuptools."""

    dynamic: ToolSetuptoolsDynamic = ToolSetuptoolsDynamic()
    package_data: ToolSetuptoolsPackageData = pydantic.Field(
        alias="package-data",
        default=ToolSetuptoolsPackageData(),
    )
    packages: ToolSetuptoolsPackages = ToolSetuptoolsPackages()


class PytestIniOptions(pydantic.BaseModel):
    """Pytest ini-options."""

    addopts: str = "--strict-markers --no-header --tb=no --cov --cov-report term-missing"
    testpaths: list[str] = ["tests"]


class Pytest(pydantic.BaseModel):
    """Pytest."""

    ini_options: PytestIniOptions = PytestIniOptions()


class CoverageRun(pydantic.BaseModel):
    """Coverage run."""

    omit: list[str] = ["tests/*"]


class Coverage(pydantic.BaseModel):
    """Coverage."""

    run: CoverageRun = CoverageRun()


class Mypy(pydantic.BaseModel):
    """Mypy."""

    strict: bool = True
    python_executable: str = (
        f"{culting_conf.package.venv}/bin/python"
        if __os__ == "linux"
        else
        f"{culting_conf.package.venv}/Scripts/python.exe"
    )
    exclude: list[str] = ["__pycache__", ".git", ".venv"]


class Pyright(pydantic.BaseModel):
    """Pyright."""

    venvPath: str = "." # noqa: N815
    venv: str = ".venv"
    enableReachabilityAnalysis: bool = False # noqa: N815
    include: list[str] = [culting_conf.package.src, "tests"]
    exclude: list[str] = ["__pycache__", ".git", ".venv"]


class RuffLintPerFileIgnores(pydantic.BaseModel):
    """Ruff lint per-file-ignores."""

    tests: list[str] = pydantic.Field(
        alias="tests/**/*.py",
        default=[
            "S101", # Use of `assert` detected
        ],
    )


class RuffLintIsort(pydantic.BaseModel):
    """Ruff lint isort."""

    known_first_party: list[str] = pydantic.Field(
        alias="known-first-party",
        default=[f"{__package__}"],
    )
    lines_after_imports: int | None = pydantic.Field(
        alias="lines-after-imports",
        default=2,
    )


class RuffLint(pydantic.BaseModel):
    """Ruff lint."""

    select: list[str] = ["ALL"]
    ignore: list[str] = [
        "D203", # `one-blank-line-before-class`
        # "D211", # `blank-line-before-class`
        "D212", # `multi-line-summary-first-line`
        # "D213", # `multi-line-summary-second-line`
    ]
    per_file_ignores: RuffLintPerFileIgnores = pydantic.Field(
        alias="per-file-ignores",
        default=RuffLintPerFileIgnores(),
    )
    isort: RuffLintIsort = RuffLintIsort()



class Ruff(pydantic.BaseModel):
    """Ruff."""

    exclude: list[str] = ["__pycache__", ".git", ".venv"]
    line_length: int = pydantic.Field(
        alias="line-length",
        default=120,
    )
    indent_width: int = pydantic.Field(
        alias="indent-width",
        default=4,
    )
    lint: RuffLint = RuffLint()


class Culting(pydantic.BaseModel):
    """Culting."""


class Tool(pydantic.BaseModel):
    """Tool."""

    setuptools: ToolSetuptools = ToolSetuptools()
    pytest: Pytest = Pytest()
    coverage: Coverage = Coverage()
    mypy: Mypy = Mypy()
    pyright: Pyright = Pyright()
    ruff: Ruff = Ruff()
    culting: Culting = Culting()


class CultingPyproj(pydantic.BaseModel):
    """Culting pyproject."""

    build_system: BuildSystem = pydantic.Field(alias="build-system", default=BuildSystem())
    project: Project = Project()
    tool: Tool = Tool()

    def toml_dump(self) -> toml.TOMLDocument:
        """Return as formatted pyproject.toml document."""
        _model_dump = self.model_dump(by_alias=True, exclude_none=True)
        _doc = toml.parse(toml.dumps(_model_dump))
        _project = _doc.get("project")
        if _project is None:
            raise KeyError
        _authors = _project.get("authors")
        _classifiers = _project.get("classifiers")
        if _classifiers is None:
            raise KeyError
        _classifiers.multiline(multiline=True)
        if _authors is None:
            raise KeyError
        _inline_authors = toml.array()
        for a in _authors:
            _tmp = toml.inline_table()
            _tmp.update(a)
            _inline_authors.add_line(_tmp, newline=True)
        _project["authors"] = _inline_authors.multiline(multiline=True)
        _project_optional_dependencies = _project["optional-dependencies"]
        _project_optional_dependencies["tests"].multiline(multiline=True)
        _project_optional_dependencies["dev"].multiline(multiline=True)
        _new_project = toml.table()
        for k, v in _project.items():
            _new_project.add(key=k, value=v)
        _project = _new_project
        _tool = _doc.get("tool")
        if _tool is None:
            raise KeyError
        _ruff_lint_ignore = _tool["ruff"]["lint"]["ignore"]
        _ruff_lint_ignore.comment("(D203) mutually exclusive with (D211) - (D212) mutually exclusive with (D213)")
        _ruff_lint_ignore.multiline(multiline=True)
        _ruff_lint_per_file_ignores = _tool["ruff"]["lint"]["per-file-ignores"]
        for k in _ruff_lint_per_file_ignores:
            _ruff_lint_per_file_ignores[k].multiline(multiline=True)
            if "S101" in _ruff_lint_per_file_ignores[k]:
                _ruff_lint_per_file_ignores[k].comment("(S101) Use of `assert`")
        _doc.add(toml.nl())
        return _doc


pyproj_default_path = __xdg_config_home__ / "pyproject-default.toml"
pyproj_custom_path = __xdg_config_home__ / "pyproject-custom.toml"

with pyproj_default_path.open("w") as file:
    toml.dump(CultingPyproj().toml_dump(), file)

try:
    if pyproj_custom_path.is_file():
        with pyproj_custom_path.open("r") as file:
            toml_value = toml.load(file).value
            culting_pyproj = CultingPyproj(**toml_value)
    else:
        culting_pyproj = CultingPyproj()
except pydantic.ValidationError as err:
    logger.exception(err)
    sys.exit(1)




