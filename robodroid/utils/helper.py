"""
  This module contains generic helper functions
"""

import os
import pathlib
from typing import List
from robodroid.utils.constants import DEFAULT_BASE_PATH, LIBRARY_FOLDER


def banner(version: str) -> None:
    """
    Print out our beautiful banner
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
    return os.path.join(pathlib.Path.home(), DEFAULT_BASE_PATH)


def robodroid_lib_folder() -> str:
    return os.path.join(robodroid_folder(), LIBRARY_FOLDER)


def is_lib_valid(libname: str) -> bool:
    required_files = ["config.yaml", "index.js"]
    libfolder = os.path.join(robodroid_lib_folder(), libname)
    if all(file in os.listdir(libfolder) for file in required_files):
        return True
    return False


def get_library() -> List[str]:
    """A function to get the scripts based on the directory names in $HOME/.RoboDroid/library"""
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
    """
    if not os.path.isdir(path):
        os.makedirs(path)
