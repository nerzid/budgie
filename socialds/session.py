from condition import Condition
from enum import Enum


class SessionStatus(Enum):
    NOT_STARTED = 'not_started'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Session:
    def __init__(self, name: str,
                 start_conditions: [Condition],
                 end_conditions: [Condition],
                 status: SessionStatus = SessionStatus.NOT_STARTED):
        self.name = name
        self.start_conditions = start_conditions
        self.end_conditions = end_conditions
        self.status = status
