from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Sit(SimpleAction):
    def __init__(self):
        super().__init__('sit', DSTPronoun.I, ActionObjType.PHYSICAL)
