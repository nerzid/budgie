from __future__ import annotations

from functools import partial
from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.effect import Effect
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation


class Learn(Action):

    def __init__(self, done_by: Agent | DSTPronoun, learned: Information, extra_effects: List[Effect] = None):
        """
        Learns a piece of information as relation. Learn is similar to Share except only agent who does
        the action saves the new information in their knowledgebase.
        :param done_by: The agent who learns the new information
        :param learned: Information to be learned and saved in agent's knowledgebase e.g., patient's eye -has-> inflammation
        """
        self.learned = learned
        super().__init__(name="learn", done_by=done_by,
                         act_type=ActionObjType.VERBAL,
                         base_effects=[
                             GainKnowledge(knowledge=learned, affected=done_by)
                         ], extra_effects=extra_effects
                         )

    def __str__(self):
        return "%s learn %s" % (self.done_by, self.learned)

    def __repr__(self):
        return "%r learn %r" % (self.done_by, self.learned)

    def insert_pronouns(self):
        self.learned.pronouns = self.pronouns
        self.learned.insert_pronouns()
        super().insert_pronouns()
