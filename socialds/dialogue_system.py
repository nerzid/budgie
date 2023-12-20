from typing import List
import logging
# from pick import pick
import questionary
from termcolor import colored

import socialds.other.dst_pronouns as dst_pronouns
import socialds.other.variables as vars
from socialds.action.action import Action
from socialds.agent import Agent
from socialds.enums import Tense, TermColor
from socialds.managers.managers import session_manager
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RelationStorage, merge_relation_storages
from socialds.states.relation import Relation, RType
from socialds.utterance import Utterance


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
        self.session_manager.update_session_statuses()
        # [print(agent.info()) for agent in self.agents]
        # print(vars.dialogue_history)
        # print(self.session_manager.get_colorful_sessions_info())

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
                vars.last_turn_actions = []
                if agent.auto:
                    selected_utt, solution = agent.planner.get_the_best_matching_utterance_with_solution(agent.planner.plan())
                    print('\n' + str(agent.name) + ' says:\n' +
                          colored(text=str(selected_utt.text), color=TermColor.RED.value) + '\n')
                    print(colored(text="selected to for the solution -> " + str(solution), color=TermColor.GREEN.value))
                    end_turn = True
                else:
                    selected_utt, end_turn = self.get_user_input(agent)
                for action in selected_utt.actions:
                    action.execute()
                    if isinstance(action, Action):
                        vars.actions_history.append(action)
                        vars.dialogue_history.add(Relation(left=agent,
                                                           rtype=RType.ACTION,
                                                           rtense=Tense.PAST,
                                                           right=action))
                        vars.last_turn_actions.append(action)
                self.remove_utterance(selected_utt)
                self.update_expectations()
                self.session_manager.update_session_statuses()

    def update_expectations(self):
        for expectation in vars.expectations:
            expectation.update_status()

    def get_user_input(self, agent):
        choose_to_do = f'{agent.name} chooses to do...'
        global_menu_options = ['Go back to main menu']
        mainmenu_options = ['Act', 'Display info']
        act_options = global_menu_options + ['Utterance', 'Verbal Act', 'Physical Act', 'Functional Act', 'Mental Act']
        display_info_options = global_menu_options + ['Sessions', 'Dialogue History', 'Agents']
        selected_option = questionary.select(choose_to_do, mainmenu_options).ask()
        if selected_option == 'Act':
            selected_option = questionary.select(choose_to_do, act_options).ask()
            if selected_option == 'Utterance':
                utts_str = [] + global_menu_options
                possible_utterances_with_solutions = agent.planner.get_possible_utterances_with_solutions(agent.planner.plan())
                for utt in possible_utterances_with_solutions:
                    utts_str.append(str(utt[0]))
                selected_option = questionary.select("Choose an utterance", utts_str).ask()
                for utt in possible_utterances_with_solutions:
                    if selected_option == str(utt[0]):
                        print(f'selected utterance is for the following solution:\n{str(utt[1])}')
                        end_turn = questionary.select("End turn?", ["Yes", "No"]).ask()
                        return utt[0], end_turn == "Yes"
            elif selected_option == 'Verbal Act':
                acts = global_menu_options + ['Acknowledge', 'Backchannel', 'Greet', 'Affirm', 'Deny', 'Thank']
                selected_option = questionary.select("Choose a verbal act", acts).ask()
                if selected_option == 'Go back to main menu':
                    return self.get_user_input(agent)
                else:
                    pass
            elif selected_option == 'Physical Act':
                acts = global_menu_options + ['Examine', 'Open', 'Sit']
                selected_option = questionary.select("Choose a verbal act", acts).ask()
                if selected_option == 'Go back to main menu':
                    return self.get_user_input(agent)
                else:
                    pass
            elif selected_option == 'Functional Act':
                acts = global_menu_options + ['Ask', 'Give', 'Move', 'Notify', 'Permit', 'Request', 'Share']
                selected_option = questionary.select("Choose a verbal act", acts).ask()
                if selected_option == 'Go back to main menu':
                    return self.get_user_input(agent)
                else:
                    pass
            elif selected_option == 'Mental Act':
                acts = global_menu_options + ['Remember', 'Forget', 'Interpret']
                selected_option = questionary.select("Choose a verbal act", acts).ask()
        elif selected_option == 'Display info':
            selected_option = questionary.select(choose_to_do, display_info_options).ask()
            if selected_option == 'Sessions':
                print(self.session_manager.get_colorful_sessions_info())
            elif selected_option == 'Dialogue History':
                print(vars.dialogue_history)
            elif selected_option == 'Agents':
                [print(agent.info()) for agent in self.agents]
            return self.get_user_input(agent)

        if selected_option == 'Go back to main menu':
            return self.get_user_input(agent)

        # questionary.print("You wrote: " + str(utt))
        # elif type_of_act == 'Gesture':
        #     questionary.select('What gesture do you want to send?', ['Hand Wave', 'Point at {resource}']).ask()

    def remove_utterance(self, selected_utt):
        self.utterances.remove(selected_utt)
        vars.utterances.remove(selected_utt)
