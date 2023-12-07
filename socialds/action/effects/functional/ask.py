from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.relation import Relation, RType


class Ask(Action):
    def __init__(self, asked: Relation, r_tense: Tense, negation: bool = False):
        self.relation = Relation(DSTPronoun.I, RType.ACTION, r_tense, asked, negation)
        self.asked_to = DSTPronoun.YOU
        self.asker = DSTPronoun.I
        self.asked = asked
        super().__init__("ask", ActionObjType.FUNCTIONAL, [])

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.asker.name} ask what {self.asked.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.asker.name} ask what {self.asked}"

    def insert_pronouns(self):
        if isinstance(self.asker, DSTPronoun):
            self.asker = pronouns[self.asker]
        if isinstance(self.asked_to, DSTPronoun):
            self.asked_to = pronouns[self.asked_to]
        self.relation.insert_pronouns()
        self.asked.insert_pronouns()
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
