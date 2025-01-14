# Copyright DST Group. Licensed under the MIT license.
import time

from csle_cyborg.shared.observation import Observation
from csle_cyborg.shared.actions.game_actions.game_action import GameAction


class GameSleep(GameAction):

    def __init__(self, t: int = 1):
        super().__init__()
        self.t = t

    def emu_execute(self, game_controller, *args, **kwargs) -> Observation:
        time.sleep(self.t)
        obs = Observation()
        obs.set_success(True)
        obs.add_raw_obs(f"I'm feeling refreshed! I slept {self.t} secs")
        return obs
