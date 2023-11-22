from typing import List
from uu import Error

from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.action_time import ActionTime
from socialds.any.any_object import AnyObject
from socialds.states.relation import Relation, RType
from termcolor import colored
from socialds.other.utility import colorize_relations_dict
from socialds.enums import TermColor, Tense


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
        if len(self.relations) > 0:
            for rel in self.relations:
                relations_str += str(rel) + '\n'
        else:
            relations_str += colored(text='Empty', color=TermColor.BLACK.value,
                                     on_color=TermColor.ON_WHITE.value) + '\n'
        return rs_info + relations_str

        # def __contains__(self, relation: Relation):

    #     try:
    #         return relation.right in self.relations[relation.left][relation.r_type][relation.negation][relation.r_tense]
    #     except KeyError:
    #         return False

    # checks for the exact relation based on the reference of relation
    def __contains__(self, item):
        return item in self.relations

    # checks for the exact relation based on the values of the relation
    def contains(self, relation: Relation):
        try:
            rel_in_rs = self.get(relation.left, relation.r_type, relation.r_tense, relation.right, relation.negation)
            if rel_in_rs is not None:
                return True
            else:
                return False
        except Error:
            return False

    def add(self, relation: Relation):
        self.relations.append(relation)

    def add_multi(self, relations: [Relation]):
        for rel in relations:
            self.add(rel)

    def remove(self, relation: Relation):
        self.relations.remove(relation)

    def get(self, left: any, r_type: RType, r_tense: Tense, right: any, negation=False, times: [ActionTime] = None):
        # if times is not None:
        #     for time in times:
        #         if isinstance(time, NumOfTimes):
        #             time_num = time.num
        for relation in self.relations:
            if isinstance(left, AnyObject):
                if relation.r_type == r_type and relation.r_tense == r_tense and relation.right == right and relation.negation == negation:
                    return relation
            elif isinstance(right, AnyObject):
                if relation.left == left and relation.r_type == r_type and relation.r_tense == r_tense and relation.negation == negation:
                    return relation
            else:
                if relation.left == left and relation.r_type == r_type and relation.r_tense == r_tense and relation.right == right and relation.negation == negation:
                    return relation
        # print('time num: ' + str(time_num))
        # print('found rel: ' + str(found_rel))
        raise Error


def merge_relation_storages(s1: RelationStorage, s2: RelationStorage):
    # s1.relations.update(s2.relations)
    # s1.relations.union(s2.relations)
    s1.relations += s2.relations
