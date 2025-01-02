"""Custom exceptions."""


class CommandNotFoundError(ImportError):
    """Binary not found."""

# class InitWarning(Warning):
#     """Init warning."""

class InitError(RuntimeError):
    """Init error."""


class RunError(RuntimeError):
    """Run error."""

