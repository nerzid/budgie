
from socialds.action.effects.effect import Effect
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType


class AddExpectedActionOptions(Effect):
    def __init__(self, actions, negation, affected: any):
        self.actions = actions
        self.negation = negation
        op_seq = [
            AddRelationToRSHolder(relation=Relation(left=affected, rel_type=RType.ACTION, rel_tense=Tense.PRESENT,
                                                    right=actions, negation=negation), rsholder=affected, rstype=RSType.EXPECTED_ACTIONS)
        ]
        super().__init__(name='add-expected-action-options',
                         from_state=[],
                         to_state=[],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'Expect the action {self.actions} from {self.affected}'

    def equals_with_pronouns(self, other, pronouns):
        if not isinstance(other, AddExpectedActionOptions):
            return False
        res = False
        for action in self.actions:
            for action2 in other.actions:
                res = res or action.equals_with_pronouns(action2, pronouns)
            if not res:
                return False
        return super().equals_with_pronouns(other, pronouns) and res
