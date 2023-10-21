from typing import List

from actions.action import Action
from definitions.definition import Definition


class TransitiveAction(Action):
    def __init__(self, name, senses: List[Definition], target):
        super().__init__(name, senses)
        self.target = target