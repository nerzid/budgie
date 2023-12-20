from __future__ import annotations

from copy import copy

from socialds.enums import Tense
from socialds.operations.modify_relation import ModifyRelation
from socialds.operations.stateoperation import StateOperation
from socialds.states.relation import Relation


class ModifyRelationTense(ModifyRelation):
    def __init__(self, relation: Relation | StateOperation, rtense: Tense | StateOperation):
        super().__init__('modify-relation-tense')
        self.relation = relation
        self.rtense = rtense

    # def __eq__(self, other):
    #     if isinstance(other, ModifyRelationTense):
    #         copied_self = copy(self)
    #         copied_self.execute_param_state_operations()
    #         copied_self.relation.insert_pronouns()
    #         copied_self.relation.rtense = copied_self.rtense
    #         copied_other = copy(other)
    #         copied_other.execute_param_state_operations()
    #         copied_other.relation.insert_pronouns()
    #         copied_other.relation.rtense = copied_other.rtense
    #         return (copied_self.relation == copied_other.relation
    #                 and copied_self.rtense == copied_other.rtense)
    #     return False

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
