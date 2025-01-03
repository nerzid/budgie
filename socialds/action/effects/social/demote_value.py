from __future__ import annotations

from socialds.action.effects.effect import Effect
from socialds.enums import Tense
from socialds.operations.find_one_relation_in_rsholder import FindOneRelationInRSHolder
from socialds.operations.modify_relation_right import ModifyRelationRight
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.states.any_state import AnyState
from socialds.states.value import Value


class DemoteValue(Effect):
    def __init__(self, affected: 'Agent' | DSTPronoun, value: Value, amount: float = 1):
        self.value = value
        self.amount = amount
        super().__init__('promote-value', [], [], affected, [
            ModifyRelationRight(
                FindOneRelationInRSHolder(rsholder=affected,
                                          left=value,
                                          rstype=RSType.VALUES,
                                          rtense=Tense.PRESENT,
                                          right=AnyState()
                                          ), right=amount)
        ])

    def __repr__(self):
        return f'{self.affected}\'s {self.value} value is demoted by amount {self.amount}'

    @staticmethod
    def get_pretty_template():
        return "The value [value] in [affected] is demoted"
