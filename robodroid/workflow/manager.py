from time import sleep
from robodroid import types
from robodroid.workflow import commands
from robodroid.services import adb, frida
from robodroid.utils import helper, logger


class RoboDroidWorkflowManager:
    """
    A class for managing a workflow
    """

    def __init__(self, config_data: types.common.ConfigData, adb_instance: adb.RoboDroidAdb):
        self.config_data = config_data
        self.adb_instance = adb_instance
        self.outputs = {}

    def _run_init(self) -> None:
        # Install packages
        if "init" in self.config_data:
            for package in self.config_data["init"]["packages"]:
                self.adb_instance.install(package)

    def _run_frida_behavior(self, behavior: types.common.ConfigStep) -> None:
        lib_name = behavior["name"]
        inputs = behavior["inputs"]
        lib_data = helper.get_lib_data(lib_name)
        package_name = lib_data["info"]["package_name"]
        # Check if permissions must be set
        if "permissions" in lib_data["info"].keys():
            permissions = lib_data["info"]["permissions"]
            for permission in permissions:
                logger.info(f"Adding permission {permission} to package {package_name}")
                commands.adb_add_permission(self.adb_instance, package_name, permission)

        # Run Frida behavior
        frida.load_frida_js(lib_data, inputs)

    def _run_command(self, command: types.common.ConfigStep) -> None:
        print(command)

    def _run_workflow(self) -> None:
        # TODO: Move this Frida setup steps in a specific function
        logger.info("Restarting adbd as root and waiting 2 seconds before continuing")
        self.adb_instance.enable_root()
        sleep(2)  # To ensure the other tests do not fail after 'enable_root'
        frida_instance = frida.RoboDroidFrida(self.adb_instance)
        frida_instance.start_frida_server()

        # Run the actual workflow
        for step in self.config_data["workflow"]:
            if step["type"] == types.enum.WorkflowStepType.FRIDA:
                outputs = self._run_frida_behavior(step)
                self.outputs[step["id"]] = outputs
            elif step["type"] == types.enum.WorkflowStepType.ADB:
                self._run_command(step)
            else:
                logger.error("Unknown step type in Workflow, skipping")

    def run(self) -> None:
        self._run_init()
        self._run_workflow()
