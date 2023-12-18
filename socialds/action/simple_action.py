from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.resource import Resource


class SimpleAction(Action):

    def __init__(self, name: str, done_by: Agent | DSTPronoun, act_type: ActionObjType,
                 recipient: Agent | DSTPronoun = None, target_resource: Resource = None):
        super().__init__(name, done_by, act_type, [], recipient=recipient, target_resource=target_resource)

    def __repr__(self):
        return f'{self.done_by} {self.name}'

    def colorless_repr(self):
        return f'{self.done_by} {self.name}'
