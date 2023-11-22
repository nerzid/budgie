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
        if not self.negation:
            return self.agent.places.contains(Relation(left=self.agent,
                                                       r_type=RType.IS_AT,
                                                       r_tense=Tense.PRESENT,
                                                       right=self.place))
        else:
            return not self.agent.places.contains(Relation(left=self.agent,
                                                           r_type=RType.IS_AT,
                                                           r_tense=Tense.PRESENT,
                                                           right=self.place))

    def colorless_repr(self):
        return f"{self.agent} ({not self.negation})at({self.tense.value}) {self.place}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.agent} ({not self.negation})at({self.tense.value}) {self.place}{super().get_times_str()}"
