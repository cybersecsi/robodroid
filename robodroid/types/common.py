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


class ConfigInit(TypedDict):
    install: List[str]
    clear: List[str]


class ConfigStepInput(TypedDict):
    id: str
    value: str


class ConfigStep(TypedDict):
    id: str
    name: str
    type: WorkflowStepTypeValue
    inputs: List[ConfigStepInput]


class ConfigData(TypedDict):
    id: str
    host: str
    port: int
    type: str
    device_name: str
    init: NotRequired[ConfigInit]
    workflow: List[ConfigStep]


class BehaviorResult(TypedDict):
    status: BehaviorResultTypeValue
    msg: str
    outputs: NotRequired[str]
