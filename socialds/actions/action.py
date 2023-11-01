from typing import List

from socialds.actions.action_obj import ActionObj
from socialds.operations.stateoperation import StateOperation


class Action(ActionObj):
    def __init__(self, name, op_seq: List[StateOperation], preconditions=None):
        if preconditions is None:
            preconditions = []
        self.name = name
        self.op_seq = op_seq
        self.preconditions = preconditions

    def __repr__(self):
        return f'{self.name}'
