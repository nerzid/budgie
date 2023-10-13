from typing import List

from actions.action import Action
from definitions.definition import Definition


class IntransitiveAction(Action):
    def __init__(self, name, denotations: List[Definition]):
        super().__init__(name, denotations)