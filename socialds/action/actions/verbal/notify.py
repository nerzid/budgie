from __future__ import annotations

from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.other.dst_pronouns import DSTPronoun
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation, RType, Negation
from socialds.enums import Tense


class Notify(Action):
    def __init__(self, done_by: Agent | DSTPronoun, notified_about: Relation | Action, recipient: Agent | DSTPronoun,
                 negation: Negation = Negation.FALSE):
        self.done_by = done_by
        self.notified_about = notified_about
        self.notification = Information(done_by, RType.ACTION, Tense.FUTURE, notified_about, negation)
        super().__init__('notify', done_by, ActionObjType.VERBAL,
                         base_effects=[
                             # this effect is incorrect for notify because there isnt any knowledge gain
                             # but it is an expectation that a certain action will happen
                             GainKnowledge(knowledge=self.notification, affected=recipient)
                         ])

    def __str__(self):
        return "%s notify %s about %s" % (self.done_by.name, self.recipient, self.notified_about)

    def __repr__(self):
        return "%r notify %r about %r" % (self.done_by.name, self.recipient, self.notified_about)

    def insert_pronouns(self):
        self.notified_about.pronouns = self.pronouns
        self.notification.pronouns = self.pronouns
        self.notified_about.insert_pronouns()
        self.notification.insert_pronouns()
        super().insert_pronouns()

# notifies other agent for an upcoming relation
# I will examine your eye now
# Joe -will do-> (Joe -examine-> Jane's eye)

# The maggot will turn into fly
# Maggot -will do-> (Maggot -turn into-> fly)
# or
# Maggot -will be-> (Maggot -is-> fly)
