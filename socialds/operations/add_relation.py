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
            self.relation = self.relation.execute(self.pronouns)
        elif isinstance(self.rs, StateOperation):
            self.rs = self.rs.execute(self.pronouns)

    def execute(self, agent, *args, **kwargs):
        super().execute(agent, *args, **kwargs)
        self.relation.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.execute_param_state_operations()
        self.rs.add(self.relation)
