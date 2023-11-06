from socialds.relationstorage import RelationStorage
from socialds.agent import Agent
from typing import List
# from pick import pick
import questionary

from socialds.utterance import Utterance
from socialds.states.relation import Relation, RelationType, RelationTense


class DialogueSystem:
    def __init__(self, agents: List[Agent], utterances: List[Utterance], history=RelationStorage('History', is_private=False)):
        self.history = history
        self.agents = agents
        self.utterances = utterances

    def run(self, turns=4):
        for i in range(0, turns):
            self.next()

    def next(self):
        for agent in self.agents:
            end_turn = False
            while not end_turn:
                if agent.auto:
                    self.history.add(Relation(left=agent,
                                              r_type=RelationType.ACTION,
                                              r_tense=RelationTense.PAST,
                                              right=agent.act()))
                else:
                    actions, end_turn = self.get_user_input(agent)
                    for action in actions:
                        self.history.add(Relation(left=agent,
                                                  r_type=RelationType.ACTION,
                                                  r_tense=RelationTense.PAST,
                                                  right=action))
                    print(agent.actor.knowledgebase)
                    print(self.history)

    def get_user_input(self, agent):
        choose_type_of_event_question = f'{agent.actor.name} chooses to do...'
        act_options = ['Utterance', 'Physical Act']
        type_of_event = questionary.select(choose_type_of_event_question, act_options).ask()
        utts_str = []
        for utt in self.utterances:
            utts_str.append(str(utt))
        if type_of_event == 'Utterance':
            selected_utt_str = questionary.select("Choose an utterance", utts_str).ask()

        for utt in self.utterances:
            if selected_utt_str == str(utt):
                selected_utt = utt
                break

        end_turn = questionary.select("End turn?", ["Yes", "No"]).ask()
        # print(end_turn)
        return selected_utt.actions, end_turn == "Yes"

        # questionary.print("You wrote: " + str(utt))
        # elif type_of_event == 'Gesture':
        #     questionary.select('What gesture do you want to send?', ['Hand Wave', 'Point at {resource}']).ask()