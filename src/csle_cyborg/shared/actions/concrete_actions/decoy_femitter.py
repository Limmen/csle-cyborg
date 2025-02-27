from random import choice
from csle_cyborg.shared.observation import Observation
from csle_cyborg.shared.actions.action import Action
from csle_cyborg.shared.enums import DecoyType
from csle_cyborg.simulator.host import Host
from csle_cyborg.simulator.session import Session
from csle_cyborg.simulator.state import State
from csle_cyborg.shared.enums import OperatingSystemType
from csle_cyborg.shared.actions.abstract_actions.misinform import Decoy, DecoyFactory, _is_host_using_port


class FemitterDecoyFactory(DecoyFactory):
    """
    Assembles process information to appear as an apache server
    """

    def make_decoy(self, host: Host) -> Decoy:
        del host
        return Decoy(service_name="femitter", name="femitter",
                     open_ports=[{'local_port': 21, 'local_address': '0.0.0.0'}],
                     process_type='femitter',
                     process_path="/usr/sbin")

    def is_host_compatible(self, host: Host) -> bool:
        has_port = not _is_host_using_port(host, 21)
        is_windows = host.os_type == OperatingSystemType.WINDOWS

        return has_port and is_windows


femitter_decoy_factory = FemitterDecoyFactory()


class DecoyFemitter(Action):
    """
    Creates a misleading process on the designated host depending on
    available and compatible options.
    """

    def __init__(self, *, session: int, agent: str, hostname: str):
        self.agent = agent
        self.session = session
        self.hostname = hostname
        self.decoy_type = DecoyType.EXPLOIT
        self.candidate_decoys = (femitter_decoy_factory,)

    def emu_execute(self) -> Observation:
        raise NotImplementedError

    def sim_execute(self, state: State) -> Observation:
        obs_fail = Observation(False)
        obs_succeed = Observation(True)

        sessions = [s for s in state.sessions[self.agent].values() if
                    s.host == self.hostname]
        if len(sessions) == 0:
            return obs_fail

        session = choice(sessions)
        host = state.hosts[self.hostname]

        try:
            decoy_factory = self.__select_one_factory(host)
            decoy = decoy_factory.make_decoy(host)
            self.__create_process(obs_succeed, session, host, decoy)
            # print ("Misinform Success. Result: {}".format(result))

            return obs_succeed

        except RuntimeError:
            # print ("Misinform FAILURE")
            return obs_fail

    def __select_one_factory(self, host: Host) -> DecoyFactory:
        """
        Examines all decoy factories and returns one randomly compatible one.
        Raises RuntimeError if no compatible ones are found.
        """

        compatible_factories = [factory for factory in self.candidate_decoys
                                if factory.is_host_compatible(host)]

        if len(compatible_factories) == 0:
            raise RuntimeError("No compatible factory")

        return choice(list(compatible_factories))

    def __create_process(self, obs: Observation, sess: Session, host: Host,
                         decoy: Decoy) -> None:
        """
        Creates a process & service from Decoy on current host, adds it
        to the observation.
        """

        parent_pid = 1

        process_name = decoy.name
        username = 'SYSTEM'
        version = decoy.version
        open_ports = decoy.open_ports
        process_type = decoy.process_type
        process_props = decoy.properties

        service_name = decoy.service_name

        new_proc = host.add_process(name=process_name, ppid=parent_pid,
                                    user=username, version=version, process_type=process_type,
                                    open_ports=open_ports, decoy_type=self.decoy_type,
                                    properties=process_props)

        host.add_service(service_name=service_name, process=new_proc.pid,
                         session=sess)

        obs.add_process(hostid=self.hostname, pid=new_proc.pid,
                        parent_pid=parent_pid, name=process_name,
                        username=username, service_name=service_name,
                        properties=process_props)

    def __str__(self):
        return f"{self.__class__.__name__} {self.hostname}"
