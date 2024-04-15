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
    def __init__(self, asked: Information, tense: Tense, negation: Negation = Negation.FALSE,
                 done_by: Agent | DSTPronoun = DSTPronoun.I, recipient: Agent | DSTPronoun = DSTPronoun.YOU, ):
        self.relation = Information(DSTPronoun.I, RType.ACTION, tense, asked, negation)
        self.asked = asked
        super().__init__("request-info", done_by=done_by, act_type=ActionObjType.VERBAL, base_effects=[
            AddExpectedEffect(effect=GainKnowledge(affected=done_by, knowledge=asked),
                              affected=recipient)
        ], recipient=recipient)

    def __str__(self):
        return "%s asks what %s" % (self.done_by.name, self.asked)

    def __repr__(self):
        return "%r asks what %r" % (self.done_by.name, self.asked)

    @staticmethod
    def get_pretty_template():
        return "[done_by] asks what [asked]([tense][negation])"

    def insert_pronouns(self, ):
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
