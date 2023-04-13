from robodroid.workflow import commands

workflow_commands = {
    "adb-apk-install-from-device": commands.adb_install_from_device,
    "adb-apk-install-from-host": commands.adb_install_from_host,
    "adb-add-permission": commands.adb_add_permission,
}
