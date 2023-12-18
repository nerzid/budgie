from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType
from socialds.states.relation import Relation


class Deduce(Action):
    def __init__(self, done_by: Agent | DSTPronoun, deduced: Relation):
        """
        Agent thinks and arrives at a certain relation.
        E.g., after thinking, doctor figures out that the patient has bacterial conjunctivitis
        :param done_by: The agent who deduces the relation as fact
        :param deduced: The deduced information as relation to be stored in the deducer's knowledgebase
        """
        self.done_by = done_by
        self.deduced = deduced
        super().__init__('deduce', done_by, ActionObjType.MENTAL, base_effects=[
            GainKnowledge(knowledge=deduced, affected=done_by)
        ])

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.done_by.name} deduce that {self.deduced.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.done_by.name} deduce that {self.deduced}"

    def insert_pronouns(self):
        if isinstance(self.done_by, DSTPronoun):
            self.done_by = pronouns[self.done_by]
        self.deduced.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        self.done_by.relation_storages[RSType.KNOWLEDGEBASE].add(self.deduced)
        super().execute()
