import threading
import queue
import time
from typing import List, Any, Callable, cast
from functools import wraps
from ppadb.client import Client as AdbClient

# from ppadb.client_async import ClientAsync as AdbClient
from ppadb.device import Device
from robodroid.utils import logger


def validate_connection(return_value: Any) -> Callable[..., Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kw: Any) -> Any:
            adb_instance: RoboDroidAdb = args[0]
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


class RoboDroidAdb:
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
    def install_from_device(self, apk_path: str, enable_handler: bool = True) -> None:
        install_cmd = f"pm install {apk_path}"
        self.shell_cmd(install_cmd, enable_handler)

    @validate_connection(None)
    def uninstall(self, package_name: str) -> None:
        if self.is_apk_installed(package_name):
            self.device.uninstall(package_name)

    @validate_connection(None)
    def push(self, src: str, dst: str, mode: int = 420) -> None:
        return self.device.push(src, dst, mode)

    @validate_connection(None)
    def shell_cmd(self, cmd: str, enable_handler: bool = True) -> None:
        if enable_handler:
            return self.device.shell(cmd, handler=dump_stdout)
        return self.device.shell(cmd)

    @validate_connection(None)
    def shell_cmd_output(self, cmd: str) -> str:
        cmd_output_queue: queue.Queue = queue.Queue()

        def handler(connection: Any) -> None:
            data = connection.read(1024)
            connection.close()
            result = data.decode("utf-8") if data else None
            cmd_output_queue.put(result)

        self.device.shell(cmd, handler)
        result = cmd_output_queue.get()
        return result

    @validate_connection(None)
    def thread_shell_cmd(self, cmd: str) -> None:
        def target() -> None:
            return self.shell_cmd(cmd)

        exec_thread = threading.Thread(target=target)
        exec_thread.setDaemon(True)
        exec_thread.start()
        # print('Waiting for the thread...')
        # exec_thread.join()
        # print('Thread completed')

    @validate_connection(None)
    def wait_for_process_up(self, process_name: str) -> None:
        cmd_output_queue: queue.Queue = queue.Queue()

        def handler(connection: Any) -> None:
            data = connection.read(1024)
            connection.close()
            result = data.decode("utf-8") if data else None
            cmd_output_queue.put(result)

        while True:
            self.device.shell(f"pidof {process_name}", handler)
            result: str = cmd_output_queue.get()
            if result != None and result.strip() != 1:
                break
            else:
                logger.info(
                    f"Process {process_name} is not running yet, waiting for 2 seconds before retrying..."
                )
                time.sleep(2)

    @validate_connection(False)
    def is_root_enabled(self) -> bool:
        result: str = self.shell_cmd_output("whoami")
        return result.strip() == "root"

    @validate_connection(False)
    def enable_root(self) -> bool:
        result = False
        try:
            result = self.device.root()
        except RuntimeError as exc:
            if "adbd is already running as root" in str(exc):
                result = True
        self.device.wait_boot_complete()
        return result
