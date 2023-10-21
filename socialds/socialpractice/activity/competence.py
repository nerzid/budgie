from socialds.actions.action import Action
from socialds.states.state import State


class Competence(State):
    def __init__(self, name: str, action: Action, negation: False):
        super().__init__()
        self.name = name
        self.action = action
        self.negation = negation
