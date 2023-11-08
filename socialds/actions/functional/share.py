from typing import List
from functools import partial

from socialds.actions.action import Action
from socialds.actions.action_obj import ActionObjType
from socialds.operations.stateoperation import StateOperation
from socialds.enums import SemanticEvent, SemanticState
from socialds.relationstorage import RelationStorage
from socialds.repositories.operation_repository import add_relation
from socialds.states.relation import Relation, RelationType, RelationTense


class Share(Action):
    def __init__(self, relation: Relation, rs: RelationStorage):
        super().__init__(name="share", act_type=ActionObjType.FUNCTIONAL, op_seq=[partial(add_relation, relation, rs)])
        self.relation = relation
        self.rs = rs

    def colorless_repr(self):
        return f"{super().__repr__()}({self.relation.colorless_repr()} with {self.rs.name})"

    def __repr__(self):
        return f"{super().__repr__()}({self.relation} with {self.rs.name})"


if __name__ == '__main__':
    a = Share(
        Relation(left="Eren",
                 r_type=RelationType.IS,
                 r_tense=RelationTense.PRESENT,
                 right='dirty')
        , RelationStorage(name='test kb'))
    print(a)
