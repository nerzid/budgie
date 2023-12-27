from __future__ import annotations

from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Open(SimpleAction):
    def __init__(self, target_resource: any, done_by: Agent | DSTPronoun):
        super().__init__('open', done_by, ActionObjType.PHYSICAL, target_resource=target_resource)

    def __str__(self):
        return "%s open %s" % (self.done_by, self.target_resource)

    def __repr__(self):
        return "%r open %r" % (self.done_by, self.target_resource)

