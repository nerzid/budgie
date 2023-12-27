from typing import List

from socialds.other.variables import dialogue_history
from socialds.action.action_time import ActionTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.states.property import Property
from socialds.states.relation import Relation, RType


class ActionOnPropertyHappens(Condition):
    def __init__(self, property: Property, action, tense: Tense, times: List[ActionTime] = None,
                 negation=False):
        super().__init__(tense, times, negation)
        self.property = property
        self.action = action

    def check(self):
        if not self.negation:
            return dialogue_history.contains(Relation(left=self.property,
                                                      rtype=RType.ACTION,
                                                      rtense=self.tense,
                                                      right=self.action))
        else:
            return not dialogue_history.contains(Relation(left=self.property,
                                                          rtype=RType.ACTION,
                                                          rtense=self.tense,
                                                          right=self.action))

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.ACTION][not self.negation][self.tense]
        return "%s %s happens on %s %s" % (self.action, tense_str, self.property, self.get_times_str())
