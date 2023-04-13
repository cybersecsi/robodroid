from robodroid.utils import helper, logger
from robodroid.types.enum import LoggerMode

logger.init(LoggerMode.DEBUG.value)


def test_get_library():
    library = helper.get_library()
    assert len(library) == 3


def test_get_configs():
    configs = helper.get_configs()
    assert len(configs) == 4
