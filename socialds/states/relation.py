from enum import Enum

from termcolor import colored

from socialds.action.action_time import ActionTime
import socialds.action.action as a
from socialds.enums import TermColor, Tense
from socialds.object import Object
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.state import State


class RType(Enum):
    IS = 'is'
    HAS = 'has'
    CAN = 'can'
    IS_PERMITTED_TO = 'has_permit'
    ACTION = 'action'
    EFFECT = 'effect'
    IS_AT = 'is_at'
    ANY = 'any'


# e.g., Eren likes apples -> left: Eren, name: likes, right: apples


class Relation(State):
    relation_types_with_tenses = {
        RType.IS: {
            True: {
                Tense.PAST: 'was',
                Tense.PRESENT: 'is',
                Tense.FUTURE: 'will'
            },
            False: {
                Tense.PAST: 'wasn\'t',
                Tense.PRESENT: 'isn\'t',
                Tense.FUTURE: 'won\'t'
            }
        },
        RType.HAS: {
            True: {
                Tense.PAST: 'had',
                Tense.PRESENT: 'has',
                Tense.FUTURE: 'will have'
            },
            False: {
                Tense.PAST: 'hadn\'t',
                Tense.PRESENT: 'hasn\'t',
                Tense.FUTURE: 'won\'t have'
            }
        },
        RType.CAN: {
            True: {
                Tense.PAST: 'could',
                Tense.PRESENT: 'can',
                Tense.FUTURE: 'will be able to'
            },
            False: {
                Tense.PAST: 'couldn\'t',
                Tense.PRESENT: 'can\'t',
                Tense.FUTURE: 'won\'t be able to'
            }
        },
        RType.ACTION: {
            True: {
                Tense.PAST: 'did',
                Tense.PRESENT: 'does',
                Tense.FUTURE: 'will do'
            },
            False: {
                Tense.PAST: 'didn\'t',
                Tense.PRESENT: 'doesn\'t',
                Tense.FUTURE: 'won\'t do'
            }
        },
        RType.IS_PERMITTED_TO: {
            True: {
                Tense.PAST: 'was permitted to',
                Tense.PRESENT: 'is permitted to',
                Tense.FUTURE: 'will be permitted to'
            },
            False: {
                Tense.PAST: 'wasn\'t permitted to',
                Tense.PRESENT: 'isn\'t permitted to',
                Tense.FUTURE: 'won\'t be permitted to'
            }
        },
        RType.IS_AT: {
            True: {
                Tense.PAST: 'was at',
                Tense.PRESENT: 'is at',
                Tense.FUTURE: 'will be at'
            },
            False: {
                Tense.PAST: 'wasn\'t at',
                Tense.PRESENT: 'isn\'t at',
                Tense.FUTURE: 'won\'t be at'
            }
        },
        RType.EFFECT: {
            True: {
                Tense.PAST: 'did the effect',
                Tense.PRESENT: 'does the effect',
                Tense.FUTURE: 'will do the effect'
            },
            False: {
                Tense.PAST: 'didn\'t do the effect',
                Tense.PRESENT: 'don\'t do the effect',
                Tense.FUTURE: 'won\'t do the effect'
            }
        },
        RType.ANY: {
            True: {
                Tense.ANY: ''
            },
            False: {
                Tense.ANY: ''
            }
        }
    }

    def __init__(self, left: any, rtype: RType, rtense: Tense, right: any, negation=False,
                 times: [ActionTime] = None):
        super().__init__()
        self.left = left
        self.rtype = rtype
        self.rtense = rtense
        self.right = right
        self.negation = negation
        self.times = times

    def colorless_repr(self):
        if (isinstance(self.right, a.Action) or isinstance(self.right, Relation)) and \
                (isinstance(self.left, a.Action) or isinstance(self.right, Relation)):
            return f'{self.left.colorless_repr()}-{self.relation_types_with_tenses[self.rtype][not self.negation][self.rtense]}->{self.right.colorless_repr()}{self.get_times_str()}'
        elif isinstance(self.right, a.Action) or isinstance(self.right, Relation):
            return f'{self.left}-{self.relation_types_with_tenses[self.rtype][not self.negation][self.rtense]}->{self.right.colorless_repr()}{self.get_times_str()}'
        elif isinstance(self.left, a.Action) or isinstance(self.left, Relation):
            return f'{self.left.colorless_repr()}-{self.relation_types_with_tenses[self.rtype][not self.negation][self.rtense]}->{self.right}{self.get_times_str()}'
        else:
            return f'{self.left}-{self.relation_types_with_tenses[self.rtype][not self.negation][self.rtense]}->{self.right}{self.get_times_str()}'

    def __repr__(self):
        left_color = TermColor.LIGHT_BLUE.value
        r_type_color = TermColor.LIGHT_RED.value
        r_tense_color = TermColor.LIGHT_CYAN.value
        right_color = TermColor.LIGHT_GREEN.value

        return f'{colored(self.left, left_color)} ' \
               f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
               f'{colored(self.relation_types_with_tenses[self.rtype][not self.negation][self.rtense], r_type_color)}' \
               f'{colored("->", TermColor.LIGHT_YELLOW.value)} ' \
               f'{colored(self.right, right_color)}{self.get_times_str()}'

    def insert_pronouns(self, ):
        if isinstance(self.left, Relation):
            self.left.insert_pronouns()
        elif isinstance(self.left, DSTPronoun):
            self.left = pronouns[self.left]
        elif isinstance(self.right, Relation):
            self.right.insert_pronouns()
        elif isinstance(self.right, DSTPronoun):
            self.right = pronouns[self.right]

    def get_times_str(self):
        if self.times is None:
            return ''
        times_str = ''
        for time in self.times:
            times_str += str(time) + ' AND '
        if len(self.times) > 0:
            times_str = ' ' + times_str[:-5]
        return times_str


# def __repr__(self):
#     negation_str = ('', '(not)')[self.negation]
#     return str(self.left) + '-' + self.r_type.value + negation_str + '-' + self.r_tense.value + '->' + str(self.right)


if __name__ == '__main__':
    print(Relation(left="Eren", rtype=RType.IS, rtense=Tense.PRESENT, right="dirty"))
