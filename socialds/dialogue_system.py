from termcolor import colored

import socialds.simple_DST as dst
from socialds.relationstorage import RelationStorage
from socialds.agent import Agent
from typing import List
# from pick import pick
import questionary

from socialds.utterance import Utterance
from socialds.states.relation import Relation, RelationType, RelationTense


class DialogueSystem:
    def __init__(self, agents: List[Agent], utterances: List[Utterance],
                 history=RelationStorage('Dialogue History', is_private=False)):
        self.history = history
        self.agents = agents
        self.utterances = utterances
        # self.dst = SimpleDST()

    def run(self, turns=4):
        [print(agent.info()) for agent in self.agents]
        print(self.history)
        for i in range(0, turns):
            self.next()

    def next(self):
        for agent in self.agents:
            end_turn = False
            while not end_turn:
                dst.me = agent
                if agent.auto:
                    self.history.add(Relation(left=agent,
                                              r_type=RelationType.ACTION,
                                              r_tense=RelationTense.PAST,
                                              right=agent.act()))
                else:
                    actions, end_turn = self.get_user_input(agent)
                    for action in actions:
                        action.execute()
                        self.history.add(Relation(left=agent,
                                                  r_type=RelationType.ACTION,
                                                  r_tense=RelationTense.PAST,
                                                  right=action))
                [print(agent.info()) for agent in self.agents]
                print(self.history)
            dst.you = dst.me
            dst.me = None

    def get_user_input(self, agent):
        choose_type_of_act_question = f'{agent.actor.name} chooses to do...'
        act_options = ['Utterance', 'Verbal Act', 'Physical Act', 'Functional Act', 'Mental Act']
        type_of_act = questionary.select(choose_type_of_act_question, act_options).ask()
        global_menu_options = ['Go back to main menu']
        if type_of_act == 'Utterance':
            utts_str = []
            for utt in self.utterances:
                utts_str.append(str(utt))
            selected_utt_str = questionary.select("Choose an utterance", utts_str).ask()
            for utt in self.utterances:
                if selected_utt_str == str(utt):
                    selected_utt = utt
                    end_turn = questionary.select("End turn?", ["Yes", "No"]).ask()
                    return selected_utt.actions, end_turn == "Yes"
        elif type_of_act == 'Verbal Act':
            acts = ['acknowledge', 'backchannel', 'greet', 'yes', 'no', 'thank'] + global_menu_options
            selected_act_str = questionary.select("Choose a verbal act", acts).ask()
            if selected_act_str == 'Go back to main menu':
                return self.get_user_input(agent)
            else:
                pass
        elif type_of_act == 'Physical Act':
            acts = ['examine', 'open', 'sit'] + global_menu_options
            selected_act_str = questionary.select("Choose a verbal act", acts).ask()
            if selected_act_str == 'Go back to main menu':
                return self.get_user_input(agent)
            else:
                pass
        elif type_of_act == 'Functional Act':
            acts = ['ask', 'give', 'move', 'notify', 'permit', 'request', 'share'] + global_menu_options
            selected_act_str = questionary.select("Choose a verbal act", acts).ask()
            if selected_act_str == 'Go back to main menu':
                return self.get_user_input(agent)
            else:
                pass
        elif type_of_act == 'Mental Act':
            acts = ['remember', 'forget', 'interpret'] + global_menu_options
            selected_act_str = questionary.select("Choose a verbal act", acts).ask()
            if selected_act_str == 'Go back to main menu':
                return self.get_user_input(agent)
            else:
                pass

        # questionary.print("You wrote: " + str(utt))
        # elif type_of_act == 'Gesture':
        #     questionary.select('What gesture do you want to send?', ['Hand Wave', 'Point at {resource}']).ask()
