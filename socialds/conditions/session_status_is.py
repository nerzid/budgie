from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.expectation import Expectation, ExpectationStatus
from socialds.session import Session, SessionStatus
from socialds.states.relation import Negation


class SessionStatusIs(Condition):
    def __init__(self, session: Session, session_status: SessionStatus, times: List[ActionHappenedAtTime] = None,
                 negation: Negation = Negation.FALSE):
        super().__init__(tense=Tense.PRESENT, times=times, negation=negation)
        self.session = session
        self.session_status = session_status

    def check(self, checker=None):
        return self.session.status == self.session_status
