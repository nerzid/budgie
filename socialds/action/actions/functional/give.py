from functools import partial

from socialds.repositories.operation_repository import find_relation, modify_relation_left, move_relation
from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.states.relation import RelationType, RelationTense


class Give(Action):
    def __init__(self, giver: Agent, taker: Agent, given: any):
        current_holding_relation = find_relation(giver, RelationType.HAS,
                                                 RelationTense.PRESENT, given,
                                                 True, giver.resources)
        super().__init__('give', ActionObjType.FUNCTIONAL, [
            partial(move_relation, current_holding_relation, giver.resources, taker.resources),
            partial(modify_relation_left, current_holding_relation, taker)])

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
