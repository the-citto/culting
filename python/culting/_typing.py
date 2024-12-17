"""Typing."""

import typing as t

import pydantic



SupportedOs = t.Literal["linux", "win32"]

PythonVersions = t.Literal["3.10", "3.11", "3.12", "3.13"]


class InitKwargs(t.TypedDict):
    """Init kwargs."""

    path: str
    name: str | None
    python_version: PythonVersions | None


GitEmails = pydantic.EmailStr | t.Literal[""] | None



