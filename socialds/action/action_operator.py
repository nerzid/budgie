from functools import partial
from typing import List

from socialds.action.action_obj import ActionObj, ActionObjType


class ActionOperator(ActionObj):
    def __init__(self, name, op_seq: List[partial]):
        super().__init__(name, ActionObjType.OPERATOR, op_seq)
        self.name = name
