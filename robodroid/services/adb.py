from typing import List, Any, Callable, cast
from functools import wraps
from ppadb.client import Client as AdbClient
from ppadb.device import Device
from robodroid.utils import logger


def validate_connection(return_value: Any) -> Callable[..., Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kw: Any) -> Any:
            adb_instance: Adb = args[0]
            if not adb_instance.device:
                logger.error("No device connected!")
                return return_value
            return func(*args, **kw)

        return wrapper

    return decorator


def dump_stdout(connection: Any) -> None:
    while True:
        data = connection.read(1024)
        if not data:
            break
        print(data.decode("utf-8"))
    connection.close()


class Adb:
    """
    A class for interacting with Android devices using 'pure-python-adb'.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5037):
        self.host = host
        self.port = port
        self.client = AdbClient(host=host, port=port)

    def get_adb_version(self) -> int:
        return self.client.version()

    def list_devices(self) -> List[Device]:
        return cast(List[Device], self.client.devices())

    def connect(self, device_name: str) -> None:
        self.device = cast(Device, self.client.device(device_name))

    @validate_connection("")
    def get_device_arch(self) -> str:
        return self.device.get_properties()["ro.product.cpu.abi"]

    @validate_connection(False)
    def is_apk_installed(self, package_name: str) -> bool:
        return self.device.is_installed(package_name)

    @validate_connection(None)
    def install(self, apk_path: str) -> None:
        self.device.install(apk_path)

    @validate_connection(None)
    def uninstall(self, package_name: str) -> None:
        if self.is_apk_installed(package_name):
            self.device.uninstall(package_name)

    @validate_connection(None)
    def shell_cmd(self, cmd: str) -> None:
        self.device.shell(cmd, handler=dump_stdout)
