from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.effects.effect import Effect
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.states.relation import Relation, RType


class Requirement(Relation):
    def __init__(self, required_for: Action | Effect, required: List[Condition]):
        super().__init__(required_for, RType.HAS_REQUIREMENTS, Tense.PRESENT, required)
        self.required_for = required_for
        self.required = required

    def check(self, checker):
        all_true = True
        for condition in self.required:
            all_true = all_true and condition.check(checker)
        return all_true
