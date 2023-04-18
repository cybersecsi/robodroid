#!/usr/bin/env python3

"""
  Entrypoint file for RoboDroid with the CLI commands
"""
import typer
import questionary
from typing import cast
from robodroid import __version__
from robodroid.services import adb
from robodroid.workflow import manager
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

    # Select device
    adb_instance = adb.RoboDroidAdb()
    devices = [d.get_serial_no() for d in adb_instance.list_devices()]
    device_to_connect = questionary.select(
        "What device do you want to connect to?",
        choices=devices,
    ).ask()
    adb_instance.connect(device_to_connect)

    # Select workflow to run
    workflows = helper.get_workflows()
    workflow_to_run = questionary.select(
        "What workflow do yo want to run?",
        choices=workflows,
    ).ask()
    workflow_data = helper.get_workflow_data(workflow_to_run)

    # Create the WorkflowManager
    wf_manager = manager.RoboDroidWorkflowManager(workflow_data, adb_instance)

    # Start the workflow
    wf_manager.run()


def main() -> None:
    """
    Entrypoint for RoboDroid, it runs the 'typer' CLI
    """
    helper.banner(__version__)
    helper.init_folders()
    app()


if __name__ == "__main__":
    main()
