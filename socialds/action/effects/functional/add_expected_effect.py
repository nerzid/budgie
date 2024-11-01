from __future__ import annotations

from socialds.action.effects.effect import Effect
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType, Negation


class AddExpectedEffect(Effect):
    def __init__(self, effect: Effect, affected: 'Agent' | DSTPronoun, negation:Negation=Negation.FALSE):
        self.effect = effect
        self.negation = negation
        op_seq = [
            AddRelationToRSHolder(relation=Relation(left=affected, rel_type=RType.EFFECT, rel_tense=Tense.PRESENT,
                                                    right=effect, negation=negation), rsholder=affected, rstype=RSType.EXPECTED_EFFECTS)
        ]
        super().__init__(name='add-expected-effect',
                         from_state=[],
                         to_state=[],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'Adds the expected effect {self.effect} to {self.affected}'

    @staticmethod
    def get_pretty_template():
        return "The expected effect [effect] will be added to [affected]"

    def insert_pronouns(self):
        super().insert_pronouns()
        self.effect.pronouns = self.pronouns
        self.effect.insert_pronouns()

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.effect.equals_with_pronouns(other.effect, pronouns)
