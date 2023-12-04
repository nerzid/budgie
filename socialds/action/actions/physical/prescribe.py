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

    def __init__(self, prescriber: Agent | DSTPronoun, prescribed: List[Property], prescribed_for: Agent | DSTPronoun, negation: bool = False,
                 times=None):
        self.prescriber = prescriber
        self.prescribed = prescribed
        self.prescribed_for = prescribed_for
        self.negation = negation
        self.times = times
        super().__init__('prescribe', ActionObjType.PHYSICAL, [], times=times)

    def colorless_repr(self):
        return f"{self.prescriber} prescribe {self.prescribed} for {self.prescribed_for}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.prescriber} prescribe {self.prescribed} for {self.prescribed_for}{super().get_times_str()}"

    def insert_pronouns(self):
        if isinstance(self.prescriber, DSTPronoun):
            self.prescriber = pronouns[self.prescriber]
        if isinstance(self.prescribed_for, DSTPronoun):
            self.prescribed_for = pronouns[self.prescribed_for]
        super().insert_pronouns()
                
    def execute(self):
        self.insert_pronouns()
        super().execute()
