from typing import List, cast
from ppadb.client import Client as AdbClient
from ppadb.device import Device
from robodroid.utils import logger


class Adb:
    """
    A class for interacting with Android devices using 'pure-python-adb'.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5037):
        self.host = host
        self.port = port
        self.client = AdbClient(host=host, port=port)
        self.device = None

    def get_adb_version(self) -> int:
        return self.client.version()

    def list_devices(self) -> List[Device]:
        return cast(List[Device], self.client.devices())

    def connect(self, device_name: str) -> None:
        self.device = cast(Device, self.client.device(device_name))

    def is_apk_installed(self, package_name: str) -> bool:
        if not self.device:
            logger.error("No device connected!")
            return False
        return self.device.is_installed(package_name)

    def install(self, apk_path: str) -> None:
        if not self.device:
            logger.error("No device connected!")
            return
        self.device.install(apk_path)

    def uninstall(self, package_name: str) -> None:
        if not self.device:
            logger.error("No device connected!")
            return
        if self.is_apk_installed(package_name):
            self.device.uninstall(package_name)

    def shell_cmd(self, cmd: str) -> None:
        if not self.device:
            logger.error("No device connected!")
            return
        self.device.shell(cmd)
