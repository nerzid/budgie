from __future__ import annotations

from socialds.conditions.condition import Condition
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun, pronouns
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

    def check(self):
        if isinstance(self.agent, DSTPronoun):
            agent = pronouns[self.agent]
        else:
            agent = self.agent
        if not self.negation:
            return Relation(left=agent, rtype=RType.IS_PERMITTED_TO, rtense=Tense.PRESENT, right=self.permit,
                            negation=self.negation) in agent.relation_storages[RSType.PERMITS]
        else:
            return Relation(left=agent, rtype=RType.IS_PERMITTED_TO, rtense=Tense.PRESENT, right=self.permit,
                            negation=self.negation) not in agent.relation_storages[RSType.PERMITS]
