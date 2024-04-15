from __future__ import annotations

import copy
from typing import List

from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.any.any_agent import AnyAgent
from socialds.other.dst_pronouns import DSTPronoun
import socialds.agent as a
from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.relationstorage import RelationNotFoundError, RSType
from socialds.states.relation import Relation, RType, Negation
from socialds.enums import Tense


class AgentCanDo(Condition):
    def __init__(self, agent: a.Agent | DSTPronoun, action, tense: Tense, times: List[ActionHappenedAtTime] = None,
                 negation: Negation = Negation.FALSE):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.action = action

    def check(self, checker=None):
        if isinstance(self.agent, DSTPronoun):
            agent = checker.pronouns[self.agent]
        else:
            agent = self.agent

        copied_action = copy.deepcopy(self.action)
        copied_action.pronouns = checker.pronouns
        copied_action.insert_pronouns()

        rel = Relation(left=copied_action.done_by, rtype=RType.ACTION, rtense=Tense.PAST, right=copied_action)

        if self.negation == Negation.TRUE:
            return not agent.relation_storages[RSType.COMPETENCES].contains(rel, checker.pronouns)
        elif self.negation == Negation.FALSE or self.negation == Negation.ANY:
            return agent.relation_storages[RSType.COMPETENCES].contains(rel, checker.pronouns)

    def __str__(self):
        tense_str = Relation.relation_types_with_tenses[RType.CAN][self.negation][self.tense]
        return "%s %s %s %s" % (self.agent, tense_str, self.action, self.get_times_str())

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.CAN][self.negation][self.tense]
        return "%r %s %r %s" % (self.agent, tense_str, self.action, self.get_times_str())

    def insert_pronouns(self, pronouns):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
        self.action.pronouns = pronouns
        self.action.insert_pronouns()
        super().insert_pronouns(pronouns)
