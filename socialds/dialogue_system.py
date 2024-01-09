from asyncio import Queue
from enum import Enum
from typing import List, Callable
import logging
# from pick import pick
# import questionary
from termcolor import colored
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

        # self.task_queue = Queue()
        self.on_new_task_added = EventListener()
        # self.on_new_task_added.subscribe(self.run_task)
        # self.dst = SimpleDST()

    def run(self, turns=4):
        self.session_manager.update_session_statuses()
        # [print(agent.info()) for agent in self.agents]
        # print(vars.dialogue_history)
        # print(self.session_manager.get_colorful_sessions_info())

        dst_pronouns.pronouns[DSTPronoun.I] = self.agents[1]
        dst_pronouns.pronouns[DSTPronoun.YOU] = self.agents[0]
        turn = 0
        # while turn < turns or len(self.utterances) > 0:
        #     await self.next()
        #     turn += 1

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

        # await asyncio.create_task(self.task_manager())

        # for agent in self.agents:
        #     if not agent.auto:
        #         self.run_user_controlled_agent(agent)
        # asyncio.get_event_loop().run_forever()

        # for agent in self.agents:
        #     if agent.auto:
        #         self.activate_agent(agent)
        #     else:
        #         selected_utt, continue_dialogue = self.get_user_input(agent)
        #         # task = asyncio.create_task(self.execute_actions_of_utterance(agent, selected_utt))
        #         # await task
        #         self.execute_actions_of_utterance(agent, selected_utt)
        #         # self.update_expectations()
        #         # self.session_manager.update_session_statuses()
        # asyncio.

    # async def run_task_manager(self):
    #     while True:
    #         # Wait for a new task to be added to the queue
    #         task = await self.task_queue.get()
    #         if task is not None:
    #             await task

    # def add_task_to_task_manager(self, task):
    #     self.task_queue.put_nowait(task)
    #     self.on_new_task_added.invoke()


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
        print('WORK FUCK')
        self.on_user_chose_utterance.invoke()
        # if asyncio.get_event_loop().is_closed():
        #     loop = asyncio.new_event_loop()
        #     loop.
        # else:
        # asyncio.ensure_future(self.execute_actions_of_utterance(agent, utterance))
        eventlet.spawn(self.execute_actions_of_utterance, agent, utterance)
        # self.task_queue.put_nowait(task)
        # self.on_new_task_added.invoke()

    # async def task_manager(self):
    #     while True:
    #         await asyncio.sleep(0.1)

    # def run_user_controlled_agent(self, agent):
    #     # loop = asyncio.get_event_loop()
    #     # loop.create_task(self.activate_user_controlled_agent(agent))
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(self.activate_user_controlled_agent(agent))
    #
    def run_auto_agent(self, agent):
        self.activate_auto_agent(agent)
        # loop = asyncio.get_event_loop()
        # loop.create_task(self.activate_auto_agent(agent))

    def activate_auto_agent(self, agent):
        # sleep a few secs before start
        # await asyncio.sleep(3)
        # eventlet.sleep(3)

        selected_utt, solution = agent.planner.get_the_best_matching_utterance_with_solution(agent.planner.plan())
        self.on_auto_chose_utterance.invoke()

        # print('\n' + str(agent.name) + ' says:\n' +
        #       colored(text=str(selected_utt.text), color=TermColor.RED.value) + '\n')
        # print(colored(text="selected to for the solution -> " + str(solution), color=TermColor.GREEN.value))

        message_streamer.add(ds_action_by_type=DSActionByType.AGENT.value,
                             ds_action_by=agent.name,
                             message=selected_utt.text,
                             ds_action=DSAction.DISPLAY_UTTERANCE.value)

        # message_streamer.add(ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
        #                      ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
        #                      message=selected_utt.text,
        #                      ds_action=DSAction.DISPLAY_LOG.value)

        # await self.execute_actions_of_utterance(agent, selected_utt)
        eventlet.spawn(self.execute_actions_of_utterance, agent, selected_utt)

    # async def activate_user_controlled_agent(self, agent):
    #     # selected_utt, continue_dialogue = self.get_user_input(agent)
    #     utterances = self.get_all_utterances_for_user()
    #
    #     message_streamer.add(ds_action_by_type=DSActionByType.AGENT, ds_action_by=agent.name,
    #                          message=selected_utt.text, ds_action=DSAction.DISPLAY_UTTERANCE)
    #     self.on_user_chose_utterance.invoke()
    #     # await self.execute_actions_of_utterance(agent, selected_utt)
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(self.execute_actions_of_utterance(agent, selected_utt))
    #
    #     # call again to get new user input
    #     self.run_user_controlled_agent(agent)
    #
    #     # asyncio.run(self.execute_actions_of_utterance(agent, selected_utt))
    #
    # # async def next(self):
    # #     for agent in self.agents:
    # #         continue_dialogue = True
    # #         # while continue_dialogue:
    # #         dst_pronouns.pronouns[DSTPronoun.YOU] = dst_pronouns.pronouns[DSTPronoun.I]
    # #         dst_pronouns.pronouns[DSTPronoun.I] = agent
    # #         # print("PRONOUNS")
    # #         # print(dst_pronouns.pronouns)
    # #         actions = []
    # #         selected_utt = None
    # #         vars.last_turn_actions = []
    # #         if agent.auto:
    # #             selected_utt, solution = agent.planner.get_the_best_matching_utterance_with_solution(
    # #                 agent.planner.plan())
    # #             print('\n' + str(agent.name) + ' says:\n' +
    # #                   colored(text=str(selected_utt.text), color=TermColor.RED.value) + '\n')
    # #             print(colored(text="selected to for the solution -> " + str(solution), color=TermColor.GREEN.value))
    # #             continue_dialogue = True
    # #         else:
    # #             selected_utt, continue_dialogue = await self.get_user_input(agent)
    # #             self.execute_actions_of_utterance(agent, selected_utt)
    # #         # Execute actions of the utterance
    # #
    # #         # Update stuff
    # #         # self.remove_utterance(selected_utt)
    # #         self.update_expectations()
    # #         self.session_manager.update_session_statuses()

    def execute_actions_of_utterance(self, agent, utterance):
        print('EXECUTING ACTIONS NOW')
        for action in utterance.actions:
            if isinstance(action, ActionOperator):
                continue
            # task = asyncio.get_event_loop().create_task(action.execute())
            eventlet.spawn(action.execute)
            # await task
            if isinstance(action, Action):
                vars.actions_history.append(action)
                vars.dialogue_history.add(Relation(left=agent,
                                                   rtype=RType.ACTION,
                                                   rtense=Tense.PAST,
                                                   right=action))
                vars.last_turn_actions.append(action)

            if not agent.auto:
                self.on_user_executed_all_actions_from_utterance.invoke()
            else:
                self.on_auto_executed_all_actions_from_utterance.invoke()

            self.update_expectations()
            self.session_manager.update_session_statuses()

    def update_expectations(self):
        for expectation in vars.expectations:
            expectation.update_status()

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
        message_streamer.add(ds_action=DSAction.REQUEST_USER_CHOOSE_MENU_OPTION.value,
                             ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                             ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                             message=utts_str)
        # selected_option = questionary.select("Choose an utterance", utts_str).ask()
        # for utt in possible_utterances_with_solutions:
        #     if selected_option == str(utt[0]):
        #         return utt

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
