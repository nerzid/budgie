from __future__ import annotations

import copy

from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType


class HasPermit(Condition):
    def __init__(self, agent, permit, negation: bool = False):
        super().__init__(tense=Tense.PRESENT, negation=negation)
        self.agent = agent
        self.negation = negation
        self.permit = permit

    def __eq__(self, other):
        if isinstance(other, HasPermit):
            return (self.agent == other.agent
                    and self.permit == other.permit
                    and self.negation == other.negation)

    def check(self, checker=None):
        if isinstance(self.agent, DSTPronoun):
            agent = checker.pronouns[self.agent]
        else:
            agent = self.agent
        copied_permit = copy.deepcopy(self.permit)
        from socialds.DSTPronounHolder import DSTPronounHolder
        if isinstance(copied_permit, DSTPronounHolder):
            copied_permit.pronouns = checker.pronouns
        copied_permit.insert_pronouns()
        print("CHECKER -> {}".format(checker))
        print("PERMIT -> {}".format(copied_permit))
        print("HAS PERMIT? -> {}".format(Relation(left=agent, rtype=RType.IS_PERMITTED_TO, rtense=Tense.PRESENT, right=copied_permit,
                            negation=self.negation) in agent.relation_storages[RSType.PERMITS]))
        if not self.negation:
            return Relation(left=agent, rtype=RType.IS_PERMITTED_TO, rtense=Tense.PRESENT, right=copied_permit,
                            negation=self.negation) in agent.relation_storages[RSType.PERMITS]
        else:
            return Relation(left=agent, rtype=RType.IS_PERMITTED_TO, rtense=Tense.PRESENT, right=copied_permit,
                            negation=self.negation) not in agent.relation_storages[RSType.PERMITS]

    def insert_pronouns(self, pronouns):
        if isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]
