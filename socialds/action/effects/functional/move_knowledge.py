from typing import List

from socialds.action.effects.effect import Effect
from socialds.operations.move_relation import MoveRelation
from socialds.relationstorage import RelationStorage, RSType
from socialds.states.relation import Relation


class MoveInformation(Effect):

    def __init__(self, information: any, from_rs: RelationStorage, to_rs: RelationStorage, affected):
        self.information = information
        super().__init__(name='move-knowledge',
                         from_state=[],
                         to_state=[],
                         affected=affected,
                         op_seq=[MoveRelation(
                             relation=information,
                             from_rs=from_rs,
                             to_rs=to_rs
                         )])

    def get_requirement_holders(self) -> List:
        return super().get_requirement_holders() + [self.information]
