from agent import Agent
from typing import List
from pick import pick
import questionary


class DialogueSystem:
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def run(self, turns=10):
        for i in range(0, turns):
            self.next()

    def next(self):
        for agent in self.agents:
            if agent.auto:
                agent.act()
            else:
                self.wait_for_user_input()
                agent.act_event(None)

    def wait_for_user_input(self):
        choose_type_of_event_question = 'Please choose which type of event you want to send'
        options = ['Text', 'Gesture']
        questionary.select(choose_type_of_event_question, options).ask()
