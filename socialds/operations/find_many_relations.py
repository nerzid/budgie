from __future__ import annotations

from socialds.enums import Tense
from socialds.operations.stateoperation import StateOperation
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RType


class FindManyRelations(StateOperation):
    def __init__(self, rs: RelationStorage | StateOperation, left: any | StateOperation = None,
                 rtype: RType | StateOperation = None, rtense: Tense | StateOperation = None,
                 right: any | StateOperation = None, negation: bool | StateOperation = None):
        """
        Finds all the matching relations
        :param rs:
        :param left:
        :param rtype:
        :param rtense:
        :param right:
        :param negation:
        """
        super().__init__('find-many-relations')
        self.left = left
        self.rtype = rtype
        self.rtense = rtense
        self.right = right
        self.negation = negation
        self.rs = rs

    def execute_param_state_operations(self):
        if isinstance(self.rs, StateOperation):
            self.rs = self.rs.execute()
        elif isinstance(self.left, StateOperation):
            self.left = self.left.execute()
        elif isinstance(self.rtype, StateOperation):
            self.rtype = self.rtype.execute()
        elif isinstance(self.rtense, StateOperation):
            self.rtense = self.rtense.execute()
        elif isinstance(self.right, StateOperation):
            self.right = self.right.execute()
        elif isinstance(self.negation, StateOperation):
            self.negation = self.negation.execute()

    def insert_pronouns(self):
        if isinstance(self.left, DSTPronoun):
            self.left = pronouns[self.left]
        elif isinstance(self.right, DSTPronoun):
            self.right = pronouns[self.right]

    def execute(self) -> Relation:
        super().execute()
        self.execute_param_state_operations()
        self.insert_pronouns()
        return self.rs.get_many(left=self.left,
                                rtype=self.rtype,
                                rtense=self.rtense,
                                right=self.right,
                                negation=self.negation)
