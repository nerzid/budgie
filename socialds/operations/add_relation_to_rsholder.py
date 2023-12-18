from __future__ import annotations

from socialds.operations.stateoperation import StateOperation
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.rs_holder import RSHolder
from socialds.states.relation import Relation
from socialds.other.dst_pronouns import pronouns


class AddRelationToRSHolder(StateOperation):
    def __init__(self, relation: Relation | StateOperation, rsholder: RSHolder | DSTPronoun | StateOperation,
                 rstype: RSType):
        super().__init__('add-relation-to-agent-rs')
        self.relation = relation
        self.rsholder = rsholder
        self.rstype = rstype

    def execute_param_state_operations(self):
        if isinstance(self.relation, StateOperation):
            self.relation = self.relation.execute()
        elif isinstance(self.rsholder, StateOperation):
            self.rsholder = self.rsholder.execute()
        elif isinstance(self.rsholder, DSTPronoun):
            self.rsholder = pronouns[self.rsholder]

    def execute(self):
        self.execute_param_state_operations()
        self.relation.insert_pronouns()
        self.rsholder.relation_storages[self.rstype].add(self.relation)
