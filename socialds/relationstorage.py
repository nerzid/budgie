from typing import List
from uu import Error

from socialds.states.relation import Relation, RelationTense, RelationType
from termcolor import colored
from socialds.other.utility import colorize_relations_dict
from socialds.enums import TermColor


class RelationStorage:
    # def __init__(self, name: str, is_private=True, relations=None):
    #     if relations is None:
    #         relations = {}
    #     self.name = name
    #     self.is_private = is_private
    #     self.relations = relations
    #
    def __init__(self, name: str, is_private=True, relations=None):
        if relations is None:
            relations = []
        self.name = name
        self.is_private = is_private
        self.relations = relations

    def __repr__(self):
        rs_info = colored(text=self.name, on_color=TermColor.ON_RED.value) \
                  + (colored(text='(public)', on_color=TermColor.ON_CYAN.value),
                     colored(text='(private)', on_color=TermColor.ON_BLUE.value))[self.is_private] + '\n'
        relations_str = ''
        for rel in self.relations:
            relations_str += str(rel) + '\n'
        return rs_info + relations_str

        # def __contains__(self, relation: Relation):

    #     try:
    #         return relation.right in self.relations[relation.left][relation.r_type][relation.negation][relation.r_tense]
    #     except KeyError:
    #         return False

    def __contains__(self, item):
        return item in self.relations

    def add(self, relation: Relation):
        self.relations.append(relation)

    # def add(self, relation: Relation):
    #     if relation.left in self.relations:
    #         if relation.r_type in self.relations[relation.left]:
    #             if relation.negation in self.relations[relation.left][relation.r_type]:
    #                 if relation.r_tense in self.relations[relation.left][relation.r_type][relation.negation]:
    #                     self.relations[relation.left][relation.r_type][relation.negation][relation.r_tense].append(
    #                         relation.right)
    #                 else:
    #                     self.relations[relation.left][relation.r_type][relation.negation][relation.r_tense] = {
    #                         relation.r_tense: [relation.right]}
    #             else:
    #                 self.relations[relation.left][relation.r_type] = {
    #                     relation.negation: {relation.r_tense: [relation.right]}}
    #         else:
    #             self.relations[relation.left] = {
    #                 relation.r_type: {relation.negation: {relation.r_tense: [relation.right]}}}
    #     else:
    #         self.relations[relation.left] = {relation.r_type: {relation.negation: {relation.r_tense: [relation.right]}}}

    def remove(self, relation: Relation):
        self.relations.remove(relation)
        
    def get(self, left:any, r_type: RelationType, r_tense: RelationTense, right: any, negation=False):
        for relation in self.relations:
            if relation.left == left and relation.r_type == r_type and relation.r_tense == r_tense and relation.right == right and relation.negation == negation:
                return relation
        raise Error


def merge_relation_storages(s1: RelationStorage, s2: RelationStorage):
    # s1.relations.update(s2.relations)
    s1.relations.union(s2.relations)
