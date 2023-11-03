from socialds.object import Object
from socialds.other.utility import SemanticRole
from socialds.actions.action import Action
from socialds.states.state import State
from socialds.states.relation import Relation, RelationType


class Competence(Relation):
    # Role -can-> Action(semantic roles)
    def __init__(self, name: str, left: Object, right: Action, negation):
        super().__init__(left, RelationType.CAN, right, negation)
        self.name = name
