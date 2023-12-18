
from socialds.action.effects.effect import Effect
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType


class AddExpectedEffect(Effect):
    def __init__(self, effect: Effect, negation, affected: any):
        op_seq = [
            AddRelationToRSHolder(relation=Relation(
                left=affected,
                rtype=RType.EFFECT,
                rtense=Tense.PRESENT,
                right=effect,
                negation=negation
            ), rsholder=affected, rstype=RSType.EXPECTED_EFFECTS)
        ]
        super().__init__(name='add-expected-effect',
                         from_state=[],
                         to_state=[],
                         affected=affected,
                         op_seq=op_seq)
