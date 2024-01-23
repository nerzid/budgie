from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.action_time import ActionHappenedAtTime
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation


class Share(Action):
    def __init__(self, information: Information, times: List[ActionHappenedAtTime] = None):
        self.recipient = DSTPronoun.YOU
        self.information = information
        super().__init__(name="share", done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL,
                         base_effects=[
                             GainKnowledge(knowledge=information, affected=self.recipient)
                         ],
                         recipient=self.recipient,
                         times=times)

    def __str__(self):
        return "%s share %s with %s" % (self.done_by, self.information, self.recipient)

    def __repr__(self):
        return "%r share %r with %r" % (self.done_by, self.information, self.recipient)

    def insert_pronouns(self):
        self.information.pronouns = self.pronouns
        self.information.insert_pronouns()
        super().insert_pronouns()

