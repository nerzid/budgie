from enum import Enum

from termcolor import colored

from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation


class TermColor(Enum):
    LIGHT_BLUE = 'light_blue'
    LIGHT_YELLOW = 'light_yellow'
    LIGHT_RED = 'light_red'
    LIGHT_GREEN = 'light_green'


class SemanticRole(Enum):
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


def add_relation_to_relations_dict(relations: dict, relation: Relation):
    if relation.left in relations:
        if relation.r_type in relations[relation.left]:
            relations[relation.left][relation.r_type].append(relation.right)
        else:
            relations[relation.left] = {relation.r_type: [relation.right]}
    else:
        relations[relation.left] = {relation.r_type: [relation.right]}


def colorize_relations_dict(relations: dict, left_color=TermColor.LIGHT_BLUE, r_type_color=TermColor.LIGHT_RED,
                            right_color=TermColor.LIGHT_GREEN):
    pretty_str = ""
    for left in relations.keys():
        for r_type in relations[left]:
            pretty_str += f'{colored(left, left_color.value)} ' \
                          f'{colored("-", TermColor.LIGHT_YELLOW.value)}' \
                          f'{colored(r_type.value, r_type_color.value)}' \
                          f'{colored("->", TermColor.LIGHT_YELLOW.value)} ' \
                          f'{colored(relations[left][r_type], right_color.value)}\n'
    return pretty_str


def merge_relation_storages(s1: RelationStorage, s2: RelationStorage):
    s1.relations.update(s2.relations)
