from __future__ import annotations

from typing import List

from socialds.action.effects.effect import Effect
import socialds.conditions.agent_knows as an
from socialds.emotion import Emotion
from socialds.emotion_expression import EmotionExpression
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.socialpractice.context.information import Information
from socialds.states.property import Property
from socialds.states.relation import Negation, RType, Relation


class FeelEmotion(Effect):

    def __init__(
        self,
        emotion: Emotion,
        felt_towards: Relation | Property,
        affected: "Agent" | DSTPronoun,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
    ):
        self.emotion = emotion
        self.felt_towards = felt_towards
        self.affected = affected
        self.tense = tense
        self.negation = negation
        self.relation = Relation(
            left=affected,
            rtype=RType.FEELS,
            rtense=tense,
            negation=negation,
            right=EmotionExpression(emotion=emotion, felt_towards=felt_towards),
        )
        op_seq = [
            AddRelationToRSHolder(
                relation=self.relation, rsholder=affected, rstype=RSType.FEELINGS
            )
        ]
        super().__init__(
            name="feel-emotion",
            from_state=[],
            to_state=[],
            affected=affected,
            op_seq=op_seq,
        )

    def __repr__(self):
        return f"{self.affected} feel {self.emotion} for {self.felt_towards}"

    @staticmethod
    def get_pretty_template():
        return "[affected] feel TBD"

    def equals_with_pronouns(self, other, pronouns):
        if not isinstance(other, FeelEmotion):
            return False
        if isinstance(self.felt_towards, Relation):
            return super().equals_with_pronouns(
                other, pronouns
            ) and self.felt_towards.equals_with_pronouns(other.felt_towards, pronouns)
        else:
            return super().equals_with_pronouns(other, pronouns)

    def insert_pronouns(self):
        super().insert_pronouns()
        if isinstance(self.felt_towards, Relation):
            self.felt_towards.pronouns = self.pronouns
            self.felt_towards.insert_pronouns()

    def get_requirement_holders(self) -> List:
        return super().get_requirement_holders() + [self.felt_towards]
