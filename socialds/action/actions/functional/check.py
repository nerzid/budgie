from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RelationTense, RelationType


class Check(Action):
    def __init__(self, checker: Agent, checked: Relation, r_tense: RelationTense, checked_rs: RelationStorage,
                 negation: bool = False):
        self.relation = Relation(checker, RelationType.ACTION, r_tense, checked, negation)
        self.checked_rs = checked_rs
        self.checker = checker
        self.checked = checked
        super().__init__("check", ActionObjType.FUNCTIONAL, [])

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.checker.name} checks if {self.checked.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.checker.name} checks if {self.checked}"

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
