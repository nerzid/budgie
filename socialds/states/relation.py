from enum import Enum

from socialds.object import Object
from socialds.states.state import State


class RelationType(Enum):
    IS = 'is'
    HAS = 'has'
    CAN = 'can'


# e.g., Eren likes apples -> left: Eren, name: likes, right: apples
class Relation(State):
    def __init__(self, left: Object, r_type: RelationType, right: any, negation=False):
        super().__init__()
        self.left = left
        self.r_type = r_type
        self.right = right
        self.negation = negation

    def __str__(self):
        negation_str = ''
        if self.negation:
            negation_str = '(not)'
        return str(self.left) + " ---" + str(self.r_type) + negation_str + "---> " + str(self.right)


