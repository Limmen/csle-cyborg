from cyborg.shared.Observation import Observation
from cyborg.shared.actions.ConcreteActions.ConcreteAction import ConcreteAction
from cyborg.simulator.Host import Host
from cyborg.simulator.State import State


class SigCheck(ConcreteAction):
    def __init__(self, session: int, agent: str, target_session: int):
        super(SigCheck, self).__init__(session=session, agent=agent)
        self.target_session = target_session

    def sim_execute(self, state: State) -> Observation:
        obs = Observation()
        if self.session not in state.sessions[self.agent] or self.target_session not in state.sessions[self.agent]:
            obs.set_success(False)
            return obs
        target_host: Host = state.hosts[state.sessions[self.agent][self.target_session].host]
        session = state.sessions[self.agent][self.session]
        target_session = state.sessions[self.agent][self.target_session]

        if not session.active or not target_session.active:
            obs.set_success(False)
            return obs
        obs.set_success(True)
        for file in target_host.files:
            obs.add_file_info(hostid=target_host.hostname, name=file.name, path=file.path, signed=file.signed)

        return obs