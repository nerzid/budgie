from socialds.agent import Agent
from typing import List
# from pick import pick
import questionary

from socialds.utterance import Utterance


class DialogueSystem:
    def __init__(self, agents: List[Agent], utterances: List[Utterance], history=None):
        if history is None:
            self.history = []
        else:
            self.history = history
        self.agents = agents
        self.utterances = utterances
        self.utterances_str = []
        for utt in utterances:
            self.utterances_str.append(str(utt))

    def run(self, turns=4):
        for i in range(0, turns):
            self.next()

    def next(self):
        for agent in self.agents:
            end_turn = False
            while not end_turn:
                if agent.auto:
                    self.history.append(agent.act())
                else:
                    end_turn = self.get_user_input(agent)
                    self.history.append(agent.act())

    def get_user_input(self, agent):
        choose_type_of_event_question = f'{agent.actor.name} chooses to do...'
        act_options = ['Utterance', 'Physical Act']
        type_of_event = questionary.select(choose_type_of_event_question, act_options).ask()
        if type_of_event == 'Utterance':
            questionary.select("Choose an utterance", self.utterances_str).ask()

        end_turn = questionary.select("End turn?", ["Yes", "No"]).ask()
        # print(end_turn)
        if end_turn == "Yes":
            return True
        else:
            return False

        # questionary.print("You wrote: " + str(utt))
        # elif type_of_event == 'Gesture':
        #     questionary.select('What gesture do you want to send?', ['Hand Wave', 'Point at {resource}']).ask()