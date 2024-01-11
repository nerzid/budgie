from __future__ import annotations

from socialds.operations.modify_relation import ModifyRelation
from socialds.operations.stateoperation import StateOperation
from socialds.states.relation import Relation


class ModifyRelationLeft(ModifyRelation):
    def __init__(self, relation: Relation | StateOperation, left: any | StateOperation):
        super().__init__('modify-relation-left')
        self.relation = relation
        self.left = left

    def execute_param_state_operations(self):
        if isinstance(self.relation, StateOperation):
            self.relation = self.relation.execute(self.pronouns)
        elif isinstance(self.left, StateOperation):
            self.left = self.left.execute(self.pronouns)

    def execute(self, pronouns, *args, **kwargs) -> Relation:
        super().execute(pronouns, *args, **kwargs)
        self.execute_param_state_operations()
        self.relation.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.relation.left = self.left
        return self.relation
