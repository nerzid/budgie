from typing import List

from socialds.managers.managers import dialogue_history
from socialds.action.action import Action
from socialds.action.action_time import ActionTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.states.property import Property
from socialds.states.relation import Relation, RType


class ActionOnPropertyHappens(Condition):
    def __init__(self, property: Property, action: Action, tense: Tense, times: List[ActionTime] = None,
                 negation=False):
        super().__init__(tense, times, negation)
        self.property = property
        self.action = action

    def check(self):
        if not self.negation:
            return dialogue_history.contains(Relation(left=self.property,
                                                      r_type=RType.ACTION,
                                                      r_tense=self.tense,
                                                      right=self.action))
        else:
            return not dialogue_history.contains(Relation(left=self.property,
                                                          r_type=RType.ACTION,
                                                          r_tense=self.tense,
                                                          right=self.action))

    def colorless_repr(self):
        return f"{self.action} ({not self.negation})happens{self.tense.value} on {self.property}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.action} ({not self.negation})happens{self.tense.value} on {self.property}{super().get_times_str()}"
