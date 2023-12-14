from __future__ import annotations

from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.relation import Relation


class Request(Action):
    def __init__(self, requester: Agent | DSTPronoun, requested: Action):
        self.requester = requester
        self.requested = requested
        super().__init__('request', ActionObjType.VERBAL, [])

    def colorless_repr(self):
        return f"{super().colorless_repr()}{str(self.requester.name)} request {self.requested.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.requester.name} request {self.requested}"

    def insert_pronouns(self):
        if isinstance(self.requester, DSTPronoun):
            self.requester = pronouns[self.requester]
        self.requested.insert_pronouns()
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()
    
# Can Joe come into the office?
# request to enter the place
# it is a request for the following Joe -move-> office assuming
# requester -> relation
