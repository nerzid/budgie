from typing import List

from socialds.states.property import Property


# Agents and Resources are both objects
class Object:
    def __init__(self, name, properties=None, relations=None):
        if properties is None:
            properties = set()
        if relations is None:
            relations = set()
        self.properties = properties
        self.relations = relations
        self.name = name

    def get_left_relations(self):
        left_relations = []
        for relation in self.relations:
            if relation.left == self:
                left_relations.append(relation)
        return left_relations

    def get_right_relations(self):
        right_relations = []
        for relation in self.relations:
            if relation.right == self:
                right_relations.append(relation)
        return right_relations

    def __str__(self):
        return self.name