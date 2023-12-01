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
