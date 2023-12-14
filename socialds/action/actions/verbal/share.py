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
        self.relation = relation
        self.shared_by = DSTPronoun.I
        self.shared_with = DSTPronoun.YOU
        super().__init__(name="share", act_type=ActionObjType.VERBAL,
                         effects=[
                             # partial(add_relation, relation, rs)
                             GainKnowledge(knowledge=relation, affected=self.shared_with)
                         ],
                         times=times)

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.relation.colorless_repr()} is shared with {self.shared_with.name}{super().get_times_str()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.relation} is shared with {self.shared_with.name}{super().get_times_str()}"

    def insert_pronouns(self):
        if isinstance(self.shared_by, DSTPronoun):
            self.shared_by = pronouns[self.shared_by]
        if isinstance(self.shared_with, DSTPronoun):
            self.shared_with = pronouns[self.shared_with]
        self.relation.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
