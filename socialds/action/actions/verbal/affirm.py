from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.agent import Agent
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
import socialds.action.actions.verbal.request_confirmation as rc
from socialds.states.relation import Relation, RType


class Affirm(Action):

    def __init__(self, affirmed: Relation, done_by: Agent | DSTPronoun = DSTPronoun.I,
                 recipient: Agent | DSTPronoun = DSTPronoun.YOU):
        self.affirmed = affirmed
        super().__init__('affirm', done_by=done_by, act_type=ActionObjType.VERBAL, base_effects=[
            GainKnowledge(knowledge=affirmed, affected=recipient)
        ])

    @staticmethod
    def get_pretty_template():
        return "[done_by] affirms [affirmed]"

    def insert_pronouns(self):
        self.affirmed.pronouns = self.pronouns
        self.affirmed.insert_pronouns()
        super().insert_pronouns()

    def check_preconditions(self, checker):
        return super().check_preconditions(checker) and \
            AgentDoesAction(agent=DSTPronoun.YOU, action=Relation(left=DSTPronoun.YOU, rtype=RType.ACTION,
                                                                  rtense=Tense.PAST,
                                                                  right=rc.RequestConfirmation(done_by=DSTPronoun.YOU,
                                                                                               asked=self.affirmed,
                                                                                               tense=Tense.ANY,
                                                                                               recipient=DSTPronoun.I)),
                            tense=Tense.PAST).check(checker=checker)

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.affirmed == other.affirmed
