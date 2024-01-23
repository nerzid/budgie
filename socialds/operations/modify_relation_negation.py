from __future__ import annotations

from socialds.operations.modify_relation import ModifyRelation
from socialds.operations.stateoperation import StateOperation
from socialds.states.relation import Relation


class ModifyRelationNegation(ModifyRelation):
    def __init__(self, relation: Relation | StateOperation, negation: bool | StateOperation):
        super().__init__('modify-relation-negation')
        self.relation = relation
        self.negation = negation

    def execute_param_state_operations(self):
        if isinstance(self.relation, StateOperation):
            self.relation = self.relation.execute(self.pronouns)
        elif isinstance(self.negation, StateOperation):
            self.negation = self.negation.execute(self.pronouns)

    def execute(self, agent, *args, **kwargs) -> Relation:
        super().execute(agent, *args, **kwargs)
        self.execute_param_state_operations()
        self.relation.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.relation.negation = self.negation
        return self.relation
