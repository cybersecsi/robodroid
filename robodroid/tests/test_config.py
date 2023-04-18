from robodroid.utils import helper, logger
from robodroid.types.enum import LoggerMode

logger.init(LoggerMode.DEBUG.value)


def test_get_library():
    library = helper.get_library()
    assert len(library) == 3


def test_get_workflows():
    workflows = helper.get_workflows()
    assert len(workflows) == 4
