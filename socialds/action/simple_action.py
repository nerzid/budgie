from __future__ import annotations

from abc import abstractmethod
from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.effect import Effect
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.resource import Resource


class SimpleAction(Action):

    @staticmethod
    def get_class_attr_mapping():
        return Action.get_class_attr_mapping()

    def __init__(self, name: str, done_by: Agent | DSTPronoun, act_type: ActionObjType,
                 recipient: Agent | DSTPronoun = None, target_resource: Resource = None,
                 base_effects: List[Effect] = None, extra_effects: List[Effect] = None):
        if base_effects is None:
            base_effects = []
        super().__init__(name, done_by, act_type, recipient=recipient, target_resource=target_resource,
                         base_effects=base_effects, extra_effects=extra_effects)

    def __str__(self):
        return "%s %s" % (self.done_by, self.name)

    # def __repr__(self):
    #     return "%r %r" % (self.done_by, self.name)

    def get_requirement_holders(self) -> List:
        requirement_holders = []
        if self.done_by is not None:
            requirement_holders.append(self.done_by)
        if self.recipient is not None:
            requirement_holders.append(self.recipient)
        if self.target_resource is not None:
            requirement_holders.append(self.target_resource)
        return requirement_holders
