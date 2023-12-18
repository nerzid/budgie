from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.action_time import ActionTime
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.property import Property
from socialds.states.relation import Relation


class Prescribe(Action):

    def __init__(self, done_by: Agent | DSTPronoun, prescribed: List[Property], recipient: Agent | DSTPronoun,
                 negation: bool = False,
                 times=None):
        self.prescribed = prescribed
        self.negation = negation
        self.times = times
        super().__init__('prescribe', done_by, ActionObjType.PHYSICAL, [], times=times, recipient=recipient)

    def colorless_repr(self):
        return f"{self.done_by} prescribe {self.prescribed} for {self.recipient}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.done_by} prescribe {self.prescribed} for {self.recipient}{super().get_times_str()}"

    def insert_pronouns(self):
        super().insert_pronouns()
                
    def execute(self):
        self.insert_pronouns()
        super().execute()
