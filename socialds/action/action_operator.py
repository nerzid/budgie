from functools import partial
from typing import List

from socialds.action.action_obj import ActionObj, ActionObjType
from socialds.operations.operation import Operation


class ActionOperator(ActionObj):
    def __init__(self, name, op_seq: List[Operation]):
        super().__init__(name, ActionObjType.OPERATOR, op_seq)
        self.name = name
