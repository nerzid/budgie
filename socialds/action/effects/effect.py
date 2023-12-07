from enum import Enum
from typing import List

from socialds.operations.operation import Operation


class EffectType(Enum):
    FUNCTIONAL = 'functional'
    SOCIAL = 'social'


class Effect:
    def __init__(self, name: str, etype: EffectType, op_seq: List[Operation]):
        self.name = name
        self.etype = etype
        self.op_seq = op_seq
