from typing import List

from socialds.states.relation import Relation
from termcolor import colored
from socialds.other.utility import add_relation_to_relations_dict, colorize_relations_dict


class RelationStorage:
    def __init__(self, name:str, is_private=True, relations=None):
        if relations is None:
            relations = {}
        self.name = name
        self.is_private = is_private
        self.relations = relations

    def add(self, relation: Relation):
        add_relation_to_relations_dict(relations=self.relations, relation=relation)

    def __repr__(self):
        return colorize_relations_dict(relations=self.relations)
