from socialds.agent import Agent
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.states.relation import Relation, RelationTense, RelationType
from socialds.states.property import Property


class Feel(Action):
    def __init__(self, felt_by: Agent, felt: Property, about: Relation, r_tense: RelationTense,
                 negation: bool = False):
        self.felt_by = felt_by
        self.felt = felt
        self.about = about
        self.r_tense = r_tense
        self.negation = negation
        super().__init__('feel', ActionObjType.FUNCTIONAL, [])

    def colorless_repr(self):
        return f"{super().__repr__()}{self.felt_by.name} feels {self.felt} about {self.about.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.felt_by.name} feels {self.felt} about {self.about}"
