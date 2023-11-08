from socialds.actions.action_obj import ActionObjType
from socialds.actions.simple_action import SimpleAction


class Sit(SimpleAction):
    def __init__(self):
        super().__init__('sit', ActionObjType.PHYSICAL)
