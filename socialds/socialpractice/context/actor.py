# Contains data for the persona, e.g., angry teenager
from typing import List

from socialds.object import Object
from socialds.states.knowledge import Knowledge


class Actor (Object):
    def __init__(self, name, competences=None, knowledgebase=None):
        super().__init__(name)
        if competences is None:
            competences = []
        if knowledgebase is None:
            knowledgebase = []
        self.competences = competences
        self.knowledgebase = knowledgebase
        self.name = name
