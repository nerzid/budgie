from typing import List

from definitions.definition import Definition


class Action:
    def __init__(self, name, denotations: List[Definition]):
        self.name = name
        self.denotations = denotations