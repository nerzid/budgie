from copy import copy
from enum import Enum
from typing import List

from termcolor import colored

from socialds.DSTPronounHolder import DSTPronounHolder
from socialds.action.action_time import ActionHappenedAtTime
from socialds.enums import TermColor, Tense
from socialds.other.dst_pronouns import DSTPronoun, pronounify
from socialds.states.state import State


class RType(Enum):
    IS = "is"
    HAS = "has"
    HAS_REQUIREMENTS = "has_requirements"
    CAN = "can"
    IS_PERMITTED_TO = "has_permit"
    ACTION = "action"
    EFFECT = "effect"
    IS_AT = "is_at"
    IS_IN = "is_in"
    SAYS = "says"
    FEELS = "feels"
    ANY = "any"


class Negation(Enum):
    TRUE = "true"
    FALSE = "false"
    ANY = "any"

    @classmethod
    def inverse(cls, negation):
        if negation == Negation.FALSE:
            return Negation.TRUE
        elif negation == Negation.TRUE:
            return Negation.FALSE
        else:
            return Negation.ANY

    # def __eq__(self, other):
    #     if not isinstance(other, Negation):
    #         return False
    #     return self.value == other.value or self.value == Negation.ANY or other.value == Negation.ANY


# e.g., Eren likes apples -> left: Eren, name: likes, right: apples


class Relation(State, DSTPronounHolder):
    relation_types_with_tenses = {
        RType.IS: {
            Negation.FALSE: {
                Tense.PAST: "was",
                Tense.PRESENT: "is",
                Tense.FUTURE: "will",
                Tense.ANY: "is-any",
            },
            Negation.TRUE: {
                Tense.PAST: "wasn't",
                Tense.PRESENT: "isn't",
                Tense.FUTURE: "won't",
                Tense.ANY: "isn't-any",
            },
            Negation.ANY: {
                Tense.PAST: "any-was",
                Tense.PRESENT: "any-is",
                Tense.FUTURE: "will",
                Tense.ANY: "is(any)-any",
            },
        },
        RType.HAS: {
            Negation.FALSE: {
                Tense.PAST: "had",
                Tense.PRESENT: "has",
                Tense.FUTURE: "will have",
                Tense.ANY: "has-any",
            },
            Negation.TRUE: {
                Tense.PAST: "hadn't",
                Tense.PRESENT: "hasn't",
                Tense.FUTURE: "won't have",
                Tense.ANY: "hasn't-any",
            },
            Negation.ANY: {
                Tense.PAST: "had-any",
                Tense.PRESENT: "has-any",
                Tense.FUTURE: "will have-any",
                Tense.ANY: "has(any)-any",
            },
        },
        RType.HAS_REQUIREMENTS: {
            Negation.FALSE: {
                Tense.PAST: "had requirements",
                Tense.PRESENT: "has requirements",
                Tense.FUTURE: "will have requirements",
                Tense.ANY: "has requirements-any",
            },
            Negation.TRUE: {
                Tense.PAST: "didn't have requirements",
                Tense.PRESENT: "doesn't have requirements",
                Tense.FUTURE: "won't have requirements",
                Tense.ANY: "doesn't have requirements-any",
            },
            Negation.ANY: {
                Tense.PAST: "had requirements-any",
                Tense.PRESENT: "has requirements-any",
                Tense.FUTURE: "will have requirements-any",
                Tense.ANY: "has requirements(any)-any",
            },
        },
        RType.CAN: {
            Negation.FALSE: {
                Tense.PAST: "could",
                Tense.PRESENT: "can",
                Tense.FUTURE: "will be able to",
                Tense.ANY: "can-any",
            },
            Negation.TRUE: {
                Tense.PAST: "couldn't",
                Tense.PRESENT: "can't",
                Tense.FUTURE: "won't be able to",
                Tense.ANY: "can't-any",
            },
            Negation.ANY: {
                Tense.PAST: "could-any",
                Tense.PRESENT: "can-any",
                Tense.FUTURE: "will be able to-any",
                Tense.ANY: "can(any)-any",
            },
        },
        RType.ACTION: {
            Negation.FALSE: {
                Tense.PAST: "did",
                Tense.PRESENT: "does",
                Tense.FUTURE: "will do",
                Tense.ANY: "does-any",
            },
            Negation.TRUE: {
                Tense.PAST: "didn't",
                Tense.PRESENT: "doesn't",
                Tense.FUTURE: "won't do",
                Tense.ANY: "doesn't-any",
            },
            Negation.ANY: {
                Tense.PAST: "did(any)",
                Tense.PRESENT: "does(any)",
                Tense.FUTURE: "will do(any)",
                Tense.ANY: "does(any)-any",
            },
        },
        RType.IS_PERMITTED_TO: {
            Negation.FALSE: {
                Tense.PAST: "was permitted to",
                Tense.PRESENT: "is permitted to",
                Tense.FUTURE: "will be permitted to",
                Tense.ANY: "is permitted to-any",
            },
            Negation.TRUE: {
                Tense.PAST: "wasn't permitted to",
                Tense.PRESENT: "isn't permitted to",
                Tense.FUTURE: "won't be permitted to",
                Tense.ANY: "isn't permitted to-any",
            },
            Negation.ANY: {
                Tense.PAST: "was permitted to(any)",
                Tense.PRESENT: "is permitted to(any)",
                Tense.FUTURE: "will be permitted to(any)",
                Tense.ANY: "is permitted to(any)-any",
            },
        },
        RType.IS_AT: {
            Negation.FALSE: {
                Tense.PAST: "was at",
                Tense.PRESENT: "is at",
                Tense.FUTURE: "will be at",
                Tense.ANY: "is at-any",
            },
            Negation.TRUE: {
                Tense.PAST: "wasn't at",
                Tense.PRESENT: "isn't at",
                Tense.FUTURE: "won't be at",
                Tense.ANY: "isn't at-any",
            },
            Negation.ANY: {
                Tense.PAST: "was at-any",
                Tense.PRESENT: "is at-any",
                Tense.FUTURE: "will be at-any",
                Tense.ANY: "is at(any)-any",
            },
        },
        RType.IS_IN: {
            Negation.FALSE: {
                Tense.PAST: "was in",
                Tense.PRESENT: "is in",
                Tense.FUTURE: "will be in",
                Tense.ANY: "is in-any",
            },
            Negation.TRUE: {
                Tense.PAST: "wasn't in",
                Tense.PRESENT: "isn't in",
                Tense.FUTURE: "won't be in",
                Tense.ANY: "isn't in-any",
            },
            Negation.ANY: {
                Tense.PAST: "was in-any",
                Tense.PRESENT: "is in-any",
                Tense.FUTURE: "will be in-any",
                Tense.ANY: "is in(any)-any",
            },
        },
        RType.FEELS: {
            Negation.FALSE: {
                Tense.PAST: "felt",
                Tense.PRESENT: "feels",
                Tense.FUTURE: "will feel",
                Tense.ANY: "feel-any",
            },
            Negation.TRUE: {
                Tense.PAST: "didn't feel",
                Tense.PRESENT: "doesn't feel",
                Tense.FUTURE: "won't feel",
                Tense.ANY: "doesn't feel-any",
            },
            Negation.ANY: {
                Tense.PAST: "felt-any",
                Tense.PRESENT: "feels-any",
                Tense.FUTURE: "will feel-any",
                Tense.ANY: "feels(any)-any",
            },
        },
        RType.EFFECT: {
            Negation.FALSE: {
                Tense.PAST: "did the effect",
                Tense.PRESENT: "does the effect",
                Tense.FUTURE: "will do the effect",
                Tense.ANY: "does the effect-any",
            },
            Negation.TRUE: {
                Tense.PAST: "didn't do the effect",
                Tense.PRESENT: "don't do the effect",
                Tense.FUTURE: "won't do the effect",
                Tense.ANY: "don't do the effect-any",
            },
            Negation.ANY: {
                Tense.PAST: "did the effect-any",
                Tense.PRESENT: "does the effect-any",
                Tense.FUTURE: "will do the effect-any",
                Tense.ANY: "does the effect(any)-any",
            },
        },
        RType.ANY: {
            Negation.FALSE: {
                Tense.PAST: "any(positive)(past)",
                Tense.PRESENT: "any(positive)(present)",
                Tense.FUTURE: "any(positive)(future)",
                Tense.ANY: "any(positive)-any",
            },
            Negation.TRUE: {
                Tense.PAST: "any(negative)(past)",
                Tense.PRESENT: "any(negative)(present)",
                Tense.FUTURE: "any(negative)(future)",
                Tense.ANY: "any(negative)-any",
            },
            Negation.ANY: {
                Tense.PAST: "any-(past)-any",
                Tense.PRESENT: "any-(present)-any",
                Tense.FUTURE: "any-(future)-any",
                Tense.ANY: "any-(any)-any",
            },
        },
        RType.SAYS: {
            Negation.FALSE: {
                Tense.PAST: "said",
                Tense.PRESENT: "says",
                Tense.FUTURE: "will say",
                Tense.ANY: "says-any",
            },
            Negation.TRUE: {
                Tense.PAST: "didn't say",
                Tense.PRESENT: "doesn't say",
                Tense.FUTURE: "won't say",
                Tense.ANY: "doesn't say-any",
            },
            Negation.ANY: {
                Tense.PAST: "said-any",
                Tense.PRESENT: "says-any",
                Tense.FUTURE: "will say-any",
                Tense.ANY: "says-any-any",
            },
        },
    }

    def __init__(
        self,
        left,
        rtype: RType,
        rtense: Tense,
        right,
        negation: Negation = Negation.FALSE,
        times: List[ActionHappenedAtTime] = None,
    ):
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
            return (
                self.left == other.left
                and (
                    self.rtype == other.rtype
                    or self.rtype == RType.ANY
                    or other.rtype == RType.ANY
                )
                and (
                    self.rtense == other.rtense
                    or self.rtense == Tense.ANY
                    or other.rtense == Tense.ANY
                )
                and self.negation == other.negation
                and self.times == other.times
            )
        return False

    def equals_with_pronouns(self, other, pronouns):
        relation_left = pronounify(other.left, pronouns)
        left = pronounify(self.left, pronouns)
        from socialds.action.action import Action
        from socialds.action.effects.effect import Effect

        if isinstance(relation_left, Action) or isinstance(relation_left, Effect):
            left_equality = relation_left.equals_with_pronouns(left, pronouns)
        else:
            left_equality = relation_left == left

        relation_right = pronounify(other.right, pronouns)
        right = pronounify(self.right, pronouns)
        if isinstance(relation_right, Action) or isinstance(relation_right, Effect):
            right_equality = relation_right.equals_with_pronouns(right, pronouns)
        else:
            right_equality = relation_right == right

        return (
            left_equality
            and (
                other.rtype == self.rtype
                or other.rtype == RType.ANY
                or self.rtype == RType.ANY
            )
            and (
                other.rtense == self.rtense
                or other.rtense == Tense.ANY
                or self.rtense == Tense.ANY
            )
            and right_equality
            and (
                other.negation == self.negation
                or self.negation == Negation.ANY
                or other.negation == Negation.ANY
            )
        )

    def __str__(self):
        return self.__repr__()
        # left_color = TermColor.LIGHT_BLUE.value
        # r_type_color = TermColor.LIGHT_RED.value
        # r_tense_color = TermColor.LIGHT_CYAN.value
        # right_color = TermColor.LIGHT_GREEN.value

        # return f'{colored(self.left, left_color)} ' \
        #        f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
        #        f'{colored(self.get_pretty_tense(), r_type_color)}' \
        #        f'{colored("->", TermColor.LIGHT_YELLOW.value)} ' \
        #        f'{colored(self.right, right_color)}{self.get_times_str()}'

    def __repr__(self):
        tense_str = self.get_pretty_tense()
        return "%r-%r->%r%r" % (self.left, tense_str, self.right, self.get_times_str())

    def get_pretty_tense(self):
        neg_str = self.negation
        # if self.negation == Negation.ANY:
        #     neg_str = Negation.FALSE
        return self.relation_types_with_tenses[self.rtype][neg_str][self.rtense]

    @staticmethod
    def get_pretty_template():
        return "[left][rtype][rtense][negation][right]"

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
            return ""
        times_str = ""
        for time in self.times:
            times_str += str(time) + " AND "
        if len(self.times) > 0:
            times_str = " " + times_str[:-5]
        return times_str


# def __repr__(self):
#     negation_str = ('', '(not)')[self.negation]
#     return str(self.left) + '-' + self.r_type.value + negation_str + '-' + self.r_tense.value + '->' + str(self.right)


if __name__ == "__main__":
    print(Relation(left="Eren", rtype=RType.IS, rtense=Tense.PRESENT, right="dirty"))
