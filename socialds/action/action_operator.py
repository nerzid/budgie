from functools import partial
from typing import List

from socialds.action.action_obj import ActionObj, ActionObjType
from socialds.action.effects.effect import Effect


class ActionOperator(ActionObj):
    def __init__(self, name, base_effects: List[Effect], extra_effects: List[Effect]):
        super().__init__(name, ActionObjType.OPERATOR, base_effects, extra_effects)
        self.name = name
