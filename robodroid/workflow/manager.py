from typing import List, Dict, Any
from robodroid import types
from robodroid.workflow import config, commands
from robodroid.services import adb, frida
from robodroid.utils import helper, logger


class RoboDroidWorkflowManager:
    """
    A class for managing a workflow
    """

    def __init__(self, config_data: types.common.ConfigData, adb_instance: adb.RoboDroidAdb):
        self.config_data = config_data
        self.adb_instance = adb_instance
        is_root_enabled = self.adb_instance.is_root_enabled()
        if not is_root_enabled:
            logger.error("Root is not enabled, restarting adbd as root (it may take a while)...")
            self.adb_instance.enable_root()
        self.frida_instance = frida.RoboDroidFrida(adb_instance)
        self.outputs: Dict[str, Any] = {}

    def _run_init(self) -> None:
        # Install packages
        if not "init" in self.config_data:
            return

        for apk in self.config_data["init"]["install"]:
            logger.info(f"Installing app from '{apk}'")
            self.adb_instance.install(apk)
        for package_name in self.config_data["init"]["clear"]:
            logger.info(f"Cleaning package '{package_name}'")
            self.adb_instance.shell_cmd(f"pm clear {package_name}", False)

    def _run_frida_behavior(self, behavior: types.common.ConfigStep) -> None:
        while True:
            reserved_output = "robodroid.outputs."
            lib_name = behavior["name"]
            inputs = behavior["inputs"]
            input_values: List[str | int] = [i["value"] for i in inputs]
            input_values = [
                self.outputs[i.split(".")[2]][i.split(".")[3]]
                if isinstance(i, str) and i.startswith(reserved_output)
                else i
                for i in input_values
            ]

            lib_data = helper.get_lib_data(lib_name)
            package_name = lib_data["info"]["package_name"]
            # Check if permissions must be set
            if "permissions" in lib_data["info"].keys():
                permissions = lib_data["info"]["permissions"]
                for permission in permissions:
                    logger.info(f"Adding permission {permission} to package {package_name}")
                    commands.adb_add_permission(self.adb_instance, package_name, permission)

            # Run Frida behavior
            self.adb_instance.shell_cmd("am clear-debug-app")
            behavior_result = self.frida_instance.run_behavior(lib_data, input_values)
            if behavior_result["status"] == types.enum.BehaviorResultType.COMPLETED.value:
                logger.success("Behavior step completed successfully")
                logger.info(f"Message: {behavior_result['msg']}")
                if "outputs" in behavior_result.keys():
                    logger.info(f"Outputs: {behavior_result['outputs']}")
                    self.outputs[behavior["id"]] = behavior_result["outputs"]
                break
            else:
                logger.error("Behavior failed, starting over")

    def _run_command(self, step: types.common.ConfigStep) -> None:
        command_name = step["name"]
        command_type = step["type"]
        if not command_name in config.workflow_commands[command_type].keys():
            logger.error(f"Unable to find command with id {command_name}")
            return

        logger.info(f"Running command '{command_name}'")
        reserved_output = "robodroid.outputs."
        inputs = step["inputs"]
        input_values: List[str | int] = [i["value"] for i in inputs]
        input_values = [
            self.outputs[i.split(".")[2]][i.split(".")[3]]
            if isinstance(i, str) and i.startswith(reserved_output)
            else i
            for i in input_values
        ]
        if command_type == types.enum.WorkflowStepType.ADB.value:
            config.workflow_commands[types.enum.WorkflowStepType.ADB.value][command_name](
                self.adb_instance, *input_values
            )
            logger.info(f"Command '{command_name}' completed")

    def _run_workflow(self) -> None:
        # TODO: Move this Frida setup steps in a specific function
        self.frida_instance.start_frida_server()

        command_types = [types.enum.WorkflowStepType.ADB.value]
        # Run the actual workflow
        for step in self.config_data["workflow"]:
            if step["type"] == types.enum.WorkflowStepType.FRIDA:
                self._run_frida_behavior(step)
            elif step["type"] in command_types:
                self._run_command(step)
            else:
                logger.error("Unknown step type in Workflow, skipping")
        logger.success("Workflow completed!")

    def run(self) -> None:
        self._run_init()
        self._run_workflow()
