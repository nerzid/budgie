from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Affirm(SimpleAction):
    def __init__(self):
        super().__init__('affirm', DSTPronoun.I, ActionObjType.VERBAL)