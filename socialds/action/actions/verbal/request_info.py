from __future__ import annotations

from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.add_expected_effect import AddExpectedEffect
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.agent import Agent
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Relation, RType, Negation


class RequestInfo(Action):

    def __init__(
        self,
        asked: Information,
        tense: Tense = Tense.ANY,
        negation: Negation = Negation.FALSE,
        done_by: Agent | DSTPronoun = DSTPronoun.I,
        recipient: Agent | DSTPronoun = DSTPronoun.YOU,
    ):
        """
        Requests information from an agent or a DSTPronoun.
        Args:
            asked: the information to request
            tense: tense of the action
            negation: negation of the action
            done_by: the agent or DSTPronoun who requests the information
            recipient: the agent or DSTPronoun who the information is request from
        """
        self.relation = Information(DSTPronoun.I, RType.ACTION, tense, asked, negation)
        self.asked = asked
        self.tense = tense
        self.negation = negation
        super().__init__(
            "request-info",
            done_by=done_by,
            act_type=ActionObjType.VERBAL,
            base_effects=[
                AddExpectedEffect(
                    effect=GainKnowledge(affected=done_by, knowledge=asked),
                    affected=recipient,
                )
            ],
            recipient=recipient,
        )

    def __deepcopy__(self, memodict={}):
        return RequestInfo(self.asked, self.tense, self.negation, self.done_by, self.recipient)

    def __str__(self):
        return "%s asks what %s" % (self.done_by.name, self.asked)

    def __repr__(self):
        return "%r asks what %r" % (self.done_by.name, self.asked)

    def to_dict(self):
        super_dict = super().to_dict()
        super_dict.update({
            "done_by": self.done_by.to_dict(),
            "recipient": self.recipient.to_dict(),
            "asked": self.asked.to_dict(),
            # "act_type": self.act_type.to_dict(),
            "tense": self.tense.to_dict(),
            "negation": self.negation.to_dict(),
            # "base_effects": [base_effect.to_dict() for base_effect in self.base_effects],
        })
        return super_dict

    @staticmethod
    def get_pretty_template():
        return "[done_by] asks what [asked]([tense][negation])"

    @staticmethod
    def build_instance_from_effects(done_by, recipient, tense, negation, effects):
        """
        Follows the same order of the self.base_effects

        Args:
            effects (_type_): _description_
        """
        if len(effects) != 1:
            return None
        add_expected_effect: AddExpectedEffect = effects[0]
        gain_knowledge_effect: GainKnowledge = add_expected_effect.effect  # type: ignore
        asked = gain_knowledge_effect.knowledge
        return RequestInfo(
            asked=asked,
            tense=tense,
            negation=negation,
            done_by=done_by,
            recipient=recipient,
        )

    def insert_pronouns(
        self,
    ):
        self.relation.pronouns = self.pronouns
        self.asked.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.asked.insert_pronouns()
        super().insert_pronouns()

    def execute(self, agent, **kwargs):
        self.pronouns = agent.pronouns
        self.insert_pronouns()
        super().execute(agent, **kwargs)

    def get_requirement_holders(self) -> List:
        pass


# joe asks color of jane's dress
# Joe -do-> ask (Jane's dress's color -is-> X)

# Joe asks for the owner of the dress
# Joe -do-> ask (X -has-> dress)

# so, both left and right side of the relations can be asked
# action itself won't give anything but this action needs to be used
# by the planner of the agent. It goes into the possible actions
# for the planner to pick from

# For simplicity reasons, we use the relation above instead of the one below
# Jane -has-> dress, dress -has-> color, color -is-> red
