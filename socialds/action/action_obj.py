from functools import partial
from typing import List

from socialds.operations.operation import Operation


class ActionObjType:
    VERBAL = 'verbal'
    PHYSICAL = 'physical'
    MENTAL = 'mental'
    FUNCTIONAL = 'functional'
    OPERATOR = 'op'

    def __repr__(self) -> str:
        return str(self.name).lower()


class ActionObj:
    def __init__(self, name: str, act_type: ActionObjType, op_seq: List[Operation]):
        self.name = name
        self.op_seq = op_seq
        self.act_type = act_type

    def insert_pronouns(self):
        pass

    def execute(self):
        for op in self.op_seq:
            op.execute()

    # def colorless_repr(self):
    #     return f'{self.act_type}:{self.name}'
    #
    # def __repr__(self):
    #     return f'{self.act_type}:{self.name}'

    # def colorless_repr(self):
    #     return f'{self.name}'
    #
    # def __repr__(self):
    #     return f'{self.name}'

    def colorless_repr(self):
        return f''

    def __repr__(self):
        return f''
