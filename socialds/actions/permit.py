from functools import partial

from socialds.actions.action_obj import ActionObjType
from socialds.relationstorage import RelationStorage
from socialds.repositories.operation_repository import add_relation
from socialds.actions.action import Action
from socialds.states.relation import Relation


class Permit(Action):
    def __init__(self, relation: Relation, rs: RelationStorage):
        super().__init__(name='permit', act_type=ActionObjType.FUNCTIONAL,
                         op_seq=[partial(add_relation, relation, rs)])
        self.relation = relation
        self.rs = rs

    def colorless_repr(self):
        return f"{super().__repr__()}({self.relation.colorless_repr()})"

    def __repr__(self):
        return f"{super().__repr__()}({self.relation})"
