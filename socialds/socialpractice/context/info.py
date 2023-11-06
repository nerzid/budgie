from socialds.object import Object
from socialds.states.relation import Relation, RelationType, RelationTense


class Info(Relation):
    def __init__(self, left: Object, r_type: RelationType, r_tense: RelationTense, right: any):
        super().__init__(left, r_type, r_tense, right)
