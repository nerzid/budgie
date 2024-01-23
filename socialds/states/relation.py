from copy import copy
from enum import Enum
from typing import List

from termcolor import colored

from socialds.DSTPronounHolder import DSTPronounHolder
from socialds.action.action_time import ActionHappenedAtTime
from socialds.enums import TermColor, Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.state import State


class RType(Enum):
    IS = 'is'
    HAS = 'has'
    HAS_REQUIREMENTS = 'has_requirements'
    CAN = 'can'
    IS_PERMITTED_TO = 'has_permit'
    ACTION = 'action'
    EFFECT = 'effect'
    IS_AT = 'is_at'
    SAYS = 'says'
    ANY = 'any'

# e.g., Eren likes apples -> left: Eren, name: likes, right: apples


class Relation(State, DSTPronounHolder):
    relation_types_with_tenses = {
        RType.IS: {
            True: {
                Tense.PAST: 'was',
                Tense.PRESENT: 'is',
                Tense.FUTURE: 'will',
                Tense.ANY: 'is'
            },
            False: {
                Tense.PAST: 'wasn\'t',
                Tense.PRESENT: 'isn\'t',
                Tense.FUTURE: 'won\'t',
                Tense.ANY: 'isn\'t'
            }
        },
        RType.HAS: {
            True: {
                Tense.PAST: 'had',
                Tense.PRESENT: 'has',
                Tense.FUTURE: 'will have',
                Tense.ANY: 'has'
            },
            False: {
                Tense.PAST: 'hadn\'t',
                Tense.PRESENT: 'hasn\'t',
                Tense.FUTURE: 'won\'t have',
                Tense.ANY: 'hasn\'t'
            }
        },
        RType.HAS_REQUIREMENTS: {
            True: {
                Tense.PAST: 'had requirements',
                Tense.PRESENT: 'has requirements',
                Tense.FUTURE: 'will have requirements',
                Tense.ANY: 'has requirements'
            },
            False: {
                Tense.PAST: 'didn\'t have requirements',
                Tense.PRESENT: 'doesn\'t have requirements',
                Tense.FUTURE: 'won\'t have requirements',
                Tense.ANY: 'doesn\'t requirements'
            }
        },
        RType.CAN: {
            True: {
                Tense.PAST: 'could',
                Tense.PRESENT: 'can',
                Tense.FUTURE: 'will be able to',
                Tense.ANY: 'can'
            },
            False: {
                Tense.PAST: 'couldn\'t',
                Tense.PRESENT: 'can\'t',
                Tense.FUTURE: 'won\'t be able to',
                Tense.ANY: 'can\'t'
            }
        },
        RType.ACTION: {
            True: {
                Tense.PAST: 'did',
                Tense.PRESENT: 'does',
                Tense.FUTURE: 'will do',
                Tense.ANY: 'does'
            },
            False: {
                Tense.PAST: 'didn\'t',
                Tense.PRESENT: 'doesn\'t',
                Tense.FUTURE: 'won\'t do',
                Tense.ANY: 'doesn\'t'
            }
        },
        RType.IS_PERMITTED_TO: {
            True: {
                Tense.PAST: 'was permitted to',
                Tense.PRESENT: 'is permitted to',
                Tense.FUTURE: 'will be permitted to',
                Tense.ANY: 'is permitted to'
            },
            False: {
                Tense.PAST: 'wasn\'t permitted to',
                Tense.PRESENT: 'isn\'t permitted to',
                Tense.FUTURE: 'won\'t be permitted to',
                Tense.ANY: 'isn\'t permitted to'
            }
        },
        RType.IS_AT: {
            True: {
                Tense.PAST: 'was at',
                Tense.PRESENT: 'is at',
                Tense.FUTURE: 'will be at',
                Tense.ANY: 'is at'
            },
            False: {
                Tense.PAST: 'wasn\'t at',
                Tense.PRESENT: 'isn\'t at',
                Tense.FUTURE: 'won\'t be at',
                Tense.ANY: 'isn\'t at'
            }
        },
        RType.EFFECT: {
            True: {
                Tense.PAST: 'did the effect',
                Tense.PRESENT: 'does the effect',
                Tense.FUTURE: 'will do the effect',
                Tense.ANY: 'does the effect'
            },
            False: {
                Tense.PAST: 'didn\'t do the effect',
                Tense.PRESENT: 'don\'t do the effect',
                Tense.FUTURE: 'won\'t do the effect',
                Tense.ANY: 'don\'t do the effect'
            }
        },
        RType.ANY: {
            True: {
                Tense.PAST: 'was',
                Tense.PRESENT: 'is',
                Tense.FUTURE: 'will',
                Tense.ANY: 'is'
            },
            False: {
                Tense.PAST: 'wasn\'t',
                Tense.PRESENT: 'isn\'t',
                Tense.FUTURE: 'won\'t',
                Tense.ANY: 'isn\'t'
            }
        },
        RType.SAYS: {
            True: {
                Tense.PAST: 'said',
                Tense.PRESENT: 'says',
                Tense.FUTURE: 'will say',
                Tense.ANY: 'says'
            },
            False: {
                Tense.PAST: 'didn\'t say',
                Tense.PRESENT: 'doesn\'t say',
                Tense.FUTURE: 'won\'t say',
                Tense.ANY: 'doesn\'t say'
            }
        }
    }

    def __init__(self, left: any, rtype: RType, rtense: Tense, right: any, negation=False,
                 times: List[ActionHappenedAtTime] = None):
        super().__init__()
        self.left = left
        self.rtype = rtype
        self.rtense = rtense
        self.right = right
        self.negation = negation
        self.times = times

    # def __eq__(self, other):
    #     if isinstance(other, Relation):
    #         copied_self = copy(self)
    #         copied_other = copy(other)
    #         copied_self.insert_pronouns()
    #         copied_other.insert_pronouns()
    #         return (copied_self.left == )
    #
    #     return False

    def __eq__(self, other):
        if isinstance(other, Relation):
            return (self.left == other.left and
                    (self.rtype == other.rtype or self.rtype == RType.ANY or other.rtype == RType.ANY) and
                    (self.rtense == other.rtense or self.rtense == Tense.ANY or other.rtense == Tense.ANY) and
                    self.negation == other.negation and
                    self.times == other.times)
        return False

    def __str__(self):
        left_color = TermColor.LIGHT_BLUE.value
        r_type_color = TermColor.LIGHT_RED.value
        r_tense_color = TermColor.LIGHT_CYAN.value
        right_color = TermColor.LIGHT_GREEN.value

        return f'{colored(self.left, left_color)} ' \
               f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
               f'{colored(self.relation_types_with_tenses[self.rtype][not self.negation][self.rtense], r_type_color)}' \
               f'{colored("->", TermColor.LIGHT_YELLOW.value)} ' \
               f'{colored(self.right, right_color)}{self.get_times_str()}'

    def __repr__(self):
        tense_str = self.relation_types_with_tenses[self.rtype][not self.negation][self.rtense]
        return "%r-%r->%r%r" % (self.left, tense_str, self.right, self.get_times_str())

    def insert_pronouns(self):
        if isinstance(self.left, Relation):
            self.left.pronouns = self.pronouns
            self.left.insert_pronouns()
        elif isinstance(self.left, DSTPronoun):
            self.left = self.pronouns[self.left]
        elif isinstance(self.right, Relation):
            self.right.pronouns = self.pronouns
            self.right.insert_pronouns()
        elif isinstance(self.right, DSTPronoun):
            self.right = self.pronouns[self.right]

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
