from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.expectation import Expectation, ExpectationStatus


class ExpectationStatusIs(Condition):
    def __init__(self, expectation: Expectation, expectation_status: ExpectationStatus, times: List[ActionHappenedAtTime] = None,
                 negation=False):
        super().__init__(tense=Tense.PRESENT, times=times, negation=negation)
        self.expectation = expectation
        self.expectation_status = expectation_status

    def check(self, checker=None):
        return self.expectation.status == self.expectation_status

    def __repr__(self):
        return "Expectation status for the expectation %s is %s" % (self.expectation.name, self.expectation_status.value)
