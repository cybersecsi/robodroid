import sys
from typing import List, Optional

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


class ConfigBehaviorInput(TypedDict):
    id: str
    value: str


class ConfigBehavior(TypedDict):
    id: str
    inputs: List[ConfigBehaviorInput]


class ConfigData(TypedDict):
    id: str
    host: str
    port: int
    type: str
    device_name: str
    init: NotRequired[ConfigInit]
    behaviors: List[ConfigBehavior]
