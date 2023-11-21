from typing import List

from socialds.action.action_time import ActionTime
from socialds.agent import Agent
from socialds.conditions.condition import Condition
from socialds.socialpractice.context.place import Place
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class AgentAtPlace(Condition):
    def __init__(self, agent: Agent, place: Place, tense: Tense, times: List[ActionTime] = None, negation=False):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.place = place

    def check(self):
        if self.negation:
            return Relation(left=self.agent,
                            r_type=RType.IS_AT,
                            r_tense=Tense.PRESENT,
                            right=self.place) in self.agent.places
        else:
            return Relation(left=self.agent,
                            r_type=RType.IS_AT,
                            r_tense=Tense.PRESENT,
                            right=self.place) not in self.agent.places

    def colorless_repr(self):
        return f"{self.agent} ({not self.negation})at({self.tense.value}) {self.place}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.agent} ({not self.negation})at({self.tense.value}) {self.place}{super().get_times_str()}"
