from __future__ import annotations

from socialds.enums import Tense
from socialds.operations.operation import OperationFailed
from socialds.operations.stateoperation import StateOperation
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.rs_holder import RSHolder
from socialds.states.relation import RType, Relation, Negation


class FindOneRelationInRSHolder(StateOperation):
    def __init__(self, rsholder: RSHolder | DSTPronoun | StateOperation,
                 rstype: RSType,
                 left: any | StateOperation = None,
                 rtype: RType | StateOperation = None,
                 rtense: Tense | StateOperation = None,
                 right: any | StateOperation = None,
                 negation: Negation = Negation.FALSE):
        super().__init__('find-one-relation-in-agent')
        self.rsholder = rsholder
        self.rstype = rstype
        self.left = left
        self.rtype = rtype
        self.rtense = rtense
        self.right = right
        self.negation = negation

    def __str__(self):
        return "NAME: {}, rsholder: {}, rstype: {}, left: {}, rtype: {}, rtense: {}, right: {}, negation: {}" \
            .format(self.name, self.rsholder, self.rstype, self.left, self.rtype, self.rtense, self.right,
                    self.negation)

    def execute_param_state_operations(self):
        if isinstance(self.rsholder, StateOperation):
            self.rsholder = self.rsholder.execute(self.pronouns)
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
        if isinstance(self.rsholder, DSTPronoun):
            self.rsholder = self.pronouns[self.rsholder]

    def execute(self, agent, *args, **kwargs) -> Relation:
        super().execute(agent, *args, **kwargs)
        self.execute_param_state_operations()
        self.insert_pronouns()
        relation = self.rsholder.relation_storages[self.rstype].get_one(left=self.left,
                                                                        rtype=self.rtype,
                                                                        rtense=self.rtense,
                                                                        right=self.right,
                                                                        negation=self.negation,
                                                                        pronouns=agent.pronouns)
        if relation is None:
            raise OperationFailed("{} doesn't have the relation {} in {}"
                                  .format(self.rsholder,
                                          Relation(left=self.left, rtype=self.rtype, rtense=self.rtense,
                                                   right=self.right, negation=self.negation),
                                          self.rsholder.relation_storages[self.rstype]))
        else:
            return relation
