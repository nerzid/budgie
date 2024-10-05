# Contains data about the role of the agent, e.g., patient, doctor, husband, etc.

from socialds.object import Object
from socialds.relationstorage import RelationStorage


class Role(Object):
    def __init__(self, name, competences: RelationStorage):
        super().__init__(name)
        self.name = name
        self.competences = competences

    def to_dict(self):
        return {
            "name": self.name,
            "competences": [competence.to_dict_with_status() for competence in self.competences],
        }
