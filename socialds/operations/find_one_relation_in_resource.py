from __future__ import annotations

from socialds.enums import Tense
from socialds.operations.stateoperation import StateOperation
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.socialpractice.context.resource import Resource
from socialds.states.relation import RType, Relation


class FindOneRelationInResource(StateOperation):
    def __init__(self, resource: Resource | DSTPronoun | StateOperation, rstype: RSType,
                 left: any | StateOperation = None,
                 rtype: RType | StateOperation = None,
                 rtense: Tense | StateOperation = None, right: any | StateOperation = None,
                 negation: bool | StateOperation = None):
        super().__init__('find-one-relation-in-agent')
        self.resource = resource
        self.rstype = rstype
        self.left = left
        self.rtype = rtype
        self.rtense = rtense
        self.right = right
        self.negation = negation

    def execute_param_state_operations(self):
        if isinstance(self.resource, StateOperation):
            self.resource = self.resource.execute(self.pronouns)
        if isinstance(self.left, StateOperation):
            self.left = self.left.execute(self.pronouns)
        if isinstance(self.rtype, StateOperation):
            self.rtype = self.rtype.execute(self.pronouns)
        if isinstance(self.rtense, StateOperation):
            self.rtense = self.rtense.execute(self.pronouns)
        if isinstance(self.right, StateOperation):
            self.right = self.right.execute(self.pronouns)
        if isinstance(self.negation, StateOperation):
            self.negation = self.negation.execute(self.pronouns)

    def insert_pronouns(self):
        if isinstance(self.left, DSTPronoun):
            self.left = self.pronouns[self.left]
        if isinstance(self.right, DSTPronoun):
            self.right = self.pronouns[self.right]
        # if isinstance(self.agent, DSTPronoun):
        #     self.agent = pronouns[self.agent]

    def execute(self, pronouns, *args, **kwargs) -> Relation:
        super().execute(pronouns, *args, **kwargs)
        self.execute_param_state_operations()
        self.insert_pronouns()
        return self.resource.relation_storages[self.rstype].get_one(left=self.left,
                                                                    rtype=self.rtype,
                                                                    rtense=self.rtense,
                                                                    right=self.right,
                                                                    negation=self.negation,
                                                                    pronouns=pronouns)
