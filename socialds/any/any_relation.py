from socialds.any.any_agent import AnyAgent
from socialds.any.any_object import AnyObject
from socialds.enums import Tense
from socialds.states.relation import Relation, RType


class AnyRelation(Relation, AnyObject):
    def __init__(self):
        super().__init__(AnyAgent(), RType.ANY, Tense.ANY, AnyObject())

    def __repr__(self):
        return 'any-relation'

    def __eq__(self, other):
        if isinstance(other, Relation):
            return True
        return False
