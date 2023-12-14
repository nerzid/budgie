from functools import partial
from typing import List

from socialds.action.action_obj import ActionObj, ActionObjType
from socialds.action.effects.effect import Effect


class ActionOperator(ActionObj):
    def __init__(self, name, op_seq: List[Effect]):
        super().__init__(name, ActionObjType.OPERATOR, op_seq)
        self.name = name
