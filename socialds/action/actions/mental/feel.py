from __future__ import annotations

from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.relation import Relation, RType
from socialds.states.property import Property
from socialds.enums import Tense


class Feel(Action):
    def __init__(self, done_by: Agent | DSTPronoun, felt: Property, about: Relation, r_tense: Tense,
                 negation: bool = False):
        self.done_by = done_by
        self.felt = felt
        self.about = about
        self.r_tense = r_tense
        self.negation = negation
        super().__init__('feel', done_by, ActionObjType.MENTAL, [])

    def __str__(self):
        return "%s feel %s about %r" % (self.done_by.name, self.felt, self.about)

    def __repr__(self):
        return "%r feel %r about %r" % (self.done_by.name, self.felt, self.about)

