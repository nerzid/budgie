from socialds.operations.stateoperation import StateOperation
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation


class AddRelation(StateOperation):
    def __init__(self, relation: Relation, rs: RelationStorage):
        super().__init__('add-relation')
        self.relation = relation
        self.rs = rs

    def execute_param_state_operations(self):
        if isinstance(self.relation, StateOperation):
            self.relation = self.relation.execute()
        elif isinstance(self.rs, StateOperation):
            self.rs = self.rs.execute()

    def execute(self):
        self.execute_param_state_operations()
        self.relation.insert_pronouns()
        self.rs.add(self.relation)
