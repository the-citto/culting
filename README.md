# 🏗️ Culting
[github_release]: https://img.shields.io/github/release/the-citto/culting.svg?logo=github&logoColor=white&color=orange
[pypi_version]: https://img.shields.io/pypi/v/culting.svg?logo=python&logoColor=white
[python_versions]: https://img.shields.io/pypi/pyversions/culting.svg?logo=python&logoColor=white
[github_license]: https://img.shields.io/github/license/the-citto/culting.svg?logo=github&logoColor=white
<!-- [github_action_tests]: https://github.com/the-citto/culting/actions/workflows/tests.yml/badge.svg -->

[![GitHub Release][github_release]](https://github.com/the-citto/culting/releases/)
[![PyPI Version][pypi_version]](https://pypi.org/project/culting/)
[![Python Versions][python_versions]](https://pypi.org/project/culting/)
[![License][github_license]](https://github.com/the-citto/culting/blob/master/LICENSE)
<br>
<!-- [![Tests][github_action_tests]](https://github.com/the-citto/culting/actions/workflows/tests.yml) -->

<!-- [![image](https://img.shields.io/pypi/v/culting.svg)](https://pypi.python.org/pypi/culting) -->
<!-- [![image](https://img.shields.io/pypi/l/culting.svg)](https://pypi.python.org/pypi/culting) -->
<!-- [![image](https://img.shields.io/pypi/pyversions/culting.svg)](https://pypi.python.org/pypi/culting) -->

> #
> **Cargo Culting** [🔗](https://en.wiktionary.org/wiki/cargo_culting)
> #
> **Etymology**
> 
> From cargo _cult_ +‎ _-ing_.
> 
> **Noun**
> 
> (chiefly computing) An approach that copies an existing successful approach
> without properly analysing and understanding it.
>
> **Further reading**
>
> _cargo cult programming_ on Wikipedia [🔗](https://en.wikipedia.org/wiki/cargo_cult_programming).
> #

## 🛠️ Python Toolchain

`git` [🔗](https://git-scm.com/) / `libgit2` `pygit2` [🔗](https://github.com/libgit2/pygit2)

`uv` [🔗](https://docs.astral.sh/uv/)


`py.typed` [🔗](https://peps.python.org/pep-0561/#packaging-type-information)

`pyproject.toml` [🔗](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
> `✅ TODO` options to split settings from `pyproject.toml`
>
> ex.
> `ruff.toml` / `.ruff.toml` [🔗](https://docs.astral.sh/ruff/configuration/), 
> `mypy.ini` / `.mypy.ini` [🔗](https://mypy.readthedocs.io/en/stable/config_file.html)

`pyright` [🔗](https://microsoft.github.io/pyright/)

`mypy` [🔗](https://mypy.readthedocs.io/)

`ruff` [🔗](https://docs.astral.sh/ruff/)

`pytest` [🔗](https://docs.pytest.org/en/stable/)

>`✅ TODO`
>
> `tox` [🔗](https://tox.wiki/) (probably covered by `uv`)

>`✅ TODO`
>
> `podman` [🔗](https://podman.io/) / `docker` [🔗](https://www.docker.com/) project setup

>`✅ TODO`
>
> `GitHub CLI` / `gh` [🔗](https://cli.github.com/manual/)

>`✅ TODO`
>
> GitHub workflows management [🔗](https://docs.github.com/en/actions/writing-workflows)

### My old toolchain
replacing the following (currently used with `make` [here](https://github.com/the-citto/pyproject-base)) with `uv`

`pip` [🔗](https://pip.pypa.io/)

`venv` [🔗](https://docs.python.org/3/library/venv.html)

`setuptools` [🔗](https://setuptools.pypa.io/en/latest/)

`pip-tools` [🔗](https://pip-tools.readthedocs.io/) based on `requirements*.in` files

`requirements` files possibly soon superseeded by a `python.lock` [file](https://discuss.python.org/t/uv-another-rust-tool-written-to-replace-pip/46039/67)?

`pyenv` [🔗](https://github.com/pyenv/pyenv)

`py` launcher [🔗](https://docs.python.org/3/using/windows.html#launcher), (for Windows)

`.python-version` [🔗](https://github.com/pyenv/pyenv?tab=readme-ov-file#understanding-python-version-selection)




