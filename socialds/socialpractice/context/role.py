# Contains data about the role of the agent, e.g., patient, doctor, husband, etc.

from socialds.object import Object
from socialds.relationstorage import RelationStorage


class Role(Object):
    def __init__(self, name, competences: RelationStorage):
        super().__init__(name)
        self.name = name
        self.competences = competences
