from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.expectation import Expectation, ExpectationStatus
from socialds.socialpractice.expectation.norm import Norm, NormStatus
from socialds.states.relation import Negation


class NormStatusIs(Condition):
    def __init__(self, norm: Norm, norm_status: NormStatus, times: List[ActionHappenedAtTime] = None,
                 negation: Negation = Negation.FALSE):
        super().__init__(tense=Tense.PRESENT, times=times, negation=negation)
        self.norm = norm
        self.norm_status = norm_status

    def check(self, checker=None):
        return self.norm.norm_status == self.norm_status
