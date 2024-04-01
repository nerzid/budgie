from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
import socialds.action.actions.verbal.request_confirmation as rc
from socialds.states.relation import Relation, RType


class Affirm(Action):

    def __init__(self, affirmed):
        self.affirmed = affirmed
        super().__init__('affirm', done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL, base_effects=[
            GainKnowledge(knowledge=affirmed, affected=DSTPronoun.YOU)
        ])

    def insert_pronouns(self):
        self.affirmed.pronouns = self.pronouns
        self.affirmed.insert_pronouns()
        super().insert_pronouns()

    def check_preconditions(self, checker):
        return super().check_preconditions(checker) and \
            AgentDoesAction(agent=DSTPronoun.YOU, action=Relation(left=DSTPronoun.YOU, rtype=RType.ACTION,
                                                                  rtense=Tense.PAST,
                                                                  right=rc.RequestConfirmation(asked=self.affirmed,
                                                                                               r_tense=Tense.ANY)),
                            tense=Tense.PAST).check(checker=checker)

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.affirmed == other.affirmed
