import sys
from typing import List, Optional
from robodroid.types.enum import WorkflowStepTypeValue, BehaviorResultTypeValue

# Manage import of 'TypedDict', 'NotRequired'
if sys.version_info >= (3, 11):
    from typing import TypedDict, NotRequired
else:
    from typing_extensions import TypedDict

    NotRequired = Optional


class LibInfo(TypedDict):
    package_name: str
    description: str
    permissions: NotRequired[List[str]]


class LibInputs(TypedDict):
    id: str
    description: str


class LibOutputs(TypedDict):
    id: str
    description: str


class LibData(TypedDict):
    id: str
    info: LibInfo
    inputs: List[LibInputs]
    outputs: List[LibOutputs]


class WorkflowInit(TypedDict):
    install: List[str]
    clear: List[str]


class WorkflowStepInput(TypedDict):
    id: str
    value: str


class WorkflowStep(TypedDict):
    id: str
    name: str
    type: WorkflowStepTypeValue
    inputs: List[WorkflowStepInput]


class WorkflowData(TypedDict):
    id: str
    init: NotRequired[WorkflowInit]
    behaviors: List[WorkflowStep]


class BehaviorResult(TypedDict):
    status: BehaviorResultTypeValue
    msg: str
    outputs: NotRequired[str]


class DbMetadata(TypedDict):
    last_library_update: int  # UNIX timestamp of the last library update


class ManagedConfigDeviceData(TypedDict):
    adb_host: str
    adb_port: int
    device_name: str


class ManagedConfigData(TypedDict):
    device: ManagedConfigDeviceData
    workflow: str
