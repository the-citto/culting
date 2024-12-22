"""Typing."""

import typing as t

import pydantic



SupportedOs = t.Literal["linux", "win32"]



class InitKwargs(t.TypedDict):
    """Init kwargs."""

    path: str
    name: str | None
    default: bool
    pyenv: str | None
    py: str | None
    uv: str | None
    venv: str
    src: str


GitEmails = pydantic.EmailStr | t.Literal[""] | None



