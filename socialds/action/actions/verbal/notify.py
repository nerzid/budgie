from __future__ import annotations

from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class Notify(Action):
    def __init__(self, done_by: Agent | DSTPronoun, notified_about: Relation | Action, recipient: Agent | DSTPronoun,
                 negation=False):
        self.done_by = done_by
        self.notified_about = notified_about
        self.notification = Relation(done_by, RType.ACTION, Tense.FUTURE, notified_about, negation)
        super().__init__('notify',done_by, ActionObjType.VERBAL,
                         base_effects=[
                             # this effect is incorrect for notify because there isnt any knowledge gain
                             # but it is an expectation that a certain action will happen
                             GainKnowledge(knowledge=self.notification, affected=recipient)
                         ])

    def colorless_repr(self):
        return f"{super().__repr__()}({self.done_by.name} notify {self.recipient} about {self.notified_about.colorless_repr()})"

    def __repr__(self):
        return f"{super().__repr__()}({self.done_by.name} notify {self.recipient} about {self.notified_about})"

    def insert_pronouns(self):
        self.notified_about.insert_pronouns()
        self.notification.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
# notifies other agent for an upcoming relation
# I will examine your eye now
# Joe -will do-> (Joe -examine-> Jane's eye)

# The maggot will turn into fly
# Maggot -will do-> (Maggot -turn into-> fly)
# or
# Maggot -will be-> (Maggot -is-> fly)
