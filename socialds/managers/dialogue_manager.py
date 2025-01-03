from copy import deepcopy
import datetime
import inspect
from enum import EnumMeta
from typing import List, Type
from uuid import UUID
import uuid

from flask import session

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
from socialds.managers import session_manager
from socialds.managers.session_manager import SessionManager
from socialds.managers.utterances_manager import UtterancesManager
from socialds.message import Message
from socialds.message_streamer import MessageStreamer
from socialds.other.dst_pronouns import DSTPronoun
from socialds.other.event_listener import EventListener
from socialds.relationstorage import RelationStorage
from socialds.scenarios.scenario import Scenario
from socialds.socialpractice.context.information import Information
from socialds.socialpractice.context.place import Place
from socialds.socialpractice.context.resource import Resource
from socialds.states.property import Property
from socialds.states.relation import Relation, RType, Negation
from socialds.states.value import Value
from socialds.strategies.turntaking.turntaking import TurnTaking
from socialds.utterance import Utterance


class DialogueManager:
    def __init__(
        self,
        scenario: Scenario,
        dialogue_history: RelationStorage = None,
        message_streamer: MessageStreamer = None,
        allow_duplicate_utterances=True,
        sync=True,
    ):
        self.id = str(uuid.uuid4())
        self.scenario = scenario
        self.sync = sync
        self.last_time_dm_used_at = datetime.datetime.now()
        self.utterances_manager = UtterancesManager(scenario)
        self.dialogue_history = dialogue_history
        if self.dialogue_history is None:
            self.dialogue_history = RelationStorage("Dialogue History") # dialogue history is shared between all the agents
        self.action_history = RelationStorage("Action History") # action history is shared between all the agents
        self.allow_duplicate_utterances = allow_duplicate_utterances
        self.message_streamer = message_streamer
        self.session_manager = SessionManager()
        self.session_manager.add_multi_sessions(scenario.sessions)
        self.session_manager.message_streamer = self.message_streamer
        self.turntaking_strategy = TurnTaking.AfterUserExecutedAllActions
        self.last_turn_actions = RelationStorage("Last Turn Actions")

        self.on_user_chose_utterance = EventListener()
        self.on_user_executed_all_actions_from_utterance = EventListener()
        self.on_auto_executed_all_actions_from_utterance = EventListener()

        for agent in self.scenario.agents:
            agent.dialogue_system.sync = self.sync

        # for age in self.agents:
        #     pronouns = {}
        #     for agent in self.agents:
        #         if age == agent:
        #             pronouns.update({DSTPronoun.I: agent})
        #         else:
        #             pronouns.update({DSTPronoun.YOU: agent})
        #     age.pronouns = pronouns

    def run(self):
        self.clear_all_listeners()
        self.set_all_listeners()
        self.session_manager.update_session_statuses(self.scenario.agents[0])

    def renew_callback_listeners(self):
        self.clear_all_listeners()
        self.set_all_listeners()

    def clear_all_listeners(self):
        self.on_user_chose_utterance.unsubscribe_all()
        self.on_user_executed_all_actions_from_utterance.unsubscribe_all()
        self.on_auto_executed_all_actions_from_utterance.unsubscribe_all()

        for agent in self.scenario.agents:
            agent.dialogue_system.clear_listeners()

    def set_all_listeners(self):
        on_user_choose_utterance_list = []
        on_user_executed_all_actions_list = []
        on_auto_choose_utterance_list = []
        on_auto_executed_all_actions_list = []
        on_agent_choose_utterance_list = []
        on_agent_executed_all_actions_list = []

        # start auto agents first
        for agent in self.scenario.agents:
            if not agent.auto:
                on_user_choose_utterance_list.append(
                    agent.dialogue_system.on_agent_chose_utterance
                )
                on_user_executed_all_actions_list.append(
                    agent.dialogue_system.on_agent_executed_all_actions_from_utterance
                )
            else:
                on_auto_choose_utterance_list.append(
                    agent.dialogue_system.on_agent_chose_utterance
                )
                on_auto_executed_all_actions_list.append(
                    agent.dialogue_system.on_agent_executed_all_actions_from_utterance
                )

        on_agent_choose_utterance_list = (
            on_user_choose_utterance_list + on_auto_choose_utterance_list
        )
        on_agent_executed_all_actions_list = (
            on_user_executed_all_actions_list + on_auto_executed_all_actions_list
        )

        for on_agent_executed_all_actions in on_agent_executed_all_actions_list:
            on_agent_executed_all_actions.subscribe(self.renew_last_turn_actions)
            on_agent_executed_all_actions.subscribe(self.send_session_info)

        for agent in self.scenario.agents:
            if agent.auto:
                if self.turntaking_strategy == TurnTaking.AfterUserChoseUtterance:
                    for on_user_choose_utterance in on_user_choose_utterance_list:
                        on_user_choose_utterance.subscribe(agent.dialogue_system.act)
                elif self.turntaking_strategy == TurnTaking.AfterUserExecutedAllActions:
                    for (
                        on_user_executed_all_actions
                    ) in on_user_executed_all_actions_list:
                        on_user_executed_all_actions.subscribe(
                            agent.dialogue_system.act
                        )
                # elif self.turntaking_strategy == TurnTaking.WheneverPossible:
                #     self.on_auto_executed_all_actions_from_utterance.subscribe(self.run_auto_agent, agent)
                #     self.run_auto_agent(agent)

        for agent in self.scenario.agents:
            # agent.dialogue_system.on_agent_executed_action.subscribe(self.add_action_to_action_history)
            agent.dialogue_system.on_agent_chose_utterance.subscribe(
                self.add_utterance_to_dialogue_history
            )
            if not self.allow_duplicate_utterances:
                agent.dialogue_system.on_agent_chose_utterance.subscribe(
                    self.remove_utterance
                )
            agent.dialogue_system.on_agent_executed_action.subscribe(
                self.session_manager.update_session_statuses, agent
            )

        for agent in self.scenario.agents:
            agent.message_streamer = self.message_streamer
            agent.session_manager = self.session_manager
            agent.utterances_manager = self.utterances_manager
            agent.dialogue_system.action_history = self.action_history
            agent.dialogue_system.dialogue_history = self.dialogue_history
            agent.dialogue_system.last_turn_actions = self.last_turn_actions

    def choose_menu_option(self, agent, menu_option, receiver):
        if menu_option == "All Utterances":
            self.message_streamer.add(
                Message(
                    ds_action=DSAction.REQUEST_USER_CHOOSE_UTTERANCE.value,
                    ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                    ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                    message=self.get_all_utterances(),
                )
            )
        elif menu_option == "Planned Utterances":
            from socialds.other.dst_pronouns import DSTPronoun

            agent.pronouns[DSTPronoun.YOU] = receiver
            self.message_streamer.add(
                Message(
                    ds_action=DSAction.REQUEST_USER_CHOOSE_UTTERANCE.value,
                    ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                    ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                    message=agent.dialogue_system.get_planned_utterances(),
                )
            )

    def get_menu_options(self):
        self.message_streamer.add(
            Message(
                ds_action=DSAction.REQUEST_USER_CHOOSE_MENU_OPTION.value,
                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                message=[
                    "All Utterances",
                    "Planned Utterances",
                    "Verbal Act",
                    "Physical Act",
                    "Functional Act",
                    "Mental Act",
                ],
                ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
            )
        )

    def get_action_attrs_by_name(self, action_name):
        return self.get_action_attrs(
            self.get_action_class_name_by_action_name(action_name)
        )

    def get_action_attrs(self, action):
        # Move()
        # Greet()
        attrs_dict = {
            "name": action.__name__,
            "template": getattr(action, "get_pretty_template")(),
            "parameters": {},
        }
        # cls = globals().get(action_name)
        for key, value in inspect.signature(action.__init__).parameters.items():
            if key == "self":
                continue
            if key == "times":
                continue
            if value.annotation == inspect._empty:
                val_list = ["any"]
            elif value.annotation == bool or value.annotation == "bool":
                val_list = ["boolean"]
            elif isinstance(value.annotation, EnumMeta):
                val_list = [value.annotation.__name__]
            else:
                val_list = [x.strip() for x in value.annotation.split("|")]
            for val in val_list:
                if key not in attrs_dict["parameters"]:
                    attrs_dict["parameters"][key] = []
                attrs_dict["parameters"][key].extend(self.get_parameters(val))
        return attrs_dict

    def get_effect_attrs(self, effect):
        attrs_dict = {
            "name": effect.__name__,
            "template": getattr(effect, "get_pretty_template")(),
            "parameters": {},
        }
        # cls = globals().get(action_name)
        for key, value in inspect.signature(effect.__init__).parameters.items():
            if key == "self":
                continue
            if key == "times":
                continue
            if value.annotation == inspect._empty:
                val_list = ["any"]
            elif value.annotation == bool or value.annotation == "bool":
                val_list = ["boolean"]
            elif isinstance(value.annotation, EnumMeta):
                val_list = [value.annotation.__name__]
            else:
                val_list = [x.strip() for x in value.annotation.split("|")]
            for val in val_list:
                if key not in attrs_dict["parameters"]:
                    attrs_dict["parameters"][key] = []
                attrs_dict["parameters"][key].extend(self.get_parameters(val))
        return attrs_dict

    def get_parameters(self, val):
        val = val.replace(
            "'", ""
        )  # for type hints that use 'Agent' instead of Agent to avoid circular imports
        params = []
        if val == Agent.__name__:
            for agent in self.scenario.agents:
                params.append({"type": val, "value": agent.name})
            params.append({"type": val, "value": AnyAgent().name})
        elif val == Resource.__name__:
            for resource in self.scenario.resources:
                params.append({"type": val, "value": resource.name})
            params.append({"type": val, "value": AnyResource().name})
        elif val == Property.__name__:
            for pproperty in self.scenario.properties:
                params.append({"type": val, "value": pproperty.name})
            params.append({"type": val, "value": AnyProperty().name})
        elif val == Place.__name__:
            for place in self.scenario.places:
                params.append({"type": val, "value": place.name})
            params.append({"type": val, "value": AnyPlace().name})
        elif val == Value.__name__:
            for value in self.scenario.values:
                params.append({"type": val, "value": value.name})
            # params.append({'type': val,
            #                'value': AnyValue().name})
        elif val == RType.__name__:
            params.extend(
                [
                    {"type": val, "value": RType.ANY.value},
                    {"type": val, "value": RType.IS.value},
                    {"type": val, "value": RType.HAS.value},
                    {"type": val, "value": RType.IS_AT.value},
                    {"type": val, "value": RType.CAN.value},
                    {"type": val, "value": RType.IS_PERMITTED_TO.value},
                    {"type": val, "value": RType.HAS_REQUIREMENTS.value},
                    {"type": val, "value": RType.ACTION.value},
                    {"type": val, "value": RType.EFFECT.value},
                ]
            )
        elif val == Information.__name__:
            rel_attrs_dict = {"parameters": {}}
            for key, value in inspect.signature(
                Information.__init__
            ).parameters.items():
                if key == "self":
                    continue
                if key == "times":
                    continue
                if value.annotation == inspect._empty:
                    val_list = ["any"]
                elif value.annotation == bool or value.annotation == "bool":
                    val_list = ["boolean"]
                elif isinstance(value.annotation, EnumMeta):
                    val_list = [value.annotation.__name__]
                else:
                    val_list = [x.strip() for x in value.annotation.split("|")]
                for vv in val_list:
                    if key not in rel_attrs_dict["parameters"]:
                        rel_attrs_dict["parameters"][key] = []
                    rel_attrs_dict["parameters"][key].extend(self.get_parameters(vv))
            params.append(
                {
                    "type": val,
                    "value": rel_attrs_dict,
                    "template": Information.get_pretty_template(),
                }
            )
        elif val == Action.__name__:
            action_names = []
            for action in self.scenario.actions:
                action_names.append(action.__name__)
            params.append({"type": val, "value": action_names})
        elif val == Effect.__name__:
            effect_names = []
            for effect in self.scenario.effects:
                effect_names.append(effect.__name__)
            params.append({"type": val, "value": effect_names})
        elif val == Tense.__name__:
            params.extend(
                [
                    {"type": val, "value": Tense.ANY.value},
                    {"type": val, "value": Tense.PAST.value},
                    {"type": val, "value": Tense.PRESENT.value},
                    {"type": val, "value": Tense.FUTURE.value},
                ]
            )
        elif val == Negation.__name__:
            params.extend(
                [
                    {"type": val, "value": Negation.ANY.value},
                    {"type": val, "value": Negation.TRUE.value},
                    {"type": val, "value": Negation.FALSE.value},
                ]
            )
        elif val == "boolean":
            params.extend(
                [
                    {"type": "boolean", "value": False},
                    {"type": "boolean", "value": True},
                ]
            )
        elif val == "any":
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
        for action in self.scenario.actions:
            attrs_list.append(self.get_action_attrs(action))
        return attrs_list

    def get_all_effect_attrs(self):
        attrs_list = []
        for effect in self.scenario.effects:
            attrs_list.append(self.get_effect_attrs(effect))
        return attrs_list

    def get_action_class_name_by_action_name(self, action_name):
        for a in self.scenario.actions:
            if action_name == a.__name__:
                return a

    def get_actions_from_actions_attrs(self, actions_attrs):
        actions = []
        for attrs_dict in actions_attrs:
            actions.append(self.get_action_from_attrs_dict(attrs_dict))
        return actions

    def get_action_from_attrs_dict(self, attrs_dict):
        action_name = attrs_dict["name"]
        del attrs_dict["name"]
        action_class = self.get_action_class_name_by_action_name(action_name)
        action_dict = {}

        for key, attr in attrs_dict["parameters"].items():
            attr_instance = self.get_attr_instance(attr)
            action_dict[key] = attr_instance

        action = action_class(**action_dict)
        return action

    def get_attr_instance(self, attr):
        attr_type = attr["type"]
        attr_value = attr["value"]
        attr_instance = None

        if attr_type == "Agent":
            attr_instance = self.get_agent_by_name(attr_value)
        if attr_type == "Resource":
            attr_instance = self.get_resource_by_name(attr_value)
        if attr_type == "Place":
            attr_instance = self.get_place_by_name(attr_value)
        if attr_type == "Property":
            attr_instance = self.get_property_by_name(attr_value)
        if attr_type == "Value":
            attr_instance = self.get_value_by_name(attr_value)
        if attr_type == "DSTPronoun":
            if attr_value == "I":
                attr_instance = DSTPronoun.I
            elif attr_value == "YOU":
                attr_instance = DSTPronoun.YOU
        if attr_type == "RType":
            if attr_value == RType.ANY.value:
                attr_instance = RType.ANY
            if attr_value == RType.IS.value:
                attr_instance = RType.IS
            if attr_value == RType.IS_AT.value:
                attr_instance = RType.IS_AT
            if attr_value == RType.HAS.value:
                attr_instance = RType.HAS
            if attr_value == RType.IS_PERMITTED_TO.value:
                attr_instance = RType.IS_PERMITTED_TO
            if attr_value == RType.EFFECT.value:
                attr_instance = RType.EFFECT
            if attr_value == RType.ACTION.value:
                attr_instance = RType.ACTION
            if attr_value == RType.CAN.value:
                attr_instance = RType.CAN
            if attr_value == RType.HAS_REQUIREMENTS.value:
                attr_instance = RType.HAS_REQUIREMENTS
        if attr_type == "Tense":
            if attr_value == Tense.ANY.value:
                attr_instance = Tense.ANY
            if attr_value == Tense.PAST.value:
                attr_instance = Tense.PAST
            if attr_value == Tense.PRESENT.value:
                attr_instance = Tense.PRESENT
            if attr_value == Tense.FUTURE.value:
                attr_instance = Tense.FUTURE
        if attr_type == "Negation":
            if attr_value == Negation.ANY.value:
                attr_instance = Negation.ANY
            if attr_value == Negation.FALSE.value:
                attr_instance = Negation.FALSE
            if attr_value == Negation.TRUE.value:
                attr_instance = Negation.TRUE
        if attr_type == "boolean":
            if attr_value == "false":
                attr_instance = False
            if attr_value == "true":
                attr_instance = True
        if attr_type == "Information":
            relation_instance_values = {}
            for k, v in attr_value.items():
                relation_instance_values[k] = self.get_attr_instance(v)
            attr_instance = Information(**relation_instance_values)
        if "Action" in attr_type:
            action_name = attr_type.split("-")[1]
            action_class = self.get_action_class_name_by_action_name(action_name)
            action_instance_values = {}
            for k, v in attr_value.items():
                action_instance_values[k] = self.get_attr_instance(v)
            attr_instance = action_class(**action_instance_values)
        if attr_type == "Effect":
            pass
        return attr_instance

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
        if agent_name == "any-agent":
            return AnyAgent()
        for agent in self.scenario.agents:
            if agent.name == agent_name:
                return agent

    def get_agent_by_id(self, agent_id) -> Agent:
        for agent in self.scenario.agents:
            if str(agent.id) == str(agent_id):
                return agent

    def get_other_agent(self, agent_id) -> Agent:
        for agent in self.scenario.agents:
            if agent.id != agent_id:
                return agent

    def get_resource_by_name(self, r_name):
        if r_name == "any-resource":
            return AnyResource()
        for resource in self.scenario.resources:
            if resource.name == r_name:
                return resource
        return None

    def get_place_by_name(self, p_name):
        if p_name == "any-place":
            return AnyPlace()
        for place in self.scenario.places:
            if place.name == p_name:
                return place
        return None

    def get_property_by_name(self, p_name):
        if p_name == "any-property":
            return AnyProperty()
        for pproperty in self.scenario.properties:
            if pproperty.name == p_name:
                return pproperty
        return None

    def get_effect_by_name(self, e_name):
        for effect in self.scenario.effects:
            if effect.__name__ == e_name:
                return effect
        return None

    def get_value_by_name(self, v_name):
        for val in self.scenario.values:
            if val.name == v_name:
                return val
        return None

    def remove_utterance(self, utterance, **kwargs):
        self.utterances_manager.utterances.remove(utterance)

    def add_utterance_to_dialogue_history(self, agent, utterance):
        self.dialogue_history.add(
            Relation(left=agent, rel_type=RType.SAYS, rel_tense=Tense.PAST, right=utterance)
        )

    # def add_utterance_to_dialogue_history(self, utterance):
    #     self.dialogue_history.add()

    def renew_last_turn_actions(self, agent, actions):
        self.last_turn_actions.remove_all()
        for action in actions:
            self.last_turn_actions.add(
                Relation(
                    left=agent, rel_type=RType.ACTION, rel_tense=Tense.PAST, right=action
                )
            )
        self.session_manager.update_session_statuses(agent)

    def send_session_info(self, agent, actions):
        self.message_streamer.add(
            message=Message(
                ds_action=DSAction.SESSIONS_INFO.value,
                ds_action_by="Dialogue Manager",
                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                message=self.session_manager.get_sessions_info_dict(),
            )
        )

    # @staticmethod
    def communicate(self, message, sender: Agent, receiver: Agent):
        if sender.auto:
            sender.dialogue_system.act(beneficiary=receiver)
        else:
            sender.dialogue_system.act(utterance=message, beneficiary=receiver)

    def communicate_sync(self, message, sender: Agent, receiver: Agent):
        if sender.auto:
            sender.dialogue_system.act_sync(beneficiary=receiver)
            return receiver.dialogue_system.act_sync(beneficiary=sender)
        else:
            sender.dialogue_system.act_sync(utterance=message, beneficiary=receiver)
            return receiver.dialogue_system.act_sync(beneficiary=sender)

    # @staticmethod
    def communicate_with_actions(self, actions, sender: Agent, receiver: Agent):
        if sender.auto:
            sender.dialogue_system.act(beneficiary=receiver)
        else:
            utterance = self.utterances_manager.get_utterance_by_action(actions, sender)
            sender.dialogue_system.act(
                actions=actions, utterance=utterance, beneficiary=receiver
            )
