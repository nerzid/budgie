from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation


class Condition:
    # def __init__(self, relation: Relation, rs: RelationStorage, negation=False):
    #     self.relation = relation
    #     self.rs = rs
    #     self.negation = negation
    def __init__(self, relation: Relation, negation=False):
        self.relation = relation
        self.negation = negation

    # def check(self):
    #     return (self.relation not in self.rs, self.relation in self.rs)[self.negation]

    def colorless_repr(self):
        return f"(({not self.negation}){self.relation.colorless_repr()})"

    def __repr__(self):
        return f"(({not self.negation}){self.relation})"
