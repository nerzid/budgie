from socialds.action.action_obj import ActionObjType
from socialds.action.actions.verbal.affirm_or_deny import AffirmOrDeny
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Deny(AffirmOrDeny):
    def __init__(self, denied):
        self.denied = denied
        super().__init__('deny', DSTPronoun.I)

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.denied == other.denied

    def insert_pronouns(self):
        self.denied.pronouns = self.pronouns
        self.denied.insert_pronouns()
        super().insert_pronouns()
