from robodroid.utils import helper, logger
from robodroid.types.enum import LoggerMode

logger.init(LoggerMode.DEBUG.value)


def test_get_latest_release():
    helper.download_robodroid_library()
    assert False
