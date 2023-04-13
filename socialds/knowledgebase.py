from socialds.agent import Agent


class Knowledgebase:
    def __init__(self, is_private: bool, agents: list[Agent], data):
        self.is_private = is_private
        self.agents = agents
        self.data = data
