from enum import Enum
from typing import List

from socialds.action.action_obj import ActionObj
from socialds.action.effects.effect import Effect


class ExpectationType(Enum):
    NORM = 'norm'
    STRATEGY = 'strategy'


class ExpectationStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class Expectation:
    def __init__(self, name: str, etype: ExpectationType, status: ExpectationStatus, base_effects: List[Effect],
                 action_seq: List[ActionObj]):
        self.name = name
        self.etype = etype
        self.status = status
        self.base_effects = base_effects
        self.action_seq = action_seq
