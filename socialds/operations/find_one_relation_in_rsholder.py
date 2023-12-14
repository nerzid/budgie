from __future__ import annotations

from socialds.agent import Agent
from socialds.enums import Tense
from socialds.operations.find_one_relation import FindOneRelation
from socialds.operations.stateoperation import StateOperation
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType, RelationStorage
from socialds.rs_holder import RSHolder
from socialds.states.relation import RType, Relation


class FindOneRelationInRSHolder(StateOperation):
    def __init__(self, rsholder: RSHolder | DSTPronoun | StateOperation, rstype: RSType,
                 left: any | StateOperation = None,
                 rtype: RType | StateOperation = None,
                 rtense: Tense | StateOperation = None, right: any | StateOperation = None,
                 negation: bool | StateOperation = None):
        super().__init__('find-one-relation-in-agent')
        self.rsholder = rsholder
        self.rstype = rstype
        self.left = left
        self.rtype = rtype
        self.rtense = rtense
        self.right = right
        self.negation = negation

    def execute_param_state_operations(self):
        if isinstance(self.rsholder, StateOperation):
            self.rsholder = self.rsholder.execute()
        if isinstance(self.left, StateOperation):
            self.left = self.left.execute()
        if isinstance(self.rtype, StateOperation):
            self.rtype = self.rtype.execute()
        if isinstance(self.rtense, StateOperation):
            self.rtense = self.rtense.execute()
        if isinstance(self.right, StateOperation):
            self.right = self.right.execute()
        if isinstance(self.negation, StateOperation):
            self.negation = self.negation.execute()

    def insert_pronouns(self):
        if isinstance(self.left, DSTPronoun):
            self.left = pronouns[self.left]
        if isinstance(self.right, DSTPronoun):
            self.right = pronouns[self.right]
        if isinstance(self.rsholder, DSTPronoun):
            self.rsholder = pronouns[self.rsholder]

    def execute(self) -> Relation:
        self.execute_param_state_operations()
        self.insert_pronouns()
        return self.rsholder.relation_storages[self.rstype].get_one(left=self.left,
                                                                    rtype=self.rtype,
                                                                    rtense=self.rtense,
                                                                    right=self.right,
                                                                    negation=self.negation)
