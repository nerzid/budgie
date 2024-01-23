from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.socialpractice.context.resource import Resource
from socialds.states.relation import Relation, RType


class ActionOnResourceHappens(Condition):
    def __init__(self, resource: Resource, action, tense: Tense, times: List[ActionHappenedAtTime] = None,
                 negation=False):
        super().__init__(tense, times, negation)
        self.resource = resource
        self.action = action

    def check(self, checker=None):
        if not self.negation:
            return checker.dialogue_system.action_history.contains(Relation(left=checker,
                                                                            rtype=RType.ACTION,
                                                                            rtense=self.tense,
                                                                            right=Relation(left=self.resource,
                                                                                           rtype=RType.ACTION,
                                                                                           rtense=self.tense,
                                                                                           right=self.action)),
                                                                   pronouns=checker.pronouns)
        else:
            return not checker.dialogue_system.action_history.contains(Relation(left=checker,
                                                                                rtype=RType.ACTION,
                                                                                rtense=self.tense,
                                                                                right=Relation(left=self.resource,
                                                                                               rtype=RType.ACTION,
                                                                                               rtense=self.tense,
                                                                                               right=self.action)),
                                                                       pronouns=checker.pronouns)

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.ACTION][not self.negation][self.tense]
        return "%s %s happens on %s %s" % (self.action, tense_str, self.resource, self.get_times_str())
