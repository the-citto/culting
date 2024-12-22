"""Typing."""

import typing as t

import pydantic



SupportedOs = t.Literal["linux", "win32"]


class InitKwargs(t.TypedDict):
    """Init kwargs."""

    path: str
    name: str | None
    default_python: str
    pyenv_python: str | None
    py_python: str | None
    uv_python: str | None


GitEmails = pydantic.EmailStr | t.Literal[""] | None



