# Contains data for the persona, e.g., angry teenager
from typing import List

from socialds.relationstorage import RelationStorage
from socialds.object import Object
from socialds.states.knowledge import Knowledge


class Actor(Object):
    def __init__(self, name, knowledgebase: RelationStorage = RelationStorage('')):
        super().__init__(name)
        self.knowledgebase = knowledgebase
        self.name = name

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'type': self.__class__.__name__,
            'knowledgebase': self.knowledgebase.to_dict()
        }
