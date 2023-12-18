from __future__ import annotations

from copy import copy
from typing import List

from socialds.action.action_obj import ActionObj, ActionObjType
from socialds.action.action_time import ActionTime
from socialds.action.effects.effect import Effect
from socialds.agent import Agent
from socialds.any.any_agent import AnyAgent
from socialds.any.any_resource import AnyResource
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.socialpractice.context.resource import Resource


class Action(ActionObj):
    def __init__(self, name, done_by: Agent | DSTPronoun,
                 act_type: ActionObjType, base_effects: List[Effect],
                 recipient: Agent | DSTPronoun | AnyAgent = None,
                 target_resource: Resource | AnyResource = None,
                 extra_effects: List[Effect] = None,
                 preconditions=None,
                 times: List[ActionTime] = None):
        self.done_by = done_by
        self.recipient = recipient
        self.target_resource = target_resource
        if times is None:
            times = []
        if extra_effects is None:
            extra_effects = []
        self.times = times
        if preconditions is None:
            preconditions = []
        self.name = name
        self.preconditions = preconditions
        super().__init__(name, act_type, base_effects, extra_effects)

    def __eq__(self, other: Action):
        copied_action = copy(other)
        copied_action.insert_pronouns()
        return ((self.name == copied_action.name)
                and (self.done_by == copied_action.done_by or isinstance(copied_action.done_by, AnyAgent) or isinstance(self.done_by, AnyAgent))
                and (self.act_type == copied_action.act_type or copied_action.act_type == ActionObjType.ANY)
                and (self.recipient == copied_action.recipient or isinstance(copied_action.recipient, AnyAgent))
                and (self.target_resource == copied_action.target_resource or isinstance(self.target_resource, AnyResource))
                and (self.base_effects == copied_action.base_effects)
                and (self.extra_effects == copied_action.extra_effects))

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
            self.done_by = pronouns[self.done_by]
        if isinstance(self.recipient, DSTPronoun):
            self.recipient = pronouns[self.recipient]
        for time in self.times:
            time.insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()

    # def update(self, key: SemanticEvent, value: any):
    #     self.semantic_roles[key] = value
    #     return self

    def change_done_by(self, agent: Agent | DSTPronoun):
        self.done_by = agent

    def change_recipient(self, agent: Agent | DSTPronoun):
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
