from typing import List

from socialds.action.action_time import ActionTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.expectation import Expectation, ExpectationStatus


class ExpectationStatusIs(Condition):
    def __init__(self, expectation: Expectation, expectation_status: ExpectationStatus, times: List[ActionTime] = None,
                 negation=False):
        super().__init__(tense=Tense.PRESENT, times=times, negation=negation)
        self.expectation = expectation
        self.expectation_status = expectation_status

    def check(self):
        return self.expectation.status == self.expectation_status

    def colorless_repr(self):
        return f"Expectation status for the expectation {self.expectation.name} is {self.expectation_status.value}"

    def __repr__(self):
        return f"Expectation status for the expectation {self.expectation.name} is {self.expectation_status.value}"
