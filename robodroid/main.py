#!/usr/bin/env python3

"""
  Entrypoint file for RoboDroid with the CLI commands
"""
import typer
import questionary
from typing import Tuple, cast
from robodroid import __version__
from robodroid.services import adb
from robodroid.workflow import manager
from robodroid.utils import helper, logger
from robodroid.types.enum import RunMode, LoggerMode, LoggerModeValue

app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})


def config_file_callback(ctx: typer.Context, value: str):
    if ctx.params["mode"] == RunMode.MANAGED.value and len(value) == 0:
        logger.error(
            "Missing required config file to load for managed mode, please add it with the --mode/-m option"
        )
        raise typer.Exit(1)
    return value


def interactive_mode(adb_instance: adb.RoboDroidAdb) -> Tuple[str, str]:
    # Select device
    devices = [d.get_serial_no() for d in adb_instance.list_devices()]
    device_to_connect = questionary.select(
        "What device do you want to connect to?",
        choices=devices,
    ).ask()

    # Select workflow to run
    workflows = helper.get_workflows()
    workflow_to_run = questionary.select(
        "What workflow do yo want to run?",
        choices=workflows,
    ).ask()
    return device_to_connect, workflow_to_run


def managed_mode(adb_instance: adb.RoboDroidAdb, config_file: str):
    logger.info("Feature in development!")
    logger.debug(adb_instance)
    logger.debug(config_file)
    raise typer.Exit(1)


@app.command()
def run(
    log_mode: LoggerMode = typer.Option(LoggerMode.NORMAL.value, help="Set logging mode"),
    mode: RunMode = typer.Option(
        RunMode.INTERACTIVE.value, "--mode", "-m", help="Set run mode", prompt=True
    ),
    config_file: str = typer.Option(
        "",
        "--config",
        "-c",
        help="Path to the managed config file to load",
        callback=config_file_callback,
    ),
) -> None:
    """
    Run RoboDroid.
    """
    if log_mode == LoggerMode.SILENT.value:
        logger.bold("Silent mode on. From now on only errors will be printed.")
    logger.init(cast(LoggerModeValue, log_mode))
    if log_mode == LoggerMode.DEBUG.value:
        logger.debug("Debug mode on")

    # Just printing out an hello msg during development
    logger.log("Hello Robots!")

    # Create adb instance
    adb_instance = adb.RoboDroidAdb()

    # Interactive mode
    if mode == RunMode.INTERACTIVE.value:
        device_to_connect, workflow_to_run = interactive_mode(adb_instance)
    # Managed mode
    elif mode == RunMode.MANAGED.value:
        managed_mode(adb_instance, config_file)

    # Connect to device
    adb_instance.connect(device_to_connect)

    # Get workflow data
    workflow_data = helper.get_workflow_data(workflow_to_run)

    # Create the WorkflowManager
    wf_manager = manager.RoboDroidWorkflowManager(workflow_data, adb_instance)

    # Start the workflow
    wf_manager.run()


@app.command()
def version() -> None:
    """
    Print the current version and exit.
    """
    print(f"RoboDroid v{__version__}")


def main() -> None:
    """
    Entrypoint for RoboDroid, it runs the 'typer' CLI
    """
    helper.banner(__version__)
    helper.init_folders()
    app()


if __name__ == "__main__":
    main()
