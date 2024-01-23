from typing import List

from socialds.DSTPronounHolder import DSTPronounHolder
from socialds.action.effects.effect import Effect
from socialds.conditions.SolutionStep import SolutionStep


class ActionObjType:
    VERBAL = 'verbal'
    PHYSICAL = 'physical'
    MENTAL = 'mental'
    OPERATOR = 'op'
    ANY = 'any'

    def __repr__(self) -> str:
        return str(self.name).lower()


class ActionObj(SolutionStep, DSTPronounHolder):
    def __init__(self, name: str, act_type: ActionObjType, base_effects: List[Effect], extra_effects: List[Effect]):
        super(SolutionStep, self).__init__()
        super(DSTPronounHolder, self).__init__()
        self.agent = None
        self.name = name
        self.base_effects = base_effects
        self.extra_effects = extra_effects
        self.act_type = act_type

    def insert_pronouns(self):
        pass

    def execute(self, agent, **kwargs):
        self.agent = agent
        for op in self.base_effects:
            op.pronouns = agent.pronouns
            op.execute(agent)
