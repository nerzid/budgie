from object import Object
from stateoperations.stateoperation import StateOperation
from states.relation import Relation


class ModifyRelation(StateOperation):
    def __init__(self, old_relation: Relation, new_relation: Relation):
        super().__init__()
        self.old_relation = old_relation
        self.new_relation = new_relation

    def execute(self):
        self.old_relation.left.relations.remove(self.old_relation)
        self.old_relation.right.relations.remove(self.old_relation)
        self.new_relation.left.relations.add(self.new_relation)
        self.new_relation.right.relations.add(self.new_relation)
