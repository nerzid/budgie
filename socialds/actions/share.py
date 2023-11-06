from typing import List

from socialds.actions.action import Action
from socialds.operations.stateoperation import StateOperation
from socialds.enums import SemanticEvent, SemanticState
from socialds.relationstorage import RelationStorage
from socialds.repositories.operation_repository import add_relation
from socialds.states.relation import Relation, RelationType, RelationTense


class Share(Action):
    def __init__(self, relation: Relation, rs: RelationStorage):
        super().__init__(name="share", op_seq=[add_relation(relation, rs)])
        self.relation = relation
        self.rs = rs

    def __repr__(self):
        return f"{self.name}({self.relation.__repr__()} to {self.rs.name})"
