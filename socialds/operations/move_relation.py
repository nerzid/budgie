from __future__ import annotations

from socialds.operations.stateoperation import StateOperation
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation


class MoveRelation(StateOperation):
    def __init__(self, relation: Relation | StateOperation,
                 from_rs: RelationStorage | StateOperation,
                 to_rs: RelationStorage | StateOperation):
        """
        Moves the relation from one relation storage to another
        :param relation:
        :param from_rs:
        :param to_rs:
        """
        super().__init__('move-relation')
        self.relation = relation
        self.from_rs = from_rs
        self.to_rs = to_rs

    def execute_param_state_operations(self):
        super().execute_param_state_operations()
        if isinstance(self.relation, StateOperation):
            self.relation.execute(self.pronouns)
        elif isinstance(self.from_rs, StateOperation):
            self.from_rs.execute(self.pronouns)
        elif isinstance(self.to_rs, StateOperation):
            self.to_rs.execute(self.pronouns)

    def execute(self, agent, *args, **kwargs):
        super().execute(agent, *args, **kwargs)
        self.execute_param_state_operations()
        self.relation.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.from_rs.remove(self.relation)
        self.to_rs.add(self.relation)
