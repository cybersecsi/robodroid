""""
Define a bunch of constants
"""
from pathlib import Path

FILE_PATH = Path(__file__)
MAIN_DIR = FILE_PATH.parent.parent.absolute()  # Root path of the project

# Folders
DEFAULT_BASE_PATH = ".RoboDroid"
LIBRARY_FOLDER = "library"
DB_FOLDER = "db"
BEHAVIORS_FOLDER = "behaviors"
CONFIGS_FOLDER = "configs"
FRIDA_FOLDER = "frida"

# Files
FRIDA_AGENT_FILE = "robodroid-library.js"
DB_METADATA_FILE = "metadata.json"

# Template files
TEMPLATE_DB_METADATA_FILE = f"{MAIN_DIR}/config/{DB_METADATA_FILE}"

# Links
ROBODROID_GIT_REPO = "https://github.com/cybersecsi/robodroid"
ROBODROID_LIBRARY_GIT_REPO = "https://github.com/cybersecsi/robodroid-library"

# Colors
SUCCESS_COLOR = "\033[32m"
ERROR_COLOR = "\033[31m"
DEBUG_COLOR = "\033[33m"
BOLD_FORMAT = "\033[1m"
END_FORMAT = "\033[0m"
