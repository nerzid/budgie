from __future__ import annotations

from typing import List

from socialds.action.action_obj import ActionObjType
from socialds.action.effects.effect import Effect
from socialds.action.simple_action import SimpleAction
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.resource import Resource


class AffirmOrDeny(SimpleAction):
    def __init__(self, name: str, done_by: Agent | DSTPronoun, recipient: Agent | DSTPronoun = None, target_resource: Resource = None,
                 base_effects: List[Effect] = None, extra_effects: List[Effect] = None):
        super().__init__(name, done_by, ActionObjType.VERBAL, recipient=recipient, target_resource=target_resource,
                         base_effects=base_effects, extra_effects=extra_effects)
