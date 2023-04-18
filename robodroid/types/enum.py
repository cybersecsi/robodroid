from typing import Literal, get_args
from enum import Enum

# Define the enums as a class


class RunMode(str, Enum):
    INTERACTIVE = "interactive"
    MANAGED = "managed"


class LoggerMode(str, Enum):
    SILENT = "silent"
    NORMAL = "normal"
    DEBUG = "debug"


class WorkflowStepType(str, Enum):
    FRIDA = "frida-behavior"
    ADB = "adb"


class BehaviorResultType(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"


# Convert to literal
RunModeValue = Literal["interactive", "managed"]
LoggerModeValue = Literal["silent", "normal", "debug"]
WorkflowStepTypeValue = Literal["frida-behavior", "adb"]
BehaviorResultTypeValue = Literal["completed", "failed"]

# Assert that the conversion is OK
assert set(get_args(RunModeValue)) == {member.value for member in RunMode}
assert set(get_args(LoggerModeValue)) == {member.value for member in LoggerMode}
assert set(get_args(WorkflowStepTypeValue)) == {member.value for member in WorkflowStepType}
assert set(get_args(BehaviorResultTypeValue)) == {member.value for member in BehaviorResultType}
