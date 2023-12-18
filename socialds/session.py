from typing import List

from socialds.conditions.condition import Condition
from enum import Enum

from socialds.expectation import Expectation
from socialds.goal import Goal


class SessionStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class Session:
    def __init__(self, name: str,
                 start_conditions: List[Condition],
                 end_goals: List[Goal],
                 expectations: List[Expectation] = None,
                 status: SessionStatus = SessionStatus.NOT_STARTED):
        if expectations is None:
            expectations = []
        self.name = name
        self.start_conditions = start_conditions
        self.expectations = expectations
        self.end_goals = end_goals
        self.status = status
