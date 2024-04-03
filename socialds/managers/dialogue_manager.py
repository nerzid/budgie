import datetime
from typing import List
from uuid import UUID

from socialds.action.action import Action
from socialds.agent import Agent
from socialds.enums import DSAction, DSActionByType, Tense
from socialds.managers.session_manager import SessionManager
from socialds.managers.utterances_manager import UtterancesManager
from socialds.message import Message
from socialds.message_streamer import MessageStreamer
from socialds.other.event_listener import EventListener
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.place import Place
from socialds.socialpractice.context.resource import Resource
from socialds.states.relation import Relation, RType
from socialds.strategies.turntaking.turntaking import TurnTaking
from socialds.utterance import Utterance


class DialogueManager:
    def __init__(self,
                 dm_id,
                 agents: List[Agent],
                 utterances: List[Utterance],
                 actions: List[Action],
                 places: List[Place],
                 resources: List[Resource],
                 dialogue_history: RelationStorage = None,
                 session_manager: SessionManager = None,
                 allow_duplicate_utterances=False):
        self.dm_id = dm_id
        self.actions = actions
        self.resources = resources
        self.places = places
        self.last_time_dm_used_at = datetime.datetime.now()
        if session_manager is None:
            self.session_manager = SessionManager()
        self.agents = agents
        self.utterances_manager = UtterancesManager(utterances)
        self.dialogue_history = dialogue_history
        if self.dialogue_history is None:
            self.dialogue_history = RelationStorage('Dialogue History')
        self.action_history = RelationStorage('Action History')
        self.allow_duplicate_utterances = allow_duplicate_utterances
        self.message_streamer = MessageStreamer()
        self.session_manager = session_manager
        session_manager.message_streamer = self.message_streamer
        self.turntaking_strategy = TurnTaking.AfterUserExecutedAllActions
        self.last_turn_actions = RelationStorage('Last Turn Actions')

        self.on_user_chose_utterance = EventListener()
        self.on_user_executed_all_actions_from_utterance = EventListener()
        self.on_auto_executed_all_actions_from_utterance = EventListener()

        # for age in self.agents:
        #     pronouns = {}
        #     for agent in self.agents:
        #         if age == agent:
        #             pronouns.update({DSTPronoun.I: agent})
        #         else:
        #             pronouns.update({DSTPronoun.YOU: agent})
        #     age.pronouns = pronouns

    def run(self):
        self.session_manager.update_session_statuses(self.agents[0])

        on_user_choose_utterance_list = []
        on_user_executed_all_actions_list = []
        on_auto_choose_utterance_list = []
        on_auto_executed_all_actions_list = []
        on_agent_choose_utterance_list = []
        on_agent_executed_all_actions_list = []

        # start auto agents first
        for agent in self.agents:
            if not agent.auto:
                on_user_choose_utterance_list.append(agent.dialogue_system.on_agent_chose_utterance)
                on_user_executed_all_actions_list.append(
                    agent.dialogue_system.on_agent_executed_all_actions_from_utterance)
            else:
                on_auto_choose_utterance_list.append(agent.dialogue_system.on_agent_chose_utterance)
                on_auto_executed_all_actions_list.append(
                    agent.dialogue_system.on_agent_executed_all_actions_from_utterance)

        on_agent_choose_utterance_list = on_user_choose_utterance_list + on_auto_choose_utterance_list
        on_agent_executed_all_actions_list = on_user_executed_all_actions_list + on_auto_executed_all_actions_list

        for on_agent_executed_all_actions in on_agent_executed_all_actions_list:
            on_agent_executed_all_actions.subscribe(self.renew_last_turn_actions)
            on_agent_executed_all_actions.subscribe(self.send_session_info)

        for agent in self.agents:
            if agent.auto:
                if self.turntaking_strategy == TurnTaking.AfterUserChoseUtterance:
                    for on_user_choose_utterance in on_user_choose_utterance_list:
                        on_user_choose_utterance.subscribe(agent.dialogue_system.act)
                elif self.turntaking_strategy == TurnTaking.AfterUserExecutedAllActions:
                    for on_user_executed_all_actions in on_user_executed_all_actions_list:
                        on_user_executed_all_actions.subscribe(agent.dialogue_system.act)
                # elif self.turntaking_strategy == TurnTaking.WheneverPossible:
                #     self.on_auto_executed_all_actions_from_utterance.subscribe(self.run_auto_agent, agent)
                #     self.run_auto_agent(agent)

        for agent in self.agents:
            # agent.dialogue_system.on_agent_executed_action.subscribe(self.add_action_to_action_history)
            agent.dialogue_system.on_agent_chose_utterance.subscribe(self.add_utterance_to_dialogue_history)
            if not self.allow_duplicate_utterances:
                agent.dialogue_system.on_agent_chose_utterance.subscribe(self.remove_utterance)
            agent.dialogue_system.on_agent_executed_action.subscribe(self.session_manager.update_session_statuses,
                                                                     agent)

        for agent in self.agents:
            agent.message_streamer = self.message_streamer
            agent.session_manager = self.session_manager
            agent.utterances_manager = self.utterances_manager
            agent.dialogue_system.action_history = self.action_history
            agent.dialogue_system.dialogue_history = self.dialogue_history
            agent.dialogue_system.last_turn_actions = self.last_turn_actions

    def choose_menu_option(self, agent, menu_option, receiver):
        if menu_option == 'All Utterances':
            self.message_streamer.add(Message(ds_action=DSAction.REQUEST_USER_CHOOSE_UTTERANCE.value,
                                              ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                                              ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                              message=self.get_all_utterances()))
        elif menu_option == 'Planned Utterances':
            from socialds.other.dst_pronouns import DSTPronoun
            agent.pronouns[DSTPronoun.YOU] = receiver
            self.message_streamer.add(Message(ds_action=DSAction.REQUEST_USER_CHOOSE_UTTERANCE.value,
                                              ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                                              ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                              message=agent.dialogue_system.get_planned_utterances()))

    def get_menu_options(self):
        self.message_streamer.add(Message(ds_action=DSAction.REQUEST_USER_CHOOSE_MENU_OPTION.value,
                                          ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                          message=['All Utterances', 'Planned Utterances', 'Verbal Act', 'Physical Act',
                                                   'Functional Act', 'Mental Act'],
                                          ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value))

    def get_action_attrs_by_name(self, action_name):
        return self.get_action_attrs(self.get_action_by_name(action_name))

    def get_action_attrs(self, action):
        attrs_dict = {}
        for attr, val_list in action.get_class_attr_mapping().items():
            attrs_dict[attr] = []
            for val in val_list:
                if isinstance(val, Agent):
                    attrs_dict[attr].extend(self.agents)
                elif isinstance(val, Resource):
                    attrs_dict[attr].extend(self.resources)
                elif isinstance(val, Place):
                    attrs_dict[attr].extend(self.places)
        return attrs_dict

    def get_action_by_name(self, action_name):
        for a in self.actions:
            if action_name == a.name:
                return a

    def get_all_utterances(self):
        utts_str = []
        for utt in self.utterances_manager.utterances:
            utts_str.append(str(utt))
        return utts_str

    def get_utterance_from_string(self, utterance):
        for utt in self.utterances_manager.utterances:
            if utterance == str(utt):
                return utt

    def get_agent_by_name(self, agent_name: str):
        for agent in self.agents:
            if agent.name == agent_name:
                return agent

    def get_agent_by_id(self, agent_id):
        for agent in self.agents:
            if agent.agent_id == UUID(agent_id):
                return agent

    def remove_utterance(self, utterance, **kwargs):
        self.utterances_manager.utterances.remove(utterance)

    def add_utterance_to_dialogue_history(self, agent, utterance):
        self.dialogue_history.add(Relation(left=agent,
                                           rtype=RType.SAYS,
                                           rtense=Tense.PAST,
                                           right=utterance))

    # def add_utterance_to_dialogue_history(self, utterance):
    #     self.dialogue_history.add()

    def renew_last_turn_actions(self, agent, actions):
        self.last_turn_actions.remove_all()
        for action in actions:
            self.last_turn_actions.add(Relation(left=agent,
                                                rtype=RType.ACTION,
                                                rtense=Tense.PAST,
                                                right=action))
        self.session_manager.update_session_statuses(agent)

    def send_session_info(self, agent, actions):
        self.message_streamer.add(
            message=Message(ds_action=DSAction.SESSIONS_INFO.value, ds_action_by="Dialogue Manager",
                            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                            message=self.session_manager.get_sessions_info_dict(agent)))

    @staticmethod
    def communicate(message, sender: Agent, receiver: Agent):
        if sender.auto:
            sender.dialogue_system.act(beneficiary=receiver)
        else:
            sender.dialogue_system.act(utterance=message, beneficiary=receiver)
