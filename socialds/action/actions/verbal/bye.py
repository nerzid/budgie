from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.agent import Agent
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.relation import Negation


class Bye(Action):
    def __init__(
        self,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
    ):
        self.tense = tense
        self.negation = negation
        super().__init__(
            "bye",
            done_by=done_by,
            act_type=ActionObjType.VERBAL,
            recipient=recipient,
            base_effects=[],
            target_relations=[],
        )

    def __str__(self):
        return "%s %s %s" % (self.done_by, self.name, self.recipient)

    @staticmethod
    def get_pretty_template():
        return "[done_by] farewells [recipient]"

    # def __repr__(self):
    #     return "%r %s %r" % (self.done_by, self.name, self.recipient)
