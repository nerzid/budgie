from socialds.actions.action_obj import ActionObjType
from socialds.actions.simple_action import SimpleAction


class Backchannel(SimpleAction):
    def __init__(self):
        super().__init__('backchannel', ActionObjType.VERBAL)
