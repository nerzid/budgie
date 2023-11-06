from enum import Enum

from termcolor import colored

from socialds.states.relation import Relation


class TermColor(Enum):
    LIGHT_BLUE = 'light_blue'
    LIGHT_YELLOW = 'light_yellow'
    LIGHT_RED = 'light_red'
    LIGHT_GREEN = 'light_green'
    LIGHT_CYAN = 'light_cyan'
    RED = 'red'
    ON_RED = 'on_red'
    ON_CYAN = 'on_cyan'
    ON_BLUE = 'on_blue'


class SemanticEvent(Enum):
    AGENT = 'agent'
    PARTNER = 'partner'
    CAUSE = 'cause'
    INSTRUMENT = 'instrument'
    PATIENT = 'patient'
    THEME = 'theme'
    BENEFICIARY = 'beneficiary'
    GOAL = 'goal'
    SOURCE = 'source'
    RESULT = 'result'
    REASON = 'reason'
    PURPOSE = 'purpose'
    MANNER = 'manner'
    MEDIUM = 'medium'
    MEANS = 'means'
    TIME = 'time'
    INITIAL_TIME = 'initial time'
    FINAL_TIME = 'final time'
    DURATION = 'duration'
    SETTING = 'setting'
    LOCATION = 'location'
    INITIAL_LOCATION = 'initial location'
    FINAL_LOCATION = 'final location'
    DISTANCE = 'distance'
    PATH = 'path'
    FREQUENCY = 'frequency'
    AMOUNT = 'amount'


class SemanticState(Enum):
    ATTRIBUTE = 'attribute'
    PIVOT = 'PIVOT'
    INSTRUMENT = 'instrument'
    SETTING = 'setting'
    THEME = 'theme'
    BENEFICIARY = 'beneficiary'
    REASON = 'reason'
    TIME = 'time'
    INITIAL_TIME = 'initial time'
    FINAL_TIME = 'final time'
    DURATION = 'duration'
    MANNER = 'manner'
    LOCATION = 'location'
    INITIAL_LOCATION = 'initial location'
    FINAL_LOCATION = 'final location'
    DISTANCE = 'distance'
    AMOUNT = 'amount'


def add_relation_to_relations_dict(relations: dict, relation: Relation):
    if relation.left in relations:
        if relation.r_type in relations[relation.left]:
            if relation.negation in relations[relation.left][relation.r_type]:
                if relation.r_tense in relations[relation.left][relation.r_type][relation.negation]:
                    relations[relation.left][relation.r_type][relation.negation][relation.r_tense].append(relation.right)
                else:
                    relations[relation.left][relation.r_type][relation.negation][relation.r_tense] = {relation.r_tense: [relation.right]}
            else:
                relations[relation.left][relation.r_type] = {relation.negation: {relation.r_tense: [relation.right]}}
        else:
            relations[relation.left] = {relation.r_type: {relation.negation: {relation.r_tense: [relation.right]}}}
    else:
        relations[relation.left] = {relation.r_type: {relation.negation: {relation.r_tense: [relation.right]}}}


def colorize_relations_dict(relations: dict, left_color=TermColor.LIGHT_BLUE,
                            r_type_color=TermColor.LIGHT_RED,
                            r_tense_color=TermColor.LIGHT_CYAN,
                            right_color=TermColor.LIGHT_GREEN):
    pretty_str = ""
    for left in relations.keys():
        for r_type in relations[left]:
            for negation in relations[left][r_type]:
                for r_tense in relations[left][r_type][negation]:
                    negation_str = ('', '(not)')[negation]
                    pretty_str += f'{colored(left, left_color.value)} ' \
                                  f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
                                  f'{colored(r_type.value, r_type_color.value)}' \
                                  f'{colored(negation_str, TermColor.RED.value)}' \
                                  f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
                                  f'{colored(r_tense.value, r_tense_color.value)}' \
                                  f'{colored("->", TermColor.LIGHT_YELLOW.value)} ' \
                                  f'{colored(relations[left][r_type][negation][r_tense], right_color.value)}\n'
    return pretty_str
