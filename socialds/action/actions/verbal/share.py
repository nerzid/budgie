from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.action_time import ActionHappenedAtTime
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.agent import Agent
from socialds.conditions.agent_knows import AgentKnows
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation


class Share(Action):

    def __init__(self, information: Information, times: List[ActionHappenedAtTime] = None,
                 done_by: Agent | DSTPronoun = DSTPronoun.I, recipient: Agent | DSTPronoun = DSTPronoun.YOU):
        self.information = information
        super().__init__(name="share", done_by=done_by, act_type=ActionObjType.VERBAL,
                         base_effects=[
                             GainKnowledge(knowledge=information, affected=recipient)
                         ],
                         recipient=recipient,
                         times=times)

    def __str__(self):
        return "%s share %s with %s" % (self.done_by, self.information, self.recipient)

    def __repr__(self):
        return "%r share %r with %r" % (self.done_by, self.information, self.recipient)

    @staticmethod
    def get_pretty_template():
        return "[done_by] shares [information] with [recipient]"

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.information == other.information

    def insert_pronouns(self):
        self.information.pronouns = self.pronouns
        self.information.insert_pronouns()
        super().insert_pronouns()

    def check_preconditions(self, checker):
        return super().check_preconditions(checker) and \
            AgentKnows(agent=DSTPronoun.I, knows=self.information, tense=Tense.ANY).check(checker=checker)

    def get_requirement_holders(self) -> List:
        return super().get_requirement_holders() + [self.information]
