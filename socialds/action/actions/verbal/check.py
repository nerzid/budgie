from __future__ import annotations

from typing import List

from socialds.enums import Tense
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun
from socialds.states.relation import Relation, RType


class Check(Action):
    def __init__(self, checked: Relation, r_tense: Tense, recipient: Agent | DSTPronoun,
                 negation: bool = False):
        super().__init__("check", DSTPronoun.I, ActionObjType.VERBAL, [], recipient=recipient)
        self.checked = checked
        self.relation = Relation(self.done_by, RType.ACTION, r_tense, checked, negation)

    def __str__(self):
        return "%s check if %r" % (self.done_by, self.checked)

    def __repr__(self):
        return "%r check if %r" % (self.done_by, self.checked)

    def insert_pronouns(self):
        self.relation.pronouns = self.pronouns
        self.checked.pronouns = self.pronouns
        self.relation.insert_pronouns()
        self.checked.insert_pronouns()
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
