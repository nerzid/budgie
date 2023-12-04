from __future__ import annotations

from typing import List

from socialds.action.action_time import ActionTime
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Sleep(Action):
    def __init__(self, sleeper: Agent | DSTPronoun, times: List[ActionTime] = None):
        self.sleeper = sleeper
        super().__init__('sleep', ActionObjType.PHYSICAL, [], times=times)

    def colorless_repr(self):
        return f"{self.sleeper} sleeps{super().get_times_str()}"

    def __repr__(self):
        return f"{self.sleeper} sleeps{super().get_times_str()}"
    
    def insert_pronouns(self):
        if isinstance(self.sleeper, DSTPronoun):
            self.sleeper = pronouns[self.sleeper]
        super().insert_pronouns()
        
    def execute(self):
        self.insert_pronouns()
        super().execute()
