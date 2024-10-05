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
import socialds.action.actions.verbal.request_action as ra
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation, RType, Negation


class Deny(Action):
    def __init__(
        self,
        denied: Information | Action,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
    ):
        """
        Denies a specific information relation as false
        Args:
            denied: the information that is indicated false
            done_by: the agent or DSTPronoun that affirms the information
            tense: tense of the action
            negation: negation of the action
            recipient: the agent or DSTPronoun who the information is affirmed for
        """
        # denied = deepcopy(
        #     denied
        # )  # BUG here. It gives error when the denied object is of Action. Deepcopy cannot serialize a 'Greenthread' object.
        self.tense = tense
        self.negation = negation
        if isinstance(denied, Information):
            if denied.negation == Negation.FALSE or denied.negation == Negation.ANY:
                self.denied = Information(
                    left=denied.left,
                    rel_type=denied.rel_type,
                    rel_tense=denied.rel_tense,
                    right=denied.right,
                    negation=Negation.TRUE,
                )
            else:
                self.denied = Information(
                    left=denied.left,
                    rel_type=denied.rel_type,
                    rel_tense=denied.rel_tense,
                    right=denied.right,
                    negation=Negation.FALSE,
                )
            super().__init__(
                name="deny",
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
                    name="deny",
                    done_by=done_by,
                    recipient=recipient,
                    act_type=ActionObjType.VERBAL,
                    base_effects=[
                        GainPermit(permit=relation, affected=permit_given_to)
                    ],
                    target_relations=[denied],
                )
            else:
                # TODO same as the comment written in affirm.py
                super().__init__(
                    name="deny",
                    done_by=done_by,
                    recipient=recipient,
                    act_type=ActionObjType.VERBAL,
                    base_effects=[

                    ],
                )

    @staticmethod
    def get_pretty_template():
        return "[done_by] denies [denied]"

    def __str__(self):
        return "%s denies %s for %s" % (self.done_by, self.denied, self.recipient)

    def __repr__(self):
        return "%r denies %r for %r" % (self.done_by, self.denied, self.recipient)

    # def equals_with_pronouns(self, other, pronouns):
    #     return (
    #         super().equals_with_pronouns(other, pronouns)
    #         and self.denied == other.denied
    #     )

    @staticmethod
    def build_instance_from_effects(done_by, recipient, tense, negation, effects):
        """
        Follows the same order of the self.base_effects

        Args:
            effects (_type_): _description_
        """
        if len(effects) != 1:
            return None
        if isinstance(effects[0], GainKnowledge):
            gain_knowledge_effect: GainKnowledge = effects[0]
            denied = gain_knowledge_effect.knowledge
            return Deny(
                denied=denied,
                done_by=done_by,
                recipient=recipient,
            )
        elif isinstance(effects[0], GainPermit):
            gain_permit_effect: GainPermit = effects[0]
            permit = gain_permit_effect.permit
            return Deny(
                denied=permit,
                done_by=done_by,
                recipient=recipient,
            )

    def check_preconditions(self, checker):
        super_check = super().check_preconditions(checker)

        if isinstance(self.denied, Information):
            if not AgentKnows(
                agent=self.done_by,
                knows=self.denied,
                tense=self.denied.rel_tense,
                negation=self.denied.negation,
            ):
                return False

            from socialds.action.actions.verbal.request_info_confirmation import RequestInfoConfirmation
            return super_check and AgentDoesAction(
                agent=DSTPronoun.YOU,
                tense=Tense.PAST,
                action=Relation(
                    left=DSTPronoun.YOU,
                    rel_type=RType.ACTION,
                    rel_tense=Tense.PAST,
                    right=RequestInfoConfirmation(
                        done_by=DSTPronoun.ANY,
                        info=self.denied,
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
                    rel_type=RType.ACTION,
                    rel_tense=Tense.PAST,
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
