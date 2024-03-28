from __future__ import annotations

from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.agent import Agent
from socialds.object import Object
from socialds.other.dst_pronouns import DSTPronoun
from socialds.requirement import Requirement
from socialds.rs_holder import RSHolder, RSHolderType
from socialds.states.relation import Relation, RType, Tense


class Information(Relation, RSHolder):
    def __init__(self, left: Object | "Information" | Agent | DSTPronoun, rtype: RType, rtense: Tense, right: any,
                 negation=False, times: List[ActionHappenedAtTime] = None):
        Relation.__init__(self, left=left, rtype=rtype, rtense=rtense, right=right, negation=negation, times=times)
        RSHolder.__init__(self, rsholder_name='information', rsholder_type=RSHolderType.INFORMATION)

    def __eq__(self, other):
        from socialds.any.any_relation import AnyRelation
        if isinstance(other, AnyRelation):
            return True
        if isinstance(other, Information):
            return (self.left == other.left and
                    (self.rtype == other.rtype or self.rtype == RType.ANY or other.rtype == RType.ANY) and
                    (self.rtense == other.rtense or self.rtense == Tense.ANY or other.rtense == Tense.ANY) and
                    self.negation == other.negation and
                    self.times == other.times and
                    self.rsholder_name == other.rsholder_name) # TODO RS check needs to check relations as well
        return False
