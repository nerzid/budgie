from __future__ import annotations

from typing import List

from socialds.enums import Tense
from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.states.property import Property
from socialds.states.relation import Relation, RType, Negation


class AgentIsInState(Condition):
    def __init__(self, agent: any, state: Property, tense: Tense, negation: Negation = Negation.FALSE):
        # agent can be either Agent or DSTpronoun. For circular import reasons, the type hinting for agent doesnt use Agent | DSTPronoun
        super().__init__(tense=tense, negation=negation)
        self.agent = agent
        self.state = state

    def __eq__(self, other):
        if isinstance(other, AgentIsInState):
            return self.agent == other.agent and self.state == other.state
        return False

    def check(self, checker=None):
        if isinstance(self.agent, DSTPronoun):
            agent = checker.pronouns[self.agent]
        else:
            agent = self.agent
        state_rel = Relation(left=agent, rel_type=RType.IS_IN, rel_tense=self.tense, right=self.state, negation=self.negation)
        if self.negation == Negation.FALSE or self.negation == Negation.ANY:
            return agent.relation_storages[RSType.STATES].contains(state_rel, pronouns=checker.pronouns)
        else:
            return not agent.relation_storages[RSType.KNOWLEDGEBASE].contains(state_rel, pronouns=checker.pronouns)

    def __str__(self):
        tense_str = Relation.relation_types_with_tenses[RType.ACTION][self.negation][self.tense]
        return "%s %s state %s %s" % (self.agent, tense_str, self.state, self.get_times_str())

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.ACTION][self.negation][self.tense]
        return "%r %r state %r %s" % (self.agent, tense_str, self.state, self.get_times_str())

    def insert_pronouns(self, pronouns):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
        super().insert_pronouns(pronouns)

# to satisfy the condition of agent knows, there are a few options
# the first choice is observing the knowledgebase of the places that the agent is at.
# E.g., if I don't know if the apple in the room is red, I look for the apple first, then see that the apple is red.
# Therefore, it uses Find and Learn. It specifically looks for the relation (Find) in all public knowledgebases and
# then add it to his own knowledgebase (Learn).
# the second choice is trying to deduce the information from the available information.
# E.g., If I eat only red apples, and I bought an apple from the store, then the apple I have is red.
# Therefore, it uses Deduce. I need a separate knowledgebase that I can put the rules which can be used for deduce.
# the third choice is asking the other agent about the information
# E.g., if I don't the know if the apple in the other agent's pocket is red, I ask him what is it.
# Therefore, it uses Ask to ask for the specific information.

# by remembering it
