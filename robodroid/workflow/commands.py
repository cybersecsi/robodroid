from robodroid.services import adb


def adb_install_from_host(adb_instance: adb.RoboDroidAdb, apk_path: str) -> None:
    adb_instance.install(apk_path)


def adb_install_from_device(adb_instance: adb.RoboDroidAdb, apk_path: str) -> None:
    adb_instance.install_from_device(apk_path)
