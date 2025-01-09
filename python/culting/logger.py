"""Logger."""

from .core import __os__


print(__os__)

# from pj_logging.pj_logging import set_logger
#
#
# logger = set_logger(
# )

# import datetime as dt
# import json
# import logging
# import logging.config
# import logging.handlers
# import typing as t
#
# import rich.panel
# import rich_click as click
#
# from .variables import logfile_path
#
#
# FILE_MAX_BITES = 100_000
#
#
# class PanelHandler(logging.Handler):
#     """Panel rich handler."""
#
#     colors: t.ClassVar[dict[str, str]] = {
#         "Debug": "blue",
#         "Info": "green",
#         "Warning": "yellow",
#         "Error": "red",
#         "Critical": "red",
#     }
#
#     def emit(self, record: logging.LogRecord) -> None:
#         """Emit rich panel."""
#         msg = record.getMessage()
#         level = record.levelname.capitalize()
#         msg_color = self.colors.get(level, "red")
#         if record.exc_info is not None:
#             err_class = record.exc_info[0]
#             if err_class is not None:
#                 level = err_class.__name__
#                 msg_color = "red"
#         panel = rich.panel.Panel(
#             msg,
#             title=level,
#             border_style=msg_color,
#             title_align=click.RichHelpConfiguration.align_errors_panel,
#         )
#         rich.print(panel)
#
#
# class FileFormatter(logging.Formatter):
#     """
#     File formatter.
#
#     Courtesy of https://github.com/mCodingLLC
#     """
#
#     @t.override
#     def format(self, record: logging.LogRecord) -> str:
#         """Customize format."""
#         message = self._log_dict(record)
#         return json.dumps(message, default=str)
#
#     def _log_dict(self, record: logging.LogRecord) -> dict[str, t.Any]:
#         message = {
#             "levelname": "",
#             "message": "",
#             "created": "",
#         }
#         message.update(record.__dict__)
#         message["created"] = dt.datetime.fromtimestamp(record.created, tz=dt.UTC).isoformat()
#         if record.relativeCreated is not None:
#             message["relativeCreated"] = dt.datetime.fromtimestamp(record.relativeCreated, tz=dt.UTC).isoformat()
#         if record.exc_info is not None:
#             message["exc_info"] = self.formatException(record.exc_info)
#         if record.stack_info is not None:
#             message["stack_info"] = self.formatStack(record.stack_info)
#         return message
#
#
# logging.config.dictConfig({
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "file": {
#             "()": FileFormatter,
#         },
#     },
#     "handlers": {
#         "stderr": {
#             "()": PanelHandler,
#             "level": "INFO",
#         },
#         "file": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "level": "DEBUG",
#             "formatter": "file",
#             "filename": logfile_path,
#             "maxBytes": FILE_MAX_BITES,
#             "backupCount": 3,
#         },
#     },
#     "loggers": {
#         "root": {
#             "level": "DEBUG",
#             "handlers": [
#                 "stderr",
#                 "file",
#             ],
#         },
#     },
# })
#
# logger = logging.getLogger(__name__)





