from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.operations.add_relation_to_agent_rs import AddRelationToAgentRS
from socialds.operations.find_one_relation_in_agent import FindOneRelationInAgent
from socialds.operations.modify_relation_tense import ModifyRelationTense
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType
from socialds.socialpractice.context.place import Place
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class Move(Action):
    def __init__(self, mover: Agent | DSTPronoun, moved: any, from_place: Place, to_place: Place):
        # self.relation = Relation(mover, RelationType.ACTION, RelationTense.PRESENT, )
        self.relation = None
        self.mover = mover
        self.moved = moved
        self.from_place = from_place
        self.to_place = to_place
        if isinstance(moved, Agent) or isinstance(moved, DSTPronoun):
            op_seq = [
                ModifyRelationTense(
                    relation=FindOneRelationInAgent(
                        agent=self.moved,
                        rstype=RSType.PLACES,
                        left=self.moved,
                        rtype=RType.IS_AT,
                        rtense=Tense.PRESENT,
                        right=self.from_place,
                        negation=False
                    ), rtense=Tense.PAST),
                AddRelationToAgentRS(
                    relation=Relation(
                        left=self.moved,
                        rtype=RType.IS_AT,
                        rtense=Tense.PRESENT,
                        right=self.to_place,
                        negation=False
                    ), agent=self.moved, rstype=RSType.PLACES)
            ]
        else:
            op_seq = [
                #     TODO
            ]
        super().__init__('move', ActionObjType.FUNCTIONAL,
                         # op_seq=[partial(modify_relation_tense, self.relation, Tense.PAST),
                         #         partial(create_then_add_relation, moved, RType.IS_AT, Tense.PRESENT,
                         #                 to_place, True, moved.places)]
                         op_seq=op_seq
                         )

    def insert_pronouns(self):
        super().insert_pronouns()
        if isinstance(self.mover, DSTPronoun):
            self.mover = pronouns[self.mover]
        if isinstance(self.moved, DSTPronoun):
            self.moved = pronouns[self.moved]

    def colorless_repr(self):
        return super().colorless_repr() + '(' + str(self.mover.name) + ' move ' + str(
            self.moved.name) + ' from ' + self.from_place.name + ' to ' + self.to_place.name + ')'

    def __repr__(self):
        return super().colorless_repr() + '(' + str(self.mover.name) + ' move ' + str(
            self.moved.name) + ' from ' + self.from_place.name + ' to ' + self.to_place.name + ')'

    def execute(self):
        self.insert_pronouns()
        super().execute()
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
