from __future__ import annotations

from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun


class SelfCure(SimpleAction):

    def __init__(self, done_by: Agent | DSTPronoun = DSTPronoun.I):
        """
        An agent cures themselves, i.e., self-cure
        Args:
            done_by: The agent or DSTPronoun who selfcured themselves
        """
        super().__init__('self-cure', done_by=done_by, act_type=ActionObjType.PHYSICAL, recipient=done_by)

    @staticmethod
    def get_pretty_template():
        return "[done_by] self-cured [recipient]"

    def __str__(self):
        return "%s %s" % (self.done_by, self.name)

    def __repr__(self):
        return "%r %r" % (self.done_by, self.name)

