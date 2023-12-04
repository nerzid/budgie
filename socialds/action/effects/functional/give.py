from __future__ import annotations

from functools import partial

from socialds.operations.find_one_relation import FindOneRelation
from socialds.operations.find_one_relation_in_agent import FindOneRelationInAgent
from socialds.operations.move_relation import MoveRelation
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType
from socialds.repositories.operation_repository import find_relation, modify_relation_left, move_relation
from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.states.relation import RType
from socialds.enums import Tense


class Give(Action):
    def __init__(self, giver: Agent | DSTPronoun, taker: Agent | DSTPronoun, given: any):
        # current_holding_relation = find_relation(giver, RType.HAS, Tense.PRESENT, given, True, giver.resources)
        # super().__init__('give', ActionObjType.FUNCTIONAL, [
        #     partial(move_relation, current_holding_relation, giver.resources, taker.resources),
        #     partial(modify_relation_left, current_holding_relation, taker)])
        self.giver = giver
        self.taker = taker
        self.given = given
        super().__init__('give', ActionObjType.FUNCTIONAL, [
            MoveRelation(relation=FindOneRelationInAgent(agent=giver,
                                                         rstype=RSType.RESOURCES,
                                                         left=giver,
                                                         rtype=RType.HAS,
                                                         rtense=Tense.PRESENT,
                                                         right=given,
                                                         negation=False),
                         from_rs=giver.relation_storages[RSType.RESOURCES],
                         to_rs=taker.relation_storages[RSType.RESOURCES])
        ])

    def insert_pronouns(self):
        if isinstance(self.giver, DSTPronoun):
            self.giver = pronouns[self.giver]
        if isinstance(self.taker, DSTPronoun):
            self.taker = pronouns[self.taker]
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()

# Joe gives an apple to Jane
# Joe -has-> an apple is removed and Jane -has-> an apple is added
# giver -has-> given is removed, then taker -has-> given is created

# instead of removing it, this code changes the location of the relation from rs to rs
# then changes the leftside of the relation

# For simplicity reasons we don't check if the resource is plural or not
# For example, if Joe has multiple apples and gives one apple to Jane
# Then Joe still should have an apple which means that
# Joe -has-> an apple shouldn't be removed.
# However, this logic gets complicated once giver gives more than one object
# and has unknown number of the same objects in his possession.
# This creates and ambiguous situation in the sense that
# the information whether Joe still has apples or not isn't known
