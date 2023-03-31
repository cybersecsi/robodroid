from typing import Literal, get_args
from enum import Enum

# Define the enums as a class


class LoggerMode(str, Enum):
    SILENT = "silent"
    NORMAL = "normal"
    DEBUG = "debug"


# Convert to literal
LoggerModeValue = Literal["silent", "normal", "debug"]

# Assert that the conversion is OK
assert set(get_args(LoggerModeValue)) == {member.value for member in LoggerMode}
