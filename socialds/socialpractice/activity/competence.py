from socialds.action.action import Action
from socialds.object import Object
from socialds.enums import SemanticEvent, Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.state import State
from socialds.states.relation import Relation, RType


class Competence(Relation):
    # Role -can-> Action(semantic roles)
    def __init__(self, name: str, action: Action, negation = False):
        super().__init__(DSTPronoun.I, RType.CAN, Tense.PRESENT, action, negation)
        self.name = name
        self.action = action
