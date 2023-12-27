from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.property import Property


class Take(Action):
    def __init__(self, taken: Property, done_by: Agent | DSTPronoun, r_tense: Tense, giver: Agent = None,
                 negation: bool = False, times=None):
        self.giver = giver
        self.taken = taken
        self.r_tense = r_tense
        self.negation = negation
        self.times = times
        super().__init__('take', done_by, ActionObjType.PHYSICAL, [], times=times)

    def __str__(self):
        from_str = ("from %s" % self.giver, '')[self.giver is None]
        return "%s take %s %s %s" % (self.done_by.name, self.taken, from_str, self.get_times_str())

    def __repr__(self):
        from_str = ("from %r" % self.giver, '')[self.giver is None]
        return "%r take %r %r %r" % (self.done_by.name, self.taken, from_str, self.get_times_str())

    def insert_pronouns(self):
        if isinstance(self.giver, DSTPronoun):
            self.giver = pronouns[self.giver]
        super().insert_pronouns()

    def execute(self):
        # act = Relation(left=self.giver, r_type=RelationType.ACTION, right=self.taker r_tense=self.r_tense, negation=self.negation)
        self.insert_pronouns()
        super().execute()
