from __future__ import annotations

from typing import List

from socialds.enums import Tense
from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.socialpractice.context.role import Role
from socialds.states.relation import Relation, RType


class AgentHasRole(Condition):
    def __init__(self, agent: any, role: Role, tense: Tense, times: List[ActionHappenedAtTime] = None, negation=False):
        # agent can be either Agent or DSTpronoun. For circular import reasons, the type hinting for agent doesnt use Agent | DSTPronoun
        super().__init__(tense, times, negation)
        self.agent = agent
        self.role = role

    def __eq__(self, other):
        if isinstance(other, AgentHasRole):
            return self.agent == other.agent and self.role == other.role
        return False

    def check(self, checker=None):
        if isinstance(self.agent, DSTPronoun):
            agent = checker.pronouns[self.agent]
        else:
            agent = self.agent
        if not self.negation:
            return self.role in agent.roles
        else:
            return not self.role in agent.roles

    def __str__(self):
        tense_str = Relation.relation_types_with_tenses[RType.ACTION][not self.negation][self.tense]
        return "%s %s has role %s %s" % (self.agent, tense_str, self.role, self.get_times_str())

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.ACTION][not self.negation][self.tense]
        return "%r %r has role %r %s" % (self.agent, tense_str, self.role, self.get_times_str())

    def insert_pronouns(self, pronouns):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
        super().insert_pronouns(pronouns)
