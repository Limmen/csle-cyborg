# Copyright DST Group. Licensed under the MIT license.
from cyborg.shared.actions.MSFActionsFolder.RemoteCodeExecutionFolder.RemoteCodeExecution import RemoteCodeExecution


class RubyOnRails(RemoteCodeExecution):
    def __init__(self):
        super().__init__()

    def sim_execute(self, state):
        pass
