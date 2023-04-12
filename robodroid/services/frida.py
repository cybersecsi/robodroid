import time
import os
import typing
import lzma
import requests
import frida
import humps
from robodroid import types
from robodroid.services import adb
from robodroid.utils import helper, logger


def on_message(message: typing.Any, data: typing.Any) -> None:
    print(data)
    if message["type"] == "send":
        print("[*] {0}".format(message["payload"]))
    else:
        print(message)


def read_hooking_script(filename: str) -> str | None:
    with open(filename, "r") as raw:
        try:
            return raw.read()
        except (IOError, OSError):
            return None


def load_frida_js(
    lib_data: types.common.LibData, inputs: typing.List[types.common.ConfigStepInput]
) -> None:
    package_name = lib_data["info"]["package_name"]
    script_name = helper.get_frida_agent()
    try:
        device = frida.get_usb_device()
        pid = device.spawn(package_name)
        device.resume(pid)
        session = device.attach(pid)
        hooking_script = session.create_script(read_hooking_script(script_name))
        if hooking_script:
            hooking_script.on("message", on_message)
            hooking_script.load()
        else:
            logger.error("The specified script '{0}' was not found!")

        time.sleep(1)  # Without it Java.perform silently fails

        # Retrieve the RPC exports and the specific method
        robodroid_agent = hooking_script.exports
        frida_fn = getattr(robodroid_agent, humps.dekebabize(lib_data["id"]))

        # Get only the values as a list
        input_values = [v["value"] for v in inputs]
        frida_fn(*input_values)

        # stop python script from terminating
        input("Press any key to continue...")
        # script = session.create_script(open(script_name).read())
        # return script
    except TimeoutError as exc:
        logger.error(str(exc))


device_arch_frida_mapping = {
    "armeabi": "arm",
    "armeabi-v7a": "arm",
    "arm64-v8a": "arm64",
}


class RoboDroidFrida:
    """
    A class for interacting with Android devices using 'frida'
    """

    def __init__(self, robodroidAdb: adb.RoboDroidAdb):
        self.adb = robodroidAdb

    def get_download_fname(self, arch: str) -> str:
        """
        Depending upon the arch provided, the function returns the filename of the frida-server file.
        """
        base_filename = "frida-server-{}-android-{}.xz"
        return base_filename.format(frida.__version__, arch)

    def get_download_url(self, arch: str) -> str:
        """
        Depending upon the arch provided, the function returns the download URL.
        """
        fname = self.get_download_fname(arch)
        base_url = "https://github.com/frida/frida/releases/download/{}/{}"
        return base_url.format(frida.__version__, fname)

    def get_frida_server_bin_path(self) -> str:
        download_folder = helper.robodroid_frida_folder()
        device_arch = self.adb.get_device_arch()
        frida_arch = device_arch_frida_mapping[device_arch]
        frida_server_bin = os.path.join(download_folder, self.get_download_fname(frida_arch)[:-3])
        return frida_server_bin

    def download_frida_server(self) -> bool:
        download_folder = helper.robodroid_frida_folder()
        device_arch = self.adb.get_device_arch()
        frida_arch = device_arch_frida_mapping[device_arch]
        download_url = self.get_download_url(frida_arch)
        logger.info(f"Downloading frida-server from '{download_url}'")
        req = requests.get(download_url, stream=True)
        if req.status_code == 200:
            fname = self.get_download_fname(frida_arch)
            frida_server_archive = os.path.join(download_folder, fname)
            req.raw.decode_content = True
            with open(frida_server_archive, "wb") as frida_archive_file:
                for chunk in req.iter_content(1024):
                    frida_archive_file.write(chunk)

            with lzma.open(frida_server_archive) as frida_archive_file:
                data = frida_archive_file.read()
                os.unlink(frida_server_archive)
        else:
            logger.error(
                f"Downloading frida-server. Got HTTP status code {req.status_code} from server."
            )

        if data:
            frida_server_bin = os.path.join(
                download_folder, self.get_download_fname(frida_arch)[:-3]
            )
            logger.info(f"Writing file as: {frida_server_bin}")
            with open(frida_server_bin, "wb") as frida_server:
                frida_server.write(data)
            return True
        return False

    def is_frida_server_bin_available(self) -> bool:
        frida_server_bin = self.get_frida_server_bin_path()
        if os.path.isfile(frida_server_bin):
            return True
        return False

    def start_frida_server(self) -> None:
        frida_server_bin = self.get_frida_server_bin_path()
        if not self.is_frida_server_bin_available():
            self.download_frida_server()
        self.adb.push(frida_server_bin, "/data/local/tmp/frida-server", 755)
        self.adb.shell_cmd("killall frida-server", False)
        self.adb.thread_shell_cmd("/data/local/tmp/frida-server")
        logger.success("Frida server correctly started")
