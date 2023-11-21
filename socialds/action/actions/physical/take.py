from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.enums import Tense
from socialds.states.property import Property


class Take(Action):
    def __init__(self, taken: Property, taker: Agent, r_tense: Tense, giver: Agent = None,
                 negation: bool = False, times=None):
        self.giver = giver
        self.taken = taken
        self.taker = taker
        self.r_tense = r_tense
        self.negation = negation
        self.times = times
        super().__init__('take', ActionObjType.PHYSICAL, [], times=times)

    def colorless_repr(self):
        from_str = (f' from {self.giver})', f'')[self.giver is None]
        return f"{super().__repr__()}{self.taker.name} takes {self.taken}{from_str}{super().get_times_str()}"

    def __repr__(self):
        from_str = (f' from {self.giver})', f'')[self.giver is None]
        return f"{super().__repr__()}{self.taker.name} takes {self.taken}{from_str}{super().get_times_str()}"

    def execute(self):
        # act = Relation(left=self.giver, r_type=RelationType.ACTION, right=self.taker r_tense=self.r_tense, negation=self.negation)
        return super().execute()
