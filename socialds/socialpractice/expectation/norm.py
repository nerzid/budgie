from typing import List

from socialds.action.action_obj import ActionObj
from socialds.action.effects.effect import Effect
from socialds.conditions.condition import Condition
from socialds.expectation import Expectation, ExpectationType, ExpectationStatus


class Norm(Expectation):
    def __init__(self, name: str, action_seq: List[ActionObj],
                 base_effects: List[Effect] = None,
                 start_conditions: List[Condition] = None,
                 end_conditions: List[Condition] = None):
        if start_conditions is None:
            start_conditions = []
        if end_conditions is None:
            end_conditions = []
        if base_effects is None:
            base_effects = []
        super().__init__(name, ExpectationType.NORM, ExpectationStatus.NOT_STARTED, base_effects, action_seq)
        self.start_conditions = start_conditions
        self.end_conditions = end_conditions

    def __repr__(self):
        text = 'Norm: ' + self.name + '\n'

        text += 'Actions:\n'
        i = 0
        for action in self.action_seq:
            text += f'{str(i)}-) {action}\n'
            i += 1

        text += 'Effects \n'
        for effect in self.base_effects:
            text += f'{effect}\n'
        return text


