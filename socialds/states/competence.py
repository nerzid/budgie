from actions.action import Action
from agent import Agent
from states.state import State


class Competence(State):
    def __init__(self, action: Action, negation: False):
        super().__init__()
        # self.agent = agent
        self.action = action
        self.negation = negation