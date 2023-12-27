from __future__ import annotations

from typing import List

import socialds.agent as a
import socialds.other.variables as vars
from socialds.action.action_time import ActionTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.relation import Relation, RType


class AgentDoesEffect(Condition):
    def __init__(self, agent: a.Agent | DSTPronoun, effect, tense: Tense, times: List[ActionTime] = None,
                 negation=False):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.effect = effect

    def check(self):
        for action in vars.actions_history:
            effects = action.base_effects + action.extra_effects
            for effect_in_action in effects:
                if self.effect == effect_in_action:
                    if not self.negation:
                        return True
                    else:
                        return False
        return False

    def __str__(self):
        tense_str = Relation.relation_types_with_tenses[RType.EFFECT][not self.negation][self.tense]
        return "%s %s %s %s" % (self.agent, tense_str, self.effect, self.get_times_str())

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.EFFECT][not self.negation][self.tense]
        return "%r %r %r %r" % (self.agent, tense_str, self.effect, self.get_times_str())

    def insert_pronouns(self):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
        self.effect.insert_pronouns()
        super().insert_pronouns()
