from typing import List

from socialds.enums import Tense
from socialds.action.action_time import ActionTime
from socialds.agent import Agent
from socialds.conditions.condition import Condition
from socialds.states.relation import Relation


class AgentKnows(Condition):
    def __init__(self, agent: Agent, knows: Relation, tense: Tense, times: List[ActionTime] = None, negation=False):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.knows = knows

    def check(self):
        if not self.negation:
            return self.agent.knowledgebase.contains(self.knows)
        else:
            return not self.agent.knowledgebase.contains(self.knows)

    def colorless_repr(self):
        return f"{self.agent} ({not self.negation})knows({self.tense.value}) {self.knows.colorless_repr()}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.agent} ({not self.negation})knows({self.tense.value}) {self.knows}{super().get_times_str()}"
