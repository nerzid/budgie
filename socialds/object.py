from typing import List

from socialds.other.unique_id_generator import get_unique_id
from socialds.states.property import Property


# Agents and Resources are both objects
class Object:
    def __init__(self, name: str):
        self.name = name
        self.id = get_unique_id()

    # def get_left_relations(self):
    #     left_relations = []
    #     for relation in self.relations:
    #         if relation.left == self:
    #             left_relations.append(relation)
    #     return left_relations
    #
    # def get_right_relations(self):
    #     right_relations = []
    #     for relation in self.relations:
    #         if relation.right == self:
    #             right_relations.append(relation)
    #     return right_relations

    def __str__(self):
        return self.name
