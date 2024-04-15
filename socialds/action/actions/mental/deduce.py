from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation


class Deduce(Action):

    def __init__(self, done_by: Agent | DSTPronoun, deduced: Information):
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

    def __str__(self):
        return "%s deduce that %s" % (self.done_by.name, self.deduced)

    def __repr__(self):
        return "%r deduce that %r" % (self.done_by.name, self.deduced)

    def insert_pronouns(self):
        self.deduced.pronouns = self.pronouns
        self.deduced.insert_pronouns()
        super().insert_pronouns()

    def get_requirement_holders(self) -> List:
        return super().get_requirement_holders() + [self.deduced]
