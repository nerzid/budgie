from enum import Enum
from typing import List, Dict
from uu import Error

from termcolor import colored

from socialds.action.action_time import ActionHappenedAtTime
from socialds.any.any_object import AnyObject
from socialds.enums import TermColor, Tense
from socialds.states.relation import Relation, RType


class RSType(Enum):
    PERMITS = 'Permits'
    REQUIREMENTS = 'Requirements'
    PROPERTIES = 'Properties'
    KNOWLEDGEBASE = 'Knowledgebase'
    PLACES = 'Places'
    RESOURCES = 'Resources'
    COMPETENCES = 'Competences'
    FORGOTTEN = 'Forgotten'
    ACTIVE_ACTIONS = 'Active Actions'
    EXPECTED_ACTIONS = 'Expected Actions'
    EXPECTED_EFFECTS = 'Expected Effects'
    VALUES = 'Values'
    ANY = 'Any RS'


class RelationNotFoundError(Exception):
    pass


class RSIterator:
    def __init__(self, rs):
        self.rs = rs
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            relation = self.rs[self.idx]
        except IndexError:
            raise StopIteration()
        self.idx += 1
        return relation


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
        return (rs_info + relations_str)[:-1]

        # def __contains__(self, relation: Relation):

    #     try:
    #         return relation.right in self.relations[relation.left][relation.r_type][relation.negation][relation.r_tense]
    #     except KeyError:
    #         return False

    def __eq__(self, other):
        if isinstance(other, RelationStorage):
            if len(self.relations) != len(other.relations) or self.name != other.name:
                return False
            for i in range(len(self.relations)):
                if self.relations[i] != other.relations[i]:
                    return False
            return True
        return False

    # checks for the exact relation based on the reference of relation
    def __contains__(self, item):
        # return item in self.relations
        return self.contains(item)

    def __iter__(self):
        return RSIterator(self.relations)

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

    def contains_unique(self, relation: Relation, excluded: List[Relation]):
        pass

    def add(self, relation: Relation):
        self.relations.append(relation)
        return relation

    def add_multi(self, relations: [Relation]):
        for rel in relations:
            self.add(rel)

    def add_from_rs(self, rs):
        self.relations += rs.relations

    def remove(self, relation: Relation):
        self.relations.remove(relation)

    def get_one(self, left: any, rtype: RType, rtense: Tense, right: any, negation=False,
                times: List[ActionHappenedAtTime] = None, excluded: List[Relation] = None):
        # if times is not None:
        #     for time in times:
        #         if isinstance(time, NumOfTimes):
        #             time_num = time.num
        # print(self.relations)
        found = False
        for relation in self.relations:

            # if isinstance(left, AnyObject):
            #     if relation.rtype == rtype and relation.rtense == rtense and relation.right == right and relation.negation == negation:
            #         found = True
            # elif isinstance(right, AnyObject):
            #     if relation.left == left and relation.rtype == rtype and relation.rtense == rtense and relation.negation == negation:
            #         found = True
            # else:
            #     if relation.left == left and relation.rtype == rtype and relation.rtense == rtense and relation.right == right and relation.negation == negation:
            #         found = True
            if relation.left == left and (relation.rtype == rtype or relation.rtype == RType.ANY or rtype == RType.ANY) \
                    and (relation.rtense == rtense or relation.rtense == Tense.ANY or rtense == Tense.ANY) \
                    and relation.right == right and relation.negation == negation:
                found = True
            if found:
                if excluded is None or len(excluded) == 0:
                    return relation
                else:
                    if relation in excluded:
                        found = False
                        continue
            # print("{} {} {} {} {}".format(relation.left == left, (relation.rtype == rtype or relation.rtype == RType.ANY or rtype == RType.ANY) \
            #         , (relation.rtense == rtense or relation.rtense == Tense.ANY or rtense == Tense.ANY) \
            #         , relation.right == right , relation.negation == negation))
        if not found:
            return None

    def get_many(self, left: any, rtype: RType, rtense: Tense, right: any, negation=False, times: [ActionHappenedAtTime] = None):
        # if times is not None:
        #     for time in times:
        #         if isinstance(time, NumOfTimes):
        #             time_num = time.num
        found = []
        for relation in self.relations:
            #     if isinstance(left, AnyObject):
            #         if relation.rtype == rtype and relation.rtense == rtense and relation.right == right and relation.negation == negation:
            #             found.append(relation)
            #     elif isinstance(right, AnyObject):
            #         if relation.left == left and relation.rtype == rtype and relation.rtense == rtense and relation.negation == negation:
            #             found.append(relation)
            #     else:
            #         if relation.left == left and relation.rtype == rtype and relation.rtense == rtense and relation.right == right and relation.negation == negation:
            #             found.append(relation)
            if relation.left == left and (relation.rtype == rtype or rtype == RType.ANY) and \
                    (relation.rtense == rtense or rtense == Tense.ANY) and relation.right == right \
                    and relation.negation == negation:
                found.append(relation)
        # print('time num: ' + str(time_num))
        # print('found rel: ' + str(found_rel))
        if len(found) <= 0:
            raise Error
        else:
            return found


@DeprecationWarning
def merge_relation_storages(s1: RelationStorage, s2: RelationStorage):
    """
    Instead use self.add_from_rs()
    @param s1:
    @param s2:
    """
    # s1.relations.update(s2.relations)
    # s1.relations.union(s2.relations)
    s1.relations += s2.relations
