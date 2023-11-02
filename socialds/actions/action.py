from typing import List

from socialds.actions.action_obj import ActionObj
from socialds.operations.stateoperation import StateOperation


class Action(ActionObj):
    def __init__(self, name, op_seq: List[StateOperation], preconditions=None, semantic_roles=None):
        if preconditions is None:
            preconditions = []
        if semantic_roles is None:
            semantic_roles = {}
        self.name = name
        self.op_seq = op_seq
        self.preconditions = preconditions
        self.semantic_roles = semantic_roles

    def __repr__(self):
        return f'{self.name}'


# doctor can examine patient's eye using ophthalmoscope
# Role -can-> Action
# Doctor -can-> Action(name="eye examination", semantic_roles)