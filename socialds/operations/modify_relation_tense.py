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

    def __str__(self):
        return "relation: {}, rtense: {}".format(self.relation, self.rtense)

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
            self.relation = self.relation.execute(self.agent)
        elif isinstance(self.rtense, StateOperation):
            self.rtense = self.rtense.execute(self.agent)

    def execute(self, agent, *args, **kwargs) -> Relation:
        super().execute(agent, *args, **kwargs)
        self.execute_param_state_operations()
        self.relation.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.relation.rel_tense = self.rtense
        return self.relation
