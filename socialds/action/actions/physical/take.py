from functools import partial
from typing import List
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.object import Object
from socialds.states.relation import Relation, RelationTense, RelationType
from socialds.states.property import Property


class Take(Action):
    def __init__(self, giver: Agent, taken: Property, taker: Agent, r_tense: RelationTense, negation: bool = False):
        self.giver = giver
        self.taken = taken
        self.taker = taker
        self.r_tense = r_tense
        self.negation = negation
        super().__init__('take', ActionObjType.PHYSICAL, [])

    def colorless_repr(self):
        return f"{super().__repr__()}({str(self.taker.name)} takes {self.taken} from {self.giver})"

    def __repr__(self):
        return f"{super().__repr__()}({self.taker.name} takes {self.taken} from {self.giver})"

    def execute(self):
        # act = Relation(left=self.giver, r_type=RelationType.ACTION, right=self.taker r_tense=self.r_tense, negation=self.negation)
        return super().execute()
