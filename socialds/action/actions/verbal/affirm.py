from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.action.effects.social.gain_permit import GainPermit
from socialds.action.effects.social.permit import Permit
from socialds.agent import Agent
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
import socialds.action.actions.verbal.request_confirmation as rc
import socialds.action.actions.verbal.request_action as ra
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Negation, Relation, RType


class Affirm(Action):

    def __init__(
        self,
        affirmed: Information | Action,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
    ):
        self.affirmed = affirmed
        if isinstance(affirmed, Information):
            super().__init__(
                "affirm",
                done_by=done_by,
                act_type=ActionObjType.VERBAL,
                recipient=recipient,
                base_effects=[GainKnowledge(knowledge=affirmed, affected=recipient)],
                target_relations=[affirmed],
            )
        elif isinstance(affirmed, Action):
            if isinstance(affirmed, Permit):
                relation = affirmed.relation
                permit_given_to = affirmed.permit_given_to
                super().__init__(
                    "affirm",
                    done_by=done_by,
                    act_type=ActionObjType.VERBAL,
                    recipient=recipient,
                    base_effects=[
                        GainPermit(permit=relation, affected=permit_given_to)
                    ],
                    target_relations=[affirmed],
                )

    @staticmethod
    def get_pretty_template():
        return "[done_by] affirms [affirmed]"

    def __str__(self):
        return "%s affirms %s for %s" % (self.done_by, self.affirmed, self.recipient)

    def __repr__(self):
        return "%r affirms %r for %r" % (self.done_by, self.affirmed, self.recipient)

    def insert_pronouns(self):
        self.affirmed.pronouns = self.pronouns
        self.affirmed.insert_pronouns()
        super().insert_pronouns()

    def check_preconditions(self, checker):
        super_check = super().check_preconditions(checker)

        if isinstance(self.affirmed, Information):
            return super_check and AgentDoesAction(
                agent=DSTPronoun.YOU,
                tense=Tense.PAST,
                action=Relation(
                    left=DSTPronoun.YOU,
                    rtype=RType.ACTION,
                    rtense=Tense.PAST,
                    right=rc.RequestConfirmation(
                        done_by=DSTPronoun.YOU,
                        asked=self.affirmed,
                        tense=Tense.ANY,
                        recipient=DSTPronoun.I,
                    ),
                ),
            ).check(checker=checker)
        elif isinstance(self.affirmed, Action):
            return super_check and AgentDoesAction(
                agent=DSTPronoun.YOU,
                tense=Tense.PAST,
                action=Relation(
                    left=DSTPronoun.YOU,
                    rtype=RType.ACTION,
                    rtense=Tense.PAST,
                    right=ra.RequestAction(
                        done_by=self.affirmed.done_by,
                        recipient=self.affirmed.recipient,
                        requested=self.affirmed,
                    ),
                ),
            ).check(checker=checker)

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns)
