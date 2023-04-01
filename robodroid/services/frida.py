import time
import os
import typing
import frida
from robodroid import types
from robodroid.utils import helper, logger
from wrapt_timeout_decorator import *


def on_message(message: typing.Any, data: typing.Any) -> None:
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


@timeout(5, use_signals=False)
def spawn_app(device: typing.Any, package_name: str) -> typing.Any:
    return device.spawn([package_name])


def load_frida_js(lib_data: types.common.LibData) -> None:
    package_name = lib_data["info"]["package_name"]
    script_name = os.path.join(helper.robodroid_lib_folder(), lib_data["id"], "index.js")

    try:
        device = frida.get_usb_device()
        pid = spawn_app(device, package_name)
        device.resume(pid)
        time.sleep(1)  # Without it Java.perform silently fails
        session = device.attach(pid)
        hooking_script = session.create_script(read_hooking_script(script_name))
        if hooking_script:
            hooking_script.on("message", on_message)
            hooking_script.load()
        else:
            logger.error("The specified script '{0}' was not found!")

        # stop python script from terminating
        input("Press any key to continue...")
        # script = session.create_script(open(script_name).read())
        # return script
    except TimeoutError as exc:
        logger.error(str(exc))
