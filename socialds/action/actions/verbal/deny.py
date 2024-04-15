from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.change_property import GainKnowledge
from socialds.agent import Agent
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
import socialds.action.actions.verbal.request_confirmation as rc
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation, RType


class Deny(Action):
    def __init__(self, denied: Information, done_by: Agent | DSTPronoun = DSTPronoun.I,
                 recipient: Agent | DSTPronoun = DSTPronoun.YOU):
        self.denied = denied
        super().__init__('deny', done_by=done_by, recipient=recipient, act_type=ActionObjType.VERBAL, base_effects=[
            GainKnowledge(knowledge=denied, affected=recipient)
        ], target_relations=[denied])

    @staticmethod
    def get_pretty_template():
        return "[done_by] denies [denied]"

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.denied == other.denied

    def check_preconditions(self, checker):
        return super().check_preconditions(checker) and \
            AgentDoesAction(agent=DSTPronoun.YOU, action=Relation(left=DSTPronoun.YOU, rtype=RType.ACTION,
                                                                  rtense=Tense.PAST,
                                                                  right=rc.RequestConfirmation(done_by=DSTPronoun.YOU,
                                                                                               asked=self.denied,
                                                                                               tense=Tense.ANY,
                                                                                               recipient=DSTPronoun.I)),
                            tense=Tense.PAST).check(checker=checker)

    def insert_pronouns(self):
        self.denied.pronouns = self.pronouns
        self.denied.insert_pronouns()
        super().insert_pronouns()
