""""
Define a bunch of constants
"""
from pathlib import Path

FILE_PATH = Path(__file__)
MAIN_DIR = FILE_PATH.parent.parent.absolute()  # Root path of the project

DEFAULT_BASE_PATH = ".RoboDroid"
LIBRARY_FOLDER = "library"
ROBODROID_GIT_REPO = "https://github.com/cybersecsi/robodroid"
ROBODROID_LIBRARY_GIT_REPO = "https://github.com/cybersecsi/robodroid-library"

# Colors
SUCCESS_COLOR = "\033[92m"
ERROR_COLOR = "\033[91m"
DEBUG_COLOR = "\033[93m"
BOLD_FORMAT = "\033[1m"
END_FORMAT = "\033[0m"
