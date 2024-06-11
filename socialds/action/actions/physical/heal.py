from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.socialpractice.context.resource import Resource
from socialds.states.property import Property
from socialds.states.relation import Negation


class Heal(Action):
    def __init__(self, healed: Resource, done_by: any = None, negation: Negation = Negation.FALSE, times: List[ActionHappenedAtTime] = None):
        self.healed = healed
        self.negation = negation
        super().__init__('heal', done_by, ActionObjType.PHYSICAL, [], times=times)

    def __str__(self):
        if self.done_by is None:
            return "%s %s %s" % (self.healed, self.negation, self.get_times_str())
        else:
            return "%s %s %s %s" % (self.done_by, self.negation, self.healed, self.get_times_str())

    def __repr__(self):
        if self.done_by is None:
            negation_str = (f"is healed", f"isn't healed")[self.negation]
            return "%r %r %r" % (self.healed, negation_str, self.get_times_str())
        else:
            negation_str = (f"heals", f"doesn't heal")[self.negation]
            return "%r %r %r %r" % (self.done_by, negation_str, self.healed, self.get_times_str())
