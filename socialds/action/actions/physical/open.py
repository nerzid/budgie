from __future__ import annotations

from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Open(SimpleAction):
    def __init__(self, target_resource: any, done_by: Agent | DSTPronoun):
        super().__init__('open', done_by, ActionObjType.PHYSICAL, target_resource=target_resource)

    def colorless_repr(self):
        return f"{super().__repr__()}({str(self.done_by.name)} open {self.target_resource.name}"

    def __repr__(self):
        return f"{super().__repr__()}({self.done_by.name} open {self.target_resource.name}"

    def insert_pronouns(self):
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
