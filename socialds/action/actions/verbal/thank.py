from __future__ import annotations

from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun


class Thank(SimpleAction):

    def __init__(self, done_by: Agent | DSTPronoun = DSTPronoun.I, recipient: Agent | DSTPronoun = DSTPronoun.YOU):
        super().__init__('thank', done_by=done_by, act_type=ActionObjType.VERBAL, recipient=recipient)

    @staticmethod
    def get_pretty_template():
        return "[done_by] thanks [recipient]"

    def __str__(self):
        return "%s %s %s" % (self.done_by, self.name, self.recipient)

    def __repr__(self):
        return "%r %r %r" % (self.done_by, self.name, self.recipient)
