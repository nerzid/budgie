from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.action_time import ActionHappenedAtTime
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.property import Property
from socialds.states.relation import Relation


class Prescribe(Action):

    def __init__(self, done_by: Agent | DSTPronoun, prescribed: List[Property], recipient: Agent | DSTPronoun,
                 negation: bool = False,
                 times=None):
        self.prescribed = prescribed
        self.negation = negation
        self.times = times
        super().__init__('prescribe', done_by, ActionObjType.PHYSICAL, [], times=times, recipient=recipient)

    def __str__(self):
        return "%s prescribe %s for %s %s" % (self.done_by, self.prescribed, self.recipient, self.get_times_str())

    def __repr__(self):
        return "%r prescribe %r for %r %r" % (self.done_by, self.prescribed, self.recipient, self.get_times_str())

    def get_requirement_holders(self) -> List:
        return self.prescribed

