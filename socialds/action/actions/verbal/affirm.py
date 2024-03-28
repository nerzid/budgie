from socialds.action.action_obj import ActionObjType
from socialds.action.actions.verbal.affirm_or_deny import AffirmOrDeny
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.other.dst_pronouns import DSTPronoun


class Affirm(AffirmOrDeny):
    def __init__(self, affirmed):
        self.affirmed = affirmed
        super().__init__('affirm', done_by=DSTPronoun.I, base_effects=[
            GainKnowledge(knowledge=affirmed, affected=DSTPronoun.YOU)
        ])

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.affirmed == other.affirmed

    def insert_pronouns(self):
        self.affirmed.pronouns = self.pronouns
        self.affirmed.insert_pronouns()
        super().insert_pronouns()
