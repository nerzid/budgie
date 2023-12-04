from __future__ import annotations

from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Open(SimpleAction):
    def __init__(self, target: any, by: Agent | DSTPronoun):
        self.target = target
        self.by = by
        super().__init__('open', ActionObjType.PHYSICAL)

    def colorless_repr(self):
        return f"{super().__repr__()}({str(self.by.name)} open {self.target.name}"

    def __repr__(self):
        return f"{super().__repr__()}({self.by.name} open {self.target.name}"
    
    def insert_pronouns(self):
        if isinstance(self.by, DSTPronoun):
            self.by = pronouns[self.by]
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()
