from functools import partial
from typing import List
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.repositories.operation_repository import find_relation_by_place, modify_relation_right, \
    modify_relation_tense, create_then_add_relation
from socialds.socialpractice.context.place import Place
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class Move(Action):
    def __init__(self, mover: Agent, moved: any, from_place: Place, to_place: Place):
        # self.relation = Relation(mover, RelationType.ACTION, RelationTense.PRESENT, )
        self.relation = None
        self.mover = mover
        self.moved = moved
        self.from_place = from_place
        self.to_place = to_place
        super().__init__('move', ActionObjType.FUNCTIONAL,
                         op_seq=[partial(modify_relation_tense, self.relation, Tense.PAST),
                                 partial(create_then_add_relation, moved, RType.IS_AT, Tense.PRESENT,
                                         to_place, True)])

    def colorless_repr(self):
        return super().colorless_repr() + '(' + str(self.mover.name) + ' moves ' + str(self.moved.name) + ' from ' + self.from_place.name + ' to ' + self.to_place.name + ')'

    def __repr__(self):
        return super().colorless_repr() + '(' + str(self.mover.name) + ' moves ' + str(self.moved.name) + ' from ' + self.from_place.name + ' to ' + self.to_place.name + ')'

    def execute(self):
        self.relation = find_relation_by_place(self.moved, RelationTense.PRESENT, self.from_place)
        super().execute()

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
