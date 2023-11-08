from functools import partial

from socialds.actions.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.relationstorage import RelationStorage
from socialds.repositories.operation_repository import add_relation, create_then_add_relation
from socialds.actions.action import Action
from socialds.states.relation import Relation, RelationTense, RelationType


class Permit(Action):
    def __init__(self, permitter:Agent, permitted:Relation, r_tense:RelationTense, negation:bool, rs: RelationStorage):
        self.relation = Relation(permitter, RelationType.HAS_PERMIT, r_tense, permitted, negation)
        self.rs = rs
        super().__init__(name='permit', act_type=ActionObjType.FUNCTIONAL,
                         op_seq=[partial(add_relation, self.relation, rs)])

    def colorless_repr(self):
        return f"{super().__repr__()}({self.relation.colorless_repr()})"

    def __repr__(self):
        return f"{super().__repr__()}({self.relation})"
