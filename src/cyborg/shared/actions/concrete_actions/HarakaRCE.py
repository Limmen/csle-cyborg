from ipaddress import IPv4Address
from cyborg.shared.Observation import Observation
from cyborg.shared.actions.concrete_actions.ExploitAction import ExploitAction
from cyborg.simulator.Process import ProcessVersion
from cyborg.simulator.Host import Host
from cyborg.simulator.Process import Process
from cyborg.simulator.State import State


class HarakaRCE(ExploitAction):
    def __init__(self, session: int, agent: str, ip_address: IPv4Address, target_session: int):
        super().__init__(session, agent, ip_address, target_session)

    def sim_execute(self, state: State) -> Observation:
        return self.sim_exploit(state, 25, 'smtp')

    def test_exploit_works(self, target_host: Host, vuln_proc: Process):
        # make sure the Haraka version < 2.8.9        
        return vuln_proc.version.value < ProcessVersion.HARAKA_2_8_9.value
