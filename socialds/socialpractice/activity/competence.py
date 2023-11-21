from socialds.object import Object
from socialds.enums import SemanticEvent
from socialds.actions.action import Action
from socialds.states.state import State
from socialds.states.relation import Relation, RType


class Competence(Relation):
    # Role -can-> Action(semantic roles)
    def __init__(self, name: str, left: Object, right: Action, negation):
        super().__init__(left, RType.CAN, right, negation)
        self.name = name
