"""
  This module provides a Logger (as a Singleton).
"""

from datetime import datetime
from robodroid.utils.constants import (
    SUCCESS_COLOR,
    ERROR_COLOR,
    DEBUG_COLOR,
    BOLD_FORMAT,
    END_FORMAT,
)
from robodroid.types.enum import LoggerMode, LoggerModeValue


class Logger:
    logger_mode: LoggerModeValue = LoggerMode.NORMAL.value

    """Implement it as a Singleton"""

    def __new__(cls) -> "Logger":
        if not hasattr(cls, "instance"):
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    def init(self, logger_mode: LoggerModeValue) -> None:
        self.logger_mode = logger_mode

    def log(self, msg: str, end: str | None = None) -> None:
        if self.logger_mode in [LoggerMode.NORMAL.value, LoggerMode.DEBUG.value]:
            print(msg, flush=True, end=end)

    def bold(self, msg: str, end: str | None = None) -> None:
        if self.logger_mode in [LoggerMode.NORMAL.value, LoggerMode.DEBUG.value]:
            print(f"{BOLD_FORMAT}{msg}{END_FORMAT}", flush=True, end=end)

    def info(self, msg: str, end: str | None = None) -> None:
        if self.logger_mode in [LoggerMode.NORMAL.value, LoggerMode.DEBUG.value]:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f"[{current_time}] - [INF] - {msg}", flush=True, end=end)

    def success(self, msg: str, end: str | None = None) -> None:
        if self.logger_mode in [LoggerMode.NORMAL.value, LoggerMode.DEBUG.value]:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(
                f"{SUCCESS_COLOR}[{current_time}] - [SUC] - {msg}{END_FORMAT}",
                flush=True,
                end=end,
            )

    def error(self, msg: str, end: str | None = None) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(
            f"{ERROR_COLOR}[{current_time}] - [ERR] - {msg}{END_FORMAT}",
            flush=True,
            end=end,
        )

    def debug(self, msg: str, end: str | None = None) -> None:
        if self.logger_mode == LoggerMode.DEBUG.value:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(
                f"{DEBUG_COLOR}[{current_time}] - [DEB] - {msg}{END_FORMAT}",
                flush=True,
                end=end,
            )


def init(logger_mode: LoggerModeValue) -> None:
    Logger().init(logger_mode)


log = Logger().log
bold = Logger().bold
info = Logger().info
success = Logger().success
error = Logger().error
debug = Logger().debug
