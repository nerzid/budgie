from typing import List
from functools import partial

from socialds.enums import SemanticEvent
from socialds.actions.action_obj import ActionObj, ActionObjType
from socialds.operations.stateoperation import StateOperation


class Action(ActionObj):
    def __init__(self, name, act_type:ActionObjType, op_seq: List[partial], preconditions=None, semantic_roles=None):
        super().__init__(name, act_type, op_seq)
        if preconditions is None:
            preconditions = []
        if semantic_roles is None:
            semantic_roles = {}
        self.name = name
        self.preconditions = preconditions
        self.semantic_roles = semantic_roles

    def update(self, key: SemanticEvent, value: any):
        self.semantic_roles[key] = value
        return self

# doctor can examine patient's eye using ophthalmoscope
# Role -can-> Action
# Doctor -can-> Action(name="eye examination", semantic_roles)
