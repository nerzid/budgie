from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.actions.verbal.affirm import Affirm
from socialds.action.actions.verbal.affirm_or_deny import AffirmOrDeny
from socialds.action.actions.verbal.deny import Deny
from socialds.action.effects.functional.add_expected_action import AddExpectedAction
from socialds.action.effects.functional.add_expected_action_options import AddExpectedActionOptions
from socialds.action.effects.functional.add_expected_effect import AddExpectedEffect
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.relation import Relation, RType


class RequestConfirmation(Action):
    def __init__(self, asked: Relation, r_tense: Tense, negation: bool = False):
        self.relation = Relation(DSTPronoun.I, RType.ACTION, r_tense, asked, negation)
        self.asked = asked
        super().__init__("request-confirmation", DSTPronoun.I, ActionObjType.VERBAL, base_effects=[
            AddExpectedActionOptions(actions=[Affirm(asked), Deny(asked)], negation=negation, affected=DSTPronoun.YOU)
        ], recipient=DSTPronoun.YOU)

    def __str__(self):
        return "%s asks confirmation for %s" % (self.done_by.name, self.asked)

    def __repr__(self):
        return "%r ask confirmation for %r" % (self.done_by.name, self.asked)

    def insert_pronouns(self, ):
        self.relation.pronouns = self.pronouns
        self.asked.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.asked.insert_pronouns()
        super().insert_pronouns()

    def execute(self, agent, **kwargs):
        self.pronouns = agent.pronouns
        self.insert_pronouns()
        super().execute(agent, **kwargs)

