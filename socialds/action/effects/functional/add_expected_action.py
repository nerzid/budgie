
from socialds.action.effects.effect import Effect
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType


class AddExpectedAction(Effect):
    def __init__(self, action, negation, affected: any):
        self.action = action
        self.negation = negation
        op_seq = [
            AddRelationToRSHolder(relation=Relation(
                left=affected,
                rtype=RType.ACTION,
                rtense=Tense.PRESENT,
                right=action,
                negation=negation
            ), rsholder=affected, rstype=RSType.EXPECTED_ACTIONS)
        ]
        super().__init__(name='add-expected-action',
                         from_state=[],
                         to_state=[],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'Expect the action {self.action} from {self.affected}'
