from functools import partial
from typing import List
from socialds.actions.action import Action
from socialds.actions.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.repositories.operation_repository import find_relation_by_place, modify_relation_right
from socialds.socialpractice.context.place import Place
from socialds.states.relation import Relation, RelationTense, RelationType


class Move(Action):
    def __init__(self, mover:Agent, moved:any, from_place:Place, to_place:Place):
        # self.relation = Relation(mover, RelationType.ACTION, RelationTense.PRESENT, )
        self.relation = find_relation_by_place(moved, RelationTense.PRESENT, from_place)
        super().__init__('move', ActionObjType.FUNCTIONAL, op_seq=[partial(modify_relation_right, self.relation, to_place)])
        

# Joe -is at-> office
# Joe -is at-> Sweden

# Joe is mover
# Joe is moved
# from_place is office
# to_place is cafe

# Joe -move-> Joe -is at-> office to Joe -is at-> cafe
# steps
# find the relation at agent.places
# change the right side of the relation to new place
# TODO instead of changing the current location
# create a new location and put that into places
# and turn the previous place to was_at instead