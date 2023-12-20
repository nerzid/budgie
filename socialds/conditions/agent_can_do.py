from __future__ import annotations

from typing import List

from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.any.any_agent import AnyAgent
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.other.variables import dialogue_history
import socialds.agent as a
from socialds.action.action_time import ActionTime
from socialds.conditions.condition import Condition
from socialds.relationstorage import RelationNotFoundError, RSType
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class AgentCanDo(Condition):
    def __init__(self, agent: a.Agent | DSTPronoun, action, tense: Tense, times: List[ActionTime] = None,
                 negation=False):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.action = action

    def check(self):
        rel = Relation(left=self.action.done_by, rtype=RType.ACTION, rtense=Tense.PAST, right=self.action)
        agent = self.agent
        if isinstance(self.agent, DSTPronoun):
            agent = pronouns[self.agent]
        if self.negation:
            return rel not in agent.relation_storages[RSType.COMPETENCES]
        else:
            return rel in agent.relation_storages[RSType.COMPETENCES]

    def colorless_repr(self):
        return f"{self.agent} {Relation.relation_types_with_tenses[RType.CAN][not self.negation][self.tense]} {self.action.colorless_repr()}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.agent} {Relation.relation_types_with_tenses[RType.CAN][not self.negation][self.tense]} {self.action}{super().get_times_str()}"

    def insert_pronouns(self):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
        self.action.insert_pronouns()
        super().insert_pronouns()