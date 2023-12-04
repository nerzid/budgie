from __future__ import annotations

from socialds.enums import Tense
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RType


class Check(Action):
    def __init__(self, checked: Relation, r_tense: Tense, checked_agent: Agent | DSTPronoun,
                 negation: bool = False):
        self.checked_agent = checked_agent
        self.checker = DSTPronoun.I
        self.checked = checked
        self.relation = Relation(self.checker, RType.ACTION, r_tense, checked, negation)
        super().__init__("check", ActionObjType.FUNCTIONAL, [])

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.checker} check if {self.checked.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.checker} check if {self.checked}"

    def insert_pronouns(self):
        if isinstance(self.checker, DSTPronoun):
            self.checker = pronouns[self.checker]
        if isinstance(self.checked_agent, DSTPronoun):
            self.checked_agent = pronouns[self.checked_agent]
        self.relation.insert_pronouns()
        self.checked.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()

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
