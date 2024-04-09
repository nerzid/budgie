from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.actions.verbal.affirm import Affirm
from socialds.action.actions.verbal.deny import Deny
from socialds.action.effects.functional.add_expected_action_options import AddExpectedActionOptions
from socialds.agent import Agent
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation, RType


class RequestConfirmation(Action):
    def __init__(self, asked: Information, done_by: Agent | DSTPronoun = DSTPronoun.I,
                 recipient: Agent | DSTPronoun = DSTPronoun.YOU,
                 tense: Tense = Tense.ANY,
                 negation: bool = False):
        self.relation = Information(done_by, RType.ACTION, tense, asked, negation)
        self.asked = asked
        super().__init__("request-confirmation", done_by=done_by, act_type=ActionObjType.VERBAL, base_effects=[
            AddExpectedActionOptions(actions=[Affirm(asked), Deny(asked)], negation=negation, affected=recipient)
        ], recipient=recipient)

    def __str__(self):
        return "%s asks confirmation for %s" % (self.done_by.name, self.asked)

    def __repr__(self):
        return "%r asks confirmation for %r" % (self.done_by.name, self.asked)

    @staticmethod
    def get_pretty_template():
        return "[done_by] asks confirmation for [asked] to [recipient]([tense][negation])"

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
