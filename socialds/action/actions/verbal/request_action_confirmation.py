from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.actions.verbal.affirm import Affirm
from socialds.action.actions.verbal.deny import Deny
from socialds.action.effects.functional.add_expected_action_options import (
    AddExpectedActionOptions,
)
from socialds.agent import Agent
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation, RType, Negation


class RequestActionConfirmation(Action):
    def __init__(
        self,
        action: Action,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
        is_any=False,
    ):
        """
        Requests confirmation for a certain information relation.
        Args:
            action: Action to be confirmed whether it is done or not.
            done_by: Agent or DSTPronoun who requests the confirmation.
            recipient: Agent or DSTPronoun who the confirmation is requested from.
            tense: Tense of the action.
            negation: Negation of the action.
        """
        self.relation = Information(done_by, RType.ACTION, tense, action, negation)
        self.action = action
        if negation == Negation.ANY:
            base_effects = [
                AddExpectedActionOptions(
                    actions=[Affirm(action), Deny(action)],
                    negation=negation,
                    affected=recipient,
                )
            ]
        else:
            base_effects = [
                AddExpectedActionOptions(
                    actions=[Affirm(action), Deny(action)],
                    negation=negation,
                    affected=recipient,
                )
            ]
        super().__init__(
            "request-action-confirmation",
            done_by=done_by,
            act_type=ActionObjType.VERBAL,
            base_effects=base_effects,
            recipient=recipient,
            is_any=is_any,
        )

    def __str__(self):
        return "%s asks confirmation for %s" % (self.done_by.name, self.action)

    def __repr__(self):
        return "%r asks confirmation for %r" % (self.done_by.name, self.action)

    @staticmethod
    def get_pretty_template():
        return (
            "[done_by] asks confirmation for [asked] to [recipient]([tense][negation])"
        )

    def insert_pronouns(
        self,
    ):
        self.relation.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.action.insert_pronouns()
        super().insert_pronouns()

    def execute(self, agent, **kwargs):
        self.pronouns = agent.pronouns
        self.insert_pronouns()
        super().execute(agent, **kwargs)
