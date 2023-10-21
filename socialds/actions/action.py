from typing import List
from socialds.senses.sense import Sense


class Action:
    def __init__(self, name, senses: List[Sense]):
        self.name = name
        self.senses = senses
