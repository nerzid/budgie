from typing import List

from socialds.actions.action import Action
from socialds.operations.stateoperation import StateOperation
from socialds.other.utility import SemanticEvent, SemanticState
from socialds.relationstorage import RelationStorage
from socialds.repositories.operation_repository import add_relation
from socialds.states.relation import Relation, RelationType, RelationTense


class Share(Action):
    def __init__(self, relation: Relation, rs: RelationStorage):
        super().__init__(name="share", op_seq=[add_relation(relation, rs)])
