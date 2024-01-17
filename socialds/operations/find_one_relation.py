from __future__ import annotations

from socialds.enums import Tense
from socialds.operations.stateoperation import StateOperation
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RType


class FindOneRelation(StateOperation):
    def __init__(self, rs: RelationStorage | StateOperation, left: any | StateOperation = None,
                 rtype: RType | StateOperation = None, rtense: Tense | StateOperation = None,
                 right: any | StateOperation = None, negation: bool | StateOperation = None):
        """
        Finds the first matching relation
        :param rs:
        :param left:
        :param rtype:
        :param rtense:
        :param right:
        :param negation:
        """
        super().__init__('find-one-relation')
        self.left = left
        self.rtype = rtype
        self.rtense = rtense
        self.right = right
        self.negation = negation
        self.rs = rs

    def execute_param_state_operations(self):
        if isinstance(self.rs, StateOperation):
            self.rs = self.rs.execute(self.pronouns)
        elif isinstance(self.left, StateOperation):
            self.left = self.left.execute(self.pronouns)
        elif isinstance(self.rtype, StateOperation):
            self.rtype = self.rtype.execute(self.pronouns)
        elif isinstance(self.rtense, StateOperation):
            self.rtense = self.rtense.execute(self.pronouns)
        elif isinstance(self.right, StateOperation):
            self.right = self.right.execute(self.pronouns)
        elif isinstance(self.negation, StateOperation):
            self.negation = self.negation.execute(self.pronouns)

    def insert_pronouns(self):
        if isinstance(self.left, DSTPronoun):
            self.left = self.pronouns[self.left]
        elif isinstance(self.right, DSTPronoun):
            self.right = self.pronouns[self.right]

    def execute(self, pronouns, *args, **kwargs) -> Relation:
        super().execute(pronouns, *args, **kwargs)
        self.execute_param_state_operations()
        self.insert_pronouns()
        return self.rs.get_one(left=self.left,
                               rtype=self.rtype,
                               rtense=self.rtense,
                               right=self.right,
                               negation=self.negation,
                               pronouns=pronouns)
