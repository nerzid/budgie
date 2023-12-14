from __future__ import annotations

from socialds.operations.modify_relation import ModifyRelation
from socialds.operations.stateoperation import StateOperation
from socialds.states.relation import Relation


class ModifyRelationRight(ModifyRelation):
    def __init__(self, relation: Relation | StateOperation, right: any | StateOperation):
        super().__init__('modify-relation-right')
        self.relation = relation
        self.right = right

    def execute_param_state_operations(self):
        if isinstance(self.relation, StateOperation):
            self.relation = self.relation.execute()
        elif isinstance(self.right, StateOperation):
            self.right = self.right.execute()

    def execute(self) -> Relation:
        super().execute()
        self.execute_param_state_operations()
        self.relation.insert_pronouns()
        self.relation.right = self.right
        return self.relation