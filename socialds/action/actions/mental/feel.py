from __future__ import annotations

from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.relation import Relation, RType
from socialds.states.property import Property
from socialds.enums import Tense


class Feel(Action):
    def __init__(self, felt_by: Agent | DSTPronoun, felt: Property, about: Relation, r_tense: Tense,
                 negation: bool = False):
        self.felt_by = felt_by
        self.felt = felt
        self.about = about
        self.r_tense = r_tense
        self.negation = negation
        super().__init__('feel', ActionObjType.FUNCTIONAL, [])

    def colorless_repr(self):
        return f"{super().__repr__()}{self.felt_by.name} feel {self.felt} about {self.about.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.felt_by.name} feel {self.felt} about {self.about}"

    def insert_pronouns(self):
        if isinstance(self.felt_by, DSTPronoun):
            self.felt_by = pronouns[self.felt_by]
        self.about.insert_pronouns()
        super().insert_pronouns()
        
    def execute(self):
        self.insert_pronouns()
        super().execute()