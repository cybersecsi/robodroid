#!/usr/bin/env python3

"""
  Entrypoint file for RoboDroid with the CLI commands
"""
import typer
import questionary
from typing import cast
from robodroid import __version__
from robodroid.services import frida
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

    configs = helper.get_configs()
    config_to_run = questionary.select(
        "What config do yo want to run?",
        choices=configs,
    ).ask()
    config_data = helper.get_config_data(config_to_run)
    for behavior in config_data["behaviors"]:
        lib_data = helper.get_lib_data(behavior["id"])
        frida.load_frida_js(lib_data)


def main() -> None:
    """
    Entrypoint for RoboDroid, it runs the 'typer' CLI
    """
    helper.banner(__version__)
    app()


if __name__ == "__main__":
    main()
