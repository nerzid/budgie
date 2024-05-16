from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.action.effects.social.set_state import SetState
from socialds.agent import Agent
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
import socialds.action.actions.verbal.request_confirmation as rc
from socialds.socialpractice.context.information import Information
from socialds.states.property import Property
from socialds.states.relation import Negation, Relation, RType


class Worry(Action):

    def __init__(
        self,
        about: Information,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
    ):
        self.about = about
        self.tense = tense
        self.negation = negation
        super().__init__(
            "worry",
            done_by=done_by,
            recipient=recipient,
            act_type=ActionObjType.VERBAL,
            base_effects=[SetState(state=Property("worried"), affected=done_by)],
            target_relations=[about],
        )

    @staticmethod
    def get_pretty_template():
        return "[done_by] worries about [about]"

    def __str__(self):
        return "%s worries about %s" % (self.done_by, self.about)

    def __repr__(self):
        return "%r worries about %r" % (self.done_by, self.about)

    def insert_pronouns(self):
        self.about.pronouns = self.pronouns
        self.about.insert_pronouns()
        super().insert_pronouns()

    # def check_preconditions(self, checker):
    #     return super().check_preconditions(checker) and \
    #         AgentDoesAction(agent=DSTPronoun.YOU, action=Relation(left=DSTPronoun.YOU, rtype=RType.ACTION,
    #                                                               rtense=Tense.PAST,
    #                                                               right=rc.RequestConfirmation(done_by=DSTPronoun.YOU,
    #                                                                                            asked=self.affirmed,
    #                                                                                            tense=Tense.ANY,
    #                                                                                            recipient=DSTPronoun.I)),
    #                         tense=Tense.PAST).check(checker=checker)

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns)
