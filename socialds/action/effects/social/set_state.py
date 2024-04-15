from typing import List

from socialds.action.effects.effect import Effect
import socialds.conditions.agent_knows as an
from socialds.conditions.has_permit import HasPermit
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.relationstorage import RSType
from socialds.states.property import Property
from socialds.states.relation import Relation, Negation, RType


class SetState(Effect):
    def __init__(self, state: Property, affected, negation: Negation = Negation.FALSE):
        self.state = state
        self.negation = negation
        self.affected = affected

        op_seq = [
            AddRelationToRSHolder(relation=Relation(left=affected, rtype=RType.IS_IN, rtense=Tense.PRESENT,
                                                    right=state, negation=negation), rsholder=self.affected,
                                  rstype=RSType.STATES)
        ]
        super().__init__(name='set-state',
                         from_state=[],
                         to_state=[],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'{self.affected}\'s state is set to {self.state}'

    def get_requirement_holders(self) -> List:
        return [self.affected]

    def insert_pronouns(self):
        super().insert_pronouns()
