from typing import List

from socialds.conditions.condition import Condition
from socialds.operations.operation import Operation


class Effect:
    def __init__(self, name: str, from_state: List[Condition], to_state: List[Condition], affected: any,
                 op_seq: List[Operation]):
        self.op_seq = op_seq
        self.name = name
        self.from_state = from_state
        self.to_state = to_state
        self.affected = affected

    def execute(self):
        for op in self.op_seq:
            op.execute()
