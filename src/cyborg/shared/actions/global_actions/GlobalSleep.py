# Copyright DST Group. Licensed under the MIT license.
import time
from cyborg.shared.Observation import Observation
from cyborg.shared.actions.global_actions.GlobalAction import GlobalAction


class GlobalSleep(GlobalAction):

    def __init__(self, t=1):
        super().__init__()
        self.t = t

    def emu_execute(self, team_server) -> Observation:
        obs = Observation()
        time.sleep(self.t)
        obs.set_success(True)
        obs.add_raw_obs("Sleeping...")
        return obs
