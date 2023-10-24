from object import Object
from operations.stateoperation import StateOperation
from states.relation import Relation


class AddRelation(StateOperation):
    def __init__(self, relation: Relation):
        super().__init__()
        self.relation = relation

    def execute(self):
        self.relation.left.relations.add(self.relation)
        self.relation.right.relations.add(self.relation)
