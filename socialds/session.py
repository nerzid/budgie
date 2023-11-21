from typing import List

from socialds.conditions.condition import Condition
from enum import Enum


class SessionStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class Session:
    def __init__(self, name: str,
                 start_conditions: List[Condition],
                 end_conditions: List[Condition],
                 status: SessionStatus = SessionStatus.NOT_STARTED):
        self.name = name
        self.start_conditions = start_conditions
        self.end_conditions = end_conditions
        self.status = status
