from typing import List

from socialds.DSTPronounHolder import DSTPronounHolder


class OperationFailed(Exception):
    pass


class Operation(DSTPronounHolder):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.agent = None

    def execute(self, agent, *args, **kwargs):
        self.agent = agent
        self.pronouns = agent.pronouns
