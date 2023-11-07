from enum import Enum

from termcolor import colored

from socialds.enums import TermColor
from socialds.object import Object
from socialds.states.state import State


class RelationType(Enum):
    IS = 'is'
    HAS = 'has'
    KNOWS = 'knows'
    CAN = 'can'
    HAS_PERMIT = 'has_permit'
    ACTION = 'action'


class RelationTense(Enum):
    PRESENT = 'present'
    PAST = 'past'
    FUTURE = 'future'


# e.g., Eren likes apples -> left: Eren, name: likes, right: apples
class Relation(State):
    def __init__(self, left: any, r_type: RelationType, r_tense: RelationTense, right: any, negation=False):
        super().__init__()
        self.left = left
        self.r_type = r_type
        self.r_tense = r_tense
        self.right = right
        self.negation = negation

    # def __repr__(self):
    #     left_color = TermColor.LIGHT_BLUE.value
    #     r_type_color = TermColor.LIGHT_RED.value
    #     r_tense_color = TermColor.LIGHT_CYAN.value
    #     right_color = TermColor.LIGHT_GREEN.value
    #
    #     negation_str = ('', '(not)')[self.negation]
    #     return f'{colored(self.left, left_color)} ' \
    #            f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
    #            f'{colored(self.r_type.value, r_type_color)}' \
    #            f'{colored(negation_str, TermColor.RED.value)}' \
    #            f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
    #            f'{colored(self.r_tense.value, r_tense_color)}' \
    #            f'{colored("->", TermColor.LIGHT_YELLOW.value)} ' \
    #            f'{colored(self.right, right_color)}'

    def __repr__(self):
        negation_str = ('', '(not)')[self.negation]
        return str(self.left) + ' -' + self.r_type.value + negation_str + '-' + self.r_tense.value + '->' + str(self.right)


if __name__ == '__main__':
    print(Relation(left="Eren", r_type=RelationType.IS, r_tense=RelationTense.PRESENT, right="dirty"))
