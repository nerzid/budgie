from socialds.enums import Tense
from socialds.operations.stateoperation import StateOperation
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RType


class CreateRelation(StateOperation):
    def __init__(self, left: any, rtype: RType, rtense: Tense, right: any, negation: bool, rs: RelationStorage):
        """
        Finds the first matching relation
        :param rs:
        :param left:
        :param rtype:
        :param rtense:
        :param right:
        :param negation:
        """
        super().__init__('find-relation')
        self.left = left
        self.rtype = rtype
        self.rtense = rtense
        self.right = right
        self.negation = negation
        self.rs = rs

    def execute(self) -> Relation:
        relation = Relation(left=self.left,
                            rtype=self.rtype,
                            rtense=self.rtense,
                            right=self.right,
                            negation=self.negation)
        relation.insert_pronouns()
        return self.rs.add(relation)