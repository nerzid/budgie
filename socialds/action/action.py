from __future__ import annotations

import eventlet

from abc import abstractmethod
from enum import Enum
from typing import List

from socialds.DSTPronounHolder import DSTPronounHolder
# import asyncio


from socialds.action.action_obj import ActionObj, ActionObjType
from socialds.action.action_time import ActionHappenedAtTime
from socialds.action.effects.effect import Effect
import socialds.agent as a
from socialds.any.any_agent import AnyAgent
from socialds.any.any_resource import AnyResource
from socialds.enums import DSActionByType, DSAction
from socialds.message import Message
from socialds.other.dst_pronouns import DSTPronoun, get_agent
from socialds.other.event_listener import EventListener
from socialds.socialpractice.context.resource import Resource
from socialds.states.relation import Relation


class ActionFailed(Exception):
    pass


# not_started, ongoing, completed, skipped
# default is not started
# when action is activated, it becomes ongoing
# when the action is finished after duration, it is completed. Effects will play
# when it is finished before duration, it is skipped. Effects may not play. If effect of action already happened,
# then the effect won't be executed

class ExecutionTimeStatus(Enum):
    NOT_STARTED = 'not-started'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    SKIPPED = 'skipped'


class ExecutionTime:
    def __init__(self, duration=2, status=ExecutionTimeStatus.NOT_STARTED):
        self.duration = duration
        self.status = status


class Action(ActionObj):

    def __init__(self, name, done_by: a.Agent | DSTPronoun,
                 act_type: ActionObjType,
                 base_effects: List[Effect],
                 extra_effects: List[Effect] = None,
                 recipient: a.Agent | DSTPronoun | AnyAgent = None,
                 target_resource: Resource | AnyResource = None,
                 target_relations: List[Relation] = None,
                 execution_time=ExecutionTime(),
                 times: List[ActionHappenedAtTime] = None,
                 specific=False):
        self.done_by = done_by
        self.recipient = recipient
        self.target_resource = target_resource
        self.specific = specific
        self.execution_time = execution_time
        self.on_action_finished_executing = EventListener()
        # self.on_action_finished_executing.subscribe(session_manager.update_expectations)
        # self.on_action_finished_executing.subscribe(session_manager.update_session_statuses)

        if times is None:
            times = []
        if extra_effects is None:
            extra_effects = []
        if target_relations is None:
            target_relations = []
        self.target_relations = target_relations
        self.times = times
        self.name = name
        super().__init__(name, act_type, base_effects, extra_effects)

    def __eq__(self, other):
        if isinstance(other, Action):
            return ((self.name == other.name)
                    and (self.done_by == other.done_by or isinstance(other.done_by, AnyAgent) or isinstance(
                        self.done_by, AnyAgent))
                    and (self.act_type == other.act_type or other.act_type == ActionObjType.ANY)
                    and (self.recipient == other.recipient or isinstance(other.recipient, AnyAgent))
                    and (self.target_resource == other.target_resource or isinstance(self.target_resource, AnyResource))
                    and (self.base_effects == other.base_effects)
                    and (self.extra_effects == other.extra_effects))
        elif isinstance(other, Effect):
            # this uses the __eq__ in Effect class. This code exist to cop&paste the same code in the Effect class
            return other == self
        return False

    @staticmethod
    def get_pretty_template():
        pass

    def equals_with_pronouns(self, other, pronouns):
        if isinstance(other, Action):
            from socialds.any.any_action import AnyAction
            if isinstance(other, AnyAction):
                return True
            self_done_by = get_agent(self.done_by, pronouns)
            other_done_by = get_agent(other.done_by, pronouns)
            self_recipient = get_agent(self.recipient, pronouns)
            other_recipient = get_agent(other.recipient, pronouns)

            recipient_equality = True
            if self_recipient is not None:
                recipient_equality = (self_recipient.equals_with_pronouns(other_recipient, pronouns)
                                      or isinstance(other.recipient, AnyAgent) or isinstance(self_recipient, AnyAgent))
            for e1 in self.base_effects:
                found = False
                for e2 in other.base_effects:
                    if e1.equals_with_pronouns(e2, pronouns):
                        found = True
                if not found:
                    return False

            for e1 in self.extra_effects:
                found = False
                for e2 in other.extra_effects:
                    if e1.equals_with_pronouns(e2, pronouns):
                        found = True
                if not found:
                    return False
            for r1 in self.target_relations:
                found = False
                for r2 in other.target_relations:
                    if r1.equals_with_pronouns(r2, pronouns):
                        found = True
                if not found:
                    return False

            return ((self.name == other.name)
                    and (self_done_by.equals_with_pronouns(other_done_by, pronouns)
                         or isinstance(other_done_by, AnyAgent) or isinstance(self_done_by, AnyAgent))
                    and (self.act_type == other.act_type or other.act_type == ActionObjType.ANY)
                    and recipient_equality
                    and (self.target_resource == other.target_resource or isinstance(self.target_resource,
                                                                                     AnyResource)))
        elif isinstance(other, Effect):
            # this uses the __eq__ in Effect class. This code exist to cop&paste the same code in the Effect class
            if len(self.base_effects + self.extra_effects) == 1:
                return (self.base_effects + self.extra_effects)[0].equals_with_pronouns(other, pronouns)
        return False

    @staticmethod
    def get_class_attr_mapping():
        return {
            "Done By": [],
            "Recipients": [],
            "Resources": [],
        }

    def is_action_in_list(self, actions, pronouns):
        for act in actions:
            if self.equals_with_pronouns(act, pronouns):
                return True
        return False

    @abstractmethod
    def get_requirement_holders(self) -> List:
        """
        Returns instances that can have requirements.
        At the moment, it resources and places only.

        All subclasses should implement this method
        """
        requirement_holders = []
        for effect in self.base_effects + self. extra_effects:
            requirement_holders.extend(effect.get_requirement_holders())
        return requirement_holders

    def get_times_str(self):
        if self.times is None:
            return ''
        times_str = ''
        for time in self.times:
            times_str += str(time) + ' AND '
        if len(self.times) > 0:
            times_str = ' ' + times_str[:-5]
        return times_str

    def insert_pronouns(self):
        if isinstance(self.done_by, DSTPronoun):
            self.done_by = self.pronouns[self.done_by]
        if isinstance(self.recipient, DSTPronoun):
            self.recipient = self.pronouns[self.recipient]
        for effect in self.base_effects:
            effect.pronouns = self.pronouns
            effect.insert_pronouns()
        for effect in self.extra_effects:
            effect.pronouns = self.pronouns
            effect.insert_pronouns()
        for time in self.times:
            time.insert_pronouns(self.pronouns)

    @abstractmethod
    def check_preconditions(self, checker):
        return True

    def execute(self, agent, **kwargs):
        self.pronouns = agent.pronouns
        self.insert_pronouns()
        print('Executing {} for {} seconds with pronouns {}'.format(self.name, self.execution_time.duration,
                                                                    self.pronouns))
        agent.message_streamer.add(Message(ds_action=DSAction.LOG_ACTION_START.value,
                                           ds_action_by=self.done_by.name,
                                           ds_action_by_type=DSActionByType.AGENT.value,
                                           message='Executing {} for {} seconds'.format(self.name,
                                                                                        self.execution_time.duration),
                                           duration=self.execution_time.duration))
        # action_manager.ongoing_actions.append(self)

        eventlet.sleep(self.execution_time.duration)
        try:
            super().execute(agent)

            agent.message_streamer.add(Message(ds_action=DSAction.LOG_ACTION_COMPLETED.value,
                                               ds_action_by=self.done_by.name,
                                               ds_action_by_type=DSActionByType.AGENT.value,
                                               message='Execution of {} is completed'.format(self.name),
                                               duration=self.execution_time.duration))
        except Exception as e:
            agent.message_streamer.add(Message(ds_action=DSAction.LOG_ACTION_FAILED.value,
                                               ds_action_by=self.done_by.name,
                                               ds_action_by_type=DSActionByType.AGENT.value,
                                               message='Execution of {} is failed'.format(self.name),
                                               reason='Reason: {}'.format(repr(e))))
        finally:
            # action_manager.remove_action(self, agent)
            self.on_action_finished_executing.invoke(agent=agent, action=self)
            # agent.session_manager.update_session_statuses(agent)

    def change_done_by(self, agent: a.Agent | DSTPronoun):
        self.done_by = agent

    def change_recipient(self, agent: a.Agent | DSTPronoun):
        self.recipient = agent

    def switch_done_by_with_recipient(self):
        # if there is no recipient, then we only need to change done_by
        if self.recipient is None:
            self.done_by = DSTPronoun.YOU if self.done_by == DSTPronoun.I else DSTPronoun.I
        else:
            temp = self.done_by
            self.done_by = self.recipient
            self.recipient = temp

    def switch_done_by_with_recipient_if_not_pronoun(self):
        if self.recipient is None or isinstance(self.done_by, DSTPronoun) or isinstance(self.recipient, DSTPronoun):
            pass
        else:
            temp = self.done_by
            self.done_by = self.recipient
            self.recipient = temp

    # doctor can examine patient's eye using ophthalmoscope
    # Role -can-> Action
    # Doctor -can-> Action(name="eye examination", semantic_roles)
