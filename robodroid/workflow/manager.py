from robodroid import types
from robodroid.services import adb, frida
from robodroid.utils import helper, logger


class RoboDroidWorkflowManager:
    """
    A class for managing a workflow
    """

    def __init__(self, config_data: types.common.ConfigData, adb_instance: adb.RoboDroidAdb):
        self.config_data = config_data
        self.adb_instance = adb_instance

    def _run_init(self) -> None:
        # Install packages
        if "init" in self.config_data:
            for package in self.config_data["init"]["packages"]:
                self.adb_instance.install(package)

    def _run_frida_behavior(self, behavior: types.common.ConfigStep) -> None:
        # Run Frida behavior
        frida_instance = frida.RoboDroidFrida(self.adb_instance)
        frida_instance.start_frida_server()
        lib_name = behavior["name"]
        inputs = behavior["inputs"]
        lib_data = helper.get_lib_data(lib_name)
        frida.load_frida_js(lib_data, inputs)

    def _run_command(self, command: types.common.ConfigStep) -> None:
        print(command)
        pass

    def _run_workflow(self) -> None:
        for step in self.config_data["workflow"]:
            if step["type"] == types.enum.WorkflowStepType.FRIDA:
                self._run_frida_behavior(step)
            elif step["type"] == types.enum.WorkflowStepType.ADB:
                self._run_command(step)
            else:
                logger.error("Unknown step type in Workflow, skipping")

    def run(self) -> None:
        self._run_init()
        self._run_workflow()
