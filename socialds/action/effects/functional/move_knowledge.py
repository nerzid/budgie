from socialds.action.effects.effect import Effect
from socialds.operations.move_relation import MoveRelation
from socialds.relationstorage import RelationStorage, RSType
from socialds.states.relation import Relation


class MoveKnowledge(Effect):
    def __init__(self, knowledge: Relation, from_rs: RelationStorage, to_rs: RelationStorage, affected):
        super().__init__(name='move-knowledge',
                         from_state=[],
                         to_state=[],
                         affected=affected,
                         op_seq=[MoveRelation(
                             relation=knowledge,
                             from_rs=from_rs,
                             to_rs=to_rs
                         )])
