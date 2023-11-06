from typing import List

from socialds.states.relation import Relation
from termcolor import colored
from socialds.other.utility import add_relation_to_relations_dict, colorize_relations_dict, TermColor


class RelationStorage:
    def __init__(self, name: str, is_private=True, relations=None):
        if relations is None:
            relations = {}
        self.name = name
        self.is_private = is_private
        self.relations = relations

    def add(self, relation: Relation):
        add_relation_to_relations_dict(relations=self.relations, relation=relation)

    def __repr__(self):
        return colored(text=self.name, on_color=TermColor.ON_RED.value)\
                + (colored(text='(public)', on_color=TermColor.ON_CYAN.value), colored(text='(private)', on_color=TermColor.ON_BLUE.value))[self.is_private] + '\n' \
                + colorize_relations_dict(relations=self.relations)


def merge_relation_storages(s1: RelationStorage, s2: RelationStorage):
    s1.relations.update(s2.relations)
