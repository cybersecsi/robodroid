from robodroid.workflow import commands

adb_commands = {
    "adb-apk-install-from-device": commands.adb_install_from_device,
    "adb-apk-install-from-host": commands.adb_install_from_host,
}

workflow_commands = {"adb": adb_commands}
