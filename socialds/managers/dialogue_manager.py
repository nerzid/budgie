import datetime
import inspect
from enum import EnumMeta
from typing import List, Type
from uuid import UUID

from socialds.action.action import Action
from socialds.action.actions.physical.move import Move
from socialds.action.actions.verbal.greet import Greet
from socialds.action.effects.effect import Effect
from socialds.agent import Agent
from socialds.any.any_agent import AnyAgent
from socialds.any.any_place import AnyPlace
from socialds.any.any_property import AnyProperty
from socialds.any.any_resource import AnyResource
from socialds.enums import DSAction, DSActionByType, Tense
from socialds.managers.session_manager import SessionManager
from socialds.managers.utterances_manager import UtterancesManager
from socialds.message import Message
from socialds.message_streamer import MessageStreamer
from socialds.other.dst_pronouns import DSTPronoun
from socialds.other.event_listener import EventListener
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.place import Place
from socialds.socialpractice.context.resource import Resource
from socialds.states.property import Property
from socialds.states.relation import Relation, RType
from socialds.strategies.turntaking.turntaking import TurnTaking
from socialds.utterance import Utterance


class DialogueManager:
    def __init__(self,
                 dm_id,
                 agents: List[Agent],
                 utterances: List[Utterance],
                 actions: List[Type[Action]],
                 places: List[Place],
                 properties: List[Property],
                 resources: List[Resource],
                 dialogue_history: RelationStorage = None,
                 session_manager: SessionManager = None,
                 allow_duplicate_utterances=False):
        self.dm_id = dm_id
        self.actions = actions
        self.properties = properties
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
        return self.get_action_attrs(self.get_action_class_name_by_action_name(action_name))

    def get_action_attrs(self, action):
        # Move()
        # Greet()
        attrs_dict = {
            'name': action.__name__,
            'template': getattr(action, 'get_pretty_template')(),
            'parameters': {}
        }
        # cls = globals().get(action_name)
        for key, value in inspect.signature(action.__init__).parameters.items():
            if key == "self":
                continue
            if key == 'times':
                continue
            if value.annotation == inspect._empty:
                val_list = ['any']
            elif value.annotation == bool or value.annotation == 'bool':
                val_list = ['boolean']
            elif isinstance(value.annotation, EnumMeta):
                val_list = [value.annotation.__name__]
            else:
                val_list = [x.strip() for x in value.annotation.split("|")]
            for val in val_list:
                if key not in attrs_dict['parameters']:
                    attrs_dict['parameters'][key] = []
                attrs_dict['parameters'][key].extend(self.get_parameters(val))
        return attrs_dict

    def get_parameters(self, val):
        params = []
        if val == Agent.__name__:
            for agent in self.agents:
                params.append({'type': val,
                               'value': agent.name})
            params.append({'type': val,
                           'value': AnyAgent().name})
        elif val == Resource.__name__:
            for resource in self.resources:
                params.append({'type': val,
                               'value': resource.name})
            params.append({'type': val,
                           'value': AnyResource().name})
        elif val == Property.__name__:
            for pproperty in self.properties:
                params.append({'type': val,
                               'value': pproperty.name})
            params.append({'type': val,
                           'value': AnyProperty().name})
        elif val == Place.__name__:
            for place in self.places:
                params.append({'type': val,
                               'value': place.name})
            params.append({'type': val,
                           'value': AnyPlace().name})
        elif val == RType.__name__:
            params.extend([{'type': val,
                            'value': RType.ANY.value},
                           {'type': val,
                            'value': RType.IS.value},
                           {'type': val,
                            'value': RType.HAS.value},
                           {'type': val,
                            'value': RType.IS_AT.value},
                           {'type': val,
                            'value': RType.CAN.value},
                           {'type': val,
                            'value': RType.IS_PERMITTED_TO.value},
                           {'type': val,
                            'value': RType.HAS_REQUIREMENTS.value},
                           {'type': val,
                            'value': RType.ACTION.value},
                           {'type': val,
                            'value': RType.EFFECT.value}
                           ])
        elif val == Relation.__name__:
            rel_attrs_dict = {'parameters': {}}
            for key, value in inspect.signature(Relation.__init__).parameters.items():
                if key == "self":
                    continue
                if key == 'times':
                    continue
                if value.annotation == inspect._empty:
                    val_list = ['any']
                elif value.annotation == bool or value.annotation == 'bool':
                    val_list = ['boolean']
                elif isinstance(value.annotation, EnumMeta):
                    val_list = [value.annotation.__name__]
                else:
                    val_list = [x.strip() for x in value.annotation.split("|")]
                for vv in val_list:
                    if key not in rel_attrs_dict['parameters']:
                        rel_attrs_dict['parameters'][key] = []
                    rel_attrs_dict['parameters'][key].extend(self.get_parameters(vv))
            params.append({'type': val,
                           'value': rel_attrs_dict,
                           'template': Relation.get_pretty_template()})
        elif val == Action.__name__:
            pass
        elif val == Effect.__name__:
            pass
        elif val == Tense.__name__:
            params.extend([{'type': val,
                            'value': Tense.ANY.value},
                           {'type': val,
                            'value': Tense.PAST.value},
                           {'type': val,
                            'value': Tense.PRESENT.value},
                           {'type': val,
                            'value': Tense.FUTURE.value}])
        elif val == 'boolean':
            # pass
            params.extend([{'type': 'boolean',
                            'value': False},
                           {'type': 'boolean',
                            'value': True}
                           ])
        elif val == 'any':
            params.extend(self.get_parameters(Agent.__name__))
            params.extend(self.get_parameters(Resource.__name__))
            params.extend(self.get_parameters(Place.__name__))
            params.extend(self.get_parameters(Property.__name__))
            # params.extend(self.get_parameters(RType.__name__))
            # params.extend(self.get_parameters(Tense.__name__))
            params.extend(self.get_parameters(Action.__name__))
            params.extend(self.get_parameters(Effect.__name__))
            # params.extend(self.get_parameters(Relation.__name__))
            # params.extend(self.get_parameters('boolean'))
            # params.extend(self.get_parameters('any'))
            # params.extend(self.get_parameters(None))
        elif val is None:
            params.append(None)
        return params

    def get_all_action_attrs(self):
        attrs_list = []
        for action in self.actions:
            attrs_list.append(self.get_action_attrs(action))
        return attrs_list

    def get_action_class_name_by_action_name(self, action_name):
        for a in self.actions:
            if action_name == a.__name__:
                return a

    def get_actions_from_actions_attrs(self, actions_attrs):
        actions = []
        for attrs_dict in actions_attrs:
            actions.append(self.get_action_from_attrs_dict(attrs_dict))
        return actions

    def get_action_from_attrs_dict(self, attrs_dict):
        action_name = attrs_dict['name']
        del attrs_dict['name']
        action_class = self.get_action_class_name_by_action_name(action_name)
        action_dict = {}

        for key, attr in attrs_dict['parameters'].items():
            attr_instance = None
            attr_type = attr['type']
            attr_value = attr['value']
            if attr_type == 'Agent':
                attr_instance = self.get_agent_by_name(attr_value)
            if attr_type == 'Resource':
                attr_instance = self.get_resource_by_name(attr_value)
            if attr_type == 'Place':
                attr_instance = self.get_place_by_name(attr_value)
            if attr_type == 'DSTPronoun':
                if attr_value == 'I':
                    attr_instance = DSTPronoun.I
                elif attr_value == 'YOU':
                    attr_instance = DSTPronoun.YOU
            action_dict[key] = attr_instance

        action = action_class(**action_dict)
        return action

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
        if agent_name == 'any-agent':
            return AnyAgent()
        for agent in self.agents:
            if agent.name == agent_name:
                return agent

    def get_agent_by_id(self, agent_id):
        for agent in self.agents:
            if agent.agent_id == UUID(agent_id):
                return agent

    def get_resource_by_name(self, r_name):
        if r_name == 'any-resource':
            return AnyResource()
        for resource in self.resources:
            if resource.name == r_name:
                return resource
        return None

    def get_place_by_name(self, p_name):
        if p_name == 'any-place':
            return AnyPlace()
        for place in self.places:
            if place.name == p_name:
                return place
        return None

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

    @staticmethod
    def communicate_with_actions(actions, sender: Agent, receiver: Agent):
        if sender.auto:
            sender.dialogue_system.act(beneficiary=receiver)
        else:
            sender.dialogue_system.act(actions=actions, beneficiary=receiver)
