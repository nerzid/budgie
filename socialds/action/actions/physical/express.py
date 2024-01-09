from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Express(SimpleAction):
    def __init__(self, emotion):
        super().__init__('express', DSTPronoun.I, ActionObjType.PHYSICAL)
        self.emotion = emotion