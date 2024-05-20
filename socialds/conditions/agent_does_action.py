from __future__ import annotations

from typing import List

from socialds.other.dst_pronouns import DSTPronoun
import socialds.agent as a
from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.states.relation import Relation, RType, Negation
from socialds.enums import Tense


class AgentDoesAction(Condition):
    def __init__(
        self,
        agent: a.Agent | DSTPronoun,
        action,
        tense: Tense,
        times: List[ActionHappenedAtTime] = None,
        negation: Negation = Negation.FALSE,
    ):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.action = action
        self.tense = tense
        self.negation = negation

    def check(self, checker=None):
        if isinstance(self.agent, DSTPronoun):
            agent = checker.pronouns[self.agent]
        else:
            agent = self.agent
        action_relation = Relation(
            left=agent,
            rtype=RType.ACTION,
            rtense=self.tense,
            right=self.action,
            negation=self.negation,
        )
        if self.negation == Negation.TRUE:
            return not agent.dialogue_system.action_history.contains(
                action_relation, checker.pronouns
            )
        elif self.negation == Negation.FALSE or self.negation == Negation.ANY:
            return agent.dialogue_system.action_history.contains(
                action_relation, checker.pronouns
            )

    # def check(self):
    #     max_count = 1
    #         for time in self.times:
    #             if isinstance(time, NumOfTimes):
    #     if self.times is not None:
    #                 max_count = time.num
    #     found = []
    #     for i in range(max_count):
    #         if not self.negation:
    #             try:
    #                 relation = dialogue_history.get_one(left=self.agent,
    #                                                     rtype=RType.ACTION,
    #                                                     rtense=self.tense,
    #                                                     right=self.action,
    #                                                     excluded=found)
    #                 if relation is None:
    #                     return False
    #                 else:
    #                     found.append(relation)
    #
    #             except RelationNotFoundError:
    #                 return False
    #
    #         else:
    #             # if agent didn't do the action, then it is either missing
    #             # from the dialogue history, or it is explicitly has
    #             # the negation True
    #             # however, it doesn't make sense to mention someone hasn't been done twice
    #             # so this just returns based on one
    #             return not dialogue_history.contains(Relation(left=self.agent,
    #                                                           rtype=RType.ACTION,
    #                                                           rtense=self.tense,
    #                                                           right=self.action))
    #     return len(found) == max_count

    def __str__(self):
        tense_str = Relation.relation_types_with_tenses[RType.ACTION][self.negation][
            self.tense
        ]
        return "%s %s %s %s" % (
            self.agent,
            tense_str,
            self.action,
            self.get_times_str(),
        )

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.ACTION][self.negation][
            self.tense
        ]
        return "%r %r %r %r" % (
            self.agent,
            tense_str,
            self.action,
            self.get_times_str(),
        )

    def insert_pronouns(self, pronouns):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
        self.action.pronouns = pronouns
        self.action.insert_pronouns()
        super().insert_pronouns(pronouns)


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
