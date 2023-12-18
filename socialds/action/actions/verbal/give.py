from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.enums import Tense
from socialds.operations.move_relation import MoveRelation
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType
from socialds.states.relation import RType


class Give(Action):
    def __init__(self, done_by: Agent | DSTPronoun, recipient: Agent | DSTPronoun, target_resource: any):
        super().__init__('give', done_by, ActionObjType.PHYSICAL, [
            # MoveRelation(relation=FindOneRelationInAgent(agent=done_by,
            #                                              rstype=RSType.RESOURCES,
            #                                              left=done_by,
            #                                              rtype=RType.HAS,
            #                                              rtense=Tense.PRESENT,
            #                                              right=given,
            #                                              negation=False),
            #              from_rs=done_by.relation_storages[RSType.RESOURCES],
            #              to_rs=taker.relation_storages[RSType.RESOURCES])
        ], recipient=recipient, target_resource=target_resource)

    def insert_pronouns(self):
        if isinstance(self.recipient, DSTPronoun):
            self.recipient = pronouns[self.recipient]
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
