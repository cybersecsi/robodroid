#!/usr/bin/env python3

"""
  Entrypoint file for RoboDroid with the CLI commands
"""
import typer
from robodroid import __version__
from robodroid.utils import helper, logger

app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def run(
    silent: bool = typer.Option(False, "--silent", "-s", help="Minimize output"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Display debug output"),
) -> None:
    """
    Manage and deploy Android machines with pre-defined behaviors for Cyber Range environments
    """
    if silent:
        logger.bold("Silent mode on. From now on only errors will be printed.")
    logger.init(silent, debug)
    if debug:
        logger.debug("Debug mode on")
    logger.log("Hello Robots!")
    print(helper.get_library())


def main() -> None:
    """
    Entrypoint for RoboDroid, it runs the 'typer' CLI
    """
    helper.banner(__version__)
    app()


if __name__ == "__main__":
    main()
