# Copyright DST Group. Licensed under the MIT license.
from cyborg.shared.actions.ShellActionsFolder.OpenConnectionFolder.OpenConnection import OpenConnection


class CredentialAccess(OpenConnection):
    def __init__(self, session, agent):
        super().__init__(session, agent)

    def sim_execute(self, state):
        pass
