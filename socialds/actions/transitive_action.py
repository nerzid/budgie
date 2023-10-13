from typing import List

from actions.action import Action
from definitions.definition import Definition


class TransitiveAction(Action):
    def __init__(self, name, denotations: List[Definition], target):
        super().__init__(name, denotations)
        self.target = target