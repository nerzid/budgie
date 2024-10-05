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
from socialds.states.relation import Negation, Relation


class Inform(Action):

    def __init__(
        self,
        information: Information,
        times: List[ActionHappenedAtTime] = None,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
    ):
        """
        Shares an information relation with another agent.
        Args:
            information: An information relation to be shared with the recipient

            tense: The tense of the action
            negation: The negation of the action
            done_by: An agent or DSTPronoun who shares the information
            recipient: An agent or DSTPronoun who the information is shared with
        """
        self.information = information
        self.tense = tense
        self.negation = negation
        super().__init__(
            name="inform",
            done_by=done_by,
            act_type=ActionObjType.VERBAL,
            base_effects=[GainKnowledge(knowledge=information, affected=recipient)],
            recipient=recipient,
            target_relations=[information],
            times=times,
        )

    def __deepcopy__(self, memodict={}):
        return Inform(self.information, self.times, self.tense, self.negation, self.done_by, self.recipient)


    def __str__(self):
        return "%s informs %s about %s" % (self.done_by, self.information, self.recipient)

    def __repr__(self):
        return "%r informs %r about %r" % (self.done_by, self.information, self.recipient)

    @staticmethod
    def get_pretty_template():
        return "[done_by] informs [information] about [recipient]"

    @staticmethod
    def build_instance_from_effects(done_by, recipient, tense, negation, effects):
        """
        Follows the same order of the self.base_effects

        Args:
            effects (_type_): _description_
        """
        if len(effects) != 1:
            return None
        gain_knowledge_effect: GainKnowledge = effects[0]
        information = gain_knowledge_effect.knowledge
        return Inform(
            information=information,
            done_by=done_by,
            recipient=recipient,
            tense=tense,
            negation=negation,
        )

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns)

    def insert_pronouns(self):
        self.information.pronouns = self.pronouns
        self.information.insert_pronouns()
        super().insert_pronouns()

    def check_preconditions(self, checker):
        return super().check_preconditions(checker) and AgentKnows(
            agent=DSTPronoun.I, knows=self.information, tense=Tense.ANY
        ).check(checker=checker)

    def get_requirement_holders(self) -> List:
        return super().get_requirement_holders() + [self.information]
