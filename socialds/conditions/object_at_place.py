from __future__ import annotations

from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.conditions.condition import Condition
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.place import Place
from socialds.states.relation import Relation, RType, Negation
from socialds.enums import Tense
from socialds.states.relation import Relation as r


class ObjectAtPlace(Condition):
    def __init__(self, rsholder, place: Place, tense: Tense, times: List[ActionHappenedAtTime] = None,
                 negation: Negation = Negation.FALSE):
        super().__init__(tense, times, negation)
        self.rsholder = rsholder
        self.place = place

    def __eq__(self, other):
        if isinstance(other, ObjectAtPlace):
            from socialds.any.any_place import AnyPlace
            return (self.rsholder == other.rsholder
                    and (self.place == other.place or isinstance(self.place, AnyPlace) or isinstance(other.place,
                                                                                                     AnyPlace))
                    and self.tense == other.tense
                    and self.times == other.times
                    and self.negation == other.negation)
        return False

    def check(self, checker=None):
        from socialds.relationstorage import RSType
        if isinstance(self.rsholder, DSTPronoun):
            rsholder = checker.pronouns[self.rsholder]
        else:
            rsholder = self.rsholder
        if self.negation == Negation.FALSE or self.negation == Negation.ANY:
            return rsholder.relation_storages[RSType.PLACES].contains(
                Relation(left=rsholder, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=self.place),
                pronouns=checker.pronouns)
        else:
            return not rsholder.relation_storages[RSType.PLACES].contains(
                Relation(left=self.rsholder, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=self.place),
                pronouns=checker.pronouns)

    def __str__(self):
        return "%s %s %s %s" % (
            self.rsholder, r.relation_types_with_tenses[RType.IS_AT][self.negation][self.tense], self.place,
            super().get_times_str())

    def __repr__(self):
        return "%r %r %r %r" % (
            self.rsholder, r.relation_types_with_tenses[RType.IS_AT][self.negation][self.tense], self.place,
            super().get_times_str())

    def insert_pronouns(self, pronouns):
        if isinstance(self.rsholder, DSTPronoun):
            self.rsholder = pronouns[self.rsholder]
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
