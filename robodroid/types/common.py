import sys
from typing import List, Optional
from robodroid.types.enum import WorkflowStepType

# Manage import of 'TypedDict', 'NotRequired'
if sys.version_info >= (3, 11):
    from typing import TypedDict, NotRequired
else:
    from typing_extensions import TypedDict

    NotRequired = Optional


class LibInfo(TypedDict):
    package_name: str
    description: str


class LibInputs(TypedDict):
    id: str
    description: str


class LibData(TypedDict):
    id: str
    info: LibInfo
    inputs: List[LibInputs]


class ConfigInit(TypedDict):
    packages: List[str]


class ConfigStepInput(TypedDict):
    id: str
    value: str


class ConfigStep(TypedDict):
    id: str
    name: str
    type: WorkflowStepType
    inputs: List[ConfigStepInput]


class ConfigData(TypedDict):
    id: str
    host: str
    port: int
    type: str
    device_name: str
    init: NotRequired[ConfigInit]
    workflow: List[ConfigStep]
