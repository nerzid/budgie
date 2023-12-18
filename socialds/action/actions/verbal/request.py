from __future__ import annotations

from socialds.action.effects.functional.add_expected_action import AddExpectedAction
from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.other.dst_pronouns import DSTPronoun


class Request(Action):
    def __init__(self, done_by: Agent | DSTPronoun, requested: Action):
        self.requested = requested
        super().__init__('request', done_by, ActionObjType.VERBAL, [
            AddExpectedAction(requested, False, DSTPronoun.YOU)
        ])

    def colorless_repr(self):
        return f"{super().colorless_repr()}{str(self.done_by.name)} request {self.requested.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.done_by.name} request {self.requested}"

    def insert_pronouns(self):
        self.requested.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()

# Can Joe come into the office?
# request to enter the place
# it is a request for the following Joe -move-> office assuming
# requester -> relation
