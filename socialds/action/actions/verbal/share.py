from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.action_time import ActionTime
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType
from socialds.states.relation import Relation


class Share(Action):
    def __init__(self, relation: Relation, times: List[ActionTime] = None):
        self.recipient = DSTPronoun.YOU
        self.relation = relation
        super().__init__(name="share", done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL,
                         base_effects=[
                             GainKnowledge(knowledge=relation, affected=self.recipient)
                         ],
                         recipient=self.recipient,
                         times=times)

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.done_by} share {self.relation.colorless_repr()} with {self.recipient.name}"

    def __repr__(self):
        return f"{super().__repr__()}{self.done_by} share {self.relation} with {self.recipient.name}"

    def insert_pronouns(self):
        self.relation.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
