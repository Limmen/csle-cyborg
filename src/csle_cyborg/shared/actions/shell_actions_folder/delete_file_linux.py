# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.actions.shell_actions_folder.shell_action import ShellAction
from csle_cyborg.shared.enums import OperatingSystemType
from csle_cyborg.shared.observation import Observation


class DeleteFileLinux(ShellAction):
    def __init__(self, session: int, agent: str, file: str, path: str):
        super().__init__(session, agent)
        self.file = file
        self.path = path

    def sim_execute(self, state):
        obs = Observation()
        obs.set_success(False)
        if self.session not in state.sessions[self.agent]:
            return obs
        if not state.sessions[self.agent][self.session].active:
            return obs

        host = state.sessions[self.agent][self.session].host
        obs.add_system_info(hostid="hostid0", os_type=host.os_type)
        if host.os_type == OperatingSystemType.LINUX:
            file = host.get_file(name=self.file, path=self.path)
            if file is not None:
                obs.set_success(True)
                host.files.remove(file)

            else:
                obs.set_success(False)

        else:
            obs.set_success(False)
        return obs
