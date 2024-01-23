from __future__ import annotations

from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.agent import Agent
from socialds.object import Object
from socialds.other.dst_pronouns import DSTPronoun
from socialds.requirement import Requirement
from socialds.states.relation import Relation, RType, Tense


class Information(Relation):
    def __init__(self, left: Object | "Information" | Agent | DSTPronoun, rtype: RType, rtense: Tense, right: any,
                 negation=False, requirements: List[Requirement] = None, times: List[ActionHappenedAtTime] = None):
        super().__init__(left, rtype, rtense, right, negation, times=times)
        if requirements is None:
            requirements = []
        self.requirements = requirements
