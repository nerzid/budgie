
from socialds.action.effects.effect import Effect
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType


class AddExpectedEffectOptions(Effect):
    def __init__(self, effects, negation, affected: any):
        self.effects = effects
        self.negation = negation
        op_seq = [
            AddRelationToRSHolder(relation=Relation(left=affected, rel_type=RType.EFFECT, rel_tense=Tense.PRESENT,
                                                    right=effects, negation=negation), rsholder=affected, rstype=RSType.EXPECTED_EFFECTS)
        ]
        super().__init__(name='add-expected-effect-options',
                         from_state=[],
                         to_state=[],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'Adds the expected effects {self.effects} to {self.affected}'

    def insert_pronouns(self):
        super().insert_pronouns()
        for effect in self.effects:
            effect.pronouns = self.pronouns
            effect.insert_pronouns()
