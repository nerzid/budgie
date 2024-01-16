import copy
from typing import List
import eventlet
import socialds.other.dst_pronouns as dst_pronouns
import socialds.other.variables as vars
from socialds.action.action import Action
from socialds.action.action_operator import ActionOperator
from socialds.agent import Agent
from socialds.enums import Tense, DSActionByType, DSAction
from socialds.managers.managers import session_manager, message_streamer
from socialds.other.dst_pronouns import DSTPronoun
from socialds.other.event_listener import EventListener
from socialds.relationstorage import RelationStorage, merge_relation_storages
from socialds.states.relation import Relation, RType
from socialds.strategies.turntaking.turntaking import TurnTaking
from socialds.utterance import Utterance


class DialogueSystem:
    def __init__(self, agents: List[Agent], utterances: List[Utterance], history: RelationStorage = None,
                 allow_duplicate_utterances=False):
        if history is not None:
            vars.dialogue_history = merge_relation_storages(vars.dialogue_history, history)
        self.agents = agents
        self.utterances = utterances
        self.allow_duplicate_utterances = allow_duplicate_utterances
        vars.utterances.extend(self.utterances)
        self.session_manager = session_manager
        self.turntaking_strategy = TurnTaking.AfterUserExecutedAllActions

        # delegates
        self.on_user_chose_utterance = EventListener()
        self.on_user_executed_all_actions_from_utterance = EventListener()
        self.on_auto_chose_utterance = EventListener()
        self.on_auto_executed_all_actions_from_utterance = EventListener()

        self.on_new_task_added = EventListener()

        self.auto_reaction_time = 2

        for age in self.agents:
            pronouns = {}
            for agent in self.agents:
                if age == agent:
                    pronouns.update({DSTPronoun.I: agent})
                else:
                    pronouns.update({DSTPronoun.YOU: agent})
            age.pronouns = pronouns

    def run(self, turns=4):
        self.session_manager.update_session_statuses(self.agents[0])

        dst_pronouns.pronouns[DSTPronoun.I] = self.agents[1]
        dst_pronouns.pronouns[DSTPronoun.YOU] = self.agents[0]
        turn = 0

        vars.last_turn_actions = []
        tasks = []

        # start auto agents first
        for agent in self.agents:
            if agent.auto:
                if self.turntaking_strategy == TurnTaking.AfterUserChoseUtterance:
                    self.on_user_chose_utterance.subscribe(self.run_auto_agent, agent)
                elif self.turntaking_strategy == TurnTaking.AfterUserExecutedAllActions:
                    self.on_user_executed_all_actions_from_utterance.subscribe(self.run_auto_agent, agent)
                elif self.turntaking_strategy == TurnTaking.WheneverPossible:
                    self.on_auto_executed_all_actions_from_utterance.subscribe(self.run_auto_agent, agent)
                    self.run_auto_agent(agent)

    def choose_menu_option(self, agent, menu_option):
        if menu_option == 'All Utterances':
            message_streamer.add(ds_action=DSAction.REQUEST_USER_CHOOSE_UTTERANCE.value,
                                 ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                                 ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                 message=self.get_all_utterances())
        elif menu_option == 'Planned Utterances':
            message_streamer.add(ds_action=DSAction.REQUEST_USER_CHOOSE_UTTERANCE.value,
                                 ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                                 ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                 message=self.get_planned_utterances(agent))

    def choose_utterance(self, agent, utterance):
        self.on_user_chose_utterance.invoke()
        message_streamer.add(ds_action_by_type=DSActionByType.AGENT.value,
                             ds_action_by=agent.name,
                             message=utterance.text,
                             ds_action=DSAction.DISPLAY_UTTERANCE.value)
        eventlet.spawn(self.execute_actions_of_utterance, agent, utterance)

    def run_auto_agent(self, agent):
        eventlet.sleep(self.auto_reaction_time)
        self.activate_auto_agent(agent)

    def activate_auto_agent(self, agent):
        selected_utt, solution = agent.planner.get_the_best_matching_utterance_with_solution(agent.planner.plan())
        self.on_auto_chose_utterance.invoke()

        message_streamer.add(ds_action_by_type=DSActionByType.AGENT.value,
                             ds_action_by=agent.name,
                             message=selected_utt.text,
                             ds_action=DSAction.DISPLAY_UTTERANCE.value)
        eventlet.spawn(self.execute_actions_of_utterance, agent, selected_utt)

    def execute_actions_of_utterance(self, agent, utterance):
        print('EXECUTING ACTIONS NOW for agent" {}'.format(agent))
        copied_utt = copy.deepcopy(utterance)
        for action in copied_utt.actions:
            if isinstance(action, ActionOperator):
                continue
            pronouns = {}
            for age in self.agents:
                if age == agent:
                    pronouns.update({DSTPronoun.I: age})
                else:
                    pronouns.update({DSTPronoun.YOU: age})
            print('Pronouns for agent {} are => {}'.format(agent, pronouns))

            eventlet.spawn(action.execute, pronouns)

            if isinstance(action, Action):
                vars.actions_history.append(action)
                vars.dialogue_history.add(Relation(left=agent,
                                                   rtype=RType.ACTION,
                                                   rtense=Tense.PAST,
                                                   right=action))
                vars.last_turn_actions.append(action)

        # self.update_expectations(agent)
        # self.session_manager.update_session_statuses(agent)

        if not self.allow_duplicate_utterances:
            self.remove_utterance(utterance)

        if not agent.auto:
            self.on_user_executed_all_actions_from_utterance.invoke()
        else:
            self.on_auto_executed_all_actions_from_utterance.invoke()


    def get_menu_options(self):
        message_streamer.add(ds_action=DSAction.REQUEST_USER_CHOOSE_MENU_OPTION.value,
                             ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                             message=['All Utterances', 'Planned Utterances', 'Verbal Act', 'Physical Act',
                                      'Functional Act', 'Mental Act'],
                             ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value)

    def get_planned_utterances(self, agent):
        utts_str = []
        possible_utterances_with_solutions = agent.planner.get_possible_utterances_with_solutions(
            agent.planner.plan())
        for utt in possible_utterances_with_solutions:
            utts_str.append(str(utt[0]))
        message_streamer.add(ds_action=DSAction.REQUEST_USER_CHOOSE_UTTERANCE.value,
                             ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                             ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                             message=utts_str)

    def get_all_utterances(self):
        utts_str = []
        for utt in vars.utterances:
            utts_str.append(str(utt))
        return utts_str

    def get_utterance_from_string(self, utterance):
        for utt in vars.utterances:
            if utterance == str(utt):
                return utt

    # def get_user_input(self, agent):
    #     choose_to_do = f'{agent.name} chooses to do...'
    #     global_menu_options = ['Go back to main menu']
    #     mainmenu_options = ['Act', 'Display info']
    #     act_options = global_menu_options + ['All Utterances', 'Planned Utterances', 'Verbal Act', 'Physical Act',
    #                                          'Functional Act', 'Mental Act']
    #     display_info_options = global_menu_options + ['Sessions', 'Dialogue History', 'Agents']
    #     selected_option = questionary.select(choose_to_do, mainmenu_options).ask()
    #     if selected_option == 'Act':
    #         selected_option = questionary.select(choose_to_do, act_options).ask()
    #         if selected_option == 'All Utterances':
    #             utts_str = [] + global_menu_options
    #             for utt in vars.utterances:
    #                 utts_str.append(str(utt))
    #
    #             selected_option = questionary.select("Choose an utterance", utts_str).ask()
    #             for utt in vars.utterances:
    #                 if selected_option == str(utt):
    #                     continue_dialogue = questionary.select("End turn?", ["Yes", "No"]).ask()
    #                     return utt, continue_dialogue == "Yes"
    #         if selected_option == 'Planned Utterances':
    #             utts_str = [] + global_menu_options
    #             possible_utterances_with_solutions = agent.planner.get_possible_utterances_with_solutions(
    #                 agent.planner.plan())
    #             for utt in possible_utterances_with_solutions:
    #                 utts_str.append(str(utt[0]))
    #             selected_option = questionary.select("Choose an utterance", utts_str).ask()
    #             for utt in possible_utterances_with_solutions:
    #                 if selected_option == str(utt[0]):
    #                     print(f'selected utterance is for the following solution:\n{str(utt[1])}')
    #                     continue_dialogue = questionary.select("End turn?", ["Yes", "No"]).ask()
    #                     return utt[0], continue_dialogue == "Yes"
    #         elif selected_option == 'Verbal Act':
    #             acts = global_menu_options + ['Acknowledge', 'Backchannel', 'Greet', 'Affirm', 'Deny', 'Thank']
    #             selected_option = questionary.select("Choose a verbal act", acts).ask()
    #             if selected_option == 'Go back to main menu':
    #                 return self.get_user_input(agent)
    #             else:
    #                 pass
    #         elif selected_option == 'Physical Act':
    #             acts = global_menu_options + ['Examine', 'Open', 'Sit']
    #             selected_option = questionary.select("Choose a verbal act", acts).ask()
    #             if selected_option == 'Go back to main menu':
    #                 return self.get_user_input(agent)
    #             else:
    #                 pass
    #         elif selected_option == 'Functional Act':
    #             acts = global_menu_options + ['Ask', 'Give', 'Move', 'Notify', 'Permit', 'Request', 'Share']
    #             selected_option = questionary.select("Choose a verbal act", acts).ask()
    #             if selected_option == 'Go back to main menu':
    #                 return self.get_user_input(agent)
    #             else:
    #                 pass
    #         elif selected_option == 'Mental Act':
    #             acts = global_menu_options + ['Remember', 'Forget', 'Interpret']
    #             selected_option = questionary.select("Choose a verbal act", acts).ask()
    #     elif selected_option == 'Display info':
    #         selected_option = questionary.select(choose_to_do, display_info_options).ask()
    #         if selected_option == 'Sessions':
    #             print(self.session_manager.get_colorful_sessions_info())
    #         elif selected_option == 'Dialogue History':
    #             print(vars.dialogue_history)
    #         elif selected_option == 'Agents':
    #             [print(agent.info()) for agent in self.agents]
    #         return self.get_user_input(agent)
    #
    #     if selected_option == 'Go back to main menu':
    #         return self.get_user_input(agent)
    #
    #     # questionary.print("You wrote: " + str(utt))
    #     # elif type_of_act == 'Gesture':
    #     #     questionary.select('What gesture do you want to send?', ['Hand Wave', 'Point at {resource}']).ask()

    def get_agent_by_name(self, agent_name: str):
        for agent in self.agents:
            if agent.name == agent_name:
                return agent

    def remove_utterance(self, selected_utt):
        self.utterances.remove(selected_utt)
        vars.utterances.remove(selected_utt)

    def communicate(self, message, receiver):
        pass
