from object import Object
from stateoperations.stateoperation import StateOperation
from states.relation import Relation


class DeleteRelation(StateOperation):
    def __init__(self, relation: Relation):
        super().__init__()
        self.relation = relation

    def execute(self):
        self.relation.left.relations.remove(self.relation)
        self.relation.right.relations.remove(self.relation)
