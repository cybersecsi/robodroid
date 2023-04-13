from typing import Literal, get_args
from enum import Enum

# Define the enums as a class


class LoggerMode(str, Enum):
    SILENT = "silent"
    NORMAL = "normal"
    DEBUG = "debug"


class WorkflowStepType(str, Enum):
    FRIDA = "frida-behavior"
    ADB = "adb"


class BehaviorResult(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"


# Convert to literal
LoggerModeValue = Literal["silent", "normal", "debug"]
WorkflowStepTypeValue = Literal["frida-behavior", "adb"]
BehaviorResultValue = Literal["completed", "failed"]

# Assert that the conversion is OK
assert set(get_args(LoggerModeValue)) == {member.value for member in LoggerMode}
assert set(get_args(WorkflowStepTypeValue)) == {member.value for member in WorkflowStepType}
assert set(get_args(BehaviorResultValue)) == {member.value for member in BehaviorResult}
