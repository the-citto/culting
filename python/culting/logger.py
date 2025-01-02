"""Logger."""

import datetime as dt
import json
import logging
import logging.config
import logging.handlers
import typing as t

import rich
import rich.panel
import rich_click as click

from .variables import logfile_path


FILE_MAX_BITES = 100_000

# class DummyHandler(logging.Handler):
#     """Dummy handler."""
#
#     def __init__(self, level: int = 0) -> None:
#         super().__init__(level)

class ColorFormatter(logging.Formatter):
    """
    Color formatter.

    Courtesy of https://github.com/click-contrib/click-log
    """

    colors: t.ClassVar[dict[str, dict[str, t.Any]]] = {
        "Debug": {"fg": "blue"},
        "Info": {"fg": "green"},
        "Warning": {"fg": "yellow"},
        "Error": {"fg": "red"},
        "Critical": {"fg": "red", "bold": True},
    }

    @t.override
    def format(self, record: logging.LogRecord) -> str:
        level = record.levelname.capitalize()
        msg = record.getMessage()
        if record.exc_info is not None:
            err_class = record.exc_info[0]
            if err_class is not None:
                err_name = click.style(err_class.__name__, fg="red")
                # return f" {err_name}: {msg}"
                panel = rich.panel.Panel(
                    msg,
                    title=err_name,
                    border_style=self.colors[level]["fg"],
                    title_align=click.RichHelpConfiguration.align_errors_panel,

                )
                rich.print(panel)
                return ""
        if level in self.colors:
            # prefix = click.style(level, **self.colors[level])
            panel = rich.panel.Panel(
                msg,
                title=level,
                border_style=self.colors[level]["fg"],
                title_align=click.RichHelpConfiguration.align_errors_panel,

            )
            rich.print(panel)
            return ""
            # return f" {prefix}: {msg}"
        return msg


class FileFormatter(logging.Formatter):
    """
    File formatter.

    Courtesy of https://github.com/mCodingLLC
    """

    @t.override
    def format(self, record: logging.LogRecord) -> str:
        """Customize format."""
        message = self._log_dict(record)
        return json.dumps(message, default=str)

    def _log_dict(self, record: logging.LogRecord) -> dict[str, t.Any]:
        message = {
            "levelname": "",
            "message": "",
            "created": "",
        }
        message.update(record.__dict__)
        message["created"] = dt.datetime.fromtimestamp(record.created, tz=dt.UTC).isoformat()
        if record.relativeCreated is not None:
            message["relativeCreated"] = dt.datetime.fromtimestamp(record.relativeCreated, tz=dt.UTC).isoformat()
        if record.exc_info is not None:
            message["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info is not None:
            message["stack_info"] = self.formatStack(record.stack_info)
        return message


logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "stderr": {
            "()": ColorFormatter,
        },
        "file": {
            "()": FileFormatter,
        },
    },
    "handlers": {
        "stderr": {
            # "()": DummyHandler,
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "stderr",
            # "stream": "ext://sys.stderr",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": logfile_path,
            "maxBytes": FILE_MAX_BITES,
            "backupCount": 3,
        },
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": [
                "stderr",
                "file",
            ],
        },
    },
})

logger = logging.getLogger(__name__)





