import re
from robodroid.services import adb


def adb_install_from_host(adb_instance: adb.RoboDroidAdb, apk_path: str) -> None:
    adb_instance.install(apk_path)


def adb_install_from_device(adb_instance: adb.RoboDroidAdb, apk_path: str) -> None:
    # Move the file to '/data/local/tmp' to make it installable
    safe_apk_path = re.escape(apk_path)
    safe_filename = safe_apk_path.split("/")[-1]
    adb_instance.shell_cmd(f"mv {safe_apk_path} /data/local/tmp", False)
    adb_instance.install_from_device(f"/data/local/tmp/{safe_filename}", False)


def adb_add_permission(adb_instance: adb.RoboDroidAdb, package_name: str, permission: str) -> None:
    adb_instance.shell_cmd(f"pm grant {package_name} {permission}")
