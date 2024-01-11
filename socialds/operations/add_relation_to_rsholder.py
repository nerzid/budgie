from __future__ import annotations

from socialds.operations.stateoperation import StateOperation
from socialds.other.dst_pronouns import DSTPronoun
import socialds.relationstorage as rs
import socialds.states.relation as r
from socialds.rs_holder import RSHolder


class AddRelationToRSHolder(StateOperation):
    def __init__(self, relation: r.Relation | StateOperation, rsholder: RSHolder | DSTPronoun | StateOperation,
                 rstype: rs.RSType):
        super().__init__('add-relation-to-agent-rs')
        self.relation = relation
        self.rsholder = rsholder
        self.rstype = rstype

    def execute_param_state_operations(self):
        if isinstance(self.relation, StateOperation):
            self.relation = self.relation.execute(self.pronouns)
        elif isinstance(self.rsholder, StateOperation):
            self.rsholder = self.rsholder.execute(self.pronouns)
        elif isinstance(self.rsholder, DSTPronoun):
            self.rsholder = self.pronouns[self.rsholder]

    def execute(self, pronouns, *args, **kwargs):
        super().execute(pronouns, *args, **kwargs)
        self.relation.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.execute_param_state_operations()
        self.rsholder.relation_storages[self.rstype].add(self.relation)
