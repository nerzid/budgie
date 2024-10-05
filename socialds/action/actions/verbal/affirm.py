from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.action.effects.social.gain_permit import GainPermit
from socialds.action.effects.social.permit import Permit
from socialds.agent import Agent
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.conditions.agent_knows import AgentKnows
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
import socialds.action.actions.verbal.request_action as ra
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Negation, Relation, RType


class Affirm(Action):

    def __init__(
        self,
        affirmed: Information | Action,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
    ):
        """
        Affirms a specific information relation as true
        Args:
            affirmed: the information that is indicated true
            done_by: the agent or DSTPronoun that affirms the information
            tense: tense of the action
            negation: negation of the action
            recipient: the agent or DSTPronoun who the information is affirmed for
        """
        self.affirmed = affirmed
        self.tense = tense
        self.negation = negation
        if isinstance(affirmed, Information):
            super().__init__(
                name="affirm",
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
                    name="affirm",
                    done_by=done_by,
                    act_type=ActionObjType.VERBAL,
                    recipient=recipient,
                    base_effects=[
                        GainPermit(permit=relation, affected=permit_given_to)
                    ],
                    target_relations=[affirmed],
                )
            else:
                # TODO needs to be implemented. This current implementation only avoids errors.
                # Intuitively,this should handle the actions when they are affirmed.
                # E.g., To the question "Did you do self-cure?" and answer Yes (Affirm) indicates the information gain
                super().__init__(
                    name="affirm",
                    done_by=done_by,
                    act_type=ActionObjType.VERBAL,
                    recipient=recipient,
                    base_effects=[

                    ]
                )

    @staticmethod
    def get_pretty_template():
        return "[done_by] affirms [affirmed]"

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
            affirmed = gain_knowledge_effect.knowledge
            return Affirm(
                affirmed=affirmed,
                done_by=done_by,
                recipient=recipient,
            )
        elif isinstance(effects[0], GainPermit):
            gain_permit_effect: GainPermit = effects[0]
            permit = gain_permit_effect.permit
            return Affirm(
                affirmed=permit,
                done_by=done_by,
                recipient=recipient,
            )

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
            if not AgentKnows(
                agent=self.done_by,
                knows=self.affirmed,
                tense=self.affirmed.rel_tense,
                negation=self.affirmed.negation,
            ).check(checker):
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
                        done_by=DSTPronoun.YOU,
                        info=self.affirmed,
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
                    rel_type=RType.ACTION,
                    rel_tense=Tense.PAST,
                    right=ra.RequestAction(
                        done_by=self.affirmed.done_by,
                        recipient=self.affirmed.recipient,
                        requested=self.affirmed,
                    ),
                ),
            ).check(checker=checker)

    # def equals_with_pronouns(self, other, pronouns):
    #     return super().equals_with_pronouns(other, pronouns)
