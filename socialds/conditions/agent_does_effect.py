from __future__ import annotations

from typing import List

import socialds.agent as a
from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.relation import Relation, RType, Negation


class AgentDoesEffect(Condition):
    def __init__(self, agent: a.Agent | DSTPronoun, effect, tense: Tense, times: List[ActionHappenedAtTime] = None,
                 negation: Negation = Negation.FALSE):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.effect = effect

    def check(self, checker=None):
        self.effect.pronouns = checker.pronouns
        for action_rel in checker.dialogue_system.action_history:
            # action.pronouns = checker.pronouns
            action = action_rel.right
            effects = action.base_effects + action.extra_effects
            for effect_in_action in effects:
                # effect_in_action.pronouns = checker.pronouns
                if self.effect.equals_with_pronouns(effect_in_action, checker.pronouns):
                    if self.negation == Negation.FALSE or self.negation == Negation.ANY:
                        return True
                    elif self.negation == Negation.TRUE:
                        return False
        return False

    def __str__(self):
        tense_str = Relation.relation_types_with_tenses[RType.EFFECT][self.negation][self.tense]
        return "%s %s %s %s" % (self.agent, tense_str, self.effect, self.get_times_str())

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.EFFECT][self.negation][self.tense]
        return "%r %r %r %r" % (self.agent, tense_str, self.effect, self.get_times_str())

    def insert_pronouns(self, pronouns):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
        self.effect.pronouns = pronouns
        self.effect.insert_pronouns()
        super().insert_pronouns(pronouns)
