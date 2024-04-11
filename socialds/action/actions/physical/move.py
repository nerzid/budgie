from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.change_place import ChangePlace
from socialds.agent import Agent
from socialds.any.any_agent import AnyAgent
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.place import Place
import inspect

from socialds.socialpractice.context.resource import Resource


class Move(Action):

    def __init__(self, moved: Resource | Agent | DSTPronoun, from_place: Place, to_place: Place,
                 done_by: Agent | DSTPronoun = DSTPronoun.I, ):
        # self.relation = Relation(mover, RelationType.ACTION, RelationTense.PRESENT, )
        self.relation = None
        self.moved = moved
        self.from_place = from_place
        self.to_place = to_place

        # TODO all inputs except done_by should go into either target_resources or recipients for correct equality check
        # TODO atm, target_resource and recipient is singular. It should be turned into array to work with the suggestion above
        target_resources = []
        recipients = []
        # if isinstance(moved, Agent) or isinstance(moved, DSTPronoun):
        #     recipients.append(moved)
        # elif isinstance(moved, Resource):
        #     target_resources.append(moved)

        effects = [
            ChangePlace(from_place=self.from_place,
                        to_place=self.to_place,
                        affected=self.moved)
        ]
        super().__init__('move', done_by, ActionObjType.PHYSICAL, base_effects=effects)

    # def equals_with_pronouns(self, other, pronouns):
    #     return super().equals_with_pronouns(other, pronouns) and self.from_place == other.from_place and self.to_place == other.to_place and \
    #         (self.moved == other.moved or isinstance(other.moved, AnyAgent) or isinstance(
    #             self.moved, AnyAgent))

    def get_requirement_holders(self) -> List:
        return [self.moved, self.from_place, self.to_place]

    def insert_pronouns(self):
        super().insert_pronouns()
        if isinstance(self.moved, DSTPronoun):
            self.moved = self.pronouns[self.moved]

    @staticmethod
    def get_pretty_template():
        return "[done_by] moves [moved] from [from_place] to [to_place]"

    def __str__(self):
        if self.done_by == self.moved:
            return "%s move from %s to %s" % (self.done_by, self.from_place.name, self.to_place.name)
        else:
            return "%s move %s from %s to %s" % (
                self.done_by, self.moved.name, self.from_place.name, self.to_place.name)

    def __repr__(self):
        if self.done_by == self.moved:
            return "%r move from %r to %r" % (self.done_by, self.from_place.name, self.to_place.name)
        else:
            return "%r move %r from %r to %r" % (
                self.done_by, self.moved.name, self.from_place.name, self.to_place.name)

    # def execute(self):
    #     self.relation = find_relation_by_place(self.moved, Tense.PRESENT, self.from_place)
    #     modify_relation_tense(self.relation, Tense.PAST)
    #     create_then_add_relation(self.moved, RType.IS_AT, Tense.PRESENT, self.to_place, False, self.moved.places)
    #     super().execute()

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
