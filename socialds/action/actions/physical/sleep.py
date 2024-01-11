from __future__ import annotations

from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun


class Sleep(Action):
    def __init__(self, done_by: Agent | DSTPronoun, times: List[ActionHappenedAtTime] = None):
        super().__init__('sleep', done_by, ActionObjType.PHYSICAL, [], times=times)

    def __str__(self):
        return "%s sleep %s" % (self.done_by, self.get_times_str())

    def __repr__(self):
        return "%r sleep %r" % (self.done_by, self.get_times_str())
