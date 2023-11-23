from typing import List

from socialds.other.variables import dialogue_history
from socialds.action.action import Action
from socialds.agent import Agent
from socialds.action.action_time import ActionTime
from socialds.conditions.condition import Condition
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class AgentDoes(Condition):
    def __init__(self, agent: Agent, action: Action, tense: Tense, times: List[ActionTime] = None,
                 negation=False):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.action = action

    def check(self):
        if not self.negation:
            return dialogue_history.contains(Relation(left=self.agent,
                                                      r_type=RType.ACTION,
                                                      r_tense=self.tense,
                                                      right=self.action))
        else:
            return not dialogue_history.contains(Relation(left=self.agent,
                                                          r_type=RType.ACTION,
                                                          r_tense=self.tense,
                                                          right=self.action))

    def colorless_repr(self):
        return f"{self.agent} ({not self.negation})does({self.tense.value}) {self.action.colorless_repr()}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.agent} ({not self.negation})does({self.tense.value}) {self.action}{super().get_times_str()}"
