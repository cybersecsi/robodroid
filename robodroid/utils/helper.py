"""
  This module contains generic helper functions
"""

import os
import shutil
import pathlib
import functools
import threading
import tarfile
import json
import time
import requests
from typing import List, Dict, Tuple, Callable, Any, cast
from yaml import safe_load, YAMLError
from cerberus import Validator
from robodroid import types
from robodroid.utils import logger, schemas
from robodroid.utils.constants import (
    DEFAULT_BASE_PATH,
    LIBRARY_FOLDER,
    BEHAVIORS_FOLDER,
    CONFIGS_FOLDER,
    DB_FOLDER,
    FRIDA_FOLDER,
    FRIDA_AGENT_FILE,
    DB_METADATA_FILE,
    TEMPLATE_DB_METADATA_FILE,
)


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
    Get the RoboDroid behaviors folder

    Returns:
        robodroid_lib_folder (str): the path to the RoboDroid library folder
    """
    return os.path.join(robodroid_folder(), LIBRARY_FOLDER)


def robodroid_behaviors_folder() -> str:
    """
    Get the RoboDroid behaviors folder

    Returns:
        robodroid_behaviors_folder (str): the path to the RoboDroid behaviors folder
    """
    return os.path.join(robodroid_lib_folder(), BEHAVIORS_FOLDER)


def robodroid_configs_folder() -> str:
    """
    Get the RoboDroid configs folder

    Returns:
        robodroid_configs_folder (str): the path to the RoboDroid configs folder
    """
    return os.path.join(robodroid_folder(), CONFIGS_FOLDER)


def robodroid_frida_folder() -> str:
    """
    Get the RoboDroid frida folder

    Returns:
        robodroid_frida_folder (str): the path to the RoboDroid frida folder
    """
    return os.path.join(robodroid_folder(), FRIDA_FOLDER)


def robodroid_db_folder() -> str:
    """
    Get the RoboDroid db folder

    Returns:
        robodroid_db_folder (str): the path to the RoboDroid db folder
    """
    return os.path.join(robodroid_folder(), DB_FOLDER)


def create_folder_if_missing(path: str) -> None:
    """
    Create a folder if not exists

    Parameters:
        path (str): the directory to create
    """
    if not os.path.isdir(path):
        logger.info(f"Creating folder '{path}'")
        os.makedirs(path)


def get_latest_github_release() -> Tuple[str, str]:
    GITHUB_API = {
        "base": "https://api.github.com/repos",
        "commits": "/commits",
        "latest_release": "releases/latest",
        "tags": "/tags",
    }
    url = f"{GITHUB_API['base']}/cybersecsi/robodroid-library/{GITHUB_API['latest_release']}"
    req = requests.get(url)
    assets = req.json()["assets"]
    asset_to_download = assets[0]
    download_url = asset_to_download["browser_download_url"]
    version = req.json()["tag_name"]
    return download_url, version


def download_robodroid_library() -> None:
    """
    Download the RoboDroid Frida Library from https://github.com/cybersecsi/robodroid-library
    """

    download_url, _ = get_latest_github_release()
    download_folder = robodroid_lib_folder()
    logger.info(f"Downloading robodroid-library from '{download_url}'")
    req = requests.get(download_url, stream=True)
    if req.status_code == 200:
        fname = os.path.join(download_folder, "robodroid-library.tar.gz")
        req.raw.decode_content = True
        with open(fname, "wb") as robodroid_library_file:
            for chunk in req.iter_content(1024):
                robodroid_library_file.write(chunk)
        with tarfile.open(fname) as robodroid_library_archive_file:
            robodroid_library_archive_file.extractall(download_folder)
            os.unlink(fname)
        set_last_library_update()
    else:
        logger.error("Error while downloading 'robodroid-library'")


def set_last_library_update() -> None:
    """
    Write the current timestamp in the $HOME/.RoboDroid/db/metadata.json file ('last_library_update' key)
    """
    metadata_file_path = os.path.join(robodroid_db_folder(), DB_METADATA_FILE)

    # Copy file from template if missing
    if not os.path.isfile(metadata_file_path):
        logger.error(f"Missing file '{metadata_file_path}', copying it from template")
        shutil.copyfile(TEMPLATE_DB_METADATA_FILE, metadata_file_path)

    with open(metadata_file_path, "r+", encoding="utf-8") as metadata_file:
        db_metadata: types.common.DbMetadata = json.load(metadata_file)
        db_metadata["last_library_update"] = int(time.time())
        metadata_file.seek(0)
        json.dump(db_metadata, metadata_file)


def init_folders() -> None:
    """
    Create the folders required to run RoboDroid
    """
    create_folder_if_missing(robodroid_folder())
    create_folder_if_missing(robodroid_configs_folder())
    create_folder_if_missing(robodroid_frida_folder())
    create_folder_if_missing(robodroid_db_folder())
    if not os.path.isdir(robodroid_lib_folder()):
        os.makedirs(robodroid_lib_folder())
        download_robodroid_library()


def validate_schema(schema: Dict, data: Any) -> bool:
    """
    Simple function to validate some data against a schema using 'cerberus'

    Parameters:
      schema (dict): the schema
      data (any): the data to be validated

    Returns:
      is_valid (bool): boolean that says if the data is valid or not
    """
    validator = Validator(schema)
    if validator.validate(data):
        return True
    else:
        logger.error(f"Data is invalid: {validator.errors}")
        return False


def is_lib_valid(lib_name: str) -> bool:
    """
    Checks if an element in the library is valid

    Parameters:
        libname (str): the name of element in the library

    Returns:
        is_valid (bool): whether the  library is valid or not
    """
    # Check for required files
    required_files = ["config.yaml", "index.js"]
    behaviors_folder = os.path.join(robodroid_behaviors_folder(), lib_name)
    if not all(file in os.listdir(behaviors_folder) for file in required_files):
        return False
    # Check if the YAML config file is valid
    config_filepath = os.path.join(robodroid_behaviors_folder(), lib_name, "config.yaml")
    with open(config_filepath, "r", encoding="utf-8") as config_file:
        try:
            config_yaml = safe_load(config_file)
            is_valid = validate_schema(schemas.lib_config_schema, config_yaml)
            if not is_valid:
                logger.debug(config_yaml)
                return False
        except YAMLError as exc:
            logger.error(str(exc))
    return True


def is_config_valid(config_name: str) -> bool:
    """
    Checks if a config file is valid

    Parameters:
        config_name (str): the name of the config in the configs folder

    Returns:
        is_valid (bool): whether the config is valid or not
    """
    # Check if the YAML config file is valid
    config_filepath = os.path.join(robodroid_configs_folder(), config_name)
    with open(config_filepath, "r", encoding="utf-8") as config_file:
        try:
            config_yaml = safe_load(config_file)
            logger.debug(config_yaml)
            is_valid = validate_schema(schemas.config_schema, config_yaml)
            if not is_valid:
                logger.debug(config_yaml)
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
    behaviors_folder = robodroid_behaviors_folder()
    library = [
        f
        for f in os.listdir(behaviors_folder)
        if not os.path.isfile(os.path.join(behaviors_folder, f))
    ]
    library = [l for l in library if is_lib_valid(l)]
    library.sort()
    return library


def get_configs() -> List[str]:
    """
    A function to get the configs based on the directory names in $HOME/.RoboDroid/configs

    Returns:
        configs (List[str]): the RoboDroid configs (only valid elements)
    """
    configs_folder = robodroid_configs_folder()
    configs = [
        f
        for f in os.listdir(configs_folder)
        if os.path.isfile(os.path.join(configs_folder, f)) and f.endswith(".yaml")
    ]
    configs = [c for c in configs if is_config_valid(c)]
    configs.sort()
    return configs


def get_lib_data(lib_name: str) -> types.common.LibData:
    if not is_lib_valid(lib_name):
        logger.error("Invalid lib!")
        raise Exception("Invalid lib")
    config_filepath = os.path.join(robodroid_behaviors_folder(), lib_name, "config.yaml")
    with open(config_filepath, "r", encoding="utf-8") as config_file:
        config_yaml = cast(types.common.LibData, safe_load(config_file))
        return config_yaml


def get_config_data(config_name: str) -> types.common.ConfigData:
    if not is_config_valid(config_name):
        logger.error("Invalid config!")
        raise Exception("Invalid config")
    config_filepath = os.path.join(robodroid_configs_folder(), config_name)
    with open(config_filepath, "r", encoding="utf-8") as config_file:
        config_yaml = cast(types.common.ConfigData, safe_load(config_file))
        return config_yaml


def get_frida_agent() -> str:
    """
    Get the path of the Frida library agent (robodroid-library.js)

    Returns:
        frida_agent_path (str): the path to the file
    """
    agent_filepath = os.path.join(robodroid_folder(), LIBRARY_FOLDER, FRIDA_AGENT_FILE)
    if not os.path.isfile(agent_filepath):
        err = "Missing RoboDroid Frida agent"
        logger.error(err)
        raise Exception(err)
    return agent_filepath


# Using 'wrapt-timeout-decorator' instead of this


def custom_timeout(timeout: int) -> Callable[..., Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            def target() -> None:
                func(*args, **kwargs)

            t = threading.Thread(target=target)
            t.start()
            t.join(timeout=timeout)  # set the timeout to 5 seconds
            if t.is_alive():
                # if `func` is still running after 5 seconds, raise a `TimeoutError`
                raise TimeoutError("Function call timed out")

        return wrapper

    return decorator
