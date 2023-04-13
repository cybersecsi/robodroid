from time import sleep
from robodroid.services import adb
from pathlib import Path

FILE_PATH = Path(__file__)
FOLDER_PATH = FILE_PATH.parent

test_data = {
    "arm64-v8a": {
        "insecure_bank_apk": f"{FOLDER_PATH}/assets/InsecureBankv2.apk",
    },
    # TODO: add for different architectures
}


def adb_connected_instance():
    adb_instance = adb.RoboDroidAdb()
    adb_instance.device = adb_instance.list_devices()[0]
    return adb_instance


def test_debug_info():
    adb_instance = adb_connected_instance()
    print(adb_instance.is_root_enabled())
    assert False  # Set to False to print stdout


def test_adb_version():
    adb_instance = adb.RoboDroidAdb()
    assert adb_instance.get_adb_version() == 41


def test_device_arch():
    adb_instance = adb_connected_instance()
    assert adb_instance.get_device_arch() == "arm64-v8a"


def test_chrome_installed():
    adb_instance = adb_connected_instance()
    assert adb_instance.is_apk_installed("com.android.chrome") == True


def test_dummy_installed():
    adb_instance = adb_connected_instance()
    assert adb_instance.is_apk_installed("com.robodroid.dummy") == False


def test_enable_root():
    adb_instance = adb_connected_instance()
    root = adb_instance.enable_root()
    sleep(5)  # To ensure the other tests do not fail after 'enable_root'
    assert root == True


def test_install_apk():
    test_package_name = "com.android.insecurebankv2"
    adb_instance = adb_connected_instance()
    # Be sure is not already installed
    adb_instance.uninstall(test_package_name)
    assert adb_instance.is_apk_installed(test_package_name) == False
    # Install the correct version
    device_arch = adb_instance.get_device_arch()
    assert adb_instance.get_device_arch() == "arm64-v8a"
    adb_instance.install(test_data[device_arch]["insecure_bank_apk"])
    assert adb_instance.is_apk_installed(test_package_name) == True
    # Uninstall it
    adb_instance.uninstall(test_package_name)
    assert adb_instance.is_apk_installed(test_package_name) == False
