from typing import List

from socialds.action.effects.effect import Effect
import socialds.conditions.agent_knows as an
from socialds.conditions.has_permit import HasPermit
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.relationstorage import RSType
from socialds.states.relation import Relation


class GainPermit(Effect):
    def __init__(self, permit: Relation, affected: any):
        self.permit = permit
        self.affected = affected
        op_seq = [
            AddRelationToRSHolder(relation=permit,
                                  rsholder=affected,
                                  rstype=RSType.PERMITS)
        ]
        super().__init__(name='gain-permit',
                         from_state=[],
                         to_state=[
                             HasPermit(agent=affected,
                                       permit=permit.right,
                                       negation=False)
                         ],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'{self.affected} gain permit {self.permit}'

    def get_requirement_holders(self) -> List:
        return [self.affected] + self.permit.right.get_requirement_holders()

    def insert_pronouns(self):
        super().insert_pronouns()
        self.permit.insert_pronouns()
