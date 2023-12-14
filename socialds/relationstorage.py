from enum import Enum
from typing import List
from uu import Error

from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.action_time import ActionTime
from socialds.any.any_object import AnyObject
from socialds.states.relation import Relation, RType
from termcolor import colored
from socialds.other.utility import colorize_relations_dict
from socialds.enums import TermColor, Tense


class RSType(Enum):
    PROPERTIES = 'Properties'
    KNOWLEDGEBASE = 'Knowledgebase'
    PLACES = 'Places'
    RESOURCES = 'Resources'
    COMPETENCES = 'Competences'
    FORGOTTEN = 'Forgotten'
    ANY = 'Any RS'


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
            rel_in_rs = self.get_one(relation.left, relation.rtype, relation.rtense, relation.right, relation.negation)
            if rel_in_rs is not None:
                return True
            else:
                return False
        except Error:
            return False

    def add(self, relation: Relation):
        self.relations.append(relation)
        return relation

    def add_multi(self, relations: [Relation]):
        for rel in relations:
            self.add(rel)

    def remove(self, relation: Relation):
        self.relations.remove(relation)

    def get_one(self, left: any, rtype: RType, rtense: Tense, right: any, negation=False, times: [ActionTime] = None):
        # if times is not None:
        #     for time in times:
        #         if isinstance(time, NumOfTimes):
        #             time_num = time.num

        for relation in self.relations:
            if isinstance(left, AnyObject):
                if relation.rtype == rtype and relation.rtense == rtense and relation.right == right and relation.negation == negation:
                    return relation
            elif isinstance(right, AnyObject):
                if relation.left == left and relation.rtype == rtype and relation.rtense == rtense and relation.negation == negation:
                    return relation
            else:
                if relation.left == left and relation.rtype == rtype and relation.rtense == rtense and relation.right == right and relation.negation == negation:
                    return relation
        raise Error

    def get_many(self, left: any, rtype: RType, rtense: Tense, right: any, negation=False, times: [ActionTime] = None):
        # if times is not None:
        #     for time in times:
        #         if isinstance(time, NumOfTimes):
        #             time_num = time.num
        found = []
        for relation in self.relations:
            if isinstance(left, AnyObject):
                if relation.rtype == rtype and relation.rtense == rtense and relation.right == right and relation.negation == negation:
                    found.append(relation)
            elif isinstance(right, AnyObject):
                if relation.left == left and relation.rtype == rtype and relation.rtense == rtense and relation.negation == negation:
                    found.append(relation)
            else:
                if relation.left == left and relation.rtype == rtype and relation.rtense == rtense and relation.right == right and relation.negation == negation:
                    found.append(relation)
        # print('time num: ' + str(time_num))
        # print('found rel: ' + str(found_rel))
        if len(found) <= 0:
            raise Error
        else:
            return found


def merge_relation_storages(s1: RelationStorage, s2: RelationStorage):
    # s1.relations.update(s2.relations)
    # s1.relations.union(s2.relations)
    s1.relations += s2.relations