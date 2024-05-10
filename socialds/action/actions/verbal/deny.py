from __future__ import annotations

from copy import deepcopy

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.change_property import GainKnowledge
from socialds.action.effects.social.gain_permit import GainPermit
from socialds.action.effects.social.permit import Permit
from socialds.agent import Agent
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.conditions.agent_knows import AgentKnows
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
import socialds.action.actions.verbal.request_confirmation as rc
import socialds.action.actions.verbal.request_action as ra
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation, RType, Negation


class Deny(Action):
    def __init__(
        self,
        denied: Information | Action,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
    ):
        # denied = deepcopy(
        #     denied
        # )  # BUG here. It gives error when the denied object is of Action. Deepcopy cannot serialize a 'Greenthread' object.
        if isinstance(denied, Information):
            if denied.negation == Negation.FALSE or denied.negation == Negation.ANY:
                self.denied = Information(
                    left=denied.left,
                    rtype=denied.rtype,
                    rtense=denied.rtense,
                    right=denied.right,
                    negation=Negation.TRUE,
                )
            else:
                self.denied = Information(
                    left=denied.left,
                    rtype=denied.rtype,
                    rtense=denied.rtense,
                    right=denied.right,
                    negation=Negation.FALSE,
                )
            super().__init__(
                "deny",
                done_by=done_by,
                recipient=recipient,
                act_type=ActionObjType.VERBAL,
                base_effects=[GainKnowledge(knowledge=self.denied, affected=recipient)],
                target_relations=[self.denied],
            )
        elif isinstance(denied, Action):
            self.denied = denied
            if isinstance(denied, Permit):
                relation = denied.relation
                permit_given_to = denied.permit_given_to
                super().__init__(
                    "deny",
                    done_by=done_by,
                    recipient=recipient,
                    act_type=ActionObjType.VERBAL,
                    base_effects=[
                        GainPermit(permit=relation, affected=permit_given_to)
                    ],
                    target_relations=[denied],
                )

    @staticmethod
    def get_pretty_template():
        return "[done_by] denies [denied]"

    def __str__(self):
        return "%s denies %s for %s" % (self.done_by, self.denied, self.recipient)

    def __repr__(self):
        return "%r denies %r for %r" % (self.done_by, self.denied, self.recipient)

    def equals_with_pronouns(self, other, pronouns):
        return (
            super().equals_with_pronouns(other, pronouns)
            and self.denied == other.denied
        )

    def check_preconditions(self, checker):
        super_check = super().check_preconditions(checker)

        if isinstance(self.denied, Information):
            if not AgentKnows(
                agent=self.done_by,
                knows=self.denied,
                tense=self.denied.rtense,
                negation=self.denied.rtense,
            ):
                return False

            return super_check and AgentDoesAction(
                agent=DSTPronoun.YOU,
                tense=Tense.PAST,
                action=Relation(
                    left=DSTPronoun.YOU,
                    rtype=RType.ACTION,
                    rtense=Tense.PAST,
                    right=rc.RequestConfirmation(
                        done_by=DSTPronoun.ANY,
                        asked=self.denied,
                        tense=Tense.ANY,
                        recipient=DSTPronoun.I,
                    ),
                ),
            ).check(checker=checker)
        elif isinstance(self.denied, Action):
            return super_check and AgentDoesAction(
                agent=DSTPronoun.YOU,
                tense=Tense.PAST,
                action=Relation(
                    left=DSTPronoun.YOU,
                    rtype=RType.ACTION,
                    rtense=Tense.PAST,
                    right=ra.RequestAction(
                        done_by=self.denied.done_by,
                        recipient=self.denied.recipient,
                        requested=self.denied,
                    ),
                ),
            ).check(checker=checker)

    def insert_pronouns(self):
        self.denied.pronouns = self.pronouns
        self.denied.insert_pronouns()
        super().insert_pronouns()
