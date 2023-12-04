from __future__ import annotations

from socialds.enums import Tense
from socialds.operations.modify_relation import ModifyRelation
from socialds.operations.stateoperation import StateOperation
from socialds.states.relation import Relation


class ModifyRelationTense(ModifyRelation):
    def __init__(self, relation: Relation | StateOperation, rtense: Tense | StateOperation):
        super().__init__('modify-relation-tense')
        self.relation = relation
        self.rtense = rtense

    def execute_param_state_operations(self):
        if isinstance(self.relation, StateOperation):
            self.relation = self.relation.execute()
        elif isinstance(self.rtense, StateOperation):
            self.rtense = self.rtense.execute()

    def execute(self) -> Relation:
        super().execute()
        self.execute_param_state_operations()
        self.relation.insert_pronouns()
        self.relation.rtense = self.rtense
        return self.relation
