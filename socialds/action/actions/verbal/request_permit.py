from __future__ import annotations

from socialds.action.effects.functional.add_expected_action import AddExpectedAction
from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.relation import Negation


class RequestPermit(Action):
    def __init__(
        self,
        requested: Action,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
    ):
        self.requested = requested
        super().__init__(
            "request",
            done_by=done_by,
            act_type=ActionObjType.VERBAL,
            recipient=recipient,
            base_effects=[AddExpectedAction(action=requested, affected=recipient)],
        )

    @staticmethod
    def get_pretty_template():
        return "[done_by] requests [requested]"

    def __str__(self):
        return "%s request %s" % (self.done_by.name, self.requested)

    def __repr__(self):
        return "%r request %r" % (self.done_by.name, self.requested)


# Can Joe come into the office?
# request to enter the place
# it is a request for the following Joe -move-> office assuming
# requester -> relation
