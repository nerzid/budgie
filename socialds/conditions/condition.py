from enum import Enum
from typing import List

from socialds.enums import Tense
from socialds.action.action_time import ActionHappenedAtTime
from socialds.states.relation import Negation


# class ConditionType(Enum):
#     ACTION_IS_DONE = 'action-is-done'
#     AGENT_DID = 'agent-did'
#     AGENT_KNOWS = 'agent-knows'
#     AGENT_AT_PLACE = 'agent-at-place'


class Condition:
    def __init__(self, tense: Tense, times: List[ActionHappenedAtTime] = None, negation:Negation=Negation.FALSE):
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

    def check(self, checker=None):
        pass

    def insert_pronouns(self, pronouns):
        for time in self.times:
            time.insert_pronouns(pronouns)

    @staticmethod
    def check_conditions(conditions, checker):
        for condition in conditions:
            # print(condition)
            if condition.check(checker=checker) is False:
                return False
        return True
