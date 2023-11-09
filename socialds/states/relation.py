from enum import Enum

from termcolor import colored

from socialds.actions.action import Action
from socialds.enums import TermColor
from socialds.object import Object
from socialds.states.state import State


class RelationType(Enum):
    IS = 'is'
    HAS = 'has'
    CAN = 'can'
    IS_PERMITTED_TO = 'has_permit'
    ACTION = 'action'
    IS_AT = 'is_at'


class RelationTense(Enum):
    PRESENT = 'present'
    PAST = 'past'
    FUTURE = 'future'


# e.g., Eren likes apples -> left: Eren, name: likes, right: apples


class Relation(State):
    relation_types_with_tenses = {
        RelationType.IS: {
            True: {
                RelationTense.PAST: 'was',
                RelationTense.PRESENT: 'is',
                RelationTense.FUTURE: 'will'
            },
            False: {
                RelationTense.PAST: 'wasn\'t',
                RelationTense.PRESENT: 'isn\'t',
                RelationTense.FUTURE: 'won\'t'
            }
        },
        RelationType.HAS: {
            True: {
                RelationTense.PAST: 'had',
                RelationTense.PRESENT: 'has',
                RelationTense.FUTURE: 'will have'
            },
            False: {
                RelationTense.PAST: 'hadn\'t',
                RelationTense.PRESENT: 'hasn\'t',
                RelationTense.FUTURE: 'won\'t have'
            }
        },
        RelationType.CAN: {
            True: {
                RelationTense.PAST: 'could',
                RelationTense.PRESENT: 'can',
                RelationTense.FUTURE: 'will be able to'
            },
            False: {
                RelationTense.PAST: 'couldn\'t',
                RelationTense.PRESENT: 'can\'t',
                RelationTense.FUTURE: 'won\'t be able to'
            }
        },
        RelationType.ACTION: {
            True: {
                RelationTense.PAST: 'did',
                RelationTense.PRESENT: 'does',
                RelationTense.FUTURE: 'will do'
            },
            False: {
                RelationTense.PAST: 'didn\'t',
                RelationTense.PRESENT: 'doesn\'t',
                RelationTense.FUTURE: 'won\'t do'
            }
        },
        RelationType.IS_PERMITTED_TO: {
            True: {
                RelationTense.PAST: 'was permitted to',
                RelationTense.PRESENT: 'is permitted to',
                RelationTense.FUTURE: 'will be permitted to'
            },
            False: {
                RelationTense.PAST: 'wasn\'t permitted to',
                RelationTense.PRESENT: 'isn\'t permitted to',
                RelationTense.FUTURE: 'won\'t be permitted to'
            }
        },
        RelationType.IS_AT: {
            True: {
                RelationTense.PAST: 'was at',
                RelationTense.PRESENT: 'is at',
                RelationTense.FUTURE: 'will be at'
            },
            False: {
                RelationTense.PAST: 'wasn\'t at',
                RelationTense.PRESENT: 'isn\'t at',
                RelationTense.FUTURE: 'won\'t be at'
            }
        }
    }

    def __init__(self, left: any, r_type: RelationType, r_tense: RelationTense, right: any, negation=False):
        super().__init__()
        self.left = left
        self.r_type = r_type
        self.r_tense = r_tense
        self.right = right
        self.negation = negation

    def colorless_repr(self):
        negation_str = ('', '(not)')[self.negation]
        if isinstance(self.right, Action):
            return f'{self.left}-{self.relation_types_with_tenses[self.r_type][not self.negation][self.r_tense]}->{self.right.colorless_repr()}'
        else:
            return f'{self.left}-{self.relation_types_with_tenses[self.r_type][not self.negation][self.r_tense]}->{self.right}'

    def __repr__(self):
        left_color = TermColor.LIGHT_BLUE.value
        r_type_color = TermColor.LIGHT_RED.value
        r_tense_color = TermColor.LIGHT_CYAN.value
        right_color = TermColor.LIGHT_GREEN.value

        return f'{colored(self.left, left_color)} ' \
               f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
               f'{colored(self.relation_types_with_tenses[self.r_type][not self.negation][self.r_tense], r_type_color)}' \
               f'{colored("->", TermColor.LIGHT_YELLOW.value)} ' \
               f'{colored(self.right, right_color)}'


# def __repr__(self):
#     negation_str = ('', '(not)')[self.negation]
#     return str(self.left) + '-' + self.r_type.value + negation_str + '-' + self.r_tense.value + '->' + str(self.right)


if __name__ == '__main__':
    print(Relation(left="Eren", r_type=RelationType.IS, r_tense=RelationTense.PRESENT, right="dirty"))
