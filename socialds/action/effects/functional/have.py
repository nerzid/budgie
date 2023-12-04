from __future__ import annotations

from socialds.action.action_time import ActionTime
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.property import Property


class Have(Action):
    def __init__(self, owner: Agent | DSTPronoun, target: Property, times: [ActionTime] = None):
        self.owner = owner
        self.target = target
        super().__init__('has', ActionObjType.PHYSICAL, [], times=times)

    def colorless_repr(self):
        return f"{self.owner} has {self.target}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.owner} has {self.target}{super().get_times_str()}"
    
    def insert_pronouns(self):
        if isinstance(self.owner, DSTPronoun):
            self.owner = pronouns[self.owner]
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()