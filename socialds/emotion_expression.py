from socialds.emotion import Emotion
from socialds.states.relation import Relation


class EmotionExpression:
    def __init__(self, emotion: Emotion, felt_towards: Relation) -> None:
        self.emotion = emotion
        self.felt_towards = felt_towards

    def equals_with_pronouns(self, other, pronouns):
        return self.emotion == other.emotion and self.felt_towards.equals_with_pronouns(
            other.felt_towards, pronouns
        )
