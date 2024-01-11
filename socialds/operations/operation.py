from typing import List

from socialds.DSTPronounHolder import DSTPronounHolder


class OperationFailed(Exception):
    pass


class Operation(DSTPronounHolder):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def execute(self, pronouns, *args, **kwargs):
        self.pronouns = pronouns
