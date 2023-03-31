"""
  This module contains generic helper functions
"""

import os
import pathlib
from typing import List, Dict, Any
from yaml import safe_load, YAMLError
from cerberus import Validator
from robodroid.utils import logger, schemas
from robodroid.utils.constants import DEFAULT_BASE_PATH, LIBRARY_FOLDER


def banner(version: str) -> None:
    """
    Print out our beautiful banner

      Parameters:
        version (str): the version string

      Returns:
        None
    """
    print(
        f"""
    ███████╗███████╗ ██████╗███████╗██╗
    ██╔════╝██╔════╝██╔════╝██╔════╝██║
    ███████╗█████╗  ██║     ███████╗██║
    ╚════██║██╔══╝  ██║     ╚════██║██║
    ███████║███████╗╚██████╗███████║██║
    ╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝
    RoboDroid v{version}
    """
    )


def robodroid_folder() -> str:
    """
    Get the RoboDroid project folder

      Returns:
        robodroid_folder (str): the path to the RoboDroid project folder
    """
    return os.path.join(pathlib.Path.home(), DEFAULT_BASE_PATH)


def robodroid_lib_folder() -> str:
    """
    Get the RoboDroid library folder

      Returns:
        robodroid_lib_folder (str): the path to the RoboDroid library folder
    """
    return os.path.join(robodroid_folder(), LIBRARY_FOLDER)


def validate_schema(schema: Dict, data: Any) -> bool:
    """
    Simple function to validate some data against a schema using 'cerberus'

    Parameters:
      schema (dict): the schema
      data (any): the data to be validated

    Returns:
      is_valid (bool): boolean that says if the data is valid or not
    """
    v = Validator(schema)
    if v.validate(data):
        return True
    else:
        logger.error(f"Data is invalid: {v.errors}")
        return False


def is_lib_valid(libname: str) -> bool:
    """
    Checks if an element in the library is valid

      Parameters:
        libname (str): the name of element in the library

      Returns
        is_valid (bool): boolean value that says if the library is valid or not
    """
    # Check for required files
    required_files = ["config.yaml", "index.ts"]
    libfolder = os.path.join(robodroid_lib_folder(), libname)
    if not all(file in os.listdir(libfolder) for file in required_files):
        return False
    # Check if the YAML config file is valid
    config_filepath = os.path.join(robodroid_lib_folder(), libname, "config.yaml")
    with open(config_filepath, "r", encoding="utf-8") as config_file:
        try:
            config_yaml = safe_load(config_file)
            is_valid = validate_schema(schemas.config_tpl_lib_schema, config_yaml)
            if not is_valid:
                return False
        except YAMLError as exc:
            logger.error(str(exc))
    return True


def get_library() -> List[str]:
    """
    A function to get the scripts based on the directory names in $HOME/.RoboDroid/library

      Returns:
        library (List[str]): the RoboDroid library (only valid elements)
    """
    library_folder = robodroid_lib_folder()
    library = [
        f for f in os.listdir(library_folder) if not os.path.isfile(os.path.join(library_folder, f))
    ]
    library = [l for l in library if is_lib_valid(l)]
    library.sort()
    return library


def create_folder_if_missing(path: str) -> None:
    """
    Check if a folder exists, if not create it

      Parameters:
        path (str): the path to check

      Returns:
        None
    """
    if not os.path.isdir(path):
        os.makedirs(path)
