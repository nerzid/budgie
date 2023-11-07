from termcolor import colored

from socialds.enums import TermColor
from socialds.states.relation import Relation


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
