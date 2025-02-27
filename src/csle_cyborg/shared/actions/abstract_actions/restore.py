from random import choice

from csle_cyborg.shared.observation import Observation
from csle_cyborg.shared.actions.action import Action
from csle_cyborg.shared.actions.concrete_actions.restore_from_backup import RestoreFromBackup
from csle_cyborg.simulator.session import VelociraptorServer


class Restore(Action):
    def __init__(self, session: int, agent: str, hostname: str):
        super().__init__()
        self.agent = agent
        self.session = session
        self.hostname = hostname

    def sim_execute(self, state) -> Observation:
        # perform monitor at start of action
        # monitor = Monitor(session=self.session, agent=self.agent)
        # obs = monitor.sim_execute(state)

        if self.session not in state.sessions[self.agent]:
            return Observation(False)
        parent_session: VelociraptorServer = state.sessions[self.agent][self.session]
        # find relevant session on the chosen host
        sessions = [s for s in state.sessions[self.agent].values() if s.host == self.hostname]
        if len(sessions) > 0:
            session = choice(sessions)
            obs = Observation(True)
            # restore host
            action = RestoreFromBackup(session=self.session, agent=self.agent, target_session=session.ident)
            action.sim_execute(state)
            # remove suspicious files
            return obs
        else:
            return Observation(False)

    @property
    def cost(self):
        return -1

    def __str__(self):
        return f"{self.__class__.__name__} {self.hostname}"
