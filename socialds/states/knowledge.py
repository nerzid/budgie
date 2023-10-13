from agent import Agent
from states.state import State


class Knowledge(State):
    def __init__(self, agent: Agent, value):
        super().__init__()
        self.agent = agent
        self.value = value
