from functools import partial
from typing import List
from socialds.actions.action import Action
from socialds.actions.action_obj import ActionObj, ActionObjType
from socialds.agent import Agent
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RelationTense, RelationType


class Ask(Action):
    def __init__(self, asker: Agent, asked: Relation, r_tense: RelationTense, negation: bool, rs: RelationStorage):
        self.relation = Relation(asker, RelationType.ACTION, r_tense, asked, negation)
        self.rs = rs
        super().__init__("ask", ActionObjType.FUNCTIONAL, [])

# joe asks color of jane's dress
# Joe -do-> ask (Jane's dress's color -is-> X)

# Joe asks for the owner of the dress
# Joe -do-> ask (X -has-> dress)

# so, both left and right side of the relations can be asked
# action it self won't give anything but this action needs to be used
# by the planner of the agent. It goes into the possible actions
# for the planner to pick from

# For simplicity reasons, we use the relation above instead of the one below
# Jane -has-> dress, dress -has-> color, color -is-> red
