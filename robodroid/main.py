#!/usr/bin/env python3

"""
  Entrypoint file for RoboDroid with the CLI commands
"""
import typer
from typing import cast
from robodroid import __version__
from robodroid.utils import helper, logger
from robodroid.types.enum import LoggerMode, LoggerModeValue

app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def run(
    log_mode: LoggerMode = typer.Option(LoggerMode.NORMAL.value, help="Set logging mode"),
) -> None:
    """
    Manage and deploy Android machines with pre-defined behaviors for Cyber Range environments
    """
    if log_mode == LoggerMode.SILENT.value:
        logger.bold("Silent mode on. From now on only errors will be printed.")
    logger.init(cast(LoggerModeValue, log_mode))
    if log_mode == LoggerMode.DEBUG.value:
        logger.debug("Debug mode on")

    # Just printing out an hello msg during development
    logger.log("Hello Robots!")


def main() -> None:
    """
    Entrypoint for RoboDroid, it runs the 'typer' CLI
    """
    helper.banner(__version__)
    app()


if __name__ == "__main__":
    main()
