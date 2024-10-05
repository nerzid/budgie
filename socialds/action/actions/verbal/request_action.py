from __future__ import annotations

from socialds.action.effects.functional.add_expected_action import AddExpectedAction
from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.relation import Negation


class RequestAction(Action):
    def __init__(
        self,
        requested: Action,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
    ):
        self.requested = requested
        self.tense = tense
        self.negation = negation
        super().__init__(
            "request-action",
            done_by=done_by,
            act_type=ActionObjType.VERBAL,
            recipient=recipient,
            base_effects=[AddExpectedAction(action=requested, affected=recipient)],
        )

    @staticmethod
    def get_pretty_template():
        return "[done_by] requests [requested]"

    @staticmethod
    def build_instance_from_effects(done_by, recipient, tense, negation, effects):
        if len(effects) != 1:
            return None
        add_expected_action: AddExpectedAction = effects[0]
        requested = add_expected_action.action
        return RequestAction(
            requested=requested,
            done_by=done_by,
            recipient=recipient,
            tense=tense,
            negation=negation,
        )

    def to_dict(self):
        super_dict = super().to_dict()
        super_dict.update({
            "done_by": self.done_by.to_dict(),
            "recipient": self.recipient.to_dict(),
            "tense": self.tense.to_dict(),
            "negation": self.negation.to_dict(),
            "requested": self.requested.to_dict(),
            "base_effects": [base_effect.to_dict() for base_effect in self.base_effects]
        })
        return super_dict

    def __str__(self):
        return "%s requests the action %s" % (self.done_by.name, self.requested)

    def __repr__(self):
        return "%r requests the action %r" % (self.done_by.name, self.requested)


# Can Joe come into the office?
# request to enter the place
# it is a request for the following Joe -move-> office assuming
# requester -> relation
