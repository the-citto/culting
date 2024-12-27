"""Typing."""

import typing as t

import pydantic



SupportedOs = t.Literal["linux", "win32"]

# PythonManager = t.Literal["pyenv", "py", "uv"]


class InitKwargs(t.TypedDict):
    """Init kwargs."""

    path: str
    name: str | None
    python_version: str
    python_path: str
    wsl: bool
    venv: str
    src: str


GitEmails = pydantic.EmailStr | t.Literal[""] | None



