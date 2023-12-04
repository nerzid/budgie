from __future__ import annotations

from typing import List

from socialds.other.dst_pronouns import DSTPronoun
from socialds.other.variables import dialogue_history
from socialds.action.action import Action
from socialds.agent import Agent
from socialds.action.action_time import ActionTime
from socialds.conditions.condition import Condition
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class AgentDoes(Condition):
    def __init__(self, agent: Agent | DSTPronoun, action: Action, tense: Tense, times: List[ActionTime] = None,
                 negation=False):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.action = action

    def check(self):
        if not self.negation:
            return dialogue_history.contains(Relation(left=self.agent,
                                                      rtype=RType.ACTION,
                                                      rtense=self.tense,
                                                      right=self.action))
        else:
            return not dialogue_history.contains(Relation(left=self.agent,
                                                          rtype=RType.ACTION,
                                                          rtense=self.tense,
                                                          right=self.action))

    def colorless_repr(self):
        return f"{self.agent} ({not self.negation})does({self.tense.value}) {self.action.colorless_repr()}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.agent} ({not self.negation})does({self.tense.value}) {self.action}{super().get_times_str()}"


# to satisfy the condition agent does, there are few options
# first option is, if the agent can do it, he does it.
# E.g., I need to tell the doctor about my problem (Share). So, I perform the Share action.
# (action in AgentDoes)
# second option is, if the agent cannot do it because he doesn't know how to do it, he learns it first then does it.
# E.g., I don't know how to cook rice, so I look it up on YouTube, learn it, then cook rice.
# there are different ways of learning things, I can read a book, search it on internet, or ask a friend
# In such, for each competence, I should have an action sequence that works as the recipe on how it can be learned.
# (Learn(Competence(action in AgentDoes)) then (Action))
# This is except when asking it to a friend which is a more direct approach and involves third parties. Therefore,
# it is the third option.
# third option is, if the agent cannot do it, he can request from the other agent to teach him how to do it.
# E.g., I don't know how to cook rice, and I know that my friend knows it, so I call him to explain the process.
# (Request (Teach(competence(action in AgentDoes))  ) from the other agent)
# for the teaching of competence, I should have an action sequence that works as the recipe on how it can be taught.
# fourth option is, if the agent cannot do it, he can request from the other agent to do it.
# E.g., My eye needs to be examined. I cannot do it, only a doctor can do it. So, I ask the doctor to do it.
# (Request (action in AgentDoes) from the other agent)

