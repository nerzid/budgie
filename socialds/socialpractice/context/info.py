from socialds.object import Object
from socialds.states.relation import Relation, RType, RelationTense


class Info(Relation):
    def __init__(self, left: Object, rtype: RType, rtense: RelationTense, right: any):
        super().__init__(left, rtype, rtense, right)
