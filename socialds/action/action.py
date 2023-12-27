from __future__ import annotations

from abc import abstractmethod
from copy import deepcopy
from typing import List

from socialds.action.action_obj import ActionObj, ActionObjType
from socialds.action.action_time import ActionTime
from socialds.action.effects.effect import Effect
import socialds.agent as a
from socialds.any.any_agent import AnyAgent
from socialds.any.any_resource import AnyResource
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.socialpractice.context.resource import Resource


class Action(ActionObj):
    def __init__(self, name, done_by: a.Agent | DSTPronoun,
                 act_type: ActionObjType,
                 base_effects: List[Effect],
                 extra_effects: List[Effect] = None,
                 recipient: a.Agent | DSTPronoun | AnyAgent = None,
                 target_resource: Resource | AnyResource = None,
                 preconditions=None,
                 times: List[ActionTime] = None,
                 specific=False):
        self.done_by = done_by
        self.recipient = recipient
        self.target_resource = target_resource
        self.specific = specific
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

    def __eq__(self, other):
        if isinstance(other, Action):
            return ((self.name == other.name)
                    and (self.done_by == other.done_by or isinstance(other.done_by, AnyAgent) or isinstance(self.done_by, AnyAgent))
                    and (self.act_type == other.act_type or other.act_type == ActionObjType.ANY)
                    and (self.recipient == other.recipient or isinstance(other.recipient, AnyAgent))
                    and (self.target_resource == other.target_resource or isinstance(self.target_resource, AnyResource))
                    and (self.base_effects == other.base_effects)
                    and (self.extra_effects == other.extra_effects))
        elif isinstance(other, Effect):
            # this uses the __eq__ in Effect class. This code exist to cop&paste the same code in the Effect class
            return other == self
        return False

    @abstractmethod
    def get_requirement_holders(self) -> List:
        """
        Returns instances that can have requirements.
        At the moment, it resources and places only.

        All subclasses should implement this method
        """
        return []

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
        for effect in self.base_effects:
            effect.insert_pronouns()
        for effect in self.extra_effects:
            effect.insert_pronouns()
        for time in self.times:
            time.insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()

    # def update(self, key: SemanticEvent, value: any):
    #     self.semantic_roles[key] = value
    #     return self

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
