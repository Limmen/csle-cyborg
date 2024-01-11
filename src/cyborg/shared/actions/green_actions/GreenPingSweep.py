from ipaddress import IPv4Network

from cyborg.shared.Observation import Observation
from cyborg.shared.actions.Action import Action
from cyborg.shared.actions.shell_actions_folder.NetworkScanFolder.PingSweep import PingSweep


class GreenPingSweep(Action):
    def __init__(self, session: int, agent: str, subnet: IPv4Network):
        super().__init__()
        self.subnet = subnet
        self.agent = agent
        self.session = session

    def sim_execute(self, state) -> Observation:
        # find session inside or close to the target subnet
        session = self.session
        # run pingsweep on the target subnet from selected session
        sub_action = PingSweep(session=self.session, agent=self.agent, subnet=self.subnet)
        obs = sub_action.sim_execute(state)
        return obs

    def __str__(self):
        return f"{self.__class__.__name__} {self.subnet}"
