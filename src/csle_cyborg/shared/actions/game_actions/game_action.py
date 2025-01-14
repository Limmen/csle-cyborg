# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.observation import Observation
from csle_cyborg.shared.actions.action import Action


class GameAction(Action):
    """Abstract class for a game level action.

    A game action is one that operates within the context of a single
    scenario/game instance but outside of a single agent.

    Examples would be:
    - creating a new agent
    - terminating a game
    - listing available agents in a game
    """

    def emu_execute(self, game_controller, *args, **kwargs) -> Observation:
        raise NotImplementedError
