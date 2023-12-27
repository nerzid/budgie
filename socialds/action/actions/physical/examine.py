from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Examine(SimpleAction):
    def __init__(self):
        super().__init__('examine', DSTPronoun.I, ActionObjType.PHYSICAL)

    def __repr__(self):
        return "%s" % self.name
