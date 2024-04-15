from __future__ import annotations

from typing import List

from socialds.action.action_time import ActionHappenedAtTime
import socialds.agent as a
from socialds.conditions.condition import Condition
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.socialpractice.context.place import Place
from socialds.states.relation import Relation, RType, Negation
from socialds.enums import Tense


class AgentAtPlace(Condition):
    def __init__(self, agent: a.Agent | DSTPronoun, place: Place, tense: Tense,
                 times: List[ActionHappenedAtTime] = None,
                 negation:Negation=Negation.FALSE):
        super().__init__(tense, times, negation)
        self.agent = agent
        self.place = place

    def check(self, checker=None):
        if isinstance(self.agent, DSTPronoun):
            agent = checker.pronouns[self.agent]
        else:
            agent = self.agent
        if self.negation == Negation.FALSE or self.negation == Negation.ANY:
            return agent.relation_storages[RSType.PLACES].contains(
                Relation(left=agent, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=self.place),
                pronouns=checker.pronouns)
        else:
            return not agent.relation_storages[RSType.PLACES].contains(
                Relation(left=agent, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=self.place),
                pronouns=checker.pronouns)

    def __str__(self):
        tense_str = Relation.relation_types_with_tenses[RType.IS_AT][self.negation][self.tense]
        return "%s %s %s %s" % (self.agent, tense_str, self.place, self.get_times_str())

    def __repr__(self):
        tense_str = Relation.relation_types_with_tenses[RType.IS_AT][self.negation][self.tense]
        return "%r %r %r %r" % (self.agent, tense_str, self.place, self.get_times_str())

    def insert_pronouns(self, pronouns):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
        super().insert_pronouns(pronouns)
# there are few options to satisfy the agent at place condition
# first option is If I can do it, I move to the place
# E.g., I move from this room to another room in the house
# Therefore it is the (Move) action
# second option is if I cannot move to the place, due to a permit, I request to have the permit
# E.g., I need to ask the doctor if I can enter the office. Request (Permit for Move)
# third option is if I cannot move to the place because I don't know where that is
# E.g., I need to attend a meeting in the room A216 but don't know where it is. So I ask the other agent share it.
# (Request (Share) from the other agent)
# fourth option is if I cannot move because I have an impairment that prevents me from walking
# E.g., I cannot walk, so I ask other agent to move me
# (Request (Move me) from the other agent)
# fifth option is if I cannot move because there is a physical restriction, so I try to undo the restriction if possible
# E.g., I cannot come to work because there is snow blocking my apartment entrance, so I shovel the snow out of the way
# This concept introduces the restrictions for the actions which is a future work.
# But it should look like this
# (Fix(issue) then Move())
