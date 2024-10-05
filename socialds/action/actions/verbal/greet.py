from __future__ import annotations

from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun


class Greet(SimpleAction):
    def __init__(
        self,
        done_by: DSTPronoun | Agent = DSTPronoun.I,
        recipient: DSTPronoun | Agent = DSTPronoun.YOU,
    ):
        """
        Greets an agent
        Args:
            done_by: The agent or DSTPronoun who greets
            recipient: The agent or DSTPronoun who is greeted
        """
        super().__init__(
            name="greet", done_by=done_by, act_type=ActionObjType.VERBAL, recipient=recipient
        )

    @staticmethod
    def get_pretty_template():
        return "[done_by] greets [recipient]"

    def __str__(self):
        return "%s %s %s" % (self.done_by, self.name, self.recipient)

    # def __repr__(self):
    #     return "%r %s %r" % (self.done_by, self.name, self.recipient)
