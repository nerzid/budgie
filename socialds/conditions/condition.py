from enum import Enum
from typing import List

from socialds.enums import Tense
from socialds.action.action_time import ActionTime
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation


# class ConditionType(Enum):
#     ACTION_IS_DONE = 'action-is-done'
#     AGENT_DID = 'agent-did'
#     AGENT_KNOWS = 'agent-knows'
#     AGENT_AT_PLACE = 'agent-at-place'


class Condition:
    def __init__(self, tense: Tense, times: List[ActionTime] = None, negation=False):
        if times is None:
            self.times = []
        else:
            self.times = times
        self.negation = negation
        self.tense = tense

    def get_times_str(self):
        if self.times is None:
            return ''
        times_str = ''
        for time in self.times:
            times_str += str(time) + ' AND '
        if len(self.times) > 0:
            times_str = ' ' + times_str[:-5]
        return times_str

    def check(self):
        pass

    def colorless_repr(self):
        return ""

    def __repr__(self):
        return ""

    def insert_pronouns(self):
        for time in self.times:
            time.insert_pronouns()

    @staticmethod
    def check_conditions(conditions):
        for condition in conditions:
            if condition.check() is False:
                return False
        return True
