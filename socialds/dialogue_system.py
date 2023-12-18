from termcolor import colored

import socialds.simple_DST as dst
from socialds.managers.managers import session_manager
import socialds.other.variables as vars
import socialds.other.dst_pronouns as pronouns
from socialds.action.action import Action
from socialds.relationstorage import RelationStorage, merge_relation_storages
from socialds.agent import Agent
from typing import List
# from pick import pick
import questionary

from socialds.utterance import Utterance
from socialds.states.relation import Relation, RType
from socialds.enums import Tense, TermColor
import socialds.other.dst_pronouns as dst_pronouns
from socialds.other.dst_pronouns import DSTPronoun


class DialogueSystem:
    def __init__(self, agents: List[Agent], utterances: List[Utterance], history: RelationStorage = None):
        if history is not None:
            vars.dialogue_history = merge_relation_storages(vars.dialogue_history, history)
        self.agents = agents
        self.utterances = utterances
        vars.utterances.extend(self.utterances)
        self.session_manager = session_manager
        # self.dst = SimpleDST()

    def run(self, turns=4):
        # [print(agent.info()) for agent in self.agents]
        print(vars.dialogue_history)
        self.session_manager.update_session_statuses()
        print(self.session_manager.get_colorful_sessions_info())

        dst_pronouns.pronouns[DSTPronoun.I] = self.agents[1]
        dst_pronouns.pronouns[DSTPronoun.YOU] = self.agents[0]
        turn = 0
        while turn < turns or len(self.utterances) > 0:
            self.next()
            turn += 1

    def next(self):
        for agent in self.agents:
            end_turn = False
            while not end_turn:
                dst_pronouns.pronouns[DSTPronoun.YOU] = dst_pronouns.pronouns[DSTPronoun.I]
                dst_pronouns.pronouns[DSTPronoun.I] = agent
                # print("PRONOUNS")
                # print(dst_pronouns.pronouns)
                actions = []
                selected_utt = None
                if agent.auto:
                    selected_utt, solution = agent.planner.get_the_best_matching_utterance(agent.planner.plan())
                    print('\n' + str(agent.name) + ' says:\n' +
                          colored(text=str(selected_utt.text), color=TermColor.RED.value) + '\n')
                    print(colored(text="selected to for the solution -> " + str(solution), color=TermColor.GREEN.value))
                    end_turn = True
                else:
                    selected_utt, end_turn = self.get_user_input(agent)
                for action in selected_utt.actions:
                    action.execute()
                    if isinstance(action, Action):
                        vars.dialogue_history.add(Relation(left=agent,
                                                           rtype=RType.ACTION,
                                                           rtense=Tense.PAST,
                                                           right=action))
                self.remove_utterance(selected_utt)
                self.session_manager.update_session_statuses()
                # [print(agent.info()) for agent in self.agents]
                print(vars.dialogue_history)
                print(session_manager.get_colorful_sessions_info())

    def get_user_input(self, agent):
        choose_type_of_act_question = f'{agent.name} chooses to do...'
        act_options = ['Utterance', 'Verbal Act', 'Physical Act', 'Functional Act', 'Mental Act']
        type_of_act = questionary.select(choose_type_of_act_question, act_options).ask()
        global_menu_options = ['Go back to main menu']
        if type_of_act == 'Utterance':
            utts_str = []
            possible_utterances = agent.planner.get_possible_utterances(agent.planner.plan())
            for utt in possible_utterances:
                utts_str.append(str(utt))
            selected_utt_str = questionary.select("Choose an utterance", utts_str).ask()
            for utt in possible_utterances:
                if selected_utt_str == str(utt):
                    end_turn = questionary.select("End turn?", ["Yes", "No"]).ask()
                    return utt, end_turn == "Yes"
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

    def remove_utterance(self, selected_utt):
        self.utterances.remove(selected_utt)
        vars.utterances = self.utterances
